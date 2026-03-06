"""GPU-batched Opus Magnum simulator using PyTorch.

Runs B simulations in parallel on a bounded radius-5 hex grid (91 hexes).
All state is stored as tensors; molecule movement uses iterative BFS through
bonds. Cross-validate against C omsim for correctness.
"""
from __future__ import annotations

import torch
import torch.nn.functional as F
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .hex import HexCoord, DIRECTIONS
from .puzzle import AtomType, BondType, Puzzle, parse_puzzle
from .solution import Solution, Part, Inst, parse_solution, solution_to_bytes
from .glyph_model import (GLYPH_SPECS, local_to_world, get_glyph_spec,
                           GlyphSpec, GlyphSlot)

# ---------------------------------------------------------------------------
# Hex grid constants — radius-5 disk, 91 hexes
# ---------------------------------------------------------------------------

GRID_RADIUS = 5
NUM_HEXES = 3 * GRID_RADIUS * (GRID_RADIUS + 1) + 1  # 91

def _build_hex_grid():
    """Build axial coord list and coord-to-index mapping for radius-5 disk."""
    coords = []
    coord_to_idx = {}
    for q in range(-GRID_RADIUS, GRID_RADIUS + 1):
        for r in range(-GRID_RADIUS, GRID_RADIUS + 1):
            if abs(q + r) <= GRID_RADIUS:
                idx = len(coords)
                coords.append((q, r))
                coord_to_idx[(q, r)] = idx
    assert len(coords) == NUM_HEXES
    return coords, coord_to_idx

HEX_COORDS_LIST, COORD_TO_IDX = _build_hex_grid()
HEX_COORDS = torch.tensor(HEX_COORDS_LIST, dtype=torch.int32)  # [91, 2]

# Direction vectors (same order as hex.py: E, SE, SW, W, NW, NE)
DIR_VECTORS = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]

def _build_neighbor_table():
    """Build [91, 6] neighbor index table. -1 for out-of-bounds."""
    table = [[-1] * 6 for _ in range(NUM_HEXES)]
    for idx, (q, r) in enumerate(HEX_COORDS_LIST):
        for d, (dq, dr) in enumerate(DIR_VECTORS):
            nq, nr = q + dq, r + dr
            nbr = COORD_TO_IDX.get((nq, nr), -1)
            table[idx][d] = nbr
    return torch.tensor(table, dtype=torch.long)  # [91, 6]

NEIGHBOR_TABLE = _build_neighbor_table()

# Reverse direction: opposite of d is (d+3)%6
REVERSE_DIR = [(d + 3) % 6 for d in range(6)]

# Rotation in hex axial coords (cube: q,r,s where s=-q-r):
# CW 60° (game visual CW, direction index -1): (q,r,s) → (-s,-q,-r) = (q+r, -q)
# CCW 60° (game visual CCW, direction index +1): (q,r,s) → (-r,-s,-q) = (-r, q+r)
def _rotate_hex_cw(q, r):
    return (q + r, -q)

def _rotate_hex_ccw(q, r):
    return (-r, q + r)

# Precompute rotation lookup: for each hex index, where does it go after
# rotating around origin? -1 if result is out of bounds.
def _build_rotation_table(rot_fn):
    table = [-1] * NUM_HEXES
    for idx, (q, r) in enumerate(HEX_COORDS_LIST):
        nq, nr = rot_fn(q, r)
        table[idx] = COORD_TO_IDX.get((nq, nr), -1)
    return torch.tensor(table, dtype=torch.long)

ROT_CW_TABLE = _build_rotation_table(_rotate_hex_cw)    # [91]
ROT_CCW_TABLE = _build_rotation_table(_rotate_hex_ccw)   # [91]

# Element constants (matching AtomType enum values)
ELEM_EMPTY = 0
ELEM_SALT = 1
ELEM_AIR = 2
ELEM_EARTH = 3
ELEM_FIRE = 4
ELEM_WATER = 5
ELEM_QUICKSILVER = 6
ELEM_GOLD = 7
ELEM_SILVER = 8
ELEM_COPPER = 9
ELEM_IRON = 10
ELEM_TIN = 11
ELEM_LEAD = 12
ELEM_VITAE = 13
ELEM_MORS = 14
ELEM_QUINTESSENCE = 16

CARDINAL_ELEMS = {ELEM_AIR, ELEM_EARTH, ELEM_FIRE, ELEM_WATER}
METAL_ELEMS = {ELEM_LEAD, ELEM_TIN, ELEM_IRON, ELEM_COPPER, ELEM_SILVER, ELEM_GOLD}
# Projection: promote metal one step (lead->tin->...->gold)
METAL_PROMOTE = {
    ELEM_LEAD: ELEM_TIN, ELEM_TIN: ELEM_IRON, ELEM_IRON: ELEM_COPPER,
    ELEM_COPPER: ELEM_SILVER, ELEM_SILVER: ELEM_GOLD,
}

# Bond types
BOND_NONE = 0
BOND_NORMAL = 1
BOND_TRIPLEX_R = 2
BOND_TRIPLEX_Y = 4
BOND_TRIPLEX_K = 8

# Instruction constants (solution file byte codes)
INST_NOOP = 0
INST_GRAB = Inst.GRAB        # 0x47
INST_DROP = Inst.DROP         # 0x67
INST_ROT_CW = Inst.ROTATE_CW   # 0x52
INST_ROT_CCW = Inst.ROTATE_CCW  # 0x72
INST_EXTEND = Inst.EXTEND     # 0x45
INST_RETRACT = Inst.RETRACT    # 0x65
INST_PIVOT_CW = Inst.PIVOT_CW   # 0x50
INST_PIVOT_CCW = Inst.PIVOT_CCW  # 0x70
INST_RESET = Inst.RESET       # 0x58
INST_REPEAT = Inst.REPEAT     # 0x43


def hex_to_idx(q: int, r: int) -> int:
    """Convert axial coords to grid index, or -1 if out of bounds."""
    return COORD_TO_IDX.get((q, r), -1)

def hexcoord_to_idx(h: HexCoord) -> int:
    return COORD_TO_IDX.get((h.q, h.r), -1)


# ---------------------------------------------------------------------------
# Glyph precomputation
# ---------------------------------------------------------------------------

@dataclass
class GlyphInstance:
    """A placed glyph with precomputed world-space slot indices."""
    glyph_type: str          # e.g. 'glyph-calcification', 'bonder'
    slot_indices: List[int]  # grid indices for each slot (in spec order)
    slot_roles: List[str]    # 'input', 'output', 'active' per slot
    slot_constraints: List[Optional[str]]  # atom constraint per slot
    is_conversion: bool
    footprint_indices: List[int]  # grid indices of footprint hexes


def precompute_glyph(part: Part) -> Optional[GlyphInstance]:
    """Convert a placed Part (glyph/bonder) into a GlyphInstance."""
    try:
        spec = get_glyph_spec(part.name)
    except KeyError:
        return None

    pos = part.position
    rot = part.rotation % 6
    slot_indices = []
    slot_roles = []
    slot_constraints = []
    for slot in spec.slots:
        world = local_to_world(pos, rot, slot.du, slot.dv)
        idx = hex_to_idx(world.q, world.r)
        slot_indices.append(idx)
        slot_roles.append(slot.role)
        slot_constraints.append(slot.atom_constraint)

    footprint_indices = []
    for du, dv in spec.footprint:
        world = local_to_world(pos, rot, du, dv)
        idx = hex_to_idx(world.q, world.r)
        footprint_indices.append(idx)

    return GlyphInstance(
        glyph_type=part.name,
        slot_indices=slot_indices,
        slot_roles=slot_roles,
        slot_constraints=slot_constraints,
        is_conversion=spec.is_conversion,
        footprint_indices=footprint_indices,
    )


