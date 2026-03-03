"""Transmutation recipe analysis for Opus Magnum puzzles.

Determines what glyphs and reactions are needed to transform input elements
into output elements, and calculates minimum costs and theoretical bounds.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple

from .puzzle import AtomType, Puzzle, METAL_CHAIN, PartFlag


class Reaction(Enum):
    """Types of transmutation reactions."""
    CALCIFICATION = auto()     # Cardinal -> Salt
    VAN_BERLO = auto()         # Salt -> Cardinal (via Wheel + Duplication)
    ANIMISMUS = auto()         # 2 Salt -> Vitae + Mors
    PROJECTION = auto()        # Metal + Quicksilver -> NextMetal
    PURIFICATION = auto()      # Metal -> PrevMetal + Quicksilver
    DISPERSION = auto()        # Quintessence -> Air + Earth + Fire + Water
    UNIFICATION = auto()       # Air + Earth + Fire + Water -> Quintessence


# Cost of each reaction's glyph
REACTION_GLYPH_COST = {
    Reaction.CALCIFICATION: 10,
    Reaction.VAN_BERLO: 50,     # baron(30) + duplication(20)
    Reaction.ANIMISMUS: 20,
    Reaction.PROJECTION: 20,
    Reaction.PURIFICATION: 20,
    Reaction.DISPERSION: 20,
    Reaction.UNIFICATION: 20,
}

# Glyph part names for each reaction
REACTION_GLYPHS = {
    Reaction.CALCIFICATION: ['glyph-calcification'],
    Reaction.VAN_BERLO: ['baron', 'glyph-duplication'],
    Reaction.ANIMISMUS: ['glyph-life-and-death'],
    Reaction.PROJECTION: ['glyph-projection'],
    Reaction.PURIFICATION: ['glyph-purification'],
    Reaction.DISPERSION: ['glyph-dispersion'],
    Reaction.UNIFICATION: ['glyph-unification'],
}


@dataclass
class Recipe:
    """A recipe describing how to transform inputs into outputs."""
    reactions: Dict[Reaction, int] = field(default_factory=dict)
    input_scale: int = 1  # How many times to use each input set
    waste: Dict[AtomType, int] = field(default_factory=dict)

    @property
    def glyph_cost(self) -> int:
        """Total cost of glyphs needed for all reactions."""
        cost = 0
        for reaction in self.reactions:
            if self.reactions[reaction] > 0:
                cost += REACTION_GLYPH_COST[reaction]
        return cost

    @property
    def required_glyphs(self) -> List[str]:
        """List of glyph part names needed."""
        glyphs = []
        for reaction, count in self.reactions.items():
            if count > 0:
                glyphs.extend(REACTION_GLYPHS[reaction])
        return glyphs


@dataclass
class PuzzleAnalysis:
    """Complete analysis of a puzzle's requirements."""
    puzzle: Puzzle
    input_elements: Dict[AtomType, int] = field(default_factory=dict)
    output_elements: Dict[AtomType, int] = field(default_factory=dict)
    element_deficit: Dict[AtomType, int] = field(default_factory=dict)
    element_surplus: Dict[AtomType, int] = field(default_factory=dict)
    recipe: Optional[Recipe] = None
    min_cost: int = 0
    min_cycles_theoretical: int = 0
    needs_bonding: bool = False
    needs_unbonding: bool = False
    num_input_sets: int = 1  # N in overlap formula
    complexity: str = "trivial"


def analyze_puzzle(puzzle: Puzzle) -> PuzzleAnalysis:
    """Perform comprehensive analysis of a puzzle."""
    analysis = PuzzleAnalysis(puzzle=puzzle)

    # Count elements in inputs and outputs
    analysis.input_elements = puzzle.input_element_counts()
    analysis.output_elements = puzzle.output_element_counts()

    # Determine element deficits and surpluses
    all_types = set(analysis.input_elements.keys()) | set(analysis.output_elements.keys())
    for t in all_types:
        inp = analysis.input_elements.get(t, 0)
        out = analysis.output_elements.get(t, 0)
        if out > inp:
            analysis.element_deficit[t] = out - inp
        elif inp > out:
            analysis.element_surplus[t] = inp - out

    # Check if bonding/unbonding needed
    for pio in puzzle.outputs:
        if pio.molecule.bonds:
            analysis.needs_bonding = True
            break
    for pio in puzzle.inputs:
        if pio.molecule.bonds:
            analysis.needs_unbonding = True
            break

    # Classify complexity
    analysis.complexity = _classify_complexity(puzzle, analysis)

    # Calculate recipe
    analysis.recipe = _calculate_recipe(puzzle, analysis)

    # Calculate minimum cost
    analysis.min_cost = _calculate_min_cost(puzzle, analysis)

    # Calculate theoretical minimum cycles
    analysis.min_cycles_theoretical = _calculate_min_cycles(puzzle, analysis)

    return analysis


