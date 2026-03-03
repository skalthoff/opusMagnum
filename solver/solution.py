"""Read and write Opus Magnum .solution binary files."""
from __future__ import annotations
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .hex import HexCoord


# Instruction byte codes as stored in .solution binary files.
# NOTE: These are DIFFERENT from omsim's internal simulation codes.
# The solution file format uses its own encoding that omsim's decode.c
# translates into simulation-level instructions.
#
# Solution file → omsim sim:
#   'R' → 'd' (rot CW)      'r' → 'a' (rot CCW)
#   'E' → 'w' (extend)       'e' → 's' (retract)
#   'G' → 'r' (grab)         'g' → 'f' (drop)
#   'P' → 'e' (pivot CW)     'p' → 'q' (pivot CCW)
#   'A' → 'g' (track fwd)    'a' → 't' (track bwd)
#   'C' → repeat (special)   'X' → reset (expanded)
#   'O' → ' ' (noop)
class Inst:
    ROTATE_CW = ord('R')   # 0x52
    ROTATE_CCW = ord('r')  # 0x72
    EXTEND = ord('E')      # 0x45
    RETRACT = ord('e')     # 0x65
    GRAB = ord('G')        # 0x47
    DROP = ord('g')        # 0x67
    PIVOT_CW = ord('P')    # 0x50
    PIVOT_CCW = ord('p')   # 0x70
    TRACK_FWD = ord('A')   # 0x41
    TRACK_BWD = ord('a')   # 0x61
    REPEAT = ord('C')      # 0x43
    RESET = ord('X')       # 0x58
    NOOP = ord('O')        # 0x4F

    NAMES = {
        ord('R'): 'rot_cw', ord('r'): 'rot_ccw',
        ord('E'): 'extend', ord('e'): 'retract',
        ord('G'): 'grab', ord('g'): 'drop',
        ord('P'): 'pivot_cw', ord('p'): 'pivot_ccw',
        ord('A'): 'track+', ord('a'): 'track-',
        ord('C'): 'repeat', ord('X'): 'reset', ord('O'): 'noop',
    }


# Part costs
PART_COSTS = {
    'arm1': 20, 'arm2': 30, 'arm3': 30, 'arm6': 30,
    'piston': 40, 'baron': 30, 'track': 5,  # per hex
    'bonder': 10, 'unbonder': 10, 'bonder-prisma': 20,
    'bonder-speed': 30, 'glyph-calcification': 10,
    'glyph-life-and-death': 20, 'glyph-projection': 20,
    'glyph-dispersion': 20, 'glyph-purification': 20,
    'glyph-duplication': 20, 'glyph-unification': 20,
    'glyph-disposal': 0, 'glyph-marker': 0,
    'input': 0, 'out-std': 0, 'out-rep': 0, 'pipe': 0,
}


@dataclass
class Instruction:
    index: int  # Position on the tape (0-based)
    instruction: int  # ASCII char code


@dataclass
class TrackHex:
    offset_q: int
    offset_r: int


@dataclass
class Part:
    name: str
    position: HexCoord
    size: int = 1  # arm length
    rotation: int = 0  # 0-5 (60-degree increments)
    io_index: int = 0  # which input/output
    instructions: List[Instruction] = field(default_factory=list)
    track_hexes: List[TrackHex] = field(default_factory=list)
    arm_number: int = 0
    conduit_id: int = 0
    conduit_hexes: List[TrackHex] = field(default_factory=list)

    @property
    def cost(self) -> int:
        if self.name == 'track':
            return 5 * len(self.track_hexes)
        return PART_COSTS.get(self.name, 0)

    @property
    def is_arm(self) -> bool:
        return self.name in ('arm1', 'arm2', 'arm3', 'arm6', 'piston', 'baron')

    @property
    def is_glyph(self) -> bool:
        return self.name.startswith('glyph-') or self.name.startswith('bonder') or self.name == 'unbonder'

    @property
    def instruction_count(self) -> int:
        """Non-noop instruction count."""
        return sum(1 for i in self.instructions if i.instruction != Inst.NOOP)

    def get_tape(self, length: int) -> List[int]:
        """Get instruction tape as a list of ints, padded to `length`."""
        tape = [0] * length
        for inst in self.instructions:
            if 0 <= inst.index < length:
                tape[inst.index] = inst.instruction
        return tape

    def set_tape(self, tape: List[int]):
        """Set instructions from a tape list."""
        self.instructions = []
        for i, code in enumerate(tape):
            if code and code != Inst.NOOP:
                self.instructions.append(Instruction(i, code))


@dataclass
class Solution:
    puzzle_name: str
    solution_name: str = "Generated Solution"
    solved: bool = True
    cycles: int = 0
    cost: int = 0
    area: int = 0
    instruction_count: int = 0
    parts: List[Part] = field(default_factory=list)

    def total_cost(self) -> int:
        return sum(p.cost for p in self.parts)

    def total_instructions(self) -> int:
        return sum(p.instruction_count for p in self.parts)

    def arms(self) -> List[Part]:
        return [p for p in self.parts if p.is_arm]

    def glyphs(self) -> List[Part]:
        return [p for p in self.parts if p.is_glyph]