# ---------------------------------------------------------------------------
# Input/Output precomputation
# ---------------------------------------------------------------------------

@dataclass
class InputInstance:
    """A placed input with precomputed atom positions."""
    io_index: int
    atom_indices: List[int]      # grid index per atom
    atom_elements: List[int]     # element type per atom


@dataclass
class OutputInstance:
    """A placed output with precomputed template."""
    io_index: int
    atom_indices: List[int]      # grid index per atom
    atom_elements: List[int]     # expected element per atom
    bond_pairs: List[Tuple[int, int, int]]  # (idx_a, idx_b, direction) for bonds
    center_idx: int              # grid index of first atom (BFS root)


# ---------------------------------------------------------------------------
# Arm precomputation
# ---------------------------------------------------------------------------

@dataclass
class ArmInstance:
    """A placed arm with precomputed geometry."""
    base_idx: int           # grid index of arm base
    arm_len: int
    initial_dir: int        # starting direction (0-5)
    arm_type: str           # 'arm1', etc.
    # Tip index is computed dynamically based on current direction


def compute_tip_idx(base_q: int, base_r: int, direction: int, arm_len: int) -> int:
    """Compute the grid index of an arm's tip."""
    dq, dr = DIR_VECTORS[direction % 6]
    tq = base_q + dq * arm_len
    tr = base_r + dr * arm_len
    return hex_to_idx(tq, tr)


# ---------------------------------------------------------------------------
# Board state
# ---------------------------------------------------------------------------

@dataclass
class BoardState:
    """Batched simulation state tensors."""
    element: torch.Tensor     # [B, 91] int32 — element type (0=empty)
    bonds: torch.Tensor       # [B, 91, 6] int8 — bond type per direction
    grabbed: torch.Tensor     # [B, 91] bool — atom is grabbed by any arm
    area_used: torch.Tensor   # [B, 91] bool — hex was ever occupied
    output_count: torch.Tensor  # [B, N_out] int32 — outputs produced per output
    done: torch.Tensor        # [B] bool
    collision: torch.Tensor   # [B] bool
    # Per-arm state
    arm_dir: torch.Tensor     # [B, A] int32 — current arm direction (0-5)
    arm_grabbing: torch.Tensor  # [B, A] bool — arm currently holding
    # Conversion glyph state
    converting: torch.Tensor  # [B, G] bool — glyph mid-conversion
    conversion_target: torch.Tensor  # [B, G] int32 — output element for conversion glyphs


# ---------------------------------------------------------------------------
# BatchSimulator
# ---------------------------------------------------------------------------

