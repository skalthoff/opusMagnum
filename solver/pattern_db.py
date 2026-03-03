"""Pattern database: extract and analyze instruction tapes from archived solutions."""
from __future__ import annotations

import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .solution import parse_solution, Inst, Part


@dataclass
class TapePattern:
    """A single arm's instruction tape extracted from an archived solution."""
    tape: Tuple[int, ...]
    puzzle_name: str
    cost: int
    cycles: int
    area: int
    instructions: int
    sum4: int  # cost + cycles + area + instructions
    n_arms: int
    n_glyphs: int
    arm_type: str

    @property
    def tape_str(self) -> str:
        """Human-readable tape using instruction names."""
        parts = []
        for code in self.tape:
            if code == 0:
                parts.append('.')
            else:
                parts.append(Inst.NAMES.get(code, f'?{code:02x}'))
        return ' '.join(parts)

    @property
    def tape_length(self) -> int:
        return len(self.tape)


class PatternDB:
    """Database of instruction tape patterns mined from the solution archive."""

    def __init__(self):
        self.patterns: List[TapePattern] = []
        self._by_puzzle: Dict[str, List[TapePattern]] = defaultdict(list)
        self._by_n_arms: Dict[int, List[TapePattern]] = defaultdict(list)
        self._tape_freq: Dict[Tuple[int, ...], int] = Counter()

    def scan_archive(self, archive_dir: str, verbose: bool = False) -> int:
        """Walk the archive directory and extract tape patterns from all .solution files.

        Returns the total number of patterns extracted.
        """
        count = 0
        errors = 0
        for root, _dirs, files in os.walk(archive_dir):
            for fname in files:
                if not fname.endswith('.solution'):
                    continue
                path = os.path.join(root, fname)
                try:
                    patterns = self._extract_from_solution(path, fname)
                    for pat in patterns:
                        self.patterns.append(pat)
                        self._by_puzzle[pat.puzzle_name].append(pat)
                        self._by_n_arms[pat.n_arms].append(pat)
                        self._tape_freq[pat.tape] += 1
                    count += len(patterns)
                except Exception as e:
                    errors += 1
                    if verbose:
                        print(f"  SKIP {fname}: {e}")
        self._build_frequency_table()
        if verbose:
            print(f"Scanned archive: {count} patterns, {errors} errors")
        return count

    def _extract_from_solution(self, path: str, filename: str) -> List[TapePattern]:
        """Parse a solution file and return a TapePattern for each arm with instructions."""
        sol = parse_solution(path)
        metrics = self._parse_filename_metrics(filename)

        cost = metrics.get('cost', sol.cost)
        cycles = metrics.get('cycles', sol.cycles)
        area = metrics.get('area', sol.area)
        instructions = metrics.get('instructions', sol.instruction_count)
        sum4 = cost + cycles + area + instructions

        arms = [p for p in sol.parts if p.is_arm]
        n_arms = len(arms)
        n_glyphs = sum(1 for p in sol.parts if p.is_glyph)

        results: List[TapePattern] = []
        for arm in arms:
            if not arm.instructions:
                continue

            # Build tape: find max index, create array, fill in
            max_idx = max(inst.index for inst in arm.instructions)
            tape_list = [0] * (max_idx + 1)
            for inst in arm.instructions:
                if 0 <= inst.index <= max_idx:
                    tape_list[inst.index] = inst.instruction

            # Strip leading zeros
            start = 0
            while start < len(tape_list) and tape_list[start] == 0:
                start += 1
            # Strip trailing zeros
            end = len(tape_list)
            while end > start and tape_list[end - 1] == 0:
                end -= 1

            if start >= end:
                continue  # empty tape after stripping

            tape = tuple(tape_list[start:end])

            results.append(TapePattern(
                tape=tape,
                puzzle_name=sol.puzzle_name,
                cost=cost,
                cycles=cycles,
                area=area,
                instructions=instructions,
                sum4=sum4,
                n_arms=n_arms,
                n_glyphs=n_glyphs,
                arm_type=arm.name,
            ))

        return results

    @staticmethod
    def _parse_filename_metrics(filename: str) -> Dict[str, int]:
        """Parse metrics from filename format like '40g-124c-21a-21i-..._PUZZLE.solution'.

        Returns dict with keys: cost, cycles, area, instructions (int values).
        Non-integer values (like infinity) are skipped.
        """
        # Strip .solution extension and split on underscore to get metrics part
        base = filename.replace('.solution', '')
        # The puzzle name comes after the first underscore that follows the metrics
        # Metrics section: separated by dashes, each ending with a letter suffix
        # We need the first 4: Xg Xc Xa Xi
        metrics: Dict[str, int] = {}

        # Match the leading metrics: digits (possibly with decimals) followed by suffix letter
        # Format: 40g-124c-21a-21i-...
        m_cost = re.match(r'(\d+)g-', base)
        if m_cost:
            metrics['cost'] = int(m_cost.group(1))

        m_cycles = re.search(r'-(\d+)c-', base)
        if m_cycles:
            metrics['cycles'] = int(m_cycles.group(1))

        m_area = re.search(r'-(\d+)a-', base)
        if m_area:
            metrics['area'] = int(m_area.group(1))

        m_instr = re.search(r'-(\d+)i-', base)
        if not m_instr:
            # instructions might be the last metric before underscore
            m_instr = re.search(r'-(\d+)i[_-]', base)
        if m_instr:
            metrics['instructions'] = int(m_instr.group(1))

        return metrics

    def _build_frequency_table(self):
        """Rebuild the tape frequency counter from all patterns."""
        self._tape_freq = Counter()
        for pat in self.patterns:
            self._tape_freq[pat.tape] += 1

    def get_best_tapes(
        self,
        puzzle_name: Optional[str] = None,
        n_arms: Optional[int] = None,
        metric: str = 'sum4',
        limit: int = 20,
    ) -> List[TapePattern]:
        """Return tapes sorted by the given metric (ascending). Lower is better.

        Args:
            puzzle_name: filter to a specific puzzle
            n_arms: filter to solutions with this many arms
            metric: one of 'sum4', 'cost', 'cycles', 'area', 'instructions'
            limit: max results
        """
        pool = self.patterns
        if puzzle_name is not None:
            pool = self._by_puzzle.get(puzzle_name, [])
        if n_arms is not None:
            pool = [p for p in pool if p.n_arms == n_arms]

        pool = sorted(pool, key=lambda p: getattr(p, metric))
        return pool[:limit]

    def get_similar_tapes(
        self,
        n_arms: int = 1,
        n_glyphs_range: Optional[Tuple[int, int]] = None,
        limit: int = 20,
    ) -> List[TapePattern]:
        """Return deduplicated tapes for solutions with the given arm count.

        Deduplicates by tape content, keeping the pattern with the best sum4.
        Optionally filters by glyph count range.
        """
        pool = self._by_n_arms.get(n_arms, [])
        if n_glyphs_range is not None:
            lo, hi = n_glyphs_range
            pool = [p for p in pool if lo <= p.n_glyphs <= hi]

        # Deduplicate: keep best sum4 per unique tape
        best: Dict[Tuple[int, ...], TapePattern] = {}
        for pat in pool:
            existing = best.get(pat.tape)
            if existing is None or pat.sum4 < existing.sum4:
                best[pat.tape] = pat

        results = sorted(best.values(), key=lambda p: p.sum4)
        return results[:limit]

    def instruction_weights(self) -> Dict[int, float]:
        """Return normalized frequency of each instruction code across all tapes.

        Useful as mutation weights: more common instructions are more likely
        to appear in good solutions.
        """
        counts: Counter = Counter()
        total = 0
        for pat in self.patterns:
            for code in pat.tape:
                if code != 0:
                    counts[code] += 1
                    total += 1
        if total == 0:
            return {}
        return {code: count / total for code, count in counts.items()}

    def common_tape_templates(self, n_arms: int = 1, limit: int = 10) -> List[Tuple[int, ...]]:
        """Return the most frequently occurring unique tapes for the given arm count.

        These can serve as starting templates for the solver.
        """
        pool = self._by_n_arms.get(n_arms, [])
        freq: Counter = Counter()
        for pat in pool:
            freq[pat.tape] += 1
        return [tape for tape, _count in freq.most_common(limit)]

    def summary(self) -> str:
        """Return a human-readable summary of the database."""
        n_patterns = len(self.patterns)
        n_puzzles = len(self._by_puzzle)
        n_unique_tapes = len(self._tape_freq)
        arm_counts = sorted(self._by_n_arms.keys())

        lines = [
            f"PatternDB: {n_patterns} patterns from {n_puzzles} puzzles",
            f"  Unique tapes: {n_unique_tapes}",
            f"  Arm counts: {arm_counts}",
        ]

        # Top instruction frequencies
        weights = self.instruction_weights()
        if weights:
            top = sorted(weights.items(), key=lambda x: -x[1])[:6]
            freq_parts = [f"{Inst.NAMES.get(code, f'?{code:02x}')}={w:.1%}" for code, w in top]
            lines.append(f"  Top instructions: {', '.join(freq_parts)}")

        return '\n'.join(lines)
