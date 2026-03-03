"""Parse Opus Magnum .puzzle binary files."""
from __future__ import annotations
import struct
from dataclasses import dataclass, field
from enum import IntEnum, IntFlag
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .hex import HexCoord


class AtomType(IntEnum):
    SALT = 1
    AIR = 2
    EARTH = 3
    FIRE = 4
    WATER = 5
    QUICKSILVER = 6
    GOLD = 7
    SILVER = 8
    COPPER = 9
    IRON = 10
    TIN = 11
    LEAD = 12
    VITAE = 13
    MORS = 14
    REPEAT = 15
    QUINTESSENCE = 16

    @property
    def is_cardinal(self) -> bool:
        return self in (AtomType.AIR, AtomType.EARTH, AtomType.FIRE, AtomType.WATER)

    @property
    def is_metal(self) -> bool:
        return self in (AtomType.LEAD, AtomType.TIN, AtomType.IRON,
                       AtomType.COPPER, AtomType.SILVER, AtomType.GOLD)

    @property
    def metal_rank(self) -> int:
        """Metal rank for projection chain: Lead=0 ... Gold=5."""
        ranks = {AtomType.LEAD: 0, AtomType.TIN: 1, AtomType.IRON: 2,
                 AtomType.COPPER: 3, AtomType.SILVER: 4, AtomType.GOLD: 5}
        return ranks.get(self, -1)


METAL_CHAIN = [AtomType.LEAD, AtomType.TIN, AtomType.IRON,
               AtomType.COPPER, AtomType.SILVER, AtomType.GOLD]


class BondType(IntEnum):
    NORMAL = 1
    TRIPLEX_R = 2
    TRIPLEX_Y = 4
    TRIPLEX_K = 8
    TRIPLEX = 14  # R|Y|K


@dataclass
class Atom:
    atom_type: AtomType
    position: HexCoord


@dataclass
class Bond:
    bond_type: BondType
    from_pos: HexCoord
    to_pos: HexCoord


@dataclass
class Molecule:
    atoms: List[Atom] = field(default_factory=list)
    bonds: List[Bond] = field(default_factory=list)

    @property
    def atom_count(self) -> int:
        return len(self.atoms)

    @property
    def is_monoatomic(self) -> bool:
        return len(self.atoms) == 1

    def element_counts(self) -> Dict[AtomType, int]:
        counts: Dict[AtomType, int] = {}
        for a in self.atoms:
            counts[a.atom_type] = counts.get(a.atom_type, 0) + 1
        return counts

    def atom_at(self, pos: HexCoord) -> Optional[Atom]:
        for a in self.atoms:
            if a.position == pos:
                return a
        return None

    @property
    def bounds(self) -> Tuple[int, int, int, int]:
        """Return (min_q, min_r, max_q, max_r)."""
        qs = [a.position.q for a in self.atoms]
        rs = [a.position.r for a in self.atoms]
        return (min(qs), min(rs), max(qs), max(rs))


class PartFlag(IntFlag):
    """Bitmask of available parts in a puzzle."""
    ARM1 = 1 << 0
    ARM2 = 1 << 1
    ARM3 = 1 << 2
    ARM6 = 1 << 3
    PISTON = 1 << 4
    TRACK = 1 << 5
    BONDER = 1 << 6
    UNBONDER = 1 << 7
    MULTI_BONDER = 1 << 8
    TRIPLEX_BONDER = 1 << 9
    CALCIFICATION = 1 << 10
    DUPLICATION = 1 << 11
    PROJECTION = 1 << 12
    PURIFICATION = 1 << 13
    ANIMISMUS = 1 << 14
    DISPOSAL = 1 << 15
    QUINTESSENCE_GLYPHS = 1 << 16  # Unification + Dispersion
    VAN_BERLO = 1 << 22
    EQUILIBRIUM = 1 << 23


@dataclass
class PuzzleIO:
    molecule: Molecule
    index: int = 0


@dataclass
class Puzzle:
    name: str
    display_name: str = ""
    inputs: List[PuzzleIO] = field(default_factory=list)
    outputs: List[PuzzleIO] = field(default_factory=list)
    output_scale: int = 1
    parts_available: int = 0xFFFFFFFFFFFFFFFF
    is_production: bool = False

    def has_part(self, flag: PartFlag) -> bool:
        return bool(self.parts_available & flag)

    @property
    def required_output_count(self) -> int:
        """How many times each output must be produced."""
        return self.output_scale

    def input_element_counts(self) -> Dict[AtomType, int]:
        """Total element counts across all inputs."""
        counts: Dict[AtomType, int] = {}
        for pio in self.inputs:
            for atom_type, count in pio.molecule.element_counts().items():
                counts[atom_type] = counts.get(atom_type, 0) + count
        return counts

    def output_element_counts(self) -> Dict[AtomType, int]:
        """Total element counts across all outputs (per scale)."""
        counts: Dict[AtomType, int] = {}
        for pio in self.outputs:
            for atom_type, count in pio.molecule.element_counts().items():
                counts[atom_type] = counts.get(atom_type, 0) + count
        return counts


def _read_string(data: bytes, offset: int) -> Tuple[str, int]:
    """Read a .NET 7-bit length-prefixed string."""
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


def _read_molecule(data: bytes, offset: int) -> Tuple[Molecule, int]:
    """Read a molecule from puzzle binary data."""
    mol = Molecule()
    num_atoms = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    for _ in range(num_atoms):
        atype = data[offset]
        q = struct.unpack_from('<b', data, offset + 1)[0]
        r = struct.unpack_from('<b', data, offset + 2)[0]
        offset += 3
        mol.atoms.append(Atom(AtomType(atype), HexCoord(q, r)))
    num_bonds = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    for _ in range(num_bonds):
        btype = data[offset]
        fq = struct.unpack_from('<b', data, offset + 1)[0]
        fr = struct.unpack_from('<b', data, offset + 2)[0]
        tq = struct.unpack_from('<b', data, offset + 3)[0]
        tr = struct.unpack_from('<b', data, offset + 4)[0]
        offset += 5
        mol.bonds.append(Bond(BondType(btype), HexCoord(fq, fr), HexCoord(tq, tr)))
    return mol, offset


def parse_puzzle(path: str) -> Puzzle:
    """Parse a .puzzle binary file."""
    data = Path(path).read_bytes()
    offset = 0
    version = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    assert version <= 3, f"Unsupported puzzle version: {version}"

    name, offset = _read_string(data, offset)
    puzzle = Puzzle(name=name)

    if version >= 2:
        _creator = struct.unpack_from('<Q', data, offset)[0]
        offset += 8

    puzzle.parts_available = struct.unpack_from('<Q', data, offset)[0]
    offset += 8

    # Inputs
    num_inputs = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    for i in range(num_inputs):
        mol, offset = _read_molecule(data, offset)
        puzzle.inputs.append(PuzzleIO(molecule=mol, index=i))

    # Outputs
    num_outputs = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    for i in range(num_outputs):
        mol, offset = _read_molecule(data, offset)
        puzzle.outputs.append(PuzzleIO(molecule=mol, index=i))

    if version >= 3:
        puzzle.output_scale = struct.unpack_from('<I', data, offset)[0]
        offset += 4
        puzzle.is_production = bool(data[offset])
        offset += 1

    return puzzle
