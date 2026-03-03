#!/usr/bin/env python3
"""Opus Magnum God Solution Solver - Main CLI.

Usage:
    python solve.py analyze <puzzle_file>          Analyze a puzzle
    python solve.py solve <puzzle_file> [target]   Generate a solution
    python solve.py verify <puzzle> <solution>     Verify a solution
    python solve.py records [metric]               Show best records from archive
    python solve.py best <puzzle_id> [metric]      Get best known solution
    python solve.py index                          Build archive index
    python solve.py benchmark                      Compare solver vs records
"""
import sys
import os
import argparse
import subprocess
import tempfile

sys.path.insert(0, os.path.dirname(__file__))

from solver.puzzle import parse_puzzle
from solver.recipe import analyze_puzzle
from solver.solution import parse_solution, write_solution, Inst
from solver.heuristics import generate_solution, OptTarget, GodHeuristics


OMSIM = os.path.join(os.path.dirname(__file__), 'tools', 'omsim', 'omsim')
PUZZLE_DIR = os.path.join(os.path.dirname(__file__), 'tools', 'omsim', 'test', 'puzzle')
ARCHIVE_DIR = os.path.join(os.path.dirname(__file__), 'tools', 'om-archive')


def find_puzzle(puzzle_id: str) -> str:
    """Find a puzzle file by ID (e.g., 'P007')."""
    for root, dirs, files in os.walk(PUZZLE_DIR):
        for f in files:
            if f == f'{puzzle_id}.puzzle':
                return os.path.join(root, f)
    raise FileNotFoundError(f"Puzzle {puzzle_id} not found in {PUZZLE_DIR}")


def verify_solution(puzzle_path: str, solution_path: str) -> dict:
    """Verify a solution with omsim and return metrics."""
    result = subprocess.run(
        [OMSIM, '-p', puzzle_path,
         '-m', 'cycles', '-m', 'cost', '-m', 'area', '-m', 'instructions',
         solution_path],
        capture_output=True, text=True, timeout=30
    )
    output = result.stdout + result.stderr
    metrics = {}
    errors = []
    for line in output.strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            v = v.strip()
            if v.isdigit():
                metrics[k.strip()] = int(v)
            else:
                errors.append(v)
    metrics['_errors'] = errors
    metrics['_valid'] = all(m in metrics for m in ('cost', 'cycles', 'area', 'instructions'))
    if metrics['_valid']:
        metrics['sum4'] = metrics['cost'] + metrics['cycles'] + metrics['area'] + metrics['instructions']
    return metrics


def cmd_analyze(args):
    """Analyze a puzzle."""
    puzzle = parse_puzzle(args.puzzle)
    analysis = analyze_puzzle(puzzle)

    print(f"Puzzle: {puzzle.name}")
    print(f"Complexity: {analysis.complexity}")
    print(f"Output scale: {puzzle.output_scale}")
    print()

    print("Inputs:")
    for i, pio in enumerate(puzzle.inputs):
        m = pio.molecule
        print(f"  [{i}] {m.atom_count} atoms: {m.element_counts()}")
        if m.bonds:
            print(f"      {len(m.bonds)} bonds")

    print("Outputs:")
    for i, pio in enumerate(puzzle.outputs):
        m = pio.molecule
        print(f"  [{i}] {m.atom_count} atoms: {m.element_counts()}")
        if m.bonds:
            print(f"      {len(m.bonds)} bonds")

    print()
    print(f"Needs bonding: {analysis.needs_bonding}")
    print(f"Needs unbonding: {analysis.needs_unbonding}")
    print(f"Element deficit: {analysis.element_deficit}")
    print(f"Element surplus: {analysis.element_surplus}")

    if analysis.recipe and analysis.recipe.reactions:
        print()
        print("Recipe:")
        for reaction, count in analysis.recipe.reactions.items():
            if count > 0:
                print(f"  {reaction.name} x{count}")
        if analysis.recipe.waste:
            print(f"  Waste: {analysis.recipe.waste}")

    print()
    print("Theoretical bounds:")
    heur = GodHeuristics()
    print(f"  Min cost: {heur.theoretical_min_cost(analysis)}g")
    print(f"  Min cycles (est): {analysis.min_cycles_theoretical}c")
    print(f"  Min glyphs: {heur.min_glyphs_needed(analysis)}")