def _read_string(data: bytes, offset: int) -> Tuple[str, int]:
    length = 0
    shift = 0
    while True:
        b = data[offset]
        offset += 1
        length |= (b & 0x7F) << shift
        shift += 7
        if not (b & 0x80):
            break
    s = data[offset:offset + length].decode('utf-8')
    return s, offset + length


def _write_string(s: str) -> bytes:
    encoded = s.encode('utf-8')
    length = len(encoded)
    header = bytearray()
    while length > 0x7F:
        header.append((length & 0x7F) | 0x80)
        length >>= 7
    header.append(length & 0x7F)
    return bytes(header) + encoded


def parse_solution(path: str) -> Solution:
    """Parse a .solution binary file."""
    data = Path(path).read_bytes()
    offset = 0

    version = struct.unpack_from('<I', data, offset)[0]
    offset += 4

    puzzle_name, offset = _read_string(data, offset)
    solution_name, offset = _read_string(data, offset)

    sol = Solution(puzzle_name=puzzle_name, solution_name=solution_name)

    solved_flag = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    sol.solved = solved_flag != 0

    if sol.solved:
        # Read 4 metric pairs: (id, value)
        for _ in range(4):
            metric_id = struct.unpack_from('<I', data, offset)[0]
            metric_val = struct.unpack_from('<I', data, offset + 4)[0]
            offset += 8
            if metric_id == 0:
                sol.cycles = metric_val
            elif metric_id == 1:
                sol.cost = metric_val
            elif metric_id == 2:
                sol.area = metric_val
            elif metric_id == 3:
                sol.instruction_count = metric_val

    num_parts = struct.unpack_from('<I', data, offset)[0]
    offset += 4

    for _ in range(num_parts):
        name, offset = _read_string(data, offset)
        _marker = data[offset]  # always 0x01
        offset += 1
        q = struct.unpack_from('<i', data, offset)[0]
        r = struct.unpack_from('<i', data, offset + 4)[0]
        size = struct.unpack_from('<I', data, offset + 8)[0]
        rotation = struct.unpack_from('<i', data, offset + 12)[0]
        io_index = struct.unpack_from('<I', data, offset + 16)[0]
        offset += 20

        part = Part(name=name, position=HexCoord(q, r), size=size,
                    rotation=rotation, io_index=io_index)

        # Instructions
        num_instr = struct.unpack_from('<I', data, offset)[0]
        offset += 4
        for _ in range(num_instr):
            idx = struct.unpack_from('<i', data, offset)[0]
            code = data[offset + 4]
            offset += 5
            part.instructions.append(Instruction(idx, code))

        # Track hexes
        if name == 'track':
            num_hexes = struct.unpack_from('<I', data, offset)[0]
            offset += 4
            for _ in range(num_hexes):
                oq = struct.unpack_from('<i', data, offset)[0]
                orr = struct.unpack_from('<i', data, offset + 4)[0]
                offset += 8
                part.track_hexes.append(TrackHex(oq, orr))

        # Arm number
        arm_num = struct.unpack_from('<I', data, offset)[0]
        offset += 4
        part.arm_number = arm_num

        # Conduit hexes
        if name == 'pipe':
            part.conduit_id = struct.unpack_from('<I', data, offset)[0]
            offset += 4
            num_ch = struct.unpack_from('<I', data, offset)[0]
            offset += 4
            for _ in range(num_ch):
                oq = struct.unpack_from('<i', data, offset)[0]
                orr = struct.unpack_from('<i', data, offset + 4)[0]
                offset += 8
                part.conduit_hexes.append(TrackHex(oq, orr))

        sol.parts.append(part)

    return sol


def solution_to_bytes(sol: Solution) -> bytes:
    """Serialize a Solution to binary format."""
    buf = bytearray()

    # Version
    buf += struct.pack('<I', 7)
    # Puzzle name
    buf += _write_string(sol.puzzle_name)
    # Solution name
    buf += _write_string(sol.solution_name)

    # Solved flag
    buf += struct.pack('<I', 1 if sol.solved else 0)

    if sol.solved:
        # Metrics
        buf += struct.pack('<II', 0, sol.cycles)
        buf += struct.pack('<II', 1, sol.cost)
        buf += struct.pack('<II', 2, sol.area)
        buf += struct.pack('<II', 3, sol.instruction_count)

    # Parts
    buf += struct.pack('<I', len(sol.parts))
    for part in sol.parts:
        buf += _write_string(part.name)
        buf += struct.pack('<B', 1)  # marker byte
        buf += struct.pack('<ii', part.position.q, part.position.r)
        buf += struct.pack('<I', part.size)
        buf += struct.pack('<i', part.rotation)
        buf += struct.pack('<I', part.io_index)

        # Instructions
        buf += struct.pack('<I', len(part.instructions))
        for inst in part.instructions:
            buf += struct.pack('<i', inst.index)
            buf += struct.pack('<B', inst.instruction)

        # Track
        if part.name == 'track':
            buf += struct.pack('<I', len(part.track_hexes))
            for th in part.track_hexes:
                buf += struct.pack('<ii', th.offset_q, th.offset_r)

        # Arm number
        buf += struct.pack('<I', part.arm_number)

        # Conduit
        if part.name == 'pipe':
            buf += struct.pack('<I', part.conduit_id)
            buf += struct.pack('<I', len(part.conduit_hexes))
            for ch in part.conduit_hexes:
                buf += struct.pack('<ii', ch.offset_q, ch.offset_r)

    return bytes(buf)


