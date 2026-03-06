"""Cross-validation test harness for GPU BatchSimulator vs C omsim.

Runs identical simulations on both and compares results. Invoke as:
    uv run python -m solver.gpu_sim_test --smoke
    uv run python -m solver.gpu_sim_test --archive-dir tools/om-archive --max 100
    uv run python -m solver.gpu_sim_test --fuzz P007 P009 --n-random 1000
    uv run python -m solver.gpu_sim_test --benchmark P056 --batch-size 10000
"""
from __future__ import annotations

import argparse
import random
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

import torch

from .gpu_sim import BatchSimulator, create_simulator, NUM_HEXES, expand_tape
from .puzzle import Puzzle, parse_puzzle
from .solution import (Solution, Part, Inst, Instruction, parse_solution,
                        solution_to_bytes)
from .simulator import Simulator, VerifyResult


@dataclass
class ValidationResult:
    """Result of comparing GPU sim vs C omsim on one solution."""
    puzzle_name: str
    solution_name: str
    passed: bool
    gpu_valid: bool = False
    cpu_valid: bool = False
    gpu_cycles: int = -1
    cpu_cycles: int = -1
    gpu_area: int = -1
    cpu_area: int = -1
    gpu_cost: int = -1
    cpu_cost: int = -1
    gpu_instructions: int = -1
    cpu_instructions: int = -1
    error: str = ""


@dataclass
class ValidationReport:
    """Summary of a batch validation run."""
    results: List[ValidationResult] = field(default_factory=list)

    @property
    def n_passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def n_failed(self) -> int:
        return sum(1 for r in self.results if not r.passed)

    @property
    def n_total(self) -> int:
        return len(self.results)

    def first_failure(self) -> Optional[ValidationResult]:
        for r in self.results:
            if not r.passed:
                return r
        return None

    def summary(self) -> str:
        lines = [f"Validation: {self.n_passed}/{self.n_total} passed"]
        fail = self.first_failure()
        if fail:
            lines.append(f"First failure: {fail.puzzle_name} / {fail.solution_name}")
            lines.append(f"  GPU: valid={fail.gpu_valid} cycles={fail.gpu_cycles} "
                         f"area={fail.gpu_area} cost={fail.gpu_cost} instr={fail.gpu_instructions}")
            lines.append(f"  CPU: valid={fail.cpu_valid} cycles={fail.cpu_cycles} "
                         f"area={fail.cpu_area} cost={fail.cpu_cost} instr={fail.cpu_instructions}")
            if fail.error:
                lines.append(f"  Error: {fail.error}")
        return "\n".join(lines)


