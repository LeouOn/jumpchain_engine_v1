"""
Calculation Engine - Handles all mechanical calculations
Includes CP budgets, power synergies, combat calculations, and build optimization
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import logging

from ..core.models import Perk, Companion, PowerSynergy, CPBudget

logger = logging.getLogger(__name__)


class CalculationEngine:
    """Handles all mechanical calculations for the game"""

    def __init__(self, llm_endpoint: Optional[str] = None):
        """
        Initialize calculation engine

        Args:
            llm_endpoint: Optional DeepSeek-R1 endpoint for complex calculations
        """
        self.llm_endpoint = llm_endpoint

        # Known synergy database
        # Format: (perk1, perk2): {multiplier, description, combo_type}
        self.known_synergies = {
            ('PtV', 'Blank'): {
                'multiplier': 15.0,
                'description': 'PtV can plot against precogs who cannot see you',
                'combo_type': 'broken',
                'suggestion': 'Infiltrate any precog-defended location with perfect success'
            },
            ('Path to Victory', 'Blank'): {
                'multiplier': 15.0,
                'description': 'PtV can plot against precogs who cannot see you',
                'combo_type': 'broken',
                'suggestion': 'Infiltrate any precog-defended location with perfect success'
            },
            ('PtV', 'Compassionate Transmutation'): {
                'multiplier': 10.0,
                'description': 'PtV tells you exactly what to create for optimal outcomes',
                'combo_type': 'broken',
                'suggestion': 'Create perfect solutions to any problem'
            },
            ('Path to Victory', 'Compassionate Transmutation'): {
                'multiplier': 10.0,
                'description': 'PtV tells you exactly what to create for optimal outcomes',
                'combo_type': 'broken',
                'suggestion': 'Create perfect solutions to any problem'
            },
            ('Team Lead', 'Power Sharing'): {
                'multiplier': 6.0,
                'description': 'Entire team shares all powers',
                'combo_type': 'broken',
                'suggestion': 'Give entire team your strongest abilities'
            },
            ('I Will Save Them All', 'Promise of Tomorrow'): {
                'multiplier': 20.0,
                'description': 'Ultimate protection combo - time loop + power boost',
                'combo_type': 'broken',
                'suggestion': 'Ensure perfect outcomes through iterative time loops'
            },
            ('Tinker', 'Resource Creation'): {
                'multiplier': 5.0,
                'description': 'Unlimited materials for tinker tech',
                'combo_type': 'utility',
                'suggestion': 'Build unlimited tinker devices without resource constraints'
            },
            ('Precognition', 'Time Stop'): {
                'multiplier': 8.0,
                'description': 'See the future and have infinite time to act on it',
                'combo_type': 'broken',
                'suggestion': 'Perfect planning with unlimited execution time'
            }
        }

        # Tag-based synergy rules
        self.tag_synergies = {
            ('precog', 'stealth'): {
                'multiplier': 3.0,
                'description': 'Know where guards will be + invisibility = perfect infiltration',
                'combo_type': 'utility'
            },
            ('time', 'combat'): {
                'multiplier': 5.0,
                'description': 'Time manipulation + enhanced combat = speedblitz',
                'combo_type': 'offensive'
            },
            ('healing', 'immortality'): {
                'multiplier': 4.0,
                'description': 'Cannot die + rapid healing = true invulnerability',
                'combo_type': 'defensive'
            },
            ('mind_control', 'telepathy'): {
                'multiplier': 6.0,
                'description': 'Read minds and control them = undetectable manipulation',
                'combo_type': 'utility'
            },
            ('creation', 'transmutation'): {
                'multiplier': 4.0,
                'description': 'Create anything and transform it further',
                'combo_type': 'utility'
            },
            ('precog', 'combat'): {
                'multiplier': 4.0,
                'description': 'See enemy attacks before they happen',
                'combo_type': 'offensive'
            }
        }

    def calculate_cp_budget(self,
                           base_cp: int,
                           drawbacks: List[Dict],
                           companions: List[Companion],
                           achievements: List) -> CPBudget:
        """
        Calculate total available CP for the jump

        Args:
            base_cp: Base CP for the jump (usually 1000)
            drawbacks: List of active drawbacks with cp_value
            companions: List of companions (each gets their own budget)
            achievements: Earned achievements that provide bonuses

        Returns:
            CPBudget object with breakdown
        """
        # Calculate drawback CP
        drawback_cp = sum(d.get('cp_value', 0) for d in drawbacks)

        # Companion CP is separate per companion
        companion_cp = sum(c.cp_budget for c in companions)

        # Achievement bonuses
        achievement_bonus = 0
        multipliers = {}

        for ach in achievements:
            tier = ach.tier
            value = ach.reward_value

            if tier == 'bronze':
                # Bronze gives flat bonus (usually 5%)
                achievement_bonus += int(base_cp * (value - 1.0) if value > 1 else value)
            elif tier == 'silver':
                # Silver gives 10% bonus
                achievement_bonus += int(base_cp * (value - 1.0) if value > 1 else value)
            elif tier == 'gold':
                # Gold gives multiplier
                multipliers['gold'] = multipliers.get('gold', 1.0) * value
            elif tier == 'platinum':
                # Platinum gives larger multiplier
                multipliers['platinum'] = multipliers.get('platinum', 1.0) * value

        # Calculate total multiplier
        total_multiplier = 1.0
        for m in multipliers.values():
            total_multiplier *= m

        # Total available for jumper (not including companion CP)
        jumper_total = int((base_cp + drawback_cp + achievement_bonus) * total_multiplier)

        logger.info(f"CP Budget: base={base_cp}, drawbacks=+{drawback_cp}, "
                   f"achievements=+{achievement_bonus}, multiplier={total_multiplier:.2f}x, "
                   f"total={jumper_total}")

        return CPBudget(
            base_cp=base_cp,
            drawback_cp=drawback_cp,
            companion_cp=companion_cp,
            achievement_bonus=achievement_bonus,
            multipliers=multipliers,
            total_available=jumper_total
        )

    def detect_synergies(self, active_perks: List[Perk]) -> List[PowerSynergy]:
        """
        Detect power synergies between perks

        Args:
            active_perks: List of active perks

        Returns:
            List of detected synergies
        """
        synergies = []

        # Check known perk name synergies
        for i, perk1 in enumerate(active_perks):
            for perk2 in active_perks[i + 1:]:
                # Try both orderings
                for key in [
                    (perk1.name, perk2.name),
                    (perk2.name, perk1.name),
                    tuple(sorted([perk1.name, perk2.name]))
                ]:
                    if key in self.known_synergies:
                        syn_data = self.known_synergies[key]
                        synergies.append(PowerSynergy(
                            perks=[perk1.name, perk2.name],
                            multiplier=syn_data['multiplier'],
                            description=syn_data['description'],
                            suggested_use=syn_data.get('suggestion',
                                f"Combine {perk1.name} and {perk2.name}"),
                            combo_type=syn_data['combo_type']
                        ))
                        break  # Don't add duplicates

        # Tag-based synergies
        tag_syns = self._detect_tag_synergies(active_perks)
        synergies.extend(tag_syns)

        # Remove duplicates
        seen = set()
        unique_synergies = []
        for syn in synergies:
            key = tuple(sorted(syn.perks))
            if key not in seen:
                seen.add(key)
                unique_synergies.append(syn)

        logger.info(f"Detected {len(unique_synergies)} synergies from {len(active_perks)} perks")

        return unique_synergies

    def _detect_tag_synergies(self, perks: List[Perk]) -> List[PowerSynergy]:
        """Detect synergies based on synergy tags"""
        synergies = []

        # Build tag index
        tag_to_perks = {}
        for perk in perks:
            for tag in perk.synergy_tags:
                if tag not in tag_to_perks:
                    tag_to_perks[tag] = []
                tag_to_perks[tag].append(perk)

        # Check tag combinations
        for (tag1, tag2), syn_data in self.tag_synergies.items():
            if tag1 in tag_to_perks and tag2 in tag_to_perks:
                # Found perks with both tags
                perk1 = tag_to_perks[tag1][0]  # Take first match
                perk2 = tag_to_perks[tag2][0]

                # Don't create synergy with self
                if perk1.id == perk2.id:
                    continue

                synergies.append(PowerSynergy(
                    perks=[perk1.name, perk2.name],
                    multiplier=syn_data['multiplier'],
                    description=syn_data['description'],
                    suggested_use=f"Use {tag1} and {tag2} together",
                    combo_type=syn_data['combo_type']
                ))

        return synergies

    def calculate_combat_power(self,
                               perks: List[Perk],
                               items: List = None,
                               buffs: List[Dict] = None) -> Dict:
        """
        Calculate effective combat statistics

        Args:
            perks: Active perks
            items: Equipped items
            buffs: Temporary buffs

        Returns:
            Dict with stats, synergies, power_level, threat_rating
        """
        if items is None:
            items = []
        if buffs is None:
            buffs = []

        base_stats = {
            'physical': 1.0,    # Human baseline
            'mental': 1.0,
            'speed': 1.0,
            'durability': 1.0,
            'energy': 1.0,
            'special': 1.0      # Esoteric abilities
        }

        # Apply perk bonuses
        for perk in perks:
            if not perk.is_active:
                continue

            mechanics = perk.mechanics
            for stat in base_stats:
                if stat in mechanics:
                    multiplier = mechanics[stat]
                    base_stats[stat] *= multiplier

        # Apply item bonuses
        for item in items:
            if hasattr(item, 'is_equipped') and item.is_equipped:
                if hasattr(item, 'properties') and 'stats' in item.properties:
                    for stat, value in item.properties['stats'].items():
                        if stat in base_stats:
                            base_stats[stat] *= value

        # Apply temporary buffs
        for buff in buffs:
            for stat, value in buff.items():
                if stat in base_stats:
                    base_stats[stat] *= value

        # Calculate synergies
        synergies = self.detect_synergies(perks)

        # Apply maximum synergy multiplier to all stats
        max_multiplier = max([s.multiplier for s in synergies], default=1.0)
        for stat in base_stats:
            base_stats[stat] *= max_multiplier

        return {
            'stats': base_stats,
            'synergies': synergies,
            'power_level': self._estimate_power_level(base_stats),
            'threat_rating': self._calculate_threat_rating(base_stats, synergies)
        }

    def _estimate_power_level(self, stats: Dict) -> str:
        """Estimate overall power level"""
        avg_stat = sum(stats.values()) / len(stats)

        if avg_stat < 2:
            return "Street Tier"
        elif avg_stat < 10:
            return "City Tier"
        elif avg_stat < 100:
            return "Country Tier"
        elif avg_stat < 1000:
            return "Planet Tier"
        elif avg_stat < 10000:
            return "Cosmic Tier"
        else:
            return "Multiversal Tier"

    def _calculate_threat_rating(self, stats: Dict, synergies: List[PowerSynergy]) -> int:
        """Calculate PRT-style threat rating (1-10+)"""
        avg_stat = sum(stats.values()) / len(stats)

        # Base rating from stats
        base_rating = min(10, int(avg_stat / 10))

        # Synergy bonus
        synergy_bonus = len([s for s in synergies if s.combo_type == 'broken']) * 2
        synergy_bonus += len([s for s in synergies if s.combo_type == 'offensive'])

        total_rating = min(10, base_rating + synergy_bonus)

        return total_rating

    def check_perk_conflicts(self,
                            new_perk: Perk,
                            existing_perks: List[Perk]) -> Dict:
        """
        Check for conflicts or redundancies when adding a perk

        Args:
            new_perk: Perk to check
            existing_perks: Currently owned perks

        Returns:
            Dict with conflicts, redundancies, safe_to_add
        """
        conflicts = []
        redundancies = []

        for perk in existing_perks:
            # Check for direct conflicts
            if self._are_conflicting(new_perk, perk):
                conflicts.append({
                    'perk': perk.name,
                    'reason': 'Powers cannot coexist (incompatible mechanics)'
                })

            # Check for redundancy
            if self._is_redundant(new_perk, perk):
                redundancies.append({
                    'perk': perk.name,
                    'reason': 'Provides similar capabilities'
                })

        return {
            'conflicts': conflicts,
            'redundancies': redundancies,
            'safe_to_add': len(conflicts) == 0,
            'warnings': redundancies
        }

    def _are_conflicting(self, perk1: Perk, perk2: Perk) -> bool:
        """Check if two perks conflict"""
        # Define conflicting tag pairs
        conflict_pairs = [
            (['immortal', 'undying', 'invulnerable'], ['mortal', 'fragile', 'temporary']),
            (['pacifist'], ['berserker', 'bloodlust', 'killer']),
            (['mute'], ['telepathy', 'persuasion', 'voice']),
            (['blind'], ['vision', 'sight', 'eye'])
        ]

        tags1 = set(perk1.synergy_tags)
        tags2 = set(perk2.synergy_tags)

        for group1, group2 in conflict_pairs:
            if (any(t in tags1 for t in group1) and
                any(t in tags2 for t in group2)):
                return True
            if (any(t in tags2 for t in group1) and
                any(t in tags1 for t in group2)):
                return True

        return False

    def _is_redundant(self, perk1: Perk, perk2: Perk) -> bool:
        """Check if perks provide redundant capabilities"""
        tags1 = set(perk1.synergy_tags)
        tags2 = set(perk2.synergy_tags)

        # Significant overlap = likely redundant
        overlap = len(tags1 & tags2)
        return overlap >= 3  # 3+ shared tags

    def optimize_build(self,
                      available_cp: int,
                      available_perks: List[Perk],
                      objectives: List[str],
                      constraints: Dict = None) -> Dict:
        """
        Suggest optimal perk selection for given objectives

        Args:
            available_cp: CP available to spend
            available_perks: Perks available in this jump
            objectives: Player's stated objectives
            constraints: Optional constraints (max_cost, required_tags, etc.)

        Returns:
            Dict with selected_perks, total_cost, remaining_cp, synergies, power
        """
        if constraints is None:
            constraints = {}

        # Simple greedy algorithm
        # TODO: Could use LLM (DeepSeek-R1) for more sophisticated optimization

        selected_perks = []
        remaining_cp = available_cp

        # Score perks by value
        scored_perks = []
        for perk in available_perks:
            score = self._score_perk(perk, objectives, constraints)
            scored_perks.append((score, perk))

        # Sort by score descending
        scored_perks.sort(reverse=True, key=lambda x: x[0])

        # Greedy selection
        for score, perk in scored_perks:
            if perk.cp_cost <= remaining_cp:
                # Check conflicts
                conflicts = self.check_perk_conflicts(perk, selected_perks)
                if conflicts['safe_to_add']:
                    selected_perks.append(perk)
                    remaining_cp -= perk.cp_cost

        # Calculate synergies and power
        synergies = self.detect_synergies(selected_perks)
        power = self.calculate_combat_power(selected_perks, [], [])

        return {
            'selected_perks': selected_perks,
            'total_cost': available_cp - remaining_cp,
            'remaining_cp': remaining_cp,
            'synergies': synergies,
            'estimated_power': power,
            'efficiency': (available_cp - remaining_cp) / available_cp if available_cp > 0 else 0
        }

    def _score_perk(self, perk: Perk, objectives: List[str], constraints: Dict) -> float:
        """Score a perk based on objectives and constraints"""
        base_score = 1.0

        # Match objectives
        objectives_lower = [obj.lower() for obj in objectives]
        for tag in perk.synergy_tags:
            for obj in objectives_lower:
                if tag in obj or obj in tag:
                    base_score += 2.0

        # Check description match
        if perk.description:
            desc_lower = perk.description.lower()
            for obj in objectives_lower:
                if obj in desc_lower:
                    base_score += 1.0

        # Penalize expensive perks
        cost_penalty = perk.cp_cost / 1000.0

        # Required tags bonus
        if 'required_tags' in constraints:
            for tag in constraints['required_tags']:
                if tag in perk.synergy_tags:
                    base_score += 5.0

        return base_score / (1 + cost_penalty)

    def suggest_synergies_for_objective(self,
                                       objective: str,
                                       available_perks: List[Perk]) -> List[Dict]:
        """
        Suggest perk combinations that would help achieve an objective

        Args:
            objective: Player's goal
            available_perks: Perks available to choose from

        Returns:
            List of suggested combinations with reasoning
        """
        suggestions = []

        # Analyze objective
        obj_lower = objective.lower()

        # Common objective patterns
        patterns = {
            'combat': ['combat', 'fight', 'defeat', 'attack', 'battle'],
            'stealth': ['stealth', 'infiltrate', 'sneak', 'hidden', 'spy'],
            'social': ['convince', 'persuade', 'negotiate', 'allies', 'friends'],
            'intelligence': ['learn', 'understand', 'analyze', 'study', 'research'],
            'survival': ['survive', 'protect', 'defend', 'safe', 'immortal'],
            'creation': ['build', 'create', 'make', 'craft', 'tinker']
        }

        # Find matching category
        matching_categories = []
        for category, keywords in patterns.items():
            if any(keyword in obj_lower for keyword in keywords):
                matching_categories.append(category)

        # Find perks for each category
        for category in matching_categories:
            category_perks = [p for p in available_perks
                            if category in p.synergy_tags or
                            any(keyword in p.description.lower()
                                for keyword in patterns[category])]

            if len(category_perks) >= 2:
                # Suggest top 2 perks
                scored = [(self._score_perk(p, [objective], {}), p)
                         for p in category_perks]
                scored.sort(reverse=True)

                suggestions.append({
                    'category': category,
                    'perks': [p.name for _, p in scored[:2]],
                    'reasoning': f"Best {category} perks for: {objective}",
                    'total_cost': sum(p.cp_cost for _, p in scored[:2])
                })

        return suggestions
