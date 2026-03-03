"""Interface to the om-archive repository of record solutions.

Provides lookup of best-known solutions for each puzzle, indexed by
optimization metric (cost, cycles, area, instructions, sum4, etc.).
"""
from __future__ import annotations
import os
import subprocess
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .solution import parse_solution, Solution, Inst


@dataclass
class SolutionRecord:
    """A verified solution with its metrics."""
    path: str
    puzzle_id: str
    cost: int
    cycles: int
    area: int
    instructions: int
    solution: Optional[Solution] = None

    @property
    def sum4(self) -> int:
        return self.cost + self.cycles + self.area + self.instructions

    @property
    def score_str(self) -> str:
        return f"{self.cost}g/{self.cycles}c/{self.area}a/{self.instructions}i (sum={self.sum4})"


@dataclass
class PuzzleRecords:
    """All known records for a single puzzle."""
    puzzle_id: str
    puzzle_name: str
    solutions: List[SolutionRecord] = field(default_factory=list)

    def best_by(self, metric: str) -> Optional[SolutionRecord]:
        """Get the best solution by a given metric."""
        if not self.solutions:
            return None
        if metric == 'sum4':
            return min(self.solutions, key=lambda s: s.sum4)
        elif metric == 'sum3_cga':
            return min(self.solutions, key=lambda s: s.cycles + s.cost + s.area)
        return min(self.solutions, key=lambda s: getattr(s, metric, float('inf')))

    def pareto_front(self) -> List[SolutionRecord]:
        """Get the Pareto-optimal solutions (non-dominated across all metrics)."""
        front = []
        for s in self.solutions:
            dominated = False
            for other in self.solutions:
                if other is s:
                    continue
                if (other.cost <= s.cost and other.cycles <= s.cycles and
                    other.area <= s.area and other.instructions <= s.instructions and
                    (other.cost < s.cost or other.cycles < s.cycles or
                     other.area < s.area or other.instructions < s.instructions)):
                    dominated = True
                    break
            if not dominated:
                front.append(s)
        return front


class Archive:
    """Index of the om-archive record solutions."""

    def __init__(self, archive_dir: str, omsim_path: str, puzzle_dir: str):
        self.archive_dir = archive_dir
        self.omsim_path = omsim_path
        self.puzzle_dir = puzzle_dir
        self._records: Dict[str, PuzzleRecords] = {}
        self._puzzle_paths: Dict[str, str] = {}

    def _discover_puzzles(self):
        """Find all puzzle files and map puzzle IDs to paths."""
        if self._puzzle_paths:
            return
        for root, dirs, files in os.walk(self.puzzle_dir):
            for f in files:
                if f.endswith('.puzzle'):
                    path = os.path.join(root, f)
                    pid = f.replace('.puzzle', '')
                    self._puzzle_paths[pid] = path

    def _verify_solution(self, puzzle_path: str, sol_path: str) -> Optional[Dict[str, int]]:
        """Verify a solution with omsim and return metrics."""
        try:
            result = subprocess.run(
                [self.omsim_path, '-p', puzzle_path,
                 '-m', 'cost', '-m', 'cycles', '-m', 'area', '-m', 'instructions',
                 sol_path],
                capture_output=True, text=True, timeout=30
            )
            metrics = {}
            for line in (result.stdout + result.stderr).strip().split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    v = v.strip()
                    if v.isdigit():
                        metrics[k.strip()] = int(v)
            if all(m in metrics for m in ('cost', 'cycles', 'area', 'instructions')):
                return metrics
        except Exception:
            pass
        return None

    def index(self, verbose: bool = False) -> Dict[str, PuzzleRecords]:
        """Build the complete archive index. Returns puzzle_id -> PuzzleRecords."""
        self._discover_puzzles()
        self._records = {}

        for root, dirs, files in os.walk(self.archive_dir):
            for f in files:
                if not f.endswith('.solution'):
                    continue
                sol_path = os.path.join(root, f)
                try:
                    sol = parse_solution(sol_path)
                    pid = sol.puzzle_name
                    if pid not in self._puzzle_paths:
                        continue

                    metrics = self._verify_solution(self._puzzle_paths[pid], sol_path)
                    if not metrics:
                        continue

                    if pid not in self._records:
                        # Try to get puzzle name
                        from .puzzle import parse_puzzle
                        puzzle = parse_puzzle(self._puzzle_paths[pid])
                        self._records[pid] = PuzzleRecords(pid, puzzle.name)

                    record = SolutionRecord(
                        path=sol_path,
                        puzzle_id=pid,
                        cost=metrics['cost'],
                        cycles=metrics['cycles'],
                        area=metrics['area'],
                        instructions=metrics['instructions'],
                    )
                    self._records[pid].solutions.append(record)

                    if verbose:
                        print(f"  {pid}: {record.score_str} ({f})")
                except Exception:
                    pass

        return self._records

    def lookup(self, puzzle_id: str) -> Optional[PuzzleRecords]:
        """Look up records for a puzzle."""
        return self._records.get(puzzle_id)

    def best_solution(self, puzzle_id: str, metric: str = 'cost') -> Optional[SolutionRecord]:
        """Get the best solution for a puzzle by metric."""
        records = self._records.get(puzzle_id)
        if records:
            return records.best_by(metric)
        return None

    def summary(self) -> str:
        """Generate a summary table of best scores per puzzle."""
        lines = []
        header = f"{'ID':<8} {'Name':<32} {'GC':>6} {'GCy':>6} {'GA':>6} {'GI':>6} {'GS4':>8}"
        lines.append(header)
        lines.append('=' * len(header))

        for pid in sorted(self._records.keys()):
            rec = self._records[pid]
            gc = rec.best_by('cost')
            gcy = rec.best_by('cycles')
            ga = rec.best_by('area')
            gi = rec.best_by('instructions')
            gs = rec.best_by('sum4')

            lines.append(
                f"{pid:<8} {rec.puzzle_name:<32} "
                f"{gc.cost if gc else '?':>5}g "
                f"{gcy.cycles if gcy else '?':>5}c "
                f"{ga.area if ga else '?':>5}a "
                f"{gi.instructions if gi else '?':>5}i "
                f"{gs.sum4 if gs else '?':>7}s"
            )

        return '\n'.join(lines)