def cmd_solve(args):
    """Generate and verify a solution."""
    puzzle = parse_puzzle(args.puzzle)
    target_map = {
        'cost': OptTarget.COST,
        'cycles': OptTarget.CYCLES,
        'area': OptTarget.AREA,
        'instructions': OptTarget.INSTRUCTIONS,
        'balanced': OptTarget.BALANCED,
    }
    target = target_map.get(args.target, OptTarget.COST)

    sol = generate_solution(puzzle, target)

    if args.output:
        write_solution(sol, args.output)
        print(f"Solution written to {args.output}")
    else:
        with tempfile.NamedTemporaryFile(suffix='.solution', delete=False) as f:
            sol_path = f.name
        write_solution(sol, sol_path)

    metrics = verify_solution(args.puzzle, sol_path if not args.output else args.output)

    if metrics['_valid']:
        print(f"Valid solution: {metrics['cost']}g / {metrics['cycles']}c / {metrics['area']}a / {metrics['instructions']}i")
        print(f"Sum4: {metrics['sum4']}")
    else:
        print(f"Invalid solution:")
        for err in metrics['_errors']:
            print(f"  {err}")

    if not args.output:
        os.unlink(sol_path)


def cmd_verify(args):
    """Verify a solution."""
    metrics = verify_solution(args.puzzle, args.solution)

    if metrics['_valid']:
        print(f"Valid: {metrics['cost']}g / {metrics['cycles']}c / {metrics['area']}a / {metrics['instructions']}i")
        print(f"Sum4: {metrics['sum4']}")
    else:
        print("Invalid:")
        for err in metrics['_errors']:
            print(f"  {err}")

    # Also show solution structure
    sol = parse_solution(args.solution)
    print(f"\nParts ({len(sol.parts)}):")
    for part in sol.parts:
        extras = []
        if part.instructions:
            extras.append(f"{len(part.instructions)} instr")
        if part.track_hexes:
            extras.append(f"{len(part.track_hexes)} track")
        extra = f" [{', '.join(extras)}]" if extras else ""
        print(f"  {part.name:25s} ({part.position.q:3d},{part.position.r:3d}) rot={part.rotation}{extra}")


def cmd_records(args):
    """Show best records from archive."""
    from solver.archive import Archive
    archive = Archive(ARCHIVE_DIR, OMSIM, PUZZLE_DIR)
    print("Indexing archive (this may take a moment)...")
    archive.index()
    print()
    print(archive.summary())


def cmd_best(args):
    """Get best known solution for a puzzle."""
    from solver.archive import Archive
    archive = Archive(ARCHIVE_DIR, OMSIM, PUZZLE_DIR)
    archive.index()

    records = archive.lookup(args.puzzle_id)
    if not records:
        print(f"No records found for {args.puzzle_id}")
        return

    metrics = ['cost', 'cycles', 'area', 'instructions', 'sum4']
    print(f"\n{args.puzzle_id}: {records.puzzle_name}")
    print(f"{'Metric':<15} {'Score':>8} {'Solution'}")
    print('-' * 70)
    for metric in metrics:
        best = records.best_by(metric)
        if best:
            val = getattr(best, metric) if metric != 'sum4' else best.sum4
            basename = os.path.basename(best.path)
            print(f"{metric:<15} {val:>8} {basename[:50]}")

    if args.output and args.metric:
        best = records.best_by(args.metric)
        if best:
            import shutil
            shutil.copy2(best.path, args.output)
            print(f"\nCopied best {args.metric} solution to {args.output}")