def _classify_complexity(puzzle: Puzzle, analysis: PuzzleAnalysis) -> str:
    """Classify puzzle complexity."""
    all_mono_in = all(pio.molecule.is_monoatomic for pio in puzzle.inputs)
    all_mono_out = all(pio.molecule.is_monoatomic for pio in puzzle.outputs)

    if not analysis.element_deficit and not analysis.element_surplus:
        if all_mono_in and all_mono_out:
            return "trivial"  # Just move atoms
        elif not analysis.needs_bonding and not analysis.needs_unbonding:
            return "rearrange"
        else:
            return "bond_only"

    has_metal_conversion = any(t.is_metal for t in analysis.element_deficit) or \
                           any(t.is_metal for t in analysis.element_surplus)
    has_cardinal_conversion = any(t.is_cardinal for t in analysis.element_deficit) or \
                              any(t.is_cardinal for t in analysis.element_surplus)
    has_quintessence = AtomType.QUINTESSENCE in analysis.element_deficit or \
                       AtomType.QUINTESSENCE in analysis.element_surplus
    has_vital = (AtomType.VITAE in analysis.element_deficit or
                 AtomType.MORS in analysis.element_deficit)

    if has_metal_conversion and has_cardinal_conversion:
        return "complex_multi"
    elif has_metal_conversion:
        return "metal_chain"
    elif has_quintessence:
        return "quintessence"
    elif has_vital:
        return "vital"
    elif has_cardinal_conversion:
        return "cardinal"
    elif all_mono_in and all_mono_out:
        return "simple_conversion"
    else:
        return "moderate"