class GPUSimValidator:
    """Cross-validate GPU simulator against C omsim."""

    def __init__(self, device: str = 'mps'):
        self.device = device
        self.cpu_sim = Simulator()

    def validate_solution(self, puzzle_path: str, solution_path: str,
                          max_cycles: int = 500) -> ValidationResult:
        """Run one solution through both simulators, compare metrics."""
        puzzle_name = Path(puzzle_path).stem
        sol_name = Path(solution_path).stem

        result = ValidationResult(puzzle_name=puzzle_name, solution_name=sol_name, passed=False)

        try:
            # 1. Parse puzzle + solution
            puzzle = parse_puzzle(puzzle_path)
            solution = parse_solution(solution_path)

            # 2. Run C omsim
            puzzle_bytes = Path(puzzle_path).read_bytes()
            sol_bytes = solution_to_bytes(solution)
            cpu_result = self.cpu_sim.verify_bytes(puzzle_bytes, sol_bytes, cycle_limit=max_cycles)

            result.cpu_valid = cpu_result.valid
            result.cpu_cycles = cpu_result.cycles
            result.cpu_area = cpu_result.area
            result.cpu_cost = cpu_result.cost
            result.cpu_instructions = cpu_result.instructions

            # 3. Run GPU sim
            gpu_sim = BatchSimulator(puzzle, solution, device=self.device, max_cycles=max_cycles)

            # Extract tapes from solution
            arms = [p for p in solution.parts if p.is_arm]
            if not arms:
                result.error = "No arms in solution"
                return result

            # Extract and expand tapes (handle RESET/REPEAT)
            raw_tape_len = max(
                (max((inst.index for inst in arm.instructions), default=0) + 1)
                for arm in arms
            ) if arms else 1
            raw_tape_len = max(raw_tape_len, 1)

            expanded_tapes = []
            for arm in arms:
                raw = arm.get_tape(raw_tape_len)
                expanded = expand_tape(raw)
                expanded_tapes.append(expanded)

            # Pad to same length
            max_tape_len = max(len(t) for t in expanded_tapes)
            tape_tensors = []
            for t in expanded_tapes:
                padded = t + [0] * (max_tape_len - len(t))
                tape_tensors.append(torch.tensor(padded, dtype=torch.int32))

            tapes = torch.stack(tape_tensors).unsqueeze(0)  # [1, A, T]

            gpu_valid, gpu_cost, gpu_cycles, gpu_area, gpu_instr = \
                gpu_sim.evaluate_tapes_detailed(tapes, max_cycles=max_cycles)

            result.gpu_valid = gpu_valid[0].item()
            result.gpu_cycles = gpu_cycles[0].item()
            result.gpu_area = gpu_area[0].item()
            result.gpu_cost = gpu_cost[0].item()
            result.gpu_instructions = gpu_instr[0].item()

            # 4. Compare
            if result.gpu_valid != result.cpu_valid:
                result.error = f"validity mismatch: GPU={result.gpu_valid} CPU={result.cpu_valid}"
                return result

            if result.gpu_valid and result.cpu_valid:
                mismatches = []
                if result.gpu_cycles != result.cpu_cycles:
                    mismatches.append(f"cycles: GPU={result.gpu_cycles} CPU={result.cpu_cycles}")
                if result.gpu_cost != result.cpu_cost:
                    mismatches.append(f"cost: GPU={result.gpu_cost} CPU={result.cpu_cost}")
                if result.gpu_area != result.cpu_area:
                    mismatches.append(f"area: GPU={result.gpu_area} CPU={result.cpu_area}")
                if result.gpu_instructions != result.cpu_instructions:
                    mismatches.append(f"instr: GPU={result.gpu_instructions} CPU={result.cpu_instructions}")
                if mismatches:
                    result.error = "; ".join(mismatches)
                    return result

            result.passed = True
            return result

        except Exception as e:
            result.error = str(e)
            return result

    def validate_archive(self, archive_dir: str, puzzle_dir: str,
                         max_solutions: int = 100) -> ValidationReport:
        """Batch validate against archive solutions."""
        report = ValidationReport()
        archive_path = Path(archive_dir)
        puzzle_base = Path(puzzle_dir)

        # Find all solution files
        sol_files = sorted(archive_path.rglob("*.solution"))[:max_solutions]

        for sol_path in sol_files:
            # Try to find matching puzzle
            try:
                sol = parse_solution(str(sol_path))
                puzzle_name = sol.puzzle_name
            except Exception:
                continue

            # Search for puzzle file
            puzzle_files = list(puzzle_base.rglob(f"{puzzle_name}.puzzle"))
            if not puzzle_files:
                # Try without prefix
                puzzle_files = list(puzzle_base.rglob(f"*{puzzle_name}*.puzzle"))
            if not puzzle_files:
                continue

            puzzle_path = str(puzzle_files[0])
            result = self.validate_solution(puzzle_path, str(sol_path))
            report.results.append(result)

            status = "PASS" if result.passed else "FAIL"
            print(f"  [{status}] {result.puzzle_name}/{result.solution_name}"
                  + (f" — {result.error}" if result.error else ""))

            if not result.passed and report.n_failed >= 5:
                print("  Stopping after 5 failures")
                break

        return report

    def validate_tape_variants(self, puzzle_path: str, solution_path: str,
                               n_random: int = 1000, max_cycles: int = 200
                               ) -> ValidationReport:
        """Generate random tape mutations, verify both sims agree."""
        report = ValidationReport()
        puzzle = parse_puzzle(puzzle_path)
        solution = parse_solution(solution_path)
        puzzle_bytes = Path(puzzle_path).read_bytes()

        arms = [p for p in solution.parts if p.is_arm]
        if not arms:
            return report

        gpu_sim = BatchSimulator(puzzle, solution, device=self.device, max_cycles=max_cycles)

        VALID_INSTS = [Inst.GRAB, Inst.DROP, Inst.ROTATE_CW, Inst.ROTATE_CCW,
                       Inst.PIVOT_CW, Inst.PIVOT_CCW, Inst.NOOP, 0]

        max_tape_len = max(
            (max((inst.index for inst in arm.instructions), default=0) + 1)
            for arm in arms
        ) if arms else 1
        tape_len = max(max_tape_len, 5)

        for i in range(n_random):
            # Generate random tape mutation
            mut_solution = _clone_solution(solution)
            for arm in [p for p in mut_solution.parts if p.is_arm]:
                tape = arm.get_tape(tape_len)
                # Mutate 1-3 positions
                n_muts = random.randint(1, 3)
                for _ in range(n_muts):
                    pos = random.randint(0, tape_len - 1)
                    tape[pos] = random.choice(VALID_INSTS)
                arm.set_tape(tape)

            # Run C omsim
            sol_bytes = solution_to_bytes(mut_solution)
            cpu_result = self.cpu_sim.verify_bytes(puzzle_bytes, sol_bytes, cycle_limit=max_cycles)

            # Run GPU sim
            mut_arms = [p for p in mut_solution.parts if p.is_arm]
            tape_tensors = []
            for arm in mut_arms:
                t = arm.get_tape(tape_len)
                tape_tensors.append(torch.tensor(t, dtype=torch.int32))
            tapes = torch.stack(tape_tensors).unsqueeze(0)

            gpu_valid, gpu_cost, gpu_cycles, gpu_area, gpu_instr = \
                gpu_sim.evaluate_tapes_detailed(tapes, max_cycles=max_cycles)

            vr = ValidationResult(
                puzzle_name=puzzle.name,
                solution_name=f"fuzz_{i}",
                passed=False,
                gpu_valid=gpu_valid[0].item(),
                cpu_valid=cpu_result.valid,
                gpu_cycles=gpu_cycles[0].item(),
                cpu_cycles=cpu_result.cycles,
                gpu_area=gpu_area[0].item(),
                cpu_area=cpu_result.area,
                gpu_cost=gpu_cost[0].item(),
                cpu_cost=cpu_result.cost,
                gpu_instructions=gpu_instr[0].item(),
                cpu_instructions=cpu_result.instructions,
            )

            if vr.gpu_valid != vr.cpu_valid:
                vr.error = f"validity mismatch"
            elif vr.gpu_valid and vr.cpu_valid:
                if vr.gpu_cycles != vr.cpu_cycles:
                    vr.error = f"cycles mismatch"
            if not vr.error:
                vr.passed = True

            report.results.append(vr)

            if not vr.passed:
                print(f"  [FAIL] fuzz_{i}: {vr.error}")
                print(f"    GPU: valid={vr.gpu_valid} cycles={vr.gpu_cycles}")
                print(f"    CPU: valid={vr.cpu_valid} cycles={vr.cpu_cycles}")

        return report

    def benchmark(self, puzzle_path: str, solution_path: str,
                  batch_size: int = 10000, max_cycles: int = 200) -> dict:
        """Benchmark GPU simulator throughput."""
        puzzle = parse_puzzle(puzzle_path)
        solution = parse_solution(solution_path)

        gpu_sim = BatchSimulator(puzzle, solution, device=self.device, max_cycles=max_cycles)

        arms = [p for p in solution.parts if p.is_arm]
        max_tape_len = max(
            (max((inst.index for inst in arm.instructions), default=0) + 1)
            for arm in arms
        ) if arms else 1
        tape_len = max(max_tape_len, 5)

        VALID_INSTS = [Inst.GRAB, Inst.DROP, Inst.ROTATE_CW, Inst.ROTATE_CCW,
                       Inst.PIVOT_CW, Inst.PIVOT_CCW, 0]

        # Generate random tapes
        n_arms = len(arms)
        tapes = torch.zeros(batch_size, n_arms, tape_len, dtype=torch.int32)
        for b in range(batch_size):
            for a in range(n_arms):
                for t in range(tape_len):
                    tapes[b, a, t] = random.choice(VALID_INSTS)

        # Warmup
        _ = gpu_sim.evaluate_tapes(tapes[:10], max_cycles=max_cycles)

        # Benchmark
        start = time.perf_counter()
        scores = gpu_sim.evaluate_tapes(tapes, max_cycles=max_cycles)
        elapsed = time.perf_counter() - start

        n_valid = (scores < float('inf')).sum().item()
        evals_per_sec = batch_size / elapsed

        return {
            'batch_size': batch_size,
            'elapsed_s': elapsed,
            'evals_per_sec': evals_per_sec,
            'n_valid': n_valid,
            'max_cycles': max_cycles,
        }


