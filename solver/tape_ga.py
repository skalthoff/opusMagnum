"""Genetic algorithm for arm tape optimization.

Evolves instruction tapes using weighted mutations, crossover,
tournament selection, and archive-seeded initial populations.
"""
from __future__ import annotations
import copy
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable

from .solution import Solution, Part, Inst, solution_to_bytes, Instruction, CachedSolutionBase
from .simulator import Simulator, VerifyResult, PuzzleContext


@dataclass
class GAConfig:
    """Configuration for the genetic algorithm."""
    pop_size: int = 30
    max_generations: int = 100
    tournament_k: int = 3
    elite_count: int = 5
    crossover_rate: float = 0.3
    stagnation_limit: int = 20
    max_tape_len: int = 40
    min_tape_len: int = 3
    # Mutation weights (must sum to ~1.0)
    mutation_weights: Dict[str, float] = field(default_factory=lambda: {
        'change': 0.30,
        'insert': 0.15,
        'delete': 0.15,
        'swap': 0.15,
        'compress': 0.10,
        'change_terminal': 0.10,
        'duplicate_segment': 0.05,
    })
    # Early abandonment thresholds
    early_abandon_gen5_ratio: float = 1.5   # abandon if >1.5x best after 5 gens
    early_abandon_gen15_ratio: float = 1.1  # abandon if >1.1x best after 15 gens
    invalid_penalty_base: int = 10000
    invalid_penalty_per_inst: int = 10
    # Cycle limit for omsim verification (valid solutions complete in <100 cycles;
    # invalid tapes hitting the default 150K limit waste ~15ms each vs ~18us for valid ones)
    cycle_limit: int = 1000


@dataclass
class Individual:
    """A single tape in the population."""
    tape: List[int]
    fitness: float = float('inf')  # lower is better (sum4 or target metric)
    metrics: Optional[Dict[str, int]] = None
    valid: bool = False


def _is_obviously_invalid(tape: List[int]) -> bool:
    """Fast-reject tapes that can never produce a valid solution.

    Checks (in order of cheapness):
    - Empty tape
    - No GRAB instruction (can never pick up an atom)
    - No terminal (RESET/REPEAT) (infinite non-repeating execution)
    - All rotations with no GRAB/DROP (arm spins forever)
    """
    if not tape:
        return True
    has_grab = False
    has_terminal = False
    has_non_rotation = False
    rotation_set = {Inst.ROTATE_CW, Inst.ROTATE_CCW, Inst.PIVOT_CW, Inst.PIVOT_CCW}
    for inst in tape:
        if inst == Inst.GRAB:
            has_grab = True
        if inst in (Inst.RESET, Inst.REPEAT):
            has_terminal = True
        if inst not in rotation_set:
            has_non_rotation = True
    if not has_grab:
        return True
    if not has_terminal:
        return True
    if not has_non_rotation:
        return True
    return False


