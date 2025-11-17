"""
Turn Orchestrator - Main game loop coordinator
Coordinates all modules: calculation, narration, background sim, companion AI
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

from .state_manager import StateManager
from .config import get_config
from .models import BackgroundEvent, Achievement
from ..engines.calculation import CalculationEngine

logger = logging.getLogger(__name__)


class TurnOrchestrator:
    """Main game loop orchestrator"""

    def __init__(self, state_manager: Optional[StateManager] = None):
        """
        Initialize orchestrator

        Args:
            state_manager: StateManager instance (creates new if None)
        """
        self.config = get_config()
        self.state_manager = state_manager or StateManager()
        self.calculation_engine = CalculationEngine()

        # Turn counter
        self.current_turn = self.state_manager.get_turn_count()

        logger.info(f"TurnOrchestrator initialized at turn {self.current_turn}")

    def process_turn(self, player_input: str) -> Dict:
        """
        Process a complete turn

        Main game loop that:
        1. Parses player input
        2. Calculates mechanical effects
        3. Generates background events (TODO: Phase 3)
        4. Updates companion states (TODO: Phase 3)
        5. Checks for achievements
        6. Generates narration (TODO: Phase 3)
        7. Updates database
        8. Returns formatted response

        Args:
            player_input: Player's action/command

        Returns:
            Dict with narration, achievements, companion_responses, etc.
        """
        self.current_turn += 1
        logger.info(f"Processing turn {self.current_turn}: {player_input[:50]}...")

        # Load current state
        jumper = self.state_manager.load_jumper()
        if not jumper:
            raise ValueError("No jumper found. Please create a character first.")

        companions = self.state_manager.load_companions()
        world_state = self.state_manager.load_world_state(jumper.current_jump)

        # Step 1: Parse action
        action = self._parse_action(player_input)

        # Step 2: Calculate mechanical effects
        mechanics = self._calculate_mechanics(action, jumper)

        # Step 3: Generate background events (stub for now - Phase 3)
        background_events = self._generate_background_events(world_state, action)

        # Step 4: Update companion states (stub for now - Phase 3)
        companion_responses = self._update_companions(companions, action, mechanics)

        # Step 5: Check achievements
        achievements = self._check_achievements(action, mechanics, jumper)

        # Step 6: Build context for narration
        narrative_context = {
            'action': action,
            'mechanics': mechanics,
            'background': background_events,
            'companions': companion_responses,
            'achievements': achievements,
            'jumper': jumper,
            'world_state': world_state,
            'turn': self.current_turn
        }

        # Step 7: Generate narration (stub for now - Phase 3)
        narration = self._generate_narration(narrative_context)

        # Step 8: Update database
        self._commit_turn(
            action=action,
            mechanics=mechanics,
            narration=narration,
            achievements=achievements,
            jumper=jumper
        )

        # Step 9: Format response
        return self._format_response(
            narration=narration,
            mechanics=mechanics,
            achievements=achievements,
            companion_responses=companion_responses,
            background_events=background_events
        )

    def _parse_action(self, player_input: str) -> Dict:
        """Parse player input into structured action"""
        # Simple parsing for now
        # TODO: Could use LLM for better parsing in Phase 3

        action = {
            'raw_input': player_input,
            'action_type': 'general',
            'perks_mentioned': [],
            'targets': [],
            'objectives': []
        }

        # Detect action type
        input_lower = player_input.lower()

        if any(word in input_lower for word in ['attack', 'fight', 'combat', 'battle']):
            action['action_type'] = 'combat'
        elif any(word in input_lower for word in ['infiltrate', 'sneak', 'stealth']):
            action['action_type'] = 'stealth'
        elif any(word in input_lower for word in ['talk', 'convince', 'persuade', 'negotiate']):
            action['action_type'] = 'social'
        elif any(word in input_lower for word in ['use', 'activate', 'trigger']):
            action['action_type'] = 'power_use'
        elif any(word in input_lower for word in ['investigate', 'search', 'analyze']):
            action['action_type'] = 'investigation'

        return action

    def _calculate_mechanics(self, action: Dict, jumper) -> Dict:
        """Calculate mechanical effects of action"""
        # Get jumper's active perks
        perks = self.state_manager.get_active_perks(jumper.id, 'jumper')

        # Calculate combat power
        power = self.calculation_engine.calculate_combat_power(perks, [], [])

        # Detect synergies
        synergies = self.calculation_engine.detect_synergies(perks)

        # Build mechanics result
        mechanics = {
            'power_stats': power['stats'],
            'power_level': power['power_level'],
            'threat_rating': power['threat_rating'],
            'synergies_active': synergies,
            'success_probability': self._estimate_success(action, power),
            'perks_used': [p.name for p in perks if p.is_active]
        }

        # Check if action mentions specific perks
        for perk in perks:
            if perk.name.lower() in action['raw_input'].lower():
                if perk.name not in mechanics['perks_used']:
                    mechanics['perks_used'].append(perk.name)

        logger.info(f"Mechanics: {power['power_level']}, {len(synergies)} synergies, "
                   f"{mechanics['success_probability']:.0%} success chance")

        return mechanics

    def _estimate_success(self, action: Dict, power: Dict) -> float:
        """Estimate probability of action success"""
        # Base success rate
        base_rate = 0.5

        # Modify based on power level
        power_level = power['power_level']
        if power_level == "Street Tier":
            modifier = 0.0
        elif power_level == "City Tier":
            modifier = 0.1
        elif power_level == "Country Tier":
            modifier = 0.2
        elif power_level == "Planet Tier":
            modifier = 0.3
        else:
            modifier = 0.4

        # Modify based on synergies
        synergy_count = len(power.get('synergies', []))
        synergy_modifier = min(0.2, synergy_count * 0.05)

        total = min(0.95, base_rate + modifier + synergy_modifier)
        return total

    def _generate_background_events(self, world_state, action: Dict) -> List[BackgroundEvent]:
        """
        Generate background events (stub for Phase 3)

        TODO: Implement BackgroundSimulator in Phase 3
        """
        # For now, return empty list
        # In Phase 3, this will call BackgroundSimulator

        if not self.config.get('background_simulation', 'enabled', default=True):
            return []

        # Stub: Create a simple event
        events = []

        # Simple reaction to player action
        if action['action_type'] == 'combat':
            events.append(BackgroundEvent(
                id=0,
                turn_number=self.current_turn,
                event_type='reaction',
                faction=None,
                description='Word of your combat prowess spreads',
                impact_level=3,
                player_aware=False,
                resolution_deadline=None,
                consequences={'reputation': 'increased'}
            ))

        return events

    def _update_companions(self, companions: List, action: Dict, mechanics: Dict) -> List[Dict]:
        """
        Update companion states and generate responses (stub for Phase 3)

        TODO: Implement CompanionAI in Phase 3
        """
        responses = []

        if not self.config.get('companion_ai', 'enabled', default=True):
            return responses

        # Stub: Simple responses
        for companion in companions[:2]:  # First 2 companions
            response = {
                'companion_name': companion.name,
                'dialogue': f"{companion.name} observes your actions.",
                'action': None,
                'relationship_change': 0
            }
            responses.append(response)

        return responses

    def _check_achievements(self, action: Dict, mechanics: Dict, jumper) -> List[Achievement]:
        """Check for newly earned achievements"""
        achievements = []

        # Get all achievement configs
        ach_configs = self.config.get_all_achievements()

        # Check each achievement
        for ach_config in ach_configs:
            if self._check_achievement_trigger(ach_config, action, mechanics, jumper):
                # Create achievement
                achievement = Achievement(
                    id=0,
                    name=ach_config['name'],
                    tier=ach_config['tier'],
                    trigger_condition=ach_config['trigger'],
                    reward_value=ach_config['reward_value'],
                    earned_date=datetime.now(),
                    description=ach_config['description'],
                    icon=ach_config.get('icon', '')
                )

                # Save to database
                self.state_manager.award_achievement(achievement)
                achievements.append(achievement)

                logger.info(f"Achievement unlocked: {achievement.name} ({achievement.tier})")

        return achievements

    def _check_achievement_trigger(self, ach_config: Dict, action: Dict,
                                   mechanics: Dict, jumper) -> bool:
        """Check if achievement conditions are met"""
        trigger = ach_config['trigger']
        condition = ach_config.get('condition', {})

        # Check if already earned
        existing = self.state_manager.get_achievements()
        if any(a.name == ach_config['name'] for a in existing):
            return False

        # Simple trigger checks
        if trigger == 'complete_first_turn':
            return self.current_turn == 1

        elif trigger == 'use_multiple_perks_creatively':
            # Check if using 3+ perks
            perks_used = mechanics.get('perks_used', [])
            synergies = mechanics.get('synergies_active', [])
            return len(perks_used) >= 3 and len(synergies) > 0

        elif trigger == 'unexpected_solution':
            # Difficult to detect automatically - placeholder
            # Could use LLM analysis in Phase 3
            return False

        # Add more trigger checks as needed
        return False

    def _generate_narration(self, context: Dict) -> str:
        """
        Generate main story narration (stub for Phase 3)

        TODO: Integrate Claude Sonnet 4.5 in Phase 3
        """
        # For now, return simple narration
        action = context['action']
        mechanics = context['mechanics']

        narration = f"You attempt to {action['raw_input']}.\n\n"

        # Add power description
        narration += f"Your current power level: {mechanics['power_level']}.\n"

        # Add synergies
        synergies = mechanics.get('synergies_active', [])
        if synergies:
            narration += f"\nActive synergies detected:\n"
            for syn in synergies[:3]:  # Top 3
                narration += f"  • {' + '.join(syn.perks)} ({syn.multiplier}x): {syn.description}\n"

        # Success estimate
        success_prob = mechanics.get('success_probability', 0.5)
        if success_prob > 0.8:
            narration += "\nYour chances of success look excellent."
        elif success_prob > 0.6:
            narration += "\nYou have a good chance of success."
        elif success_prob > 0.4:
            narration += "\nThe outcome is uncertain."
        else:
            narration += "\nThis will be challenging."

        # Placeholder for actual narration
        narration += "\n\n[Full narration will be generated by Claude in Phase 3]"

        return narration

    def _commit_turn(self, action: Dict, mechanics: Dict, narration: str,
                    achievements: List, jumper):
        """Commit turn to database"""
        # Log turn
        self.state_manager.log_turn(
            turn_number=self.current_turn,
            jump_name=jumper.current_jump,
            player_action=action['raw_input'],
            mechanical_result=mechanics,
            narration=narration,
            achievements=[a.name for a in achievements]
        )

        # Advance time
        self.state_manager.advance_turn()

        # Auto-backup if configured
        if self.config.get('database', 'auto_backup', default=True):
            backup_interval = self.config.get('database', 'backup_interval', default=10)
            if self.current_turn % backup_interval == 0:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"data/jumpchain_backup_{timestamp}.db"
                self.state_manager.backup(backup_path)
                logger.info(f"Auto-backup created: {backup_path}")

    def _format_response(self, narration: str, mechanics: Dict,
                        achievements: List, companion_responses: List,
                        background_events: List) -> Dict:
        """Format turn result for display"""
        response = {
            'narration': narration,
            'mechanics': mechanics if self.config.get('narration', 'show_mechanics', default=False) else None,
            'achievements': [
                {
                    'name': a.name,
                    'tier': a.tier,
                    'description': a.description,
                    'icon': a.icon
                }
                for a in achievements
            ],
            'companion_responses': companion_responses,
            'background_events': [
                {
                    'description': e.description,
                    'impact_level': e.impact_level
                }
                for e in background_events if e.player_aware
            ],
            'turn_number': self.current_turn
        }

        return response

    def get_game_summary(self) -> Dict:
        """Get current game state summary"""
        jumper = self.state_manager.load_jumper()
        companions = self.state_manager.load_companions()
        perks = self.state_manager.get_active_perks(jumper.id, 'jumper')
        achievements = self.state_manager.get_achievements()

        # Calculate power
        power = self.calculation_engine.calculate_combat_power(perks, [], [])

        return {
            'jumper': {
                'name': jumper.name,
                'current_jump': jumper.current_jump,
                'location': jumper.current_location,
                'day': jumper.current_day,
                'year': jumper.current_year,
                'cp_available': jumper.available_cp
            },
            'companions': len(companions),
            'active_perks': len(perks),
            'power_level': power['power_level'],
            'threat_rating': power['threat_rating'],
            'achievements': len(achievements),
            'turn': self.current_turn
        }