class BatchSimulator:
    """GPU-batched Opus Magnum simulator.

    Precomputes fixed geometry from a puzzle + solution layout, then
    evaluates batches of tapes in parallel.
    """

    def __init__(self, puzzle: Puzzle, solution: Solution,
                 device: str = 'mps', max_cycles: int = 200):
        self.device = torch.device(device)
        self.max_cycles = max_cycles
        self.puzzle = puzzle
        self.n_outputs = len(puzzle.outputs)
        self.target_count = puzzle.output_scale

        # Move constant tables to device
        self.neighbor_table = NEIGHBOR_TABLE.to(self.device)  # [91, 6]
        self.rot_cw_table = ROT_CW_TABLE.to(self.device)
        self.rot_ccw_table = ROT_CCW_TABLE.to(self.device)

        # Parse layout from solution
        self.arms: List[ArmInstance] = []
        self.glyphs: List[GlyphInstance] = []
        self.inputs: List[InputInstance] = []
        self.outputs: List[OutputInstance] = []
        self.cost = 0

        self._parse_solution(solution)
        self._instruction_count = solution.total_instructions()

        # Precompute arm base coords for tip calculation
        self._arm_base_qr = []
        for arm in self.arms:
            q, r = HEX_COORDS_LIST[arm.base_idx]
            self._arm_base_qr.append((q, r))

    def _parse_solution(self, sol: Solution):
        """Extract arms, glyphs, inputs, outputs from solution."""
        self.cost = sol.total_cost()

        for part in sol.parts:
            if part.is_arm:
                base_idx = hexcoord_to_idx(part.position)
                if base_idx < 0:
                    continue
                self.arms.append(ArmInstance(
                    base_idx=base_idx,
                    arm_len=part.size,
                    initial_dir=part.rotation % 6,
                    arm_type=part.name,
                ))

            elif part.is_glyph:
                gi = precompute_glyph(part)
                if gi is not None:
                    self.glyphs.append(gi)

            elif part.name == 'input':
                io = self.puzzle.inputs[part.io_index]
                atom_indices = []
                atom_elements = []
                for atom in io.molecule.atoms:
                    world = atom.position + part.position
                    idx = hex_to_idx(world.q, world.r)
                    atom_indices.append(idx)
                    atom_elements.append(int(atom.atom_type))
                self.inputs.append(InputInstance(
                    io_index=part.io_index,
                    atom_indices=atom_indices,
                    atom_elements=atom_elements,
                ))

            elif part.name in ('out-std', 'out-rep'):
                io = self.puzzle.outputs[part.io_index]
                rot = part.rotation % 6
                atom_indices = []
                atom_elements = []
                for atom in io.molecule.atoms:
                    # Output atoms are in local coords, need rotation
                    world = _rotate_local_to_world(part.position, rot, atom.position)
                    idx = hex_to_idx(world.q, world.r)
                    atom_indices.append(idx)
                    atom_elements.append(int(atom.atom_type))

                bond_pairs = []
                for bond in io.molecule.bonds:
                    from_world = _rotate_local_to_world(part.position, rot, bond.from_pos)
                    to_world = _rotate_local_to_world(part.position, rot, bond.to_pos)
                    fi = hex_to_idx(from_world.q, from_world.r)
                    ti = hex_to_idx(to_world.q, to_world.r)
                    # Find direction from fi to ti
                    d = _find_direction(from_world, to_world)
                    bond_pairs.append((fi, ti, d))

                center_idx = atom_indices[0] if atom_indices else -1
                self.outputs.append(OutputInstance(
                    io_index=part.io_index,
                    atom_indices=atom_indices,
                    atom_elements=atom_elements,
                    bond_pairs=bond_pairs,
                    center_idx=center_idx,
                ))

    def _init_state(self, B: int) -> BoardState:
        """Create fresh board state for B simulations."""
        dev = self.device
        A = len(self.arms)
        G = len(self.glyphs)
        N_out = self.n_outputs

        state = BoardState(
            element=torch.zeros(B, NUM_HEXES, dtype=torch.int32, device=dev),
            bonds=torch.zeros(B, NUM_HEXES, 6, dtype=torch.int8, device=dev),
            grabbed=torch.zeros(B, NUM_HEXES, dtype=torch.bool, device=dev),
            area_used=torch.zeros(B, NUM_HEXES, dtype=torch.bool, device=dev),
            output_count=torch.zeros(B, N_out, dtype=torch.int32, device=dev),
            done=torch.zeros(B, dtype=torch.bool, device=dev),
            collision=torch.zeros(B, dtype=torch.bool, device=dev),
            arm_dir=torch.zeros(B, A, dtype=torch.int32, device=dev),
            arm_grabbing=torch.zeros(B, A, dtype=torch.bool, device=dev),
            converting=torch.zeros(B, G, dtype=torch.bool, device=dev),
            conversion_target=torch.zeros(B, G, dtype=torch.int32, device=dev),
        )

        # Set initial arm directions
        for ai, arm in enumerate(self.arms):
            state.arm_dir[:, ai] = arm.initial_dir

        # Mark static area per omsim convention: arm bases, glyph footprints,
        # I/O positions, arm sweep along current direction.
        # omsim's initial_setup marks: glyph footprints, I/O positions,
        # arm base, arm length hexes, track hexes, cabinet walls.
        for arm in self.arms:
            if arm.base_idx >= 0:
                state.area_used[:, arm.base_idx] = True
            # Mark arm length hexes along initial direction
            bq, br = self._arm_base_qr[self.arms.index(arm)]
            dq, dr = DIR_VECTORS[arm.initial_dir]
            for step in range(1, arm.arm_len + 1):
                sq, sr = bq + dq * step, br + dr * step
                idx = hex_to_idx(sq, sr)
                if idx >= 0:
                    state.area_used[:, idx] = True
        for gi in self.glyphs:
            for fi in gi.footprint_indices:
                if fi >= 0:
                    state.area_used[:, fi] = True
        for inp in self.inputs:
            for ai in inp.atom_indices:
                if ai >= 0:
                    state.area_used[:, ai] = True
        for out in self.outputs:
            for ai in out.atom_indices:
                if ai >= 0:
                    state.area_used[:, ai] = True

        return state

    def _get_tip_idx(self, arm_idx: int, direction: int) -> int:
        """Get grid index of arm tip given current direction."""
        bq, br = self._arm_base_qr[arm_idx]
        return compute_tip_idx(bq, br, direction, self.arms[arm_idx].arm_len)

    def _get_tip_indices_batched(self, state: BoardState, arm_idx: int) -> torch.Tensor:
        """Get [B] tensor of tip grid indices for one arm."""
        B = state.arm_dir.shape[0]
        arm = self.arms[arm_idx]
        bq, br = self._arm_base_qr[arm_idx]
        dirs = state.arm_dir[:, arm_idx]  # [B]

        tip_indices = torch.full((B,), -1, dtype=torch.long, device=self.device)
        for d in range(6):
            mask = (dirs == d)
            if mask.any():
                tidx = compute_tip_idx(bq, br, d, arm.arm_len)
                tip_indices[mask] = tidx
        return tip_indices

    def evaluate_tapes(self, tapes: torch.Tensor, max_cycles: Optional[int] = None
                       ) -> torch.Tensor:
        """Run B simulations, return sum4 scores (inf if invalid).

        Args:
            tapes: [B, A, T] int32 tensor of instruction tapes per arm.
                   For single-arm, can be [B, T] (auto-expanded).
            max_cycles: Override max cycles.

        Returns:
            [B] float32 tensor of sum4 scores.
        """
        if max_cycles is None:
            max_cycles = self.max_cycles

        # Handle single-arm shorthand
        if tapes.dim() == 2:
            tapes = tapes.unsqueeze(1)  # [B, 1, T]

        tapes = tapes.to(self.device)
        B, A, T = tapes.shape
        assert A == len(self.arms), f"Expected {len(self.arms)} arms, got {A}"

        state = self._init_state(B)

        # Expand REPEAT instructions in tapes
        # REPEAT doubles the tape by copying prefix. For simplicity, we handle
        # it by pre-expanding into a flat tape indexed by cycle % period.
        # For now, strip REPEAT/RESET and just use raw tape with modular indexing.
        tape_lens = torch.full((B, A), T, dtype=torch.int32, device=self.device)

        for cycle in range(max_cycles):
            if state.done.all():
                break

            # Two half-cycles per cycle
            for half in range(2):
                self._step_half_cycle(state, tapes, tape_lens, cycle, half, B, A, T)

            # Check completion
            all_outputs = (state.output_count >= self.target_count).all(dim=1)  # [B]
            state.done |= all_outputs
            state.done |= state.collision

        # Compute metrics
        # cycles = cycle number when done (or max_cycles if not done)
        # We need to track per-sim completion cycle. For simplicity, we run
        # all sims for the same number of cycles and check at end.
        # Re-run to get accurate cycle counts:
        scores = self._compute_scores(state, tapes, tape_lens, max_cycles, B, A, T)
        return scores

    def evaluate_tapes_detailed(self, tapes: torch.Tensor,
                                max_cycles: Optional[int] = None
                                ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor,
                                           torch.Tensor, torch.Tensor]:
        """Like evaluate_tapes but returns (valid, cost, cycles, area, instructions).

        Returns:
            valid: [B] bool
            cost: [B] int32
            cycles: [B] int32
            area: [B] int32
            instructions: [B] int32
        """
        if max_cycles is None:
            max_cycles = self.max_cycles

        if tapes.dim() == 2:
            tapes = tapes.unsqueeze(1)

        tapes = tapes.to(self.device)
        B, A, T = tapes.shape
        state = self._init_state(B)
        tape_lens = torch.full((B, A), T, dtype=torch.int32, device=self.device)

        # Track completion cycle
        completion_cycle = torch.full((B,), max_cycles, dtype=torch.int32, device=self.device)

        for cycle in range(max_cycles):
            if state.done.all():
                break
            for half in range(2):
                self._step_half_cycle(state, tapes, tape_lens, cycle, half, B, A, T)

            all_outputs = (state.output_count >= self.target_count).all(dim=1)
            newly_done = all_outputs & ~state.done
            completion_cycle[newly_done] = cycle + 1
            state.done |= all_outputs

            collision_done = state.collision & ~state.done
            state.done |= state.collision

        valid = (state.output_count >= self.target_count).all(dim=1) & ~state.collision
        cost_t = torch.full((B,), self.cost, dtype=torch.int32, device=self.device)
        area_t = state.area_used.sum(dim=1).to(torch.int32)

        # Instructions: count from original tape (not expanded).
        # omsim counts non-noop instructions, excluding REPEAT/RESET markers.
        # Since we receive expanded tapes, the instruction count should be
        # pre-computed from the original solution and passed as a constant.
        instr_count = torch.full((B,), self._instruction_count, dtype=torch.int32, device=self.device)

        return valid, cost_t, completion_cycle, area_t, instr_count

    def _compute_scores(self, state: BoardState, tapes: torch.Tensor,
                        tape_lens: torch.Tensor, max_cycles: int,
                        B: int, A: int, T: int) -> torch.Tensor:
        """Compute sum4 scores from final state.

        Note: This is approximate — for accurate cycle counts, use
        evaluate_tapes_detailed which tracks completion per-sim.
        """
        valid = (state.output_count >= self.target_count).all(dim=1) & ~state.collision
        scores = torch.full((B,), float('inf'), dtype=torch.float32, device=self.device)

        if valid.any():
            cost_val = self.cost
            area = state.area_used.sum(dim=1).to(torch.float32)
            instr_val = self._instruction_count
            cycles = torch.full((B,), max_cycles, dtype=torch.float32, device=self.device)
            scores[valid] = (cost_val + cycles + area + instr_val)[valid]

        return scores

    def _step_half_cycle(self, state: BoardState, tapes: torch.Tensor,
                         tape_lens: torch.Tensor, cycle: int, half: int,
                         B: int, A: int, T: int):
        """Execute one half-cycle for all simulations."""
        active = ~state.done  # [B]
        if not active.any():
            return

        # 1. Decode and execute arm instructions
        for ai in range(A):
            self._execute_arm_instruction(state, tapes, tape_lens, cycle, half, ai, B, T, active)

        # 2. Mark arm area (arm sweeps)
        self._mark_arm_area(state, B, A)

        # 3. Spawn inputs (unblocked only)
        self._spawn_inputs(state, B, active)

        # 4. Apply glyphs
        self._apply_glyphs(state, B, half, active)

        # 5. Consume outputs
        self._consume_outputs(state, B, active)

        # 6. Check collisions (two atoms on same hex)
        self._check_collisions(state, B, active)

        # 7. Update area
        self._update_area(state, B)

    def _execute_arm_instruction(self, state: BoardState, tapes: torch.Tensor,
                                 tape_lens: torch.Tensor, cycle: int, half: int,
                                 arm_idx: int, B: int, T: int,
                                 active: torch.Tensor):
        """Execute one arm's instruction for this half-cycle.

        In omsim, arm instructions execute on BOTH half-cycles of each cycle.
        This is critical because atoms spawned in half 0 can be grabbed in half 1.
        """
        # Get current instruction
        tape_pos = cycle % T
        instr = tapes[:, arm_idx, tape_pos]  # [B]

        arm = self.arms[arm_idx]

        # omsim half-cycle split (sim.c line 909):
        #   half_cycle 1 (half=0): grab and drop
        #   half_cycle 2 (half=1): rotate, pivot, extend, retract, track

        if half == 0:
            # GRAB
            is_grab = (instr == INST_GRAB) & active
            if is_grab.any():
                self._do_grab(state, arm_idx, is_grab, B)

            # DROP
            is_drop = (instr == INST_DROP) & active
            if is_drop.any():
                self._do_drop(state, arm_idx, is_drop, B)

        else:  # half == 1
            # ROTATE CW
            is_rcw = (instr == INST_ROT_CW) & active
            if is_rcw.any():
                self._do_rotate(state, arm_idx, is_rcw, clockwise=True, B=B)

            # ROTATE CCW
            is_rccw = (instr == INST_ROT_CCW) & active
            if is_rccw.any():
                self._do_rotate(state, arm_idx, is_rccw, clockwise=False, B=B)

            # PIVOT CW
            is_pcw = (instr == INST_PIVOT_CW) & active
            if is_pcw.any():
                self._do_pivot(state, arm_idx, is_pcw, clockwise=True, B=B)

            # PIVOT CCW
            is_pccw = (instr == INST_PIVOT_CCW) & active
            if is_pccw.any():
                self._do_pivot(state, arm_idx, is_pccw, clockwise=False, B=B)

            # EXTEND / RETRACT — skip for now (piston-only)
            # TRACK — skip for now

    def _do_grab(self, state: BoardState, arm_idx: int,
                 mask: torch.Tensor, B: int):
        """Grab: arm grabs atom at tip position."""
        tip_indices = self._get_tip_indices_batched(state, arm_idx)  # [B]
        valid_tip = (tip_indices >= 0) & mask
        if not valid_tip.any():
            return

        # Set arm as grabbing
        state.arm_grabbing[:, arm_idx] |= mask

        # Mark tip atoms as grabbed (where there's actually an atom)
        for b_idx in valid_tip.nonzero(as_tuple=True)[0]:
            ti = tip_indices[b_idx].item()
            if state.element[b_idx, ti] != ELEM_EMPTY:
                state.grabbed[b_idx, ti] = True

    def _do_drop(self, state: BoardState, arm_idx: int,
                 mask: torch.Tensor, B: int):
        """Drop: arm releases all grabbed atoms."""
        # Clear arm grabbing state
        dropping = state.arm_grabbing[:, arm_idx] & mask
        state.arm_grabbing[:, arm_idx] &= ~mask

        if not dropping.any():
            return

        # Find all atoms grabbed by this arm and release them
        # In a single-arm case, just clear all grabbed flags
        # For multi-arm, we'd need per-arm grab tracking
        if len(self.arms) == 1:
            state.grabbed[dropping] = False
        else:
            # Multi-arm: only ungrab atoms at this arm's tip molecule
            for b_idx in dropping.nonzero(as_tuple=True)[0]:
                tip_idx = self._get_tip_indices_batched(state, arm_idx)[b_idx].item()
                if tip_idx >= 0:
                    # BFS to find connected molecule from tip
                    molecule = self._bfs_molecule(state, b_idx.item(), tip_idx)
                    for mi in molecule:
                        state.grabbed[b_idx, mi] = False

    def _do_rotate(self, state: BoardState, arm_idx: int,
                   mask: torch.Tensor, clockwise: bool, B: int):
        """Rotate arm: move tip and all grabbed connected atoms by ±60°."""
        arm = self.arms[arm_idx]
        bq, br = self._arm_base_qr[arm_idx]
        base_q, base_r = bq, br

        # Update arm direction
        if clockwise:
            state.arm_dir[:, arm_idx] = torch.where(
                mask, (state.arm_dir[:, arm_idx] - 1) % 6, state.arm_dir[:, arm_idx])
        else:
            state.arm_dir[:, arm_idx] = torch.where(
                mask, (state.arm_dir[:, arm_idx] + 1) % 6, state.arm_dir[:, arm_idx])

        # Move grabbed atoms
        grabbing = state.arm_grabbing[:, arm_idx] & mask
        if not grabbing.any():
            return

        self._rotate_grabbed_atoms(state, arm_idx, grabbing, clockwise, B)

    def _rotate_grabbed_atoms(self, state: BoardState, arm_idx: int,
                              mask: torch.Tensor, clockwise: bool, B: int):
        """Rotate all atoms grabbed by arm around its base."""
        arm = self.arms[arm_idx]
        bq, br = self._arm_base_qr[arm_idx]

        for b_idx in mask.nonzero(as_tuple=True)[0]:
            b = b_idx.item()

            # Find ALL grabbed atoms and their connected molecules.
            # We can't just look at the tip — after pivots, grabbed atoms
            # may not be at the current tip position.
            grabbed_indices = []
            for idx in range(NUM_HEXES):
                if state.grabbed[b, idx].item() and state.element[b, idx].item() != ELEM_EMPTY:
                    grabbed_indices.append(idx)

            if not grabbed_indices:
                continue

            # BFS from all grabbed atoms to find the full molecule
            molecule = set()
            for gi in grabbed_indices:
                if gi not in molecule:
                    mol = self._bfs_molecule(state, b, gi)
                    molecule.update(mol)

            molecule = list(molecule)
            if not molecule:
                continue

            # Compute new positions by rotating around arm base
            # We need to work in relative coords (offset by base)
            old_elements = {}
            old_bonds = {}
            old_grabbed = {}
            for mi in molecule:
                mq, mr = HEX_COORDS_LIST[mi]
                old_elements[mi] = state.element[b, mi].item()
                old_bonds[mi] = state.bonds[b, mi].clone()
                old_grabbed[mi] = state.grabbed[b, mi].item()

            # Clear old positions
            for mi in molecule:
                state.element[b, mi] = ELEM_EMPTY
                state.bonds[b, mi] = 0
                state.grabbed[b, mi] = False
                # Also clear bonds pointing TO these atoms
                for d in range(6):
                    nbr = NEIGHBOR_TABLE[mi, d].item()
                    if nbr >= 0 and nbr not in molecule:
                        state.bonds[b, nbr, REVERSE_DIR[d]] = 0

            # Compute new positions and place atoms
            new_positions = {}
            for mi in molecule:
                mq, mr = HEX_COORDS_LIST[mi]
                # Offset relative to arm base
                rq, rr = mq - bq, mr - br
                # Rotate
                if clockwise:
                    nrq, nrr = _rotate_hex_cw(rq, rr)
                else:
                    nrq, nrr = _rotate_hex_ccw(rq, rr)
                # Back to absolute
                nq, nr = nrq + bq, nrr + br
                new_idx = hex_to_idx(nq, nr)
                new_positions[mi] = new_idx

            # Place atoms at new positions
            for mi in molecule:
                new_idx = new_positions[mi]
                if new_idx < 0:
                    state.collision[b] = True
                    continue
                if state.element[b, new_idx] != ELEM_EMPTY and new_idx not in [new_positions[m] for m in molecule]:
                    state.collision[b] = True
                    continue
                state.element[b, new_idx] = old_elements[mi]
                state.grabbed[b, new_idx] = old_grabbed[mi]

            # Reconstruct bonds between moved atoms
            for mi in molecule:
                new_from = new_positions[mi]
                if new_from < 0:
                    continue
                for d in range(6):
                    bond_val = old_bonds[mi][d].item()
                    if bond_val == 0:
                        continue
                    nbr_old = NEIGHBOR_TABLE[mi, d].item()
                    if nbr_old >= 0 and nbr_old in molecule:
                        new_to = new_positions[nbr_old]
                        # Find new direction
                        new_d = _find_neighbor_dir(new_from, new_to)
                        if new_d >= 0 and new_to >= 0:
                            state.bonds[b, new_from, new_d] = bond_val

    def _do_pivot(self, state: BoardState, arm_idx: int,
                  mask: torch.Tensor, clockwise: bool, B: int):
        """Pivot: rotate arm base around grabbed molecule (reverse of rotate)."""
        # Pivot moves the arm base, not the atoms. For simplicity in initial
        # implementation, treat like rotate but without moving atoms.
        # Update arm direction only.
        if clockwise:
            state.arm_dir[:, arm_idx] = torch.where(
                mask, (state.arm_dir[:, arm_idx] - 1) % 6, state.arm_dir[:, arm_idx])
        else:
            state.arm_dir[:, arm_idx] = torch.where(
                mask, (state.arm_dir[:, arm_idx] + 1) % 6, state.arm_dir[:, arm_idx])

    def _bfs_molecule(self, state: BoardState, b: int, start: int) -> List[int]:
        """BFS from start hex to find all connected atoms via bonds (single sim)."""
        if state.element[b, start].item() == ELEM_EMPTY:
            return []
        visited = {start}
        frontier = [start]
        while frontier:
            next_frontier = []
            for idx in frontier:
                for d in range(6):
                    if state.bonds[b, idx, d].item() > 0:
                        nbr = NEIGHBOR_TABLE[idx, d].item()
                        if nbr >= 0 and nbr not in visited and state.element[b, nbr].item() != ELEM_EMPTY:
                            visited.add(nbr)
                            next_frontier.append(nbr)
            frontier = next_frontier
        return list(visited)

    def _bfs_molecule_grabbed(self, state: BoardState, b: int, start: int) -> List[int]:
        """BFS from start to find connected atoms, including grabbed check."""
        if state.element[b, start].item() == ELEM_EMPTY:
            return []
        if not state.grabbed[b, start].item():
            return []
        visited = {start}
        frontier = [start]
        while frontier:
            next_frontier = []
            for idx in frontier:
                for d in range(6):
                    if state.bonds[b, idx, d].item() > 0:
                        nbr = NEIGHBOR_TABLE[idx, d].item()
                        if nbr >= 0 and nbr not in visited and state.element[b, nbr].item() != ELEM_EMPTY:
                            visited.add(nbr)
                            next_frontier.append(nbr)
            frontier = next_frontier
        return list(visited)

    def _mark_arm_area(self, state: BoardState, B: int, A: int):
        """Mark hexes along arm length as used area."""
        for ai in range(A):
            arm = self.arms[ai]
            bq, br = self._arm_base_qr[ai]
            for d in range(6):
                d_mask = (state.arm_dir[:, ai] == d)
                if not d_mask.any():
                    continue
                dq, dr = DIR_VECTORS[d]
                for step in range(1, arm.arm_len + 1):
                    sq, sr = bq + dq * step, br + dr * step
                    idx = hex_to_idx(sq, sr)
                    if idx >= 0:
                        state.area_used[d_mask, idx] = True

    def _spawn_inputs(self, state: BoardState, B: int, active: torch.Tensor):
        """Spawn input atoms at unblocked input positions."""
        for inp in self.inputs:
            # Check if all input positions are empty (unblocked)
            blocked = torch.zeros(B, dtype=torch.bool, device=self.device)
            for ai in inp.atom_indices:
                if ai >= 0:
                    blocked |= (state.element[:, ai] != ELEM_EMPTY)

            spawn = active & ~blocked
            if not spawn.any():
                continue

            # Place atoms
            for j, ai in enumerate(inp.atom_indices):
                if ai >= 0:
                    state.element[spawn, ai] = inp.atom_elements[j]

    def _apply_glyphs(self, state: BoardState, B: int, half: int,
                      active: torch.Tensor):
        """Apply all glyphs (vectorized across batch)."""
        for gi_idx, gi in enumerate(self.glyphs):
            if gi.glyph_type == 'glyph-calcification':
                self._apply_calcification(state, gi, active, B)
            elif gi.glyph_type == 'bonder':
                self._apply_bonding(state, gi, active, B)
            elif gi.glyph_type == 'unbonder':
                self._apply_unbonding(state, gi, active, B)
            elif gi.glyph_type == 'bonder-prisma':
                self._apply_triplex_bonding(state, gi, active, B)
            elif gi.glyph_type == 'bonder-speed':
                self._apply_multi_bonding(state, gi, active, B)
            elif gi.glyph_type == 'glyph-projection':
                self._apply_projection(state, gi, active, B)
            elif gi.glyph_type == 'glyph-life-and-death':
                self._apply_animismus(state, gi, gi_idx, half, active, B)
            elif gi.glyph_type == 'glyph-purification':
                self._apply_purification(state, gi, gi_idx, half, active, B)
            elif gi.glyph_type == 'glyph-dispersion':
                self._apply_dispersion(state, gi, gi_idx, half, active, B)
            elif gi.glyph_type == 'glyph-unification':
                self._apply_unification(state, gi, gi_idx, half, active, B)
            elif gi.glyph_type == 'glyph-duplication':
                self._apply_duplication(state, gi, active, B)
            elif gi.glyph_type == 'glyph-disposal':
                self._apply_disposal(state, gi, active, B)

    def _apply_calcification(self, state: BoardState, gi: GlyphInstance,
                             active: torch.Tensor, B: int):
        """Calcification: cardinal element → salt."""
        idx = gi.slot_indices[0]
        if idx < 0:
            return
        elem = state.element[:, idx]  # [B]
        is_cardinal = (
            (elem == ELEM_AIR) | (elem == ELEM_EARTH) |
            (elem == ELEM_FIRE) | (elem == ELEM_WATER)
        )
        # Calcification does NOT check grab state (omsim behavior)
        do_calc = active & is_cardinal
        state.element[:, idx] = torch.where(do_calc, ELEM_SALT, state.element[:, idx])

    def _apply_bonding(self, state: BoardState, gi: GlyphInstance,
                       active: torch.Tensor, B: int):
        """Bonding: create normal bond between two active slots."""
        if len(gi.slot_indices) < 2:
            return
        s0, s1 = gi.slot_indices[0], gi.slot_indices[1]
        if s0 < 0 or s1 < 0:
            return

        # Bonding does NOT check grab state (omsim behavior)
        has_both = (
            (state.element[:, s0] != ELEM_EMPTY) &
            (state.element[:, s1] != ELEM_EMPTY) &
            active
        )
        if not has_both.any():
            return

        d = _find_neighbor_dir(s0, s1)
        if d < 0:
            return

        # Don't bond if triplex bond already exists
        no_triplex = (state.bonds[:, s0, d] & (BOND_TRIPLEX_R | BOND_TRIPLEX_Y | BOND_TRIPLEX_K)) == 0
        do_bond = has_both & no_triplex

        state.bonds[:, s0, d] = torch.where(
            do_bond, torch.tensor(BOND_NORMAL, dtype=torch.int8, device=self.device),
            state.bonds[:, s0, d])
        rd = REVERSE_DIR[d]
        state.bonds[:, s1, rd] = torch.where(
            do_bond, torch.tensor(BOND_NORMAL, dtype=torch.int8, device=self.device),
            state.bonds[:, s1, rd])

    def _apply_unbonding(self, state: BoardState, gi: GlyphInstance,
                         active: torch.Tensor, B: int):
        """Unbonding: remove bond between two active slots."""
        if len(gi.slot_indices) < 2:
            return
        s0, s1 = gi.slot_indices[0], gi.slot_indices[1]
        if s0 < 0 or s1 < 0:
            return

        d = _find_neighbor_dir(s0, s1)
        if d < 0:
            return

        has_bond = (state.bonds[:, s0, d] != BOND_NONE) & active
        state.bonds[:, s0, d] = torch.where(
            has_bond, torch.tensor(BOND_NONE, dtype=torch.int8, device=self.device),
            state.bonds[:, s0, d])
        rd = REVERSE_DIR[d]
        state.bonds[:, s1, rd] = torch.where(
            has_bond, torch.tensor(BOND_NONE, dtype=torch.int8, device=self.device),
            state.bonds[:, s1, rd])

    def _apply_triplex_bonding(self, state: BoardState, gi: GlyphInstance,
                               active: torch.Tensor, B: int):
        """Triplex bonding: create R/Y/K bonds between 3 slots (all must be fire)."""
        if len(gi.slot_indices) < 3:
            return
        s0, s1, s2 = gi.slot_indices[0], gi.slot_indices[1], gi.slot_indices[2]
        if any(s < 0 for s in (s0, s1, s2)):
            return

        # All three must be fire and ungrabbed
        all_fire = (
            (state.element[:, s0] == ELEM_FIRE) &
            (state.element[:, s1] == ELEM_FIRE) &
            (state.element[:, s2] == ELEM_FIRE) &
            ~state.grabbed[:, s0] & ~state.grabbed[:, s1] & ~state.grabbed[:, s2] &
            active
        )
        if not all_fire.any():
            return

        # Bond pairs: (s0,s1)=R, (s0,s2)=Y, (s1,s2)=K (approximately)
        pairs_types = [(s0, s1, BOND_TRIPLEX_R), (s0, s2, BOND_TRIPLEX_Y), (s1, s2, BOND_TRIPLEX_K)]
        for sa, sb, btype in pairs_types:
            d = _find_neighbor_dir(sa, sb)
            if d < 0:
                continue
            state.bonds[:, sa, d] = torch.where(
                all_fire, torch.tensor(btype, dtype=torch.int8, device=self.device),
                state.bonds[:, sa, d])
            rd = REVERSE_DIR[d]
            state.bonds[:, sb, rd] = torch.where(
                all_fire, torch.tensor(btype, dtype=torch.int8, device=self.device),
                state.bonds[:, sb, rd])

    def _apply_multi_bonding(self, state: BoardState, gi: GlyphInstance,
                             active: torch.Tensor, B: int):
        """Multi-bonder: bond center to each neighbor slot."""
        if len(gi.slot_indices) < 2:
            return
        center = gi.slot_indices[0]
        if center < 0:
            return

        for si in gi.slot_indices[1:]:
            if si < 0:
                continue
            # Multi-bonding does NOT check grab state
            has_both = (
                (state.element[:, center] != ELEM_EMPTY) &
                (state.element[:, si] != ELEM_EMPTY) &
                active
            )
            d = _find_neighbor_dir(center, si)
            if d < 0:
                continue
            no_triplex = (state.bonds[:, center, d] & (BOND_TRIPLEX_R | BOND_TRIPLEX_Y | BOND_TRIPLEX_K)) == 0
            do_bond = has_both & no_triplex
            state.bonds[:, center, d] = torch.where(
                do_bond, torch.tensor(BOND_NORMAL, dtype=torch.int8, device=self.device),
                state.bonds[:, center, d])
            rd = REVERSE_DIR[d]
            state.bonds[:, si, rd] = torch.where(
                do_bond, torch.tensor(BOND_NORMAL, dtype=torch.int8, device=self.device),
                state.bonds[:, si, rd])

    def _apply_projection(self, state: BoardState, gi: GlyphInstance,
                          active: torch.Tensor, B: int):
        """Projection: consume quicksilver, promote adjacent metal."""
        if len(gi.slot_indices) < 2:
            return
        qs_idx = gi.slot_indices[0]   # quicksilver slot
        metal_idx = gi.slot_indices[1]  # metal slot
        if qs_idx < 0 or metal_idx < 0:
            return

        has_qs = (state.element[:, qs_idx] == ELEM_QUICKSILVER) & ~state.grabbed[:, qs_idx]
        # Check quicksilver has no bonds (must be unbonded)
        qs_unbonded = (state.bonds[:, qs_idx].sum(dim=1) == 0)

        metal_elem = state.element[:, metal_idx]
        is_promotable = (
            (metal_elem == ELEM_LEAD) | (metal_elem == ELEM_TIN) |
            (metal_elem == ELEM_IRON) | (metal_elem == ELEM_COPPER) |
            (metal_elem == ELEM_SILVER)
        )

        do_project = active & has_qs & qs_unbonded & is_promotable
        if not do_project.any():
            return

        # Remove quicksilver
        state.element[:, qs_idx] = torch.where(
            do_project, ELEM_EMPTY, state.element[:, qs_idx])

        # Promote metal
        for old, new in METAL_PROMOTE.items():
            match = do_project & (metal_elem == old)
            state.element[:, metal_idx] = torch.where(
                match, new, state.element[:, metal_idx])

    def _apply_animismus(self, state: BoardState, gi: GlyphInstance,
                         gi_idx: int, half: int, active: torch.Tensor, B: int):
        """Animismus (Life and Death): 2 salt → vitae + mors (conversion glyph).

        Half 0: consume inputs, set converting flag.
        Half 1: produce outputs if converting.
        """
        # Slots: [salt_0, salt_1, vitae_out, mors_out]
        if len(gi.slot_indices) < 4:
            return
        s_in0, s_in1 = gi.slot_indices[0], gi.slot_indices[1]
        s_out0, s_out1 = gi.slot_indices[2], gi.slot_indices[3]

        if half == 0:
            # Check inputs: both must be salt, ungrabbed, unbonded
            can_convert = (
                active &
                (state.element[:, s_in0] == ELEM_SALT) &
                (state.element[:, s_in1] == ELEM_SALT) &
                ~state.grabbed[:, s_in0] & ~state.grabbed[:, s_in1] &
                (state.bonds[:, s_in0].sum(dim=1) == 0) &
                (state.bonds[:, s_in1].sum(dim=1) == 0) &
                (state.element[:, s_out0] == ELEM_EMPTY) &
                (state.element[:, s_out1] == ELEM_EMPTY)
            )
            # Consume inputs
            state.element[:, s_in0] = torch.where(can_convert, ELEM_EMPTY, state.element[:, s_in0])
            state.element[:, s_in1] = torch.where(can_convert, ELEM_EMPTY, state.element[:, s_in1])
            state.converting[:, gi_idx] = can_convert
        else:  # half == 1
            converting = state.converting[:, gi_idx] & active
            if converting.any():
                state.element[:, s_out0] = torch.where(
                    converting, ELEM_VITAE, state.element[:, s_out0])
                state.element[:, s_out1] = torch.where(
                    converting, ELEM_MORS, state.element[:, s_out1])
                state.converting[:, gi_idx] = False

    def _apply_purification(self, state: BoardState, gi: GlyphInstance,
                            gi_idx: int, half: int, active: torch.Tensor, B: int):
        """Purification: 2 same metals → 1 promoted metal (conversion)."""
        if len(gi.slot_indices) < 3:
            return
        s_in0, s_in1, s_out = gi.slot_indices[0], gi.slot_indices[1], gi.slot_indices[2]

        if half == 0:
            elem0 = state.element[:, s_in0]
            elem1 = state.element[:, s_in1]
            same_metal = (elem0 == elem1)
            is_promotable = (
                (elem0 == ELEM_LEAD) | (elem0 == ELEM_TIN) |
                (elem0 == ELEM_IRON) | (elem0 == ELEM_COPPER) |
                (elem0 == ELEM_SILVER)
            )
            can_convert = (
                active & same_metal & is_promotable &
                ~state.grabbed[:, s_in0] & ~state.grabbed[:, s_in1] &
                (state.bonds[:, s_in0].sum(dim=1) == 0) &
                (state.bonds[:, s_in1].sum(dim=1) == 0) &
                (state.element[:, s_out] == ELEM_EMPTY)
            )
            # Compute promoted element and store it
            target = torch.zeros(B, dtype=torch.int32, device=self.device)
            for old, new in METAL_PROMOTE.items():
                target = torch.where(can_convert & (elem0 == old), new, target)
            state.conversion_target[:, gi_idx] = torch.where(
                can_convert, target, state.conversion_target[:, gi_idx])

            state.element[:, s_in0] = torch.where(can_convert, ELEM_EMPTY, state.element[:, s_in0])
            state.element[:, s_in1] = torch.where(can_convert, ELEM_EMPTY, state.element[:, s_in1])
            state.converting[:, gi_idx] = can_convert
        else:
            converting = state.converting[:, gi_idx] & active
            if converting.any():
                target = state.conversion_target[:, gi_idx]
                state.element[:, s_out] = torch.where(converting, target, state.element[:, s_out])
                state.converting[:, gi_idx] = False

    def _apply_dispersion(self, state: BoardState, gi: GlyphInstance,
                          gi_idx: int, half: int, active: torch.Tensor, B: int):
        """Dispersion: quintessence → earth + water + fire + air (conversion)."""
        if len(gi.slot_indices) < 5:
            return
        s_in = gi.slot_indices[0]
        s_earth, s_water, s_fire, s_air = gi.slot_indices[1], gi.slot_indices[2], gi.slot_indices[3], gi.slot_indices[4]

        if half == 0:
            can_convert = (
                active &
                (state.element[:, s_in] == ELEM_QUINTESSENCE) &
                ~state.grabbed[:, s_in] &
                (state.bonds[:, s_in].sum(dim=1) == 0) &
                (state.element[:, s_earth] == ELEM_EMPTY) &
                (state.element[:, s_water] == ELEM_EMPTY) &
                (state.element[:, s_fire] == ELEM_EMPTY) &
                (state.element[:, s_air] == ELEM_EMPTY)
            )
            state.element[:, s_in] = torch.where(can_convert, ELEM_EMPTY, state.element[:, s_in])
            state.converting[:, gi_idx] = can_convert
        else:
            converting = state.converting[:, gi_idx] & active
            if converting.any():
                state.element[:, s_earth] = torch.where(converting, ELEM_EARTH, state.element[:, s_earth])
                state.element[:, s_water] = torch.where(converting, ELEM_WATER, state.element[:, s_water])
                state.element[:, s_fire] = torch.where(converting, ELEM_FIRE, state.element[:, s_fire])
                state.element[:, s_air] = torch.where(converting, ELEM_AIR, state.element[:, s_air])
                state.converting[:, gi_idx] = False

    def _apply_unification(self, state: BoardState, gi: GlyphInstance,
                           gi_idx: int, half: int, active: torch.Tensor, B: int):
        """Unification: earth + water + fire + air → quintessence (conversion)."""
        if len(gi.slot_indices) < 5:
            return
        s_card0, s_card1, s_card2, s_card3 = gi.slot_indices[0], gi.slot_indices[1], gi.slot_indices[2], gi.slot_indices[3]
        s_out = gi.slot_indices[4]

        if half == 0:
            # Need one of each cardinal, ungrabbed, unbonded
            elems = [state.element[:, s] for s in [s_card0, s_card1, s_card2, s_card3]]
            all_cardinal = torch.ones(B, dtype=torch.bool, device=self.device)
            elem_set = torch.zeros(B, 17, dtype=torch.bool, device=self.device)
            for i, s in enumerate([s_card0, s_card1, s_card2, s_card3]):
                e = state.element[:, s]
                is_card = (e == ELEM_AIR) | (e == ELEM_EARTH) | (e == ELEM_FIRE) | (e == ELEM_WATER)
                all_cardinal &= is_card
                all_cardinal &= ~state.grabbed[:, s]
                all_cardinal &= (state.bonds[:, s].sum(dim=1) == 0)
                # Track which elements present
                for ce in [ELEM_AIR, ELEM_EARTH, ELEM_FIRE, ELEM_WATER]:
                    elem_set[:, ce] |= (e == ce)

            has_all_four = elem_set[:, ELEM_AIR] & elem_set[:, ELEM_EARTH] & elem_set[:, ELEM_FIRE] & elem_set[:, ELEM_WATER]

            can_convert = active & all_cardinal & has_all_four & (state.element[:, s_out] == ELEM_EMPTY)
            for s in [s_card0, s_card1, s_card2, s_card3]:
                state.element[:, s] = torch.where(can_convert, ELEM_EMPTY, state.element[:, s])
            state.converting[:, gi_idx] = can_convert
        else:
            converting = state.converting[:, gi_idx] & active
            if converting.any():
                state.element[:, s_out] = torch.where(converting, ELEM_QUINTESSENCE, state.element[:, s_out])
                state.converting[:, gi_idx] = False

    def _apply_duplication(self, state: BoardState, gi: GlyphInstance,
                           active: torch.Tensor, B: int):
        """Duplication: cardinal + salt → cardinal + copy(cardinal)."""
        if len(gi.slot_indices) < 2:
            return
        s_card = gi.slot_indices[0]  # cardinal input
        s_salt = gi.slot_indices[1]  # salt that becomes copy
        if s_card < 0 or s_salt < 0:
            return

        elem = state.element[:, s_card]
        is_cardinal = (elem == ELEM_AIR) | (elem == ELEM_EARTH) | (elem == ELEM_FIRE) | (elem == ELEM_WATER)
        has_salt = (state.element[:, s_salt] == ELEM_SALT)
        do_dup = active & is_cardinal & has_salt & ~state.grabbed[:, s_card] & ~state.grabbed[:, s_salt]

        # Salt becomes copy of cardinal
        state.element[:, s_salt] = torch.where(do_dup, elem, state.element[:, s_salt])

    def _apply_disposal(self, state: BoardState, gi: GlyphInstance,
                        active: torch.Tensor, B: int):
        """Disposal: remove atom at center if ungrabbed and unbonded."""
        idx = gi.slot_indices[0]
        if idx < 0:
            return
        has_atom = (state.element[:, idx] != ELEM_EMPTY) & ~state.grabbed[:, idx]
        unbonded = (state.bonds[:, idx].sum(dim=1) == 0)
        do_dispose = active & has_atom & unbonded
        state.element[:, idx] = torch.where(do_dispose, ELEM_EMPTY, state.element[:, idx])

    def _consume_outputs(self, state: BoardState, B: int, active: torch.Tensor):
        """Check and consume completed output molecules."""
        for out in self.outputs:
            if out.center_idx < 0:
                continue

            # Check center has an atom
            has_center = (state.element[:, out.center_idx] != ELEM_EMPTY) & active
            if not has_center.any():
                continue

            # Check all atoms match expected elements
            match = has_center.clone()
            for j, (ai, expected_elem) in enumerate(zip(out.atom_indices, out.atom_elements)):
                if ai < 0:
                    match[:] = False
                    break
                match &= (state.element[:, ai] == expected_elem)
                match &= ~state.grabbed[:, ai]

            # Check bonds match
            for fi, ti, d in out.bond_pairs:
                if fi < 0 or ti < 0 or d < 0:
                    match[:] = False
                    break
                match &= (state.bonds[:, fi, d] != BOND_NONE)

            # Check molecule size matches (BFS from center should find exactly N atoms)
            # Skip exact size check for performance — atom+bond match is usually sufficient

            if not match.any():
                continue

            # Remove matched atoms
            for ai in out.atom_indices:
                if ai >= 0:
                    state.element[:, ai] = torch.where(match, ELEM_EMPTY, state.element[:, ai])
                    state.bonds[match, ai, :] = 0
                    state.grabbed[:, ai] = torch.where(match, False, state.grabbed[:, ai])
                    # Clear incoming bonds
                    for d in range(6):
                        nbr = NEIGHBOR_TABLE[ai, d].item()
                        if nbr >= 0:
                            rd = REVERSE_DIR[d]
                            state.bonds[match, nbr, rd] = 0

            state.output_count[:, out.io_index] += match.to(torch.int32)

    def _check_collisions(self, state: BoardState, B: int, active: torch.Tensor):
        """Check for two atoms occupying the same hex (shouldn't happen with correct movement)."""
        # In our model, collisions are detected during movement.
        # This is a safety check — if element has a value and we tried to place another.
        pass  # Handled during _rotate_grabbed_atoms

    def _update_area(self, state: BoardState, B: int):
        """Update area tracking: area_used |= (element != 0)."""
        has_atom = (state.element != ELEM_EMPTY)  # [B, 91]
        state.area_used |= has_atom


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _rotate_local_to_world(origin: HexCoord, rotation: int, local: HexCoord) -> HexCoord:
    """Rotate a local coordinate around origin by rotation*60°.

    Uses the omsim convention: world = origin + DIRECTIONS[rot]*q + DIRECTIONS[(rot+1)%6]*r
    where local.q and local.r are the du, dv offsets.
    """
    return local_to_world(origin, rotation, local.q, local.r)