def write_solution(sol: Solution, path: str):
    """Write a .solution binary file."""
    Path(path).write_bytes(solution_to_bytes(sol))


def _serialize_arm_part(arm_type: str, pos: 'HexCoord', size: int,
                        rotation: int, tape: List[int]) -> bytes:
    """Serialize a single arm part to binary format."""
    buf = bytearray()
    buf += _write_string(arm_type)
    buf += struct.pack('<B', 1)  # marker byte
    buf += struct.pack('<ii', pos.q, pos.r)
    buf += struct.pack('<I', size)
    buf += struct.pack('<i', rotation)
    buf += struct.pack('<I', 0)  # io_index

    # Instructions: only non-noop entries
    instructions = [(i, code) for i, code in enumerate(tape) if code and code != Inst.NOOP]
    buf += struct.pack('<I', len(instructions))
    for idx, code in instructions:
        buf += struct.pack('<i', idx)
        buf += struct.pack('<B', code)

    # Arm number
    buf += struct.pack('<I', 0)

    return bytes(buf)


class CachedSolutionBase:
    """Pre-serialized solution bytes with the arm omitted.

    The part count field is at a known offset so we can patch it when
    splicing in different arm tapes without re-serializing the base.
    """

    __slots__ = ('_header', '_parts_data', '_base_part_count',
                 '_arm_type', '_arm_pos', '_arm_size', '_arm_rot')

    def __init__(self, base_sol: Solution, layout_info: dict):
        # Serialize the header (everything before parts data)
        header = bytearray()
        header += struct.pack('<I', 7)  # version
        header += _write_string(base_sol.puzzle_name)
        header += _write_string(base_sol.solution_name)
        header += struct.pack('<I', 1 if base_sol.solved else 0)
        if base_sol.solved:
            header += struct.pack('<II', 0, base_sol.cycles)
            header += struct.pack('<II', 1, base_sol.cost)
            header += struct.pack('<II', 2, base_sol.area)
            header += struct.pack('<II', 3, base_sol.instruction_count)

        self._base_part_count = len(base_sol.parts)
        # Part count placeholder — will be patched in splice()
        header += struct.pack('<I', self._base_part_count + 1)

        # Serialize all base parts (non-arm)
        parts_data = bytearray()
        for part in base_sol.parts:
            parts_data += _write_string(part.name)
            parts_data += struct.pack('<B', 1)
            parts_data += struct.pack('<ii', part.position.q, part.position.r)
            parts_data += struct.pack('<I', part.size)
            parts_data += struct.pack('<i', part.rotation)
            parts_data += struct.pack('<I', part.io_index)

            parts_data += struct.pack('<I', len(part.instructions))
            for inst in part.instructions:
                parts_data += struct.pack('<i', inst.index)
                parts_data += struct.pack('<B', inst.instruction)

            if part.name == 'track':
                parts_data += struct.pack('<I', len(part.track_hexes))
                for th in part.track_hexes:
                    parts_data += struct.pack('<ii', th.offset_q, th.offset_r)

            parts_data += struct.pack('<I', part.arm_number)

            if part.name == 'pipe':
                parts_data += struct.pack('<I', part.conduit_id)
                parts_data += struct.pack('<I', len(part.conduit_hexes))
                for ch in part.conduit_hexes:
                    parts_data += struct.pack('<ii', ch.offset_q, ch.offset_r)

        self._header = bytes(header)
        self._parts_data = bytes(parts_data)
        self._arm_type = layout_info.get('arm_type', 'arm1')
        self._arm_pos = layout_info['arm_pos']
        self._arm_size = layout_info['arm_len']
        self._arm_rot = layout_info['arm_rot']

    def splice(self, tape: List[int]) -> bytes:
        """Build complete solution bytes with the given arm tape.

        Much faster than full solution_to_bytes() since header+base parts
        are pre-serialized and only the arm bytes change.
        """
        arm_bytes = _serialize_arm_part(
            self._arm_type, self._arm_pos, self._arm_size,
            self._arm_rot, tape)
        return self._header + self._parts_data + arm_bytes