class TapeGA:
    """Genetic algorithm for tape optimization."""

    def __init__(self, simulator: Simulator, config: GAConfig = None,
                 instruction_weights: Optional[Dict[int, float]] = None,
                 seed: int = 42):
        self.sim = simulator
        self.config = config or GAConfig()
        self.rng = random.Random(seed)
        self._inst_weights = instruction_weights or self._default_weights()
        self._inst_choices, self._inst_probs = self._build_weighted_choices()
        self.total_evaluations = 0
        self.total_prerejected = 0
        self.best_ever: Optional[Individual] = None
        self._best_cycles: Optional[int] = None  # for adaptive cycle limit scaling

    def _default_weights(self) -> Dict[int, float]:
        return {
            Inst.GRAB: 0.20, Inst.DROP: 0.10,
            Inst.ROTATE_CW: 0.25, Inst.ROTATE_CCW: 0.10,
            Inst.RESET: 0.15, Inst.REPEAT: 0.10,
            Inst.PIVOT_CW: 0.05, Inst.PIVOT_CCW: 0.03,
            Inst.EXTEND: 0.01, Inst.RETRACT: 0.01,
        }

    def _build_weighted_choices(self):
        items = list(self._inst_weights.items())
        choices = [k for k, v in items]
        total = sum(v for k, v in items)
        probs = [v / total for k, v in items]
        return choices, probs

    def _weighted_random_inst(self) -> int:
        """Pick a random instruction weighted by archive frequency."""
        r = self.rng.random()
        cumulative = 0.0
        for inst, prob in zip(self._inst_choices, self._inst_probs):
            cumulative += prob
            if r <= cumulative:
                return inst
        return self._inst_choices[-1]

    # -----------------------------------------------------------------
    # Main entry point
    # -----------------------------------------------------------------

    def optimize(
        self,
        base_sol: Solution,
        layout_info: dict,
        puzzle_bytes: bytes,
        seed_tapes: List[List[int]],
        target: str = 'sum4',
        current_best: Optional[float] = None,
    ) -> Optional[Individual]:
        """Run the genetic algorithm to find an optimized tape.

        Args:
            base_sol: Solution without arm (has glyphs, inputs, outputs).
            layout_info: Must have 'arm_pos' (HexCoord), 'arm_len' (int),
                         'arm_rot' (int), 'arm_type' (str).
            puzzle_bytes: Raw puzzle file bytes for the simulator.
            seed_tapes: Initial tape templates to seed the population.
            target: Optimization target metric ('sum4', 'cost', 'cycles', etc.).
            current_best: Current best score for early abandonment checks.

        Returns:
            Best valid Individual found, or None if no valid tape was found.
        """
        # Pre-serialize base solution for fast tape splicing
        cached_base = CachedSolutionBase(base_sol, layout_info)

        # Create reusable puzzle context (parses puzzle once for all evals)
        puzzle_ctx = self.sim.create_puzzle_context(puzzle_bytes)

        # 1. Create initial population from seed tapes + mutations
        population = self._create_initial_population(seed_tapes)

        # 2. Evaluate all individuals
        for ind in population:
            evaluated = self._evaluate(ind.tape, base_sol, layout_info, puzzle_bytes, target, cached_base, puzzle_ctx)
            ind.fitness = evaluated.fitness
            ind.metrics = evaluated.metrics
            ind.valid = evaluated.valid
            if evaluated.valid:
                if self.best_ever is None or evaluated.fitness < self.best_ever.fitness:
                    self.best_ever = Individual(
                        tape=list(evaluated.tape),
                        fitness=evaluated.fitness,
                        metrics=evaluated.metrics,
                        valid=True,
                    )

        stagnation_counter = 0
        prev_best_fitness = float('inf')

        # 3. Generational loop
        for gen in range(self.config.max_generations):
            # Find current generation's best
            gen_best = min(population, key=lambda ind: ind.fitness)

            # 3a. Check early abandonment
            if current_best is not None and gen_best.valid:
                if gen >= 5 and gen_best.fitness > current_best * self.config.early_abandon_gen5_ratio:
                    break
                if gen >= 15 and gen_best.fitness > current_best * self.config.early_abandon_gen15_ratio:
                    break

            # 3b. Check stagnation
            if gen_best.fitness < prev_best_fitness:
                prev_best_fitness = gen_best.fitness
                stagnation_counter = 0
            else:
                stagnation_counter += 1
            if stagnation_counter >= self.config.stagnation_limit:
                break

            # 3c-d. Create children via selection, crossover, and mutation
            children: List[Individual] = []
            while len(children) < self.config.pop_size:
                parent1 = self._tournament_select(population)
                if self.rng.random() < self.config.crossover_rate and len(population) >= 2:
                    parent2 = self._tournament_select(population)
                    child_tape = self._crossover(parent1.tape, parent2.tape)
                else:
                    child_tape = list(parent1.tape)
                child_tape = self._mutate(child_tape)
                children.append(Individual(tape=child_tape))

            # 3e. Evaluate children
            for child in children:
                evaluated = self._evaluate(child.tape, base_sol, layout_info, puzzle_bytes, target, cached_base, puzzle_ctx)
                child.fitness = evaluated.fitness
                child.metrics = evaluated.metrics
                child.valid = evaluated.valid

            # 3f. Combine with elite, select survivors
            # Sort current population to find elites
            population.sort(key=lambda ind: ind.fitness)
            elites = population[:self.config.elite_count]

            # Combine elites + children, keep best pop_size
            combined = elites + children
            combined.sort(key=lambda ind: ind.fitness)
            population = combined[:self.config.pop_size]

            # 3g. Update best_ever
            for ind in population:
                if ind.valid:
                    if self.best_ever is None or ind.fitness < self.best_ever.fitness:
                        self.best_ever = Individual(
                            tape=list(ind.tape),
                            fitness=ind.fitness,
                            metrics=ind.metrics,
                            valid=True,
                        )

        # Clean up puzzle context
        puzzle_ctx.destroy()

        # Return best valid individual
        if self.best_ever is not None and self.best_ever.valid:
            return self.best_ever
        return None

    # -----------------------------------------------------------------
    # Evaluation
    # -----------------------------------------------------------------

    def _evaluate(
        self,
        tape: List[int],
        base_sol: Solution,
        layout_info: dict,
        puzzle_bytes: bytes,
        target: str,
        cached_base: Optional[CachedSolutionBase] = None,
        puzzle_ctx: Optional[PuzzleContext] = None,
    ) -> Individual:
        """Build solution with tape, verify, and return scored Individual."""
        self.total_evaluations += 1

        # Fast-reject obviously invalid tapes before FFI
        if _is_obviously_invalid(tape):
            self.total_prerejected += 1
            penalty = self.config.invalid_penalty_base + len(tape) * self.config.invalid_penalty_per_inst
            return Individual(
                tape=list(tape),
                fitness=float(penalty),
                metrics=None,
                valid=False,
            )

        # Use cached base bytes if available (avoids full rebuild + serialize)
        if cached_base is not None:
            sol_bytes = cached_base.splice(tape)
        else:
            sol = self._build_solution_with_tape(base_sol, layout_info, tape)
            sol_bytes = solution_to_bytes(sol)

        # Adaptive cycle limit: use 3x best known cycles, floored at config default
        if self._best_cycles is not None:
            cycle_limit = max(self.config.cycle_limit, 3 * self._best_cycles)
        else:
            cycle_limit = self.config.cycle_limit

        # Use puzzle context (single FFI call) when available, else fallback
        if puzzle_ctx is not None:
            result: VerifyResult = puzzle_ctx.verify(sol_bytes, cycle_limit=cycle_limit)
        else:
            result: VerifyResult = self.sim.verify_bytes(puzzle_bytes, sol_bytes,
                                                         cycle_limit=cycle_limit)

        if result.valid:
            metrics = {
                'cycles': result.cycles,
                'cost': result.cost,
                'area': result.area,
                'instructions': result.instructions,
            }
            metrics['sum4'] = metrics['cost'] + metrics['cycles'] + metrics['area'] + metrics['instructions']

            # Adaptive scaling: tighten cycle limit based on best observed cycles
            if self._best_cycles is None or result.cycles < self._best_cycles:
                self._best_cycles = result.cycles

            if target in metrics:
                fitness = float(metrics[target])
            else:
                fitness = float(metrics['sum4'])

            return Individual(
                tape=list(tape),
                fitness=fitness,
                metrics=metrics,
                valid=True,
            )
        else:
            penalty = self.config.invalid_penalty_base + len(tape) * self.config.invalid_penalty_per_inst
            return Individual(
                tape=list(tape),
                fitness=float(penalty),
                metrics=None,
                valid=False,
            )

    def _build_solution_with_tape(
        self,
        base_sol: Solution,
        layout_info: dict,
        tape: List[int],
    ) -> Solution:
        """Copy base_sol and add an arm part with the given tape."""
        sol = Solution(
            puzzle_name=base_sol.puzzle_name,
            solution_name=base_sol.solution_name,
        )
        # Deep copy existing parts (without arms)
        for p in base_sol.parts:
            new_part = Part(
                name=p.name,
                position=p.position,
                size=p.size,
                rotation=p.rotation,
                io_index=p.io_index,
                track_hexes=list(p.track_hexes),
                arm_number=p.arm_number,
                conduit_id=p.conduit_id,
                conduit_hexes=list(p.conduit_hexes),
            )
            # Copy instructions for non-arm parts
            new_part.instructions = [
                Instruction(inst.index, inst.instruction)
                for inst in p.instructions
            ]
            sol.parts.append(new_part)

        # Add arm with tape
        arm_type = layout_info.get('arm_type', 'arm1')
        arm = Part(
            name=arm_type,
            position=layout_info['arm_pos'],
            size=layout_info['arm_len'],
            rotation=layout_info['arm_rot'],
        )
        arm.set_tape(tape)
        sol.parts.append(arm)
        return sol

    # -----------------------------------------------------------------
    # Mutation operators
    # -----------------------------------------------------------------

    def _mutate_change(self, tape: List[int]) -> List[int]:
        """Replace a random instruction with a weighted-random one."""
        tape = list(tape)
        if not tape:
            return tape
        idx = self.rng.randint(0, len(tape) - 1)
        tape[idx] = self._weighted_random_inst()
        return tape

    def _mutate_insert(self, tape: List[int]) -> List[int]:
        """Insert a weighted-random instruction at a random position."""
        tape = list(tape)
        if len(tape) >= self.config.max_tape_len:
            return tape
        pos = self.rng.randint(0, len(tape))
        tape.insert(pos, self._weighted_random_inst())
        return tape

    def _mutate_delete(self, tape: List[int]) -> List[int]:
        """Remove a random instruction, protecting the terminal."""
        tape = list(tape)
        if len(tape) <= self.config.min_tape_len:
            return tape
        # Protect terminal: if last instruction is Reset or Repeat, avoid deleting it
        if len(tape) >= 2 and tape[-1] in (Inst.RESET, Inst.REPEAT):
            idx = self.rng.randint(0, len(tape) - 2)
        else:
            idx = self.rng.randint(0, len(tape) - 1)
        tape.pop(idx)
        return tape

    def _mutate_swap(self, tape: List[int]) -> List[int]:
        """Swap two adjacent instructions."""
        tape = list(tape)
        if len(tape) < 2:
            return tape
        idx = self.rng.randint(0, len(tape) - 2)
        tape[idx], tape[idx + 1] = tape[idx + 1], tape[idx]
        return tape

    def _mutate_compress(self, tape: List[int]) -> List[int]:
        """Simplify rotation sequences: 5 CW -> 1 CCW, and vice versa."""
        tape = list(tape)

        # Find runs of consecutive CW or CCW rotations
        i = 0
        while i < len(tape):
            # Count consecutive CW rotations
            if tape[i] == Inst.ROTATE_CW:
                run_start = i
                count = 0
                while i < len(tape) and tape[i] == Inst.ROTATE_CW:
                    count += 1
                    i += 1
                if count >= 5:
                    # Replace 5 CW with 1 CCW (net 6-5=1 CCW equivalent of 5 CW)
                    replacement_count = 6 - count if count < 6 else 0
                    if replacement_count > 0:
                        tape[run_start:run_start + count] = [Inst.ROTATE_CCW] * replacement_count
                        i = run_start + replacement_count
                    elif replacement_count == 0:
                        # 6 CW = full rotation = remove entirely
                        tape[run_start:run_start + count] = []
                        i = run_start
                continue
            # Count consecutive CCW rotations
            if tape[i] == Inst.ROTATE_CCW:
                run_start = i
                count = 0
                while i < len(tape) and tape[i] == Inst.ROTATE_CCW:
                    count += 1
                    i += 1
                if count >= 5:
                    replacement_count = 6 - count if count < 6 else 0
                    if replacement_count > 0:
                        tape[run_start:run_start + count] = [Inst.ROTATE_CW] * replacement_count
                        i = run_start + replacement_count
                    elif replacement_count == 0:
                        tape[run_start:run_start + count] = []
                        i = run_start
                continue
            i += 1

        return tape

    def _mutate_change_terminal(self, tape: List[int]) -> List[int]:
        """Swap last instruction between Reset and Repeat."""
        tape = list(tape)
        if not tape:
            return tape
        if tape[-1] == Inst.RESET:
            tape[-1] = Inst.REPEAT
        elif tape[-1] == Inst.REPEAT:
            tape[-1] = Inst.RESET
        else:
            # Last instruction is neither; add a terminal
            tape.append(self.rng.choice([Inst.RESET, Inst.REPEAT]))
        return tape

    def _mutate_duplicate_segment(self, tape: List[int]) -> List[int]:
        """Copy a short segment (1-3 instructions) before the terminal."""
        tape = list(tape)
        if len(tape) < 2:
            return tape
        if len(tape) >= self.config.max_tape_len:
            return tape

        seg_len = self.rng.randint(1, min(3, len(tape) - 1))
        start = self.rng.randint(0, len(tape) - 1 - seg_len)
        segment = tape[start:start + seg_len]

        # Insert before terminal (last element)
        insert_pos = len(tape) - 1 if tape[-1] in (Inst.RESET, Inst.REPEAT) else len(tape)
        # Clamp to max_tape_len
        allowed = self.config.max_tape_len - len(tape)
        if allowed <= 0:
            return tape
        segment = segment[:allowed]
        tape[insert_pos:insert_pos] = segment
        return tape

    def _mutate(self, tape: List[int]) -> List[int]:
        """Apply one random mutation operator (weighted by config)."""
        operators = {
            'change': self._mutate_change,
            'insert': self._mutate_insert,
            'delete': self._mutate_delete,
            'swap': self._mutate_swap,
            'compress': self._mutate_compress,
            'change_terminal': self._mutate_change_terminal,
            'duplicate_segment': self._mutate_duplicate_segment,
        }

        weights = self.config.mutation_weights
        names = list(weights.keys())
        probs = [weights[n] for n in names]
        total = sum(probs)
        probs = [p / total for p in probs]

        r = self.rng.random()
        cumulative = 0.0
        chosen_name = names[-1]
        for name, prob in zip(names, probs):
            cumulative += prob
            if r <= cumulative:
                chosen_name = name
                break

        op = operators.get(chosen_name, self._mutate_change)
        return op(tape)

    # -----------------------------------------------------------------
    # Crossover
    # -----------------------------------------------------------------

    def _crossover(self, t1: List[int], t2: List[int]) -> List[int]:
        """Single-point crossover with independent cut points."""
        if not t1 or not t2:
            return list(t1 or t2)
        c1 = self.rng.randint(0, len(t1))
        c2 = self.rng.randint(0, len(t2))
        child = t1[:c1] + t2[c2:]
        # Clamp to max length
        if len(child) > self.config.max_tape_len:
            child = child[:self.config.max_tape_len]
        # Ensure minimum length
        if len(child) < self.config.min_tape_len:
            while len(child) < self.config.min_tape_len:
                child.append(self._weighted_random_inst())
        return child

    # -----------------------------------------------------------------
    # Selection
    # -----------------------------------------------------------------

    def _tournament_select(self, population: List[Individual]) -> Individual:
        """Pick k random individuals, return the one with best fitness."""
        k = min(self.config.tournament_k, len(population))
        contestants = self.rng.sample(population, k)
        return min(contestants, key=lambda ind: ind.fitness)

    # -----------------------------------------------------------------
    # Initial population
    # -----------------------------------------------------------------

    def _create_initial_population(self, seed_tapes: List[List[int]]) -> List[Individual]:
        """Build the initial population from seed tapes and their mutations.

        - Add all seed tapes as individuals.
        - Fill remaining slots with mutated versions of seed tapes.
        - Ensure pop_size individuals total.
        """
        population: List[Individual] = []

        # Add all seed tapes
        for tape in seed_tapes:
            population.append(Individual(tape=list(tape)))
            if len(population) >= self.config.pop_size:
                break

        # Fill remaining slots with mutated versions
        if not seed_tapes:
            # Fallback: generate random short tapes
            for _ in range(self.config.pop_size):
                tape_len = self.rng.randint(self.config.min_tape_len, 8)
                tape = [self._weighted_random_inst() for _ in range(tape_len)]
                population.append(Individual(tape=tape))
        else:
            while len(population) < self.config.pop_size:
                base = self.rng.choice(seed_tapes)
                mutated = self._mutate(list(base))
                population.append(Individual(tape=mutated))

        return population[:self.config.pop_size]


