"""
Data models for Jumpchain Engine
Defines core data structures used throughout the system
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class JumperState:
    """Core jumper character state"""
    id: int
    name: str
    age: int
    current_jump: str
    total_cp_earned: int
    total_cp_spent: int
    jump_count: int
    current_year: int
    current_day: int
    current_location: str

    # Derived fields
    available_cp: int = field(init=False)
    active_multipliers: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        self.available_cp = self.total_cp_earned - self.total_cp_spent


@dataclass
class Perk:
    """Individual perk/power"""
    id: int
    owner_id: int
    owner_type: str  # 'jumper' or 'companion'
    name: str
    source_jump: str
    cp_cost: int
    description: str
    is_active: bool
    evolution_stage: int
    synergy_tags: List[str]
    mechanics: Dict  # JSON: damage, range, cooldown, stats, etc.

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'owner_type': self.owner_type,
            'name': self.name,
            'source_jump': self.source_jump,
            'cp_cost': self.cp_cost,
            'description': self.description,
            'is_active': self.is_active,
            'evolution_stage': self.evolution_stage,
            'synergy_tags': self.synergy_tags,
            'mechanics': self.mechanics
        }


@dataclass
class Companion:
    """Companion character"""
    id: int
    name: str
    origin: str
    source_jump: str
    cp_budget: int
    cp_spent: int
    relationship_level: int  # 1-10
    is_active: bool
    personality_profile: Dict
    current_activity: str
    perks: List[Perk] = field(default_factory=list)
    items: List['Item'] = field(default_factory=list)

    # Personality traits for AI generation
    traits: Dict[str, int] = field(default_factory=dict)
    goals: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'origin': self.origin,
            'source_jump': self.source_jump,
            'cp_budget': self.cp_budget,
            'cp_spent': self.cp_spent,
            'relationship_level': self.relationship_level,
            'is_active': self.is_active,
            'personality_profile': self.personality_profile,
            'current_activity': self.current_activity,
            'traits': self.traits,
            'goals': self.goals
        }


@dataclass
class Item:
    """Item/equipment"""
    id: int
    owner_id: int
    owner_type: str
    name: str
    source_jump: str
    cp_cost: int
    description: str
    quantity: int
    is_equipped: bool
    properties: Dict


@dataclass
class WorldState:
    """Current jump world state"""
    id: int
    jump_name: str
    current_date: str
    current_year: int
    current_day: int
    key_events: List[Dict]
    factions: Dict[str, Dict]
    known_characters: Dict[str, Dict]
    active_threats: List[Dict]
    completed_objectives: List[str]
    available_objectives: List[Dict]

    def get_active_crisis(self) -> List[Dict]:
        """Return threats requiring immediate attention"""
        return [t for t in self.active_threats if t.get('urgency', 0) >= 8]

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'jump_name': self.jump_name,
            'current_date': self.current_date,
            'current_year': self.current_year,
            'current_day': self.current_day,
            'key_events': self.key_events,
            'factions': self.factions,
            'known_characters': self.known_characters,
            'active_threats': self.active_threats,
            'completed_objectives': self.completed_objectives,
            'available_objectives': self.available_objectives
        }


@dataclass
class BackgroundEvent:
    """Off-screen event that occurred"""
    id: int
    turn_number: int
    event_type: str  # 'faction_action', 'npc_action', 'natural', 'opportunity', 'crisis'
    faction: Optional[str]
    description: str
    impact_level: int  # 1-10
    player_aware: bool
    resolution_deadline: Optional[str]
    consequences: Dict

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'turn_number': self.turn_number,
            'event_type': self.event_type,
            'faction': self.faction,
            'description': self.description,
            'impact_level': self.impact_level,
            'player_aware': self.player_aware,
            'resolution_deadline': self.resolution_deadline,
            'consequences': self.consequences
        }


@dataclass
class Achievement:
    """Gamification reward"""
    id: int
    name: str
    tier: str  # bronze, silver, gold, platinum
    trigger_condition: str
    reward_value: float  # CP multiplier or bonus
    earned_date: datetime
    description: str
    icon: str = ""

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'tier': self.tier,
            'trigger_condition': self.trigger_condition,
            'reward_value': self.reward_value,
            'earned_date': self.earned_date.isoformat() if isinstance(self.earned_date, datetime) else self.earned_date,
            'description': self.description,
            'icon': self.icon
        }


@dataclass
class PowerSynergy:
    """Detected synergy between powers"""
    perks: List[str]
    multiplier: float
    description: str
    suggested_use: str
    combo_type: str  # 'offensive', 'defensive', 'utility', 'broken'


@dataclass
class CPBudget:
    """CP budget calculation result"""
    base_cp: int
    drawback_cp: int
    companion_cp: int
    achievement_bonus: int
    multipliers: Dict[str, float]
    total_available: int


@dataclass
class FactionState:
    """Current state of a faction"""
    name: str
    resources: int  # 0-100
    morale: int  # 0-100
    military_power: int  # 0-100
    territory: List[str]
    goals: List[str]
    recent_actions: List[str]
    relationship_with_player: int  # -100 to +100


@dataclass
class NPCState:
    """Current state of an NPC"""
    name: str
    location: str
    status: str  # alive, captured, injured, deceased, etc.
    loyalty: int  # -100 to +100 (to player)
    current_goal: str
    aware_of_player: bool
    power_level: int  # 1-10