def _clone_solution(sol: Solution) -> Solution:
    """Deep-copy a solution for mutation."""
    import copy
    return copy.deepcopy(sol)


def _find_puzzle_file(puzzle_id: str) -> Optional[str]:
    """Find puzzle file by ID (e.g. P007)."""
    base = Path(__file__).parent.parent / "tools" / "omsim" / "test" / "puzzle"
    matches = list(base.rglob(f"{puzzle_id}.puzzle"))
    if matches:
        return str(matches[0])
    # Try with wildcard
    matches = list(base.rglob(f"*{puzzle_id}*.puzzle"))
    return str(matches[0]) if matches else None


def _find_solution_for_puzzle(puzzle_id: str) -> Optional[str]:
    """Find an archive solution for a puzzle."""
    archive = Path(__file__).parent.parent / "tools" / "om-archive"
    if not archive.exists():
        return None
    for sol_path in archive.rglob("*.solution"):
        try:
            sol = parse_solution(str(sol_path))
            if puzzle_id in sol.puzzle_name:
                return str(sol_path)
        except Exception:
            continue
    return None


def main():
    parser = argparse.ArgumentParser(description="GPU sim cross-validation")
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests")
    parser.add_argument("--archive-dir", help="Archive solutions directory")
    parser.add_argument("--puzzle-dir", default="tools/omsim/test/puzzle",
                        help="Puzzle files directory")
    parser.add_argument("--max", type=int, default=100, help="Max solutions to test")
    parser.add_argument("--fuzz", nargs="+", help="Puzzle IDs for fuzz testing")
    parser.add_argument("--n-random", type=int, default=1000, help="Random tapes per puzzle")
    parser.add_argument("--benchmark", help="Puzzle ID for benchmarking")
    parser.add_argument("--batch-size", type=int, default=10000)
    parser.add_argument("--device", default="mps", help="Torch device")
    args = parser.parse_args()

    validator = GPUSimValidator(device=args.device)

    if args.smoke:
        print("=== Smoke Tests ===")
        for pid in ["P007", "P009", "P011"]:
            pf = _find_puzzle_file(pid)
            sf = _find_solution_for_puzzle(pid)
            if pf and sf:
                result = validator.validate_solution(pf, sf)
                status = "PASS" if result.passed else "FAIL"
                print(f"[{status}] {pid}: {result.error or 'OK'}")
            else:
                print(f"[SKIP] {pid}: puzzle={pf is not None} solution={sf is not None}")

    if args.archive_dir:
        print(f"\n=== Archive Validation (max {args.max}) ===")
        report = validator.validate_archive(args.archive_dir, args.puzzle_dir, args.max)
        print(report.summary())

    if args.fuzz:
        for pid in args.fuzz:
            pf = _find_puzzle_file(pid)
            sf = _find_solution_for_puzzle(pid)
            if pf and sf:
                print(f"\n=== Fuzz Test: {pid} ({args.n_random} random tapes) ===")
                report = validator.validate_tape_variants(pf, sf, args.n_random)
                print(report.summary())
            else:
                print(f"[SKIP] {pid}: puzzle={pf is not None} solution={sf is not None}")

    if args.benchmark:
        pf = _find_puzzle_file(args.benchmark)
        sf = _find_solution_for_puzzle(args.benchmark)
        if pf and sf:
            print(f"\n=== Benchmark: {args.benchmark} (batch={args.batch_size}) ===")
            stats = validator.benchmark(pf, sf, args.batch_size)
            print(f"  {stats['evals_per_sec']:.0f} evals/s")
            print(f"  {stats['elapsed_s']:.3f}s for {stats['batch_size']} evals")
            print(f"  {stats['n_valid']} valid / {stats['batch_size']} total")
        else:
            print(f"[SKIP] {args.benchmark}: puzzle={pf is not None} solution={sf is not None}")


if __name__ == "__main__":
    main()