# =====================================================================
# Geometric template generation (standalone function)
# =====================================================================

def generate_geometric_tapes(
    n_stations: int,
    n_inputs: int,
    directions: List[int],
) -> List[List[int]]:
    """Generate tape templates based on layout geometry.

    Creates tapes for CW-sweep patterns where an arm grabs from an input,
    rotates clockwise through glyph stations, and drops at the output.

    Args:
        n_stations: Total number of stations (inputs + glyphs + output).
        n_inputs: Number of input stations.
        directions: Direction index for each station (length == n_stations),
                    in the order they appear around the arm.

    Returns:
        A list of tape templates (each a list of Inst codes).
    """
    tapes: List[List[int]] = []

    n_distinct = len(set(directions))

    if n_inputs == 1:
        cw = n_stations - 1  # CW steps from first input to output
        ccw = 6 - cw if cw > 0 else 0  # CCW equivalent (opposite direction)

        # --- CW templates ---
        # Template 1: G R*cw X
        tapes.append([Inst.GRAB] + [Inst.ROTATE_CW] * cw + [Inst.RESET])
        # Template 2: G R*cw g X (explicit drop)
        tapes.append([Inst.GRAB] + [Inst.ROTATE_CW] * cw + [Inst.DROP, Inst.RESET])
        # Template 3: G R*cw g r*cw C (manual return, repeat)
        tapes.append(
            [Inst.GRAB] + [Inst.ROTATE_CW] * cw + [Inst.DROP]
            + [Inst.ROTATE_CCW] * cw + [Inst.REPEAT]
        )

        # --- CCW mirror templates ---
        # Template 4: G r*ccw X
        if ccw > 0:
            tapes.append([Inst.GRAB] + [Inst.ROTATE_CCW] * ccw + [Inst.RESET])
            # Template 5: G r*ccw g X (explicit drop)
            tapes.append([Inst.GRAB] + [Inst.ROTATE_CCW] * ccw + [Inst.DROP, Inst.RESET])
            # Template 6: G r*ccw g R*ccw C (manual return, repeat)
            tapes.append(
                [Inst.GRAB] + [Inst.ROTATE_CCW] * ccw + [Inst.DROP]
                + [Inst.ROTATE_CW] * ccw + [Inst.REPEAT]
            )

        # Templates with pivots at the output
        for np_ in range(1, 6):
            # CW rotation + pivot variants
            tapes.append(
                [Inst.GRAB] + [Inst.ROTATE_CW] * cw
                + [Inst.PIVOT_CW] * np_ + [Inst.RESET]
            )
            tapes.append(
                [Inst.GRAB] + [Inst.ROTATE_CW] * cw
                + [Inst.PIVOT_CCW] * np_ + [Inst.RESET]
            )
            tapes.append(
                [Inst.GRAB] + [Inst.ROTATE_CW] * cw
                + [Inst.DROP] + [Inst.PIVOT_CW] * np_ + [Inst.RESET]
            )
            tapes.append(
                [Inst.GRAB] + [Inst.ROTATE_CW] * cw
                + [Inst.DROP] + [Inst.PIVOT_CCW] * np_ + [Inst.RESET]
            )
            # CCW rotation + pivot variants
            if ccw > 0:
                tapes.append(
                    [Inst.GRAB] + [Inst.ROTATE_CCW] * ccw
                    + [Inst.PIVOT_CW] * np_ + [Inst.RESET]
                )
                tapes.append(
                    [Inst.GRAB] + [Inst.ROTATE_CCW] * ccw
                    + [Inst.PIVOT_CCW] * np_ + [Inst.RESET]
                )
                tapes.append(
                    [Inst.GRAB] + [Inst.ROTATE_CCW] * ccw
                    + [Inst.DROP] + [Inst.PIVOT_CW] * np_ + [Inst.RESET]
                )
                tapes.append(
                    [Inst.GRAB] + [Inst.ROTATE_CCW] * ccw
                    + [Inst.DROP] + [Inst.PIVOT_CCW] * np_ + [Inst.RESET]
                )

    elif n_inputs == 2:
        cw_total = n_stations - 1
        cw0 = cw_total       # input 0 to output
        cw1 = cw_total - 1   # input 1 to output (one fewer CW step)
        ccw0 = 6 - cw0 if cw0 > 0 else 0  # CCW equivalents
        ccw1 = 6 - cw1 if cw1 > 0 else 0

        # --- CW templates ---
        # a) Grab in0, CW to output, reset, CCW to in1, grab, CW to output, reset
        tape_a = ([Inst.GRAB] + [Inst.ROTATE_CW] * cw0 + [Inst.RESET]
                  + [Inst.ROTATE_CCW]
                  + [Inst.GRAB] + [Inst.ROTATE_CW] * cw1 + [Inst.RESET])
        tapes.append(tape_a)

        # b) Same with explicit drops
        tape_b = ([Inst.GRAB] + [Inst.ROTATE_CW] * cw0 + [Inst.DROP, Inst.RESET]
                  + [Inst.ROTATE_CCW]
                  + [Inst.GRAB] + [Inst.ROTATE_CW] * cw1 + [Inst.DROP, Inst.RESET])
        tapes.append(tape_b)

        # c) Return via CCW instead of reset
        tape_c = ([Inst.GRAB] + [Inst.ROTATE_CW] * cw0 + [Inst.DROP]
                  + [Inst.ROTATE_CCW] * cw1 + [Inst.GRAB]
                  + [Inst.ROTATE_CW] * cw1 + [Inst.DROP]
                  + [Inst.ROTATE_CCW] * cw0 + [Inst.REPEAT])
        tapes.append(tape_c)

        # --- CCW mirror templates ---
        if ccw0 > 0:
            # a-ccw) Grab in0, CCW to output, reset, CW to in1, grab, CCW to output, reset
            tape_a_ccw = ([Inst.GRAB] + [Inst.ROTATE_CCW] * ccw0 + [Inst.RESET]
                          + [Inst.ROTATE_CW]
                          + [Inst.GRAB] + [Inst.ROTATE_CCW] * ccw1 + [Inst.RESET])
            tapes.append(tape_a_ccw)

            # b-ccw) Same with explicit drops
            tape_b_ccw = ([Inst.GRAB] + [Inst.ROTATE_CCW] * ccw0 + [Inst.DROP, Inst.RESET]
                          + [Inst.ROTATE_CW]
                          + [Inst.GRAB] + [Inst.ROTATE_CCW] * ccw1 + [Inst.DROP, Inst.RESET])
            tapes.append(tape_b_ccw)

            # c-ccw) Return via CW instead of reset
            tape_c_ccw = ([Inst.GRAB] + [Inst.ROTATE_CCW] * ccw0 + [Inst.DROP]
                          + [Inst.ROTATE_CW] * ccw1 + [Inst.GRAB]
                          + [Inst.ROTATE_CCW] * ccw1 + [Inst.DROP]
                          + [Inst.ROTATE_CW] * ccw0 + [Inst.REPEAT])
            tapes.append(tape_c_ccw)

        # d) With pivots (both CW and CCW rotation directions)
        for np_ in range(1, 4):
            for piv in [Inst.PIVOT_CW, Inst.PIVOT_CCW]:
                # CW rotation
                tape_d = ([Inst.GRAB] + [Inst.ROTATE_CW] * cw0
                          + [piv] * np_ + [Inst.RESET]
                          + [Inst.ROTATE_CCW]
                          + [Inst.GRAB] + [Inst.ROTATE_CW] * cw1
                          + [piv] * np_ + [Inst.RESET])
                tapes.append(tape_d)
                # CCW rotation
                if ccw0 > 0:
                    tape_d_ccw = ([Inst.GRAB] + [Inst.ROTATE_CCW] * ccw0
                                  + [piv] * np_ + [Inst.RESET]
                                  + [Inst.ROTATE_CW]
                                  + [Inst.GRAB] + [Inst.ROTATE_CCW] * ccw1
                                  + [piv] * np_ + [Inst.RESET])
                    tapes.append(tape_d_ccw)

        # e) Grab in0, CW to output, drop, CCW back to in1, grab, CW to output, drop, CCW back, repeat
        if len(directions) >= 2:
            ccw_out_to_in1 = (directions[1] - directions[-1]) % 6
            ccw_out_to_in0 = (directions[0] - directions[-1]) % 6
            tape_e = ([Inst.GRAB] + [Inst.ROTATE_CW] * cw0 + [Inst.DROP]
                      + [Inst.ROTATE_CCW] * ccw_out_to_in1
                      + [Inst.GRAB] + [Inst.ROTATE_CW] * cw1 + [Inst.DROP]
                      + [Inst.ROTATE_CCW] * ccw_out_to_in0
                      + [Inst.REPEAT])
            tapes.append(tape_e)

            # e-ccw) CCW mirror of template e
            cw_out_to_in1 = (directions[-1] - directions[1]) % 6
            cw_out_to_in0 = (directions[-1] - directions[0]) % 6
            tape_e_ccw = ([Inst.GRAB] + [Inst.ROTATE_CCW] * ccw0 + [Inst.DROP]
                          + [Inst.ROTATE_CW] * cw_out_to_in1
                          + [Inst.GRAB] + [Inst.ROTATE_CCW] * ccw1 + [Inst.DROP]
                          + [Inst.ROTATE_CW] * cw_out_to_in0
                          + [Inst.REPEAT])
            tapes.append(tape_e_ccw)

    elif n_inputs >= 3:
        # Sequential: grab each input, rotate to output, drop, reset, navigate to next
        import itertools
        cw_total = n_stations - 1
        for perm in itertools.permutations(range(n_inputs)):
            tape: List[int] = []
            for pi, inp_idx in enumerate(perm):
                cw_i = cw_total - inp_idx  # steps from this input to output

                if pi > 0:
                    # Navigate from reset position (dir of input perm[0]) to this input
                    from_dir = directions[perm[0]]
                    to_dir = directions[inp_idx]
                    ccw = (to_dir - from_dir) % 6
                    cw_rev = (from_dir - to_dir) % 6
                    if ccw <= 3:
                        tape += [Inst.ROTATE_CCW] * ccw
                    else:
                        tape += [Inst.ROTATE_CW] * cw_rev

                tape += [Inst.GRAB] + [Inst.ROTATE_CW] * cw_i
                tape += [Inst.DROP, Inst.RESET]
            tapes.append(tape)

        # CCW mirror: grab each input, rotate CCW to output, drop, reset
        for perm in itertools.permutations(range(n_inputs)):
            tape_ccw: List[int] = []
            for pi, inp_idx in enumerate(perm):
                ccw_i = 6 - (cw_total - inp_idx) if (cw_total - inp_idx) > 0 else 0

                if pi > 0:
                    from_dir = directions[perm[0]]
                    to_dir = directions[inp_idx]
                    cw_nav = (from_dir - to_dir) % 6
                    ccw_nav = (to_dir - from_dir) % 6
                    if cw_nav <= 3:
                        tape_ccw += [Inst.ROTATE_CW] * cw_nav
                    else:
                        tape_ccw += [Inst.ROTATE_CCW] * ccw_nav

                if ccw_i > 0:
                    tape_ccw += [Inst.GRAB] + [Inst.ROTATE_CCW] * ccw_i
                    tape_ccw += [Inst.DROP, Inst.RESET]
            if tape_ccw:
                tapes.append(tape_ccw)

    # Stacked templates: when multiple stations share directions
    if n_distinct < n_stations:
        for n_cw in range(1, n_distinct):
            tapes.append([Inst.GRAB] + [Inst.ROTATE_CW] * n_cw + [Inst.RESET])
            tapes.append([Inst.GRAB] + [Inst.ROTATE_CW] * n_cw + [Inst.DROP, Inst.RESET])
            # CCW mirrors for stacked templates
            n_ccw = 6 - n_cw if n_cw > 0 else 0
            if n_ccw > 0:
                tapes.append([Inst.GRAB] + [Inst.ROTATE_CCW] * n_ccw + [Inst.RESET])
                tapes.append([Inst.GRAB] + [Inst.ROTATE_CCW] * n_ccw + [Inst.DROP, Inst.RESET])

    # -----------------------------------------------------------------
    # Repeat-based templates (tight loops used in archive solutions)
    # -----------------------------------------------------------------
    # G R g C — grab, CW, drop, repeat (tight CW delivery loop)
    tapes.append([Inst.GRAB, Inst.ROTATE_CW, Inst.DROP, Inst.REPEAT])
    # G r g C — grab, CCW, drop, repeat
    tapes.append([Inst.GRAB, Inst.ROTATE_CCW, Inst.DROP, Inst.REPEAT])
    # G R R g C — grab, 2xCW, drop, repeat
    tapes.append([Inst.GRAB, Inst.ROTATE_CW, Inst.ROTATE_CW, Inst.DROP, Inst.REPEAT])
    # G r r g C — grab, 2xCCW, drop, repeat
    tapes.append([Inst.GRAB, Inst.ROTATE_CCW, Inst.ROTATE_CCW, Inst.DROP, Inst.REPEAT])
    # G R R R g C — grab, 3xCW, drop, repeat
    tapes.append([Inst.GRAB, Inst.ROTATE_CW, Inst.ROTATE_CW, Inst.ROTATE_CW,
                  Inst.DROP, Inst.REPEAT])
    # G r r r g C — grab, 3xCCW, drop, repeat
    tapes.append([Inst.GRAB, Inst.ROTATE_CCW, Inst.ROTATE_CCW, Inst.ROTATE_CCW,
                  Inst.DROP, Inst.REPEAT])
    # G R g C . . R R — repeat loop with setup (like P011's archive solution)
    tapes.append([Inst.GRAB, Inst.ROTATE_CW, Inst.DROP, Inst.REPEAT,
                  Inst.NOOP, Inst.NOOP, Inst.ROTATE_CW, Inst.ROTATE_CW])
    # G r g C . . r r — CCW mirror of setup pattern
    tapes.append([Inst.GRAB, Inst.ROTATE_CCW, Inst.DROP, Inst.REPEAT,
                  Inst.NOOP, Inst.NOOP, Inst.ROTATE_CCW, Inst.ROTATE_CCW])

    # -----------------------------------------------------------------
    # Multi-delivery templates (output needs more atoms than single grab)
    # -----------------------------------------------------------------
    # G R g R G R g X — grab, deliver, grab again, deliver, reset (2 deliveries CW)
    tapes.append([Inst.GRAB, Inst.ROTATE_CW, Inst.DROP, Inst.ROTATE_CW,
                  Inst.GRAB, Inst.ROTATE_CW, Inst.DROP, Inst.RESET])
    # G r g r G r g X — same with CCW
    tapes.append([Inst.GRAB, Inst.ROTATE_CCW, Inst.DROP, Inst.ROTATE_CCW,
                  Inst.GRAB, Inst.ROTATE_CCW, Inst.DROP, Inst.RESET])
    # G R g G R g G R g X — 3 deliveries per cycle (CW)
    tapes.append([Inst.GRAB, Inst.ROTATE_CW, Inst.DROP,
                  Inst.GRAB, Inst.ROTATE_CW, Inst.DROP,
                  Inst.GRAB, Inst.ROTATE_CW, Inst.DROP, Inst.RESET])
    # G r g G r g G r g X — 3 deliveries per cycle (CCW)
    tapes.append([Inst.GRAB, Inst.ROTATE_CCW, Inst.DROP,
                  Inst.GRAB, Inst.ROTATE_CCW, Inst.DROP,
                  Inst.GRAB, Inst.ROTATE_CCW, Inst.DROP, Inst.RESET])
    # Multi-delivery with Repeat terminal
    tapes.append([Inst.GRAB, Inst.ROTATE_CW, Inst.DROP, Inst.ROTATE_CW,
                  Inst.GRAB, Inst.ROTATE_CW, Inst.DROP, Inst.REPEAT])
    tapes.append([Inst.GRAB, Inst.ROTATE_CCW, Inst.DROP, Inst.ROTATE_CCW,
                  Inst.GRAB, Inst.ROTATE_CCW, Inst.DROP, Inst.REPEAT])

    # -----------------------------------------------------------------
    # Pivot templates (archive solutions use pivots for atom positioning)
    # -----------------------------------------------------------------
    # G r P P P X — grab, CCW rotate, pivot CW sequence
    tapes.append([Inst.GRAB, Inst.ROTATE_CCW,
                  Inst.PIVOT_CW, Inst.PIVOT_CW, Inst.PIVOT_CW, Inst.RESET])
    # G R p p p X — grab, CW rotate, pivot CCW sequence
    tapes.append([Inst.GRAB, Inst.ROTATE_CW,
                  Inst.PIVOT_CCW, Inst.PIVOT_CCW, Inst.PIVOT_CCW, Inst.RESET])
    # G r P P P P P X — grab, CCW rotate, 5x pivot CW
    tapes.append([Inst.GRAB, Inst.ROTATE_CCW,
                  Inst.PIVOT_CW, Inst.PIVOT_CW, Inst.PIVOT_CW,
                  Inst.PIVOT_CW, Inst.PIVOT_CW, Inst.RESET])
    # G R p p p p p X — grab, CW rotate, 5x pivot CCW
    tapes.append([Inst.GRAB, Inst.ROTATE_CW,
                  Inst.PIVOT_CCW, Inst.PIVOT_CCW, Inst.PIVOT_CCW,
                  Inst.PIVOT_CCW, Inst.PIVOT_CCW, Inst.RESET])
    # Pivot + drop + reset combinations
    tapes.append([Inst.GRAB, Inst.ROTATE_CCW,
                  Inst.PIVOT_CW, Inst.PIVOT_CW, Inst.PIVOT_CW,
                  Inst.DROP, Inst.RESET])
    tapes.append([Inst.GRAB, Inst.ROTATE_CW,
                  Inst.PIVOT_CCW, Inst.PIVOT_CCW, Inst.PIVOT_CCW,
                  Inst.DROP, Inst.RESET])

    return tapes
