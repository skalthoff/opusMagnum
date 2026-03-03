# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Opus Magnum god-sum solver. Generates optimal solutions for the puzzle game Opus Magnum, targeting the "sum4" metric (cost + cycles + area + instructions). The solver uses Z3 constraint-based layout generation, genetic algorithm tape optimization, and omsim (C library via ctypes) for fast verification (~28K eval/s single-threaded, parallelizable across cores).

## Commands

```bash
# Solve a puzzle by ID (searches tools/omsim/test/puzzle/ recursively)
python3 solve.py search P007 --target sum4 -v --time-limit 30

# Analyze puzzle structure
python3 solve.py analyze tools/omsim/test/puzzle/campaign/ch1-and-prologue/P007.puzzle

# Verify an existing solution
python3 solve.py verify <puzzle_file> <solution_file>

# Solve all campaign puzzles
python3 solve.py search P007 --all --time-limit 60 -v

# Build omsim shared library (required for Simulator ctypes FFI)
cd tools/omsim && make libverify.so  # Linux
cd tools/omsim && make libverify.dylib  # macOS

# Run omsim C tests
cd tools/omsim && make run-tests && ./run-tests
```

There is no Python test suite. Regression testing is done by running the solver on known puzzles and comparing sum4 scores:
```bash
# Regression baselines: P007=25, P008=144, P009=70, P010=37, P011=133
python3 solve.py search P007 --target sum4 -v --time-limit 30
```

## Architecture

The solver pipeline has 5 phases:

```
Puzzle → Recipe Analysis → Station Graph → Layout Generation → Tape Compilation → GA + omsim
```

**Phase 0 — Zero-arm overlap** (`search.py:_try_zero_arm`): Tries solutions with no arm by overlapping inputs/outputs on glyphs. Solves trivial puzzles instantly (P007, P010).

**Phase 1 — Layout generation** (`layout_z3.py`): Generates valid spatial placements of parts. Three strategies: CW-sweep (arm sweeps clockwise through stations), stacked (all process parts share one hex), and spread (each output atom gets its own arm direction). Layouts specify arm position/length, station directions, glyph/output rotations.

**Phase 2 — Lower bound pruning**: Branch-and-bound using `compute_lower_bound()` to skip layouts that can't beat the current best.

**Phase 3 — Tape optimization** (`tape_ga.py`, `tape_compiler.py`): Seed tapes come from 5 sources: graph-compiled, plan-compiled, dataflow-derived, geometric templates, and archive patterns. GA evolves tapes via mutation/crossover, with omsim verifying each candidate.

### Key modules

- **`station_graph.py`** — Central IR. `build_station_graph()` creates StationGraph with flows (atom routes) and SlotConstraints (bonder-output alignment). Converts back to ProductionPlan via `graph_to_plan()`.
- **`recipe.py`** — `analyze_puzzle()` determines reactions needed, element deficits, complexity class, and theoretical bounds.
- **`production_planner.py`** — `generate_plans()` traces atom routes backward through recipes. Returns cost-min and cycle-min plan variants.
- **`layout_z3.py`** — `generate_layouts()` / `generate_stacked_layouts()` / `generate_layouts_from_graph()`. The `Layout` dataclass carries stations, directions, positions, and rotations. `_check_bonder_output_alignment()` filters infeasible bonder-output combos.
- **`tape_compiler.py`** — Compilation strategies: single-delivery, multi-delivery, jiggle (pass-through glyphs), conversion (ungrab at glyph), spread (per-atom slot targeting). `compile_tapes_from_graph()` reads flows directly from StationGraph.
- **`glyph_model.py`** — All 13 glyph specs with slot layouts and `local_to_world()` coordinate transform.
- **`simulator.py`** — ctypes wrapper for `tools/omsim/libverify.{so,dylib}`. `Simulator.verify_bytes()` returns `VerifyResult` with cost/cycles/area/instructions.
- **`hex.py`** — Axial hex coordinates. `DIRECTIONS[0..5]` = E,SE,SW,W,NW,NE (CW order). CW rotation decrements direction index.

### Data flow

`Layout` is the key interchange type between modules. It carries:
- `stations: List[Tuple[str, object]]` — `[('input', io_idx), ('glyph', name), ('bonder', name), ('output', 0)]`
- `directions: List[int]` — arm direction (0-5) for each station
- `positions: List[HexCoord]` — world position for each station
- `glyph_rotations / output_rotations: Dict[int, int]` — station index → rotation

Tapes are `List[int]` where each int is an `Inst` constant (GRAB=0x47, DROP=0x67, ROTATE_CW=0x52, ROTATE_CCW=0x72, RESET=0x58, REPEAT=0x43).

### Coordinate convention

omsim uses flat-top hexagonal grid with axial coordinates (q, r). `local_to_world(origin, rotation, du, dv)` transforms glyph-local offsets: `world = origin + DIRECTIONS[rot]*du + DIRECTIONS[(rot+1)%6]*dv`.

## Puzzle files

Puzzle files are at `tools/omsim/test/puzzle/campaign/ch1-and-prologue/P0XX.puzzle`. Archive solutions are at `tools/om-archive/CHAPTER_N/PUZZLE_NAME/`.

## Git

GPG signing is configured via 1Password (`commit.gpgsign=true`). Use `--no-gpg-sign` if the 1Password agent isn't running.

## Context Efficiency

### Subagent Discipline

**Context-aware delegation:**
 - Under ~50k context: prefer inline work for tasks under ~5 tool calls.
 - Over ~50k context: prefer subagents for self-contained tasks, even simple ones — the per-call token tax on large contexts adds up fast.

When using subagents, include output rules: "Final response under 2000 characters. List outcomes, not process."
Never call TaskOutput twice for the same subagent. If it times out, increase the timeout — don't re-read.

### File Reading
Read files with purpose. Before reading a file, know what you're looking for.
Use Grep to locate relevant sections before reading entire large files.
Never re-read a file you've already read in this session.
For files over 500 lines, use offset/limit to read only the relevant section.

### Responses
Don't echo back file contents you just read — the user can see them.
Don't narrate tool calls ("Let me read the file..." / "Now I'll edit..."). Just do it.
Keep explanations proportional to complexity. Simple changes need one sentence, not three paragraphs.

**Tables — STRICT RULES (apply everywhere, always):**
- Markdown tables: use minimum separator (`|-|-|`). Never pad with repeated hyphens (`|---|---|`).
- NEVER use box-drawing / ASCII-art tables with characters like `┌`, `┬`, `─`, `│`, `└`, `┘`, `├`, `┤`, `┼`. These are completely banned.
- No exceptions. Not for "clarity", not for alignment, not for terminal output.