def _find_direction(from_hex: HexCoord, to_hex: HexCoord) -> int:
    """Find direction index from one hex to adjacent hex. -1 if not adjacent."""
    dq = to_hex.q - from_hex.q
    dr = to_hex.r - from_hex.r
    for d, (vq, vr) in enumerate(DIR_VECTORS):
        if dq == vq and dr == vr:
            return d
    return -1


def _find_neighbor_dir(idx_a: int, idx_b: int) -> int:
    """Find direction from grid index a to grid index b. -1 if not neighbors."""
    for d in range(6):
        if NEIGHBOR_TABLE[idx_a, d].item() == idx_b:
            return d
    return -1


# ---------------------------------------------------------------------------
# Convenience: create simulator from puzzle + solution files
# ---------------------------------------------------------------------------

def expand_tape(tape: List[int]) -> List[int]:
    """Expand RESET and REPEAT instructions in a tape.

    RESET ('X'): copies the prefix before the RESET to double the tape.
    REPEAT ('C'): copies the prefix before the REPEAT.
    Both are removed from the final tape.
    """
    result = list(tape)

    # Handle RESET: find it, copy prefix
    while True:
        try:
            idx = result.index(INST_RESET)
        except ValueError:
            break
        # Everything before the RESET is the prefix
        prefix = result[:idx]
        # Replace: prefix + reset + suffix → prefix + prefix + suffix
        result = prefix + prefix + result[idx + 1:]

    # Handle REPEAT: similar to RESET
    while True:
        try:
            idx = result.index(INST_REPEAT)
        except ValueError:
            break
        prefix = result[:idx]
        result = prefix + prefix + result[idx + 1:]

    # Remove any remaining 0 (null/noop) entries at the end
    while result and result[-1] == 0:
        result.pop()

    return result if result else [0]


def create_simulator(puzzle_path: str, solution_path: str,
                     device: str = 'mps', max_cycles: int = 200) -> BatchSimulator:
    """Create a BatchSimulator from puzzle and solution file paths."""
    puzzle = parse_puzzle(puzzle_path)
    solution = parse_solution(solution_path)
    return BatchSimulator(puzzle, solution, device=device, max_cycles=max_cycles)


def create_simulator_from_objects(puzzle: Puzzle, solution: Solution,
                                  device: str = 'mps',
                                  max_cycles: int = 200) -> BatchSimulator:
    """Create a BatchSimulator from pre-parsed puzzle and solution objects."""
    return BatchSimulator(puzzle, solution, device=device, max_cycles=max_cycles)