def _calculate_recipe(puzzle: Puzzle, analysis: PuzzleAnalysis) -> Recipe:
    """Calculate the minimum set of reactions needed."""
    recipe = Recipe()
    # Start with element balance from one input set -> one output set
    need = dict(analysis.element_deficit)
    have_extra = dict(analysis.element_surplus)

    # Handle Quintessence
    qn = need.get(AtomType.QUINTESSENCE, 0)
    qs = have_extra.get(AtomType.QUINTESSENCE, 0)
    if qn > 0 and puzzle.has_part(PartFlag.QUINTESSENCE_GLYPHS):
        recipe.reactions[Reaction.UNIFICATION] = qn
        # Unification needs 4 cardinals
        for cardinal in [AtomType.AIR, AtomType.EARTH, AtomType.FIRE, AtomType.WATER]:
            need[cardinal] = need.get(cardinal, 0) + qn
        need.pop(AtomType.QUINTESSENCE, None)
    if qs > 0 and puzzle.has_part(PartFlag.QUINTESSENCE_GLYPHS):
        recipe.reactions[Reaction.DISPERSION] = qs
        for cardinal in [AtomType.AIR, AtomType.EARTH, AtomType.FIRE, AtomType.WATER]:
            have_extra[cardinal] = have_extra.get(cardinal, 0) + qs
        have_extra.pop(AtomType.QUINTESSENCE, None)

    # Handle Vitae/Mors
    vitae_need = need.get(AtomType.VITAE, 0)
    mors_need = need.get(AtomType.MORS, 0)
    if vitae_need > 0 or mors_need > 0:
        animismus_count = max(vitae_need, mors_need)
        recipe.reactions[Reaction.ANIMISMUS] = animismus_count
        need[AtomType.SALT] = need.get(AtomType.SALT, 0) + 2 * animismus_count
        need.pop(AtomType.VITAE, None)
        need.pop(AtomType.MORS, None)
        if vitae_need < animismus_count:
            recipe.waste[AtomType.VITAE] = animismus_count - vitae_need
        if mors_need < animismus_count:
            recipe.waste[AtomType.MORS] = animismus_count - mors_need

    # Handle metals via Projection
    for i in range(len(METAL_CHAIN) - 1, 0, -1):
        metal = METAL_CHAIN[i]
        metal_need = need.get(metal, 0)
        if metal_need > 0:
            prev_metal = METAL_CHAIN[i - 1]
            if puzzle.has_part(PartFlag.PROJECTION):
                recipe.reactions[Reaction.PROJECTION] = \
                    recipe.reactions.get(Reaction.PROJECTION, 0) + metal_need
                need[prev_metal] = need.get(prev_metal, 0) + metal_need
                need[AtomType.QUICKSILVER] = need.get(AtomType.QUICKSILVER, 0) + metal_need
                need.pop(metal, None)

    # Handle cardinals needed -> use Van Berlo or Salt
    total_cardinal_need = sum(need.get(c, 0) for c in
                              [AtomType.AIR, AtomType.EARTH, AtomType.FIRE, AtomType.WATER])
    if total_cardinal_need > 0:
        if puzzle.has_part(PartFlag.QUINTESSENCE_GLYPHS):
            # Use dispersion if we have quintessence surplus
            pass
        if puzzle.has_part(PartFlag.CALCIFICATION):
            # Check if we have cardinal surplus to convert to salt
            total_cardinal_surplus = sum(have_extra.get(c, 0) for c in
                                         [AtomType.AIR, AtomType.EARTH, AtomType.FIRE, AtomType.WATER])
            if total_cardinal_surplus > 0:
                calc_count = min(total_cardinal_surplus, need.get(AtomType.SALT, 0))
                if calc_count > 0:
                    recipe.reactions[Reaction.CALCIFICATION] = calc_count

    # Handle salt needed for conversions
    salt_need = need.get(AtomType.SALT, 0)
    salt_surplus = have_extra.get(AtomType.SALT, 0)
    if salt_need > salt_surplus:
        # Need more salt - use calcification
        if puzzle.has_part(PartFlag.CALCIFICATION):
            recipe.reactions[Reaction.CALCIFICATION] = \
                recipe.reactions.get(Reaction.CALCIFICATION, 0) + (salt_need - salt_surplus)

    # Handle Van Berlo for missing cardinals
    for cardinal in [AtomType.AIR, AtomType.EARTH, AtomType.FIRE, AtomType.WATER]:
        cn = need.get(cardinal, 0)
        cs = have_extra.get(cardinal, 0)
        if cn > cs and puzzle.has_part(PartFlag.VAN_BERLO):
            vb_count = cn - cs
            recipe.reactions[Reaction.VAN_BERLO] = \
                recipe.reactions.get(Reaction.VAN_BERLO, 0) + vb_count

    return recipe


def _calculate_min_cost(puzzle: Puzzle, analysis: PuzzleAnalysis) -> int:
    """Calculate theoretical minimum cost."""
    cost = 0

    # At least one arm
    cost += 20  # arm1

    # Glyphs from recipe
    if analysis.recipe:
        cost += analysis.recipe.glyph_cost

    # Bonding/unbonding
    if analysis.needs_bonding:
        cost += 10  # bonder
    if analysis.needs_unbonding:
        cost += 10  # unbonder

    return cost


def _calculate_min_cycles(puzzle: Puzzle, analysis: PuzzleAnalysis) -> int:
    """Calculate theoretical minimum cycles using N-D+L formula.

    N = number of input sets needed
    D = number of double-consume opportunities
    L = latency from final input to final output

    This is a simplified estimate - exact values require deeper analysis.
    """
    # N: input sets needed per output scale
    total_input_atoms = sum(pio.molecule.atom_count for pio in puzzle.inputs)
    total_output_atoms = sum(pio.molecule.atom_count for pio in puzzle.outputs)

    if total_input_atoms == 0:
        return 1

    # Simple estimate: N = output_scale * max ratio of any element
    n = puzzle.output_scale
    if analysis.recipe and analysis.recipe.reactions:
        # More inputs needed if transmutations consume extra atoms
        n = max(n, puzzle.output_scale)

    # D: double-consume opportunities (simplified - assume 0 for basic estimate)
    d = 0

    # L: latency (simplified)
    # At minimum: 1 cycle to grab + process + drop
    l = 1
    if analysis.recipe and analysis.recipe.reactions:
        # Each conversion glyph adds +1 latency
        l += len([r for r, c in analysis.recipe.reactions.items() if c > 0])

    return max(1, n - d + l)