def cmd_benchmark(args):
    """Compare solver output vs archive records."""
    from solver.archive import Archive
    archive = Archive(ARCHIVE_DIR, OMSIM, PUZZLE_DIR)
    print("Indexing archive...")
    archive.index()
    print()

    results = []
    for pid in sorted(archive._records.keys()):
        rec = archive._records[pid]
        puzzle_path = archive._puzzle_paths.get(pid)
        if not puzzle_path:
            continue

        try:
            puzzle = parse_puzzle(puzzle_path)
            sol = generate_solution(puzzle, OptTarget.COST)

            with tempfile.NamedTemporaryFile(suffix='.solution', delete=False) as f:
                sol_path = f.name
            write_solution(sol, sol_path)

            metrics = verify_solution(puzzle_path, sol_path)
            os.unlink(sol_path)

            gc = rec.best_by('cost')
            gs = rec.best_by('sum4')

            if metrics['_valid']:
                our_sum = metrics['sum4']
                best_sum = gs.sum4 if gs else 0
                ratio = our_sum / best_sum if best_sum > 0 else 0
                results.append((pid, rec.puzzle_name, 'OK', metrics['cost'],
                                gc.cost if gc else 0, our_sum, best_sum, ratio))
            else:
                results.append((pid, rec.puzzle_name, 'FAIL',
                                0, gc.cost if gc else 0, 0, 0, 0))
        except Exception as e:
            results.append((pid, rec.puzzle_name, 'ERR', 0, 0, 0, 0, 0))

    print(f"{'Puzzle':<8} {'Name':<28} {'Status':>6} {'Our$':>6} {'GC$':>6} {'OurΣ':>8} {'GCΣ':>8} {'Ratio':>6}")
    print('=' * 86)
    ok = 0
    for pid, name, status, our_cost, gc_cost, our_sum, gc_sum, ratio in results:
        if status == 'OK':
            ok += 1
        flag = 'OK' if status == 'OK' else 'FAIL'
        print(f"{pid:<8} {name:<28} {flag:>6} {our_cost:>5}g {gc_cost:>5}g {our_sum:>7}s {gc_sum:>7}s {ratio:>5.1f}x")

    print(f"\n{ok}/{len(results)} valid solutions")


def main():
    parser = argparse.ArgumentParser(description='Opus Magnum God Solution Solver')
    subs = parser.add_subparsers(dest='command')

    p_analyze = subs.add_parser('analyze', help='Analyze a puzzle')
    p_analyze.add_argument('puzzle', help='Path to .puzzle file')

    p_solve = subs.add_parser('solve', help='Generate a solution')
    p_solve.add_argument('puzzle', help='Path to .puzzle file')
    p_solve.add_argument('target', nargs='?', default='cost',
                         choices=['cost', 'cycles', 'area', 'instructions', 'balanced'])
    p_solve.add_argument('-o', '--output', help='Output .solution file path')

    p_verify = subs.add_parser('verify', help='Verify a solution')
    p_verify.add_argument('puzzle', help='Path to .puzzle file')
    p_verify.add_argument('solution', help='Path to .solution file')

    p_records = subs.add_parser('records', help='Show archive records')
    p_records.add_argument('metric', nargs='?', default='cost')

    p_best = subs.add_parser('best', help='Get best solution for a puzzle')
    p_best.add_argument('puzzle_id', help='Puzzle ID (e.g., P007)')
    p_best.add_argument('metric', nargs='?', default='cost')
    p_best.add_argument('-o', '--output', help='Copy solution to this path')

    p_bench = subs.add_parser('benchmark', help='Benchmark solver vs records')

    args = parser.parse_args()

    if args.command == 'analyze':
        cmd_analyze(args)
    elif args.command == 'solve':
        cmd_solve(args)
    elif args.command == 'verify':
        cmd_verify(args)
    elif args.command == 'records':
        cmd_records(args)
    elif args.command == 'best':
        cmd_best(args)
    elif args.command == 'benchmark':
        cmd_benchmark(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
