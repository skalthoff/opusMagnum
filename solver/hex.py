"""Hexagonal grid math for Opus Magnum."""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Set
import math


@dataclass(frozen=True)
class HexCoord:
    """Axial hex coordinate (q, r). Third axis s = -q - r."""
    q: int
    r: int

    @property
    def s(self) -> int:
        return -self.q - self.r

    def __add__(self, other: HexCoord) -> HexCoord:
        return HexCoord(self.q + other.q, self.r + other.r)

    def __sub__(self, other: HexCoord) -> HexCoord:
        return HexCoord(self.q - other.q, self.r - other.r)

    def __neg__(self) -> HexCoord:
        return HexCoord(-self.q, -self.r)

    def distance_to(self, other: HexCoord) -> int:
        return (abs(self.q - other.q) + abs(self.r - other.r) + abs(self.s - other.s)) // 2

    def length(self) -> int:
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2

    def rotated(self, turns: int) -> HexCoord:
        """Rotate around origin by `turns` * 60 degrees CCW."""
        turns = turns % 6
        q, r, s = self.q, self.r, self.s
        for _ in range(turns):
            q, r, s = -r, -s, -q
        return HexCoord(q, r)

    def rotated_around(self, pivot: HexCoord, turns: int) -> HexCoord:
        return (self - pivot).rotated(turns) + pivot

    def neighbors(self) -> List[HexCoord]:
        return [self + d for d in DIRECTIONS]

    def to_pixel(self) -> tuple[float, float]:
        """Convert to pixel coordinates (matching game's coordinate system)."""
        x = 82.0 * (self.q + 0.5 * self.r)
        y = 71.0 * self.r
        return (x, y)

    def __repr__(self) -> str:
        return f"Hex({self.q},{self.r})"


# The 6 hex directions in CW order, matching omsim's u_offset_for_direction().
# In flat-top hex with axial coords: +q = East, +r = Southeast.
# CW rotation decreases direction index by 1; CCW increases by 1.
DIRECTIONS = [
    HexCoord(1, 0),   # 0: E
    HexCoord(0, 1),   # 1: SE
    HexCoord(-1, 1),  # 2: SW
    HexCoord(-1, 0),  # 3: W
    HexCoord(0, -1),  # 4: NW
    HexCoord(1, -1),  # 5: NE
]

ORIGIN = HexCoord(0, 0)


class HexRotation:
    """Represents a rotation in 60-degree increments."""
    R0 = 0
    R60 = 1
    R120 = 2
    R180 = 3
    R240 = 4
    R300 = 5

    @staticmethod
    def normalize(turns: int) -> int:
        return turns % 6


def hex_ring(center: HexCoord, radius: int) -> List[HexCoord]:
    """Get all hexes at exactly `radius` distance from center."""
    if radius == 0:
        return [center]
    results = []
    h = center + HexCoord(radius, 0)
    for i in range(6):
        for _ in range(radius):
            results.append(h)
            h = h + DIRECTIONS[(i + 2) % 6]
    return results


def hex_spiral(center: HexCoord, radius: int) -> List[HexCoord]:
    """Get all hexes within `radius` distance from center, spiraling outward."""
    results = [center]
    for r in range(1, radius + 1):
        results.extend(hex_ring(center, r))
    return results


def hex_area(coords: Set[HexCoord]) -> int:
    """Count unique hex cells."""
    return len(coords)
