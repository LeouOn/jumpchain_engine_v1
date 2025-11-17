"""
State Manager - Handles all database persistence for Jumpchain Engine
"""

import sqlite3
import json
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

from .models import (
    JumperState, Perk, Companion, Item, WorldState,
    BackgroundEvent, Achievement
)


class StateManager:
    """Manages all game state persistence"""

    def __init__(self, db_path: str = "data/jumpchain.db"):
        """Initialize state manager with database connection"""
        self.db_path = db_path

        # Ensure data directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.init_database()

    def init_database(self):
        """Create all tables if they don't exist"""
        schema_path = Path(__file__).parent.parent.parent / "schema.sql"

        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        with open(schema_path, 'r') as f:
            schema = f.read()

        self.db.executescript(schema)
        self.db.commit()

    # ===== JUMPER OPERATIONS =====

    def save_jumper(self, jumper: JumperState):
        """Save jumper state"""
        self.db.execute("""
            INSERT OR REPLACE INTO jumper
            (id, name, age, current_jump, total_cp_earned, total_cp_spent,
             jump_count, current_year, current_day, current_location, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (jumper.id, jumper.name, jumper.age, jumper.current_jump,
              jumper.total_cp_earned, jumper.total_cp_spent,
              jumper.jump_count, jumper.current_year, jumper.current_day,
              jumper.current_location))
        self.db.commit()

    def load_jumper(self, jumper_id: int = 1) -> Optional[JumperState]:
        """Load jumper state"""
        row = self.db.execute(
            "SELECT * FROM jumper WHERE id = ?", (jumper_id,)
        ).fetchone()

        if not row:
            return None

        return JumperState(
            id=row['id'],
            name=row['name'],
            age=row['age'],
            current_jump=row['current_jump'],
            total_cp_earned=row['total_cp_earned'],
            total_cp_spent=row['total_cp_spent'],
            jump_count=row['jump_count'],
            current_year=row['current_year'],
            current_day=row['current_day'],
            current_location=row['current_location']
        )

    # ===== PERK OPERATIONS =====

    def save_perk(self, perk: Perk):
        """Save perk to database"""
        self.db.execute("""
            INSERT OR REPLACE INTO perks
            (id, owner_id, owner_type, name, source_jump, cp_cost,
             description, is_active, evolution_stage, synergy_tags, mechanics)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (perk.id if perk.id else None, perk.owner_id, perk.owner_type, perk.name,
              perk.source_jump, perk.cp_cost, perk.description,
              perk.is_active, perk.evolution_stage,
              json.dumps(perk.synergy_tags), json.dumps(perk.mechanics)))
        self.db.commit()

        # Get the inserted ID if this was a new perk
        if not perk.id:
            perk.id = self.db.execute("SELECT last_insert_rowid()").fetchone()[0]

    def get_active_perks(self, owner_id: int, owner_type: str) -> List[Perk]:
        """Get all active perks for an owner"""
        rows = self.db.execute("""
            SELECT * FROM perks
            WHERE owner_id = ? AND owner_type = ? AND is_active = 1
        """, (owner_id, owner_type)).fetchall()

        perks = []
        for row in rows:
            perks.append(Perk(
                id=row['id'],
                owner_id=row['owner_id'],
                owner_type=row['owner_type'],
                name=row['name'],
                source_jump=row['source_jump'],
                cp_cost=row['cp_cost'],
                description=row['description'],
                is_active=bool(row['is_active']),
                evolution_stage=row['evolution_stage'],
                synergy_tags=json.loads(row['synergy_tags']) if row['synergy_tags'] else [],
                mechanics=json.loads(row['mechanics']) if row['mechanics'] else {}
            ))

        return perks

    def get_all_perks(self, owner_id: int, owner_type: str) -> List[Perk]:
        """Get all perks (active and inactive) for an owner"""
        rows = self.db.execute("""
            SELECT * FROM perks
            WHERE owner_id = ? AND owner_type = ?
        """, (owner_id, owner_type)).fetchall()

        perks = []
        for row in rows:
            perks.append(Perk(
                id=row['id'],
                owner_id=row['owner_id'],
                owner_type=row['owner_type'],
                name=row['name'],
                source_jump=row['source_jump'],
                cp_cost=row['cp_cost'],
                description=row['description'],
                is_active=bool(row['is_active']),
                evolution_stage=row['evolution_stage'],
                synergy_tags=json.loads(row['synergy_tags']) if row['synergy_tags'] else [],
                mechanics=json.loads(row['mechanics']) if row['mechanics'] else {}
            ))

        return perks

    # ===== COMPANION OPERATIONS =====

    def save_companion(self, companion: Companion):
        """Save companion state"""
        self.db.execute("""
            INSERT OR REPLACE INTO companions
            (id, name, origin, source_jump, cp_budget, cp_spent,
             relationship_level, is_active, personality_profile, current_activity,
             traits, goals, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (companion.id if companion.id else None,
              companion.name, companion.origin,
              companion.source_jump, companion.cp_budget, companion.cp_spent,
              companion.relationship_level, companion.is_active,
              json.dumps(companion.personality_profile),
              companion.current_activity,
              json.dumps(companion.traits),
              json.dumps(companion.goals)))
        self.db.commit()

        # Get the inserted ID if this was a new companion
        if not companion.id:
            companion.id = self.db.execute("SELECT last_insert_rowid()").fetchone()[0]

        # Save companion's perks
        for perk in companion.perks:
            perk.owner_id = companion.id
            perk.owner_type = 'companion'
            self.save_perk(perk)

    def load_companions(self, active_only: bool = True) -> List[Companion]:
        """Load all companions"""
        query = "SELECT * FROM companions"
        if active_only:
            query += " WHERE is_active = 1"

        rows = self.db.execute(query).fetchall()

        companions = []
        for row in rows:
            companion = Companion(
                id=row['id'],
                name=row['name'],
                origin=row['origin'],
                source_jump=row['source_jump'],
                cp_budget=row['cp_budget'],
                cp_spent=row['cp_spent'],
                relationship_level=row['relationship_level'],
                is_active=bool(row['is_active']),
                personality_profile=json.loads(row['personality_profile']) if row['personality_profile'] else {},
                current_activity=row['current_activity'],
                traits=json.loads(row['traits']) if row['traits'] else {},
                goals=json.loads(row['goals']) if row['goals'] else []
            )

            # Load companion's perks
            companion.perks = self.get_active_perks(companion.id, 'companion')

            companions.append(companion)

        return companions

    def get_companion_by_name(self, name: str) -> Optional[Companion]:
        """Get companion by name"""
        row = self.db.execute(
            "SELECT * FROM companions WHERE name = ?", (name,)
        ).fetchone()

        if not row:
            return None

        companion = Companion(
            id=row['id'],
            name=row['name'],
            origin=row['origin'],
            source_jump=row['source_jump'],
            cp_budget=row['cp_budget'],
            cp_spent=row['cp_spent'],
            relationship_level=row['relationship_level'],
            is_active=bool(row['is_active']),
            personality_profile=json.loads(row['personality_profile']) if row['personality_profile'] else {},
            current_activity=row['current_activity'],
            traits=json.loads(row['traits']) if row['traits'] else {},
            goals=json.loads(row['goals']) if row['goals'] else []
        )

        companion.perks = self.get_active_perks(companion.id, 'companion')
        return companion

    # ===== WORLD STATE OPERATIONS =====

    def save_world_state(self, world: WorldState):
        """Save current world state"""
        self.db.execute("""
            INSERT OR REPLACE INTO world_state
            (id, jump_name, current_date, current_year, current_day,
             key_events, factions, known_characters, active_threats,
             completed_objectives, available_objectives, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (world.id if world.id else None,
              world.jump_name, world.current_date,
              world.current_year, world.current_day,
              json.dumps(world.key_events), json.dumps(world.factions),
              json.dumps(world.known_characters),
              json.dumps(world.active_threats),
              json.dumps(world.completed_objectives),
              json.dumps(world.available_objectives)))
        self.db.commit()

    def load_world_state(self, jump_name: str) -> Optional[WorldState]:
        """Load world state for current jump"""
        row = self.db.execute(
            "SELECT * FROM world_state WHERE jump_name = ?", (jump_name,)
        ).fetchone()

        if not row:
            return None

        return WorldState(
            id=row['id'],
            jump_name=row['jump_name'],
            current_date=row['current_date'],
            current_year=row['current_year'],
            current_day=row['current_day'],
            key_events=json.loads(row['key_events']) if row['key_events'] else [],
            factions=json.loads(row['factions']) if row['factions'] else {},
            known_characters=json.loads(row['known_characters']) if row['known_characters'] else {},
            active_threats=json.loads(row['active_threats']) if row['active_threats'] else [],
            completed_objectives=json.loads(row['completed_objectives']) if row['completed_objectives'] else [],
            available_objectives=json.loads(row['available_objectives']) if row['available_objectives'] else []
        )

    # ===== BACKGROUND EVENTS =====

    def log_background_event(self, event: BackgroundEvent):
        """Log a background event"""
        self.db.execute("""
            INSERT INTO background_events
            (turn_number, event_type, faction, description, impact_level,
             player_aware, resolution_deadline, consequences)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (event.turn_number, event.event_type, event.faction,
              event.description, event.impact_level, event.player_aware,
              event.resolution_deadline, json.dumps(event.consequences)))
        self.db.commit()

    def get_recent_events(self, limit: int = 10, turn_number: Optional[int] = None) -> List[BackgroundEvent]:
        """Get recent background events"""
        if turn_number:
            rows = self.db.execute("""
                SELECT * FROM background_events
                WHERE turn_number <= ?
                ORDER BY turn_number DESC LIMIT ?
            """, (turn_number, limit)).fetchall()
        else:
            rows = self.db.execute("""
                SELECT * FROM background_events
                ORDER BY turn_number DESC LIMIT ?
            """, (limit,)).fetchall()

        events = []
        for row in rows:
            events.append(BackgroundEvent(
                id=row['id'],
                turn_number=row['turn_number'],
                event_type=row['event_type'],
                faction=row['faction'],
                description=row['description'],
                impact_level=row['impact_level'],
                player_aware=bool(row['player_aware']),
                resolution_deadline=row['resolution_deadline'],
                consequences=json.loads(row['consequences']) if row['consequences'] else {}
            ))

        return events

    # ===== ACHIEVEMENTS =====

    def award_achievement(self, achievement: Achievement):
        """Award an achievement"""
        self.db.execute("""
            INSERT INTO rewards
            (name, type, trigger_condition, reward_value, earned_date, description, icon)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (achievement.name, achievement.tier, achievement.trigger_condition,
              achievement.reward_value,
              achievement.earned_date if isinstance(achievement.earned_date, str) else achievement.earned_date.isoformat(),
              achievement.description, achievement.icon))
        self.db.commit()

    def get_achievements(self, tier: Optional[str] = None) -> List[Achievement]:
        """Get all earned achievements"""
        if tier:
            rows = self.db.execute(
                "SELECT * FROM rewards WHERE type = ? ORDER BY earned_date DESC",
                (tier,)
            ).fetchall()
        else:
            rows = self.db.execute(
                "SELECT * FROM rewards ORDER BY earned_date DESC"
            ).fetchall()

        achievements = []
        for row in rows:
            achievements.append(Achievement(
                id=row['id'],
                name=row['name'],
                tier=row['type'],
                trigger_condition=row['trigger_condition'],
                reward_value=row['reward_value'],
                earned_date=row['earned_date'],
                description=row['description'],
                icon=row['icon'] or ""
            ))

        return achievements

    # ===== TURN MANAGEMENT =====

    def advance_turn(self) -> JumperState:
        """Advance game state by one turn (one day)"""
        jumper = self.load_jumper()
        if not jumper:
            raise ValueError("No jumper found in database")

        jumper.current_day += 1

        # Handle year transitions (assuming 365 days per year)
        if jumper.current_day > 365:
            jumper.current_day = 1
            jumper.current_year += 1

        self.save_jumper(jumper)
        return jumper

    def log_turn(self, turn_number: int, jump_name: str, player_action: str,
                 mechanical_result: Dict, narration: str, achievements: List[str]):
        """Log a turn for replay/analysis"""
        self.db.execute("""
            INSERT INTO turn_log
            (turn_number, jump_name, player_action, mechanical_result, narration, achievements_earned)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (turn_number, jump_name, player_action,
              json.dumps(mechanical_result), narration, json.dumps(achievements)))
        self.db.commit()

    def get_turn_count(self) -> int:
        """Get the current turn count"""
        result = self.db.execute("SELECT MAX(turn_number) as max_turn FROM turn_log").fetchone()
        return result['max_turn'] if result['max_turn'] else 0

    # ===== UTILITY =====

    def close(self):
        """Close database connection"""
        self.db.close()

    def backup(self, backup_path: str):
        """Create a backup of the database"""
        import shutil
        shutil.copy2(self.db_path, backup_path)
