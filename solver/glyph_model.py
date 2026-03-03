"""Glyph model for Opus Magnum god-sum solver.

Defines all 13 glyph types with their local-coordinate slot layouts,
costs, footprints, and conversion semantics.  Coordinate transforms
follow omsim's convention:

    world = origin + DIRECTIONS[rot]*du + DIRECTIONS[(rot+1)%6]*dv
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .hex import DIRECTIONS, HexCoord


# ---------------------------------------------------------------------------
# Core data-classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GlyphSlot:
    """One interaction slot of a glyph, in local (du, dv) coordinates.

    Parameters
    ----------
    du, dv : int
        Local offsets along the glyph's u and v axes.
    role : str
        One of 'input', 'output', or 'active'.
    atom_constraint : str or None
        If set, the atom type this slot expects/produces.  Values are
        semantic tags such as 'salt', 'vitae', 'cardinal', 'metal', etc.
    """
    du: int
    dv: int
    role: str
    atom_constraint: Optional[str] = None


@dataclass(frozen=True)
class GlyphSpec:
    """Static specification for one glyph type.

    Parameters
    ----------
    name : str
        The omsim glyph identifier (e.g. 'glyph-calcification').
    cost : int
        Gold cost to place this glyph.
    slots : tuple of GlyphSlot
        All interaction slots (inputs, outputs, actives).
    footprint : tuple of (int, int)
        Local (du, dv) pairs for every hex this glyph occupies.
    is_conversion : bool
        True for glyphs that consume inputs and produce outputs over
        multiple half-steps (animismus, dispersion, purification,
        unification).  False for immediate glyphs.
    """
    name: str
    cost: int
    slots: Tuple[GlyphSlot, ...]
    footprint: Tuple[Tuple[int, int], ...]
    is_conversion: bool

    @property
    def input_slots(self) -> Tuple[GlyphSlot, ...]:
        """Slots with role 'input'."""
        return tuple(s for s in self.slots if s.role == 'input')

    @property
    def output_slots(self) -> Tuple[GlyphSlot, ...]:
        """Slots with role 'output'."""
        return tuple(s for s in self.slots if s.role == 'output')

    @property
    def active_slots(self) -> Tuple[GlyphSlot, ...]:
        """Slots with role 'active'."""
        return tuple(s for s in self.slots if s.role == 'active')


# ---------------------------------------------------------------------------
# Coordinate transforms
# ---------------------------------------------------------------------------

def local_to_world(origin: HexCoord, rotation: int, du: int, dv: int) -> HexCoord:
    """Convert a local (du, dv) offset to a world hex coordinate.

    Uses the omsim convention::

        u_dir = DIRECTIONS[rotation % 6]
        v_dir = DIRECTIONS[(rotation + 1) % 6]
        world = origin + u_dir * du + v_dir * dv
    """
    rot = rotation % 6
    u_dir = DIRECTIONS[rot]
    v_dir = DIRECTIONS[(rot + 1) % 6]
    return HexCoord(
        origin.q + u_dir.q * du + v_dir.q * dv,
        origin.r + u_dir.r * du + v_dir.r * dv,
    )


def footprint_world(origin: HexCoord, rotation: int, spec: GlyphSpec) -> List[HexCoord]:
    """Return every world-space hex occupied by *spec* placed at *origin* with *rotation*."""
    return [local_to_world(origin, rotation, du, dv) for du, dv in spec.footprint]


def slot_world(origin: HexCoord, rotation: int, slot: GlyphSlot) -> HexCoord:
    """Return the world-space hex for a single glyph slot."""
    return local_to_world(origin, rotation, slot.du, slot.dv)


# ---------------------------------------------------------------------------
# Glyph definitions — all 13 glyphs
# ---------------------------------------------------------------------------

# 1. Calcification
CALCIFICATION = GlyphSpec(
    name='glyph-calcification',
    cost=10,
    slots=(
        GlyphSlot(0, 0, 'active', 'cardinal'),
    ),
    footprint=((0, 0),),
    is_conversion=False,
)

# 2. Animismus (Life and Death)
ANIMISMUS = GlyphSpec(
    name='glyph-life-and-death',
    cost=20,
    slots=(
        GlyphSlot(0, 0, 'input', 'salt'),
        GlyphSlot(1, 0, 'input', 'salt'),
        GlyphSlot(0, 1, 'output', 'vitae'),
        GlyphSlot(1, -1, 'output', 'mors'),
    ),
    footprint=((0, 1), (1, 0), (1, -1), (0, 0)),
    is_conversion=True,
)

# 3. Projection
PROJECTION = GlyphSpec(
    name='glyph-projection',
    cost=20,
    slots=(
        GlyphSlot(0, 0, 'input', 'quicksilver'),
        GlyphSlot(1, 0, 'active', 'metal'),
    ),
    footprint=((1, 0), (0, 0)),
    is_conversion=False,
)

# 4. Dispersion
DISPERSION = GlyphSpec(
    name='glyph-dispersion',
    cost=20,
    slots=(
        GlyphSlot(0, 0, 'input', 'quintessence'),
        GlyphSlot(1, 0, 'output', 'earth'),
        GlyphSlot(1, -1, 'output', 'water'),
        GlyphSlot(0, -1, 'output', 'fire'),
        GlyphSlot(-1, 0, 'output', 'air'),
    ),
    footprint=((1, 0), (1, -1), (0, -1), (-1, 0), (0, 0)),
    is_conversion=True,
)

# 5. Purification
PURIFICATION = GlyphSpec(
    name='glyph-purification',
    cost=20,
    slots=(
        GlyphSlot(0, 0, 'input', 'metal'),
        GlyphSlot(1, 0, 'input', 'metal'),
        GlyphSlot(0, 1, 'output', 'metal_prev'),
    ),
    footprint=((1, 0), (0, 1), (0, 0)),
    is_conversion=True,
)

# 6. Duplication
DUPLICATION = GlyphSpec(
    name='glyph-duplication',
    cost=20,
    slots=(
        GlyphSlot(0, 0, 'input', 'cardinal'),
        GlyphSlot(1, 0, 'active', 'salt'),
    ),
    footprint=((1, 0), (0, 0)),
    is_conversion=False,
)

# 7. Unification
UNIFICATION = GlyphSpec(
    name='glyph-unification',
    cost=20,
    slots=(
        GlyphSlot(0, 1, 'input', 'cardinal'),
        GlyphSlot(-1, 1, 'input', 'cardinal'),
        GlyphSlot(0, -1, 'input', 'cardinal'),
        GlyphSlot(1, -1, 'input', 'cardinal'),
        GlyphSlot(0, 0, 'output', 'quintessence'),
    ),
    footprint=((0, 1), (-1, 1), (0, -1), (1, -1), (0, 0)),
    is_conversion=True,
)

# 8. Bonding
BONDING = GlyphSpec(
    name='bonder',
    cost=10,
    slots=(
        GlyphSlot(0, 0, 'active'),
        GlyphSlot(1, 0, 'active'),
    ),
    footprint=((1, 0), (0, 0)),
    is_conversion=False,
)

# 9. Unbonding
UNBONDING = GlyphSpec(
    name='unbonder',
    cost=10,
    slots=(
        GlyphSlot(0, 0, 'active'),
        GlyphSlot(1, 0, 'active'),
    ),
    footprint=((1, 0), (0, 0)),
    is_conversion=False,
)

# 10. Triplex Bonding
TRIPLEX_BONDING = GlyphSpec(
    name='bonder-prisma',
    cost=20,
    slots=(
        GlyphSlot(0, 0, 'active'),
        GlyphSlot(0, 1, 'active'),
        GlyphSlot(1, 0, 'active'),
    ),
    footprint=((1, 0), (0, 1), (0, 0)),
    is_conversion=False,
)

# 11. Multi Bonding
MULTI_BONDING = GlyphSpec(
    name='bonder-speed',
    cost=30,
    slots=(
        GlyphSlot(0, 0, 'active'),
        GlyphSlot(1, 0, 'active'),
        GlyphSlot(0, -1, 'active'),
        GlyphSlot(-1, 1, 'active'),
    ),
    footprint=((1, 0), (0, -1), (-1, 1), (0, 0)),
    is_conversion=False,
)

# 12. Disposal
DISPOSAL = GlyphSpec(
    name='glyph-disposal',
    cost=0,
    slots=(
        GlyphSlot(0, 0, 'active'),
    ),
    footprint=((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1), (0, 0)),
    is_conversion=False,
)

# 13. Equilibrium
EQUILIBRIUM = GlyphSpec(
    name='glyph-marker',
    cost=0,
    slots=(),
    footprint=((0, 0),),
    is_conversion=False,
)


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

GLYPH_SPECS: Dict[str, GlyphSpec] = {
    spec.name: spec
    for spec in (
        CALCIFICATION,
        ANIMISMUS,
        PROJECTION,
        DISPERSION,
        PURIFICATION,
        DUPLICATION,
        UNIFICATION,
        BONDING,
        UNBONDING,
        TRIPLEX_BONDING,
        MULTI_BONDING,
        DISPOSAL,
        EQUILIBRIUM,
    )
}


def get_glyph_spec(name: str) -> GlyphSpec:
    """Look up a GlyphSpec by its omsim name.  Raises KeyError if unknown."""
    return GLYPH_SPECS[name]
