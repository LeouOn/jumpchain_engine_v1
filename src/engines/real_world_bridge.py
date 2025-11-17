"""
Real World Achievement Bridge
Connect in-game achievements to actual practices and growth
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json


@dataclass
class RealWorldPractice:
    """A real-world practice that bridges to game rewards"""

    # Identity
    practice_id: str
    practice_name: str
    category: str  # meditation, exercise, shadow_work, creative, service

    # Practice details
    description: str
    duration_minutes: int
    frequency: str  # daily, weekly, etc.
    difficulty: int  # 1-10

    # Game integration
    game_achievement_name: str
    cp_reward: int
    in_game_perk_unlock: Optional[str] = None
    stat_bonuses: Dict[str, int] = field(default_factory=dict)

    # Real benefits
    real_world_benefits: str
    spiritual_reward: str

    # Progress tracking
    sessions_completed: int = 0
    total_minutes: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    last_completed: Optional[datetime] = None

    # Verification
    verification_method: str = "honor_system"  # honor_system, journal_entry, photo
    journal_prompts: List[str] = field(default_factory=list)

    # Completion tracking
    is_complete: bool = False
    completion_date: Optional[datetime] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'practice_id': self.practice_id,
            'practice_name': self.practice_name,
            'category': self.category,
            'description': self.description,
            'duration_minutes': self.duration_minutes,
            'frequency': self.frequency,
            'difficulty': self.difficulty,
            'game_achievement_name': self.game_achievement_name,
            'cp_reward': self.cp_reward,
            'in_game_perk_unlock': self.in_game_perk_unlock,
            'stat_bonuses': self.stat_bonuses,
            'real_world_benefits': self.real_world_benefits,
            'spiritual_reward': self.spiritual_reward,
            'sessions_completed': self.sessions_completed,
            'total_minutes': self.total_minutes,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'last_completed': self.last_completed.isoformat() if self.last_completed else None,
            'verification_method': self.verification_method,
            'journal_prompts': self.journal_prompts,
            'is_complete': self.is_complete,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None
        }


class RealWorldBridge:
    """Manage real-world practice integration"""

    # Practice library
    PRACTICE_LIBRARY = {
        # Meditation & Mindfulness
        'daily_meditation': RealWorldPractice(
            practice_id='daily_meditation',
            practice_name='Daily Meditation Practice',
            category='meditation',
            description='20 minutes of mindfulness meditation daily for 7 consecutive days',
            duration_minutes=20,
            frequency='daily',
            difficulty=4,
            game_achievement_name='Master of the Inner World',
            cp_reward=200,
            in_game_perk_unlock='Inner Stillness (Precognition enhancement)',
            stat_bonuses={'mental': 5, 'special': 3},
            real_world_benefits='Improved focus, reduced anxiety, greater emotional regulation',
            spiritual_reward='Deepened awareness, access to inner stillness',
            journal_prompts=[
                'What thoughts arose during meditation?',
                'Did you notice any patterns in your mind?',
                'How did you feel before vs after?',
                'What insights emerged?'
            ]
        ),

        # Shadow Work
        'shadow_journaling': RealWorldPractice(
            practice_id='shadow_journaling',
            practice_name='Shadow Work Journaling',
            category='shadow_work',
            description='Write about a fear, shame, or rejected part of yourself for 15 minutes, 5 days in a row',
            duration_minutes=15,
            frequency='5 days in 7',
            difficulty=7,
            game_achievement_name='Face the Darkness',
            cp_reward=300,
            in_game_perk_unlock='Shadow Integration (Drawback mitigation)',
            stat_bonuses={'mental': 3, 'special': 5},
            real_world_benefits='Greater self-awareness, reduced internal conflict, emotional healing',
            spiritual_reward='Integration of disowned parts, increased wholeness',
            verification_method='journal_entry',
            journal_prompts=[
                'What part of myself have I been rejecting?',
                'What is this part trying to protect me from?',
                'What happens if I accept this part instead of fighting it?',
                'How has rejecting this part cost me?'
            ]
        ),

        # Physical Cultivation
        'body_temple': RealWorldPractice(
            practice_id='body_temple',
            practice_name='Body as Temple',
            category='exercise',
            description='30 minutes of intentional physical practice daily for 14 days',
            duration_minutes=30,
            frequency='daily',
            difficulty=5,
            game_achievement_name='Physical Cultivation',
            cp_reward=250,
            in_game_perk_unlock='Enhanced Vitality (Physical stat boost)',
            stat_bonuses={'physical': 8, 'durability': 5},
            real_world_benefits='Increased strength, energy, and physical health',
            spiritual_reward='Embodiment, grounding, energy flow',
            journal_prompts=[
                'How did my body feel today?',
                'What resistance came up?',
                'What changed in my energy levels?'
            ]
        ),

        # Energy Work
        'qi_cultivation': RealWorldPractice(
            practice_id='qi_cultivation',
            practice_name='Qi Gong / Energy Cultivation',
            category='energy_work',
            description='20 minutes of Qi Gong, Tai Chi, or conscious breathwork daily for 10 days',
            duration_minutes=20,
            frequency='daily',
            difficulty=4,
            game_achievement_name='Energy Master',
            cp_reward=350,
            in_game_perk_unlock='Internal Energy (Energy stat unlock)',
            stat_bonuses={'energy': 10, 'durability': 3},
            real_world_benefits='Improved energy flow, vitality, mind-body connection',
            spiritual_reward='Direct experience of subtle energy, cultivation',
            journal_prompts=[
                'What sensations did I notice in my body?',
                'Where did energy feel blocked or flowing?',
                'What shifted during the practice?'
            ]
        ),

        # Creative Practice
        'creative_flow': RealWorldPractice(
            practice_id='creative_flow',
            practice_name='Creative Flow Practice',
            category='creative',
            description='30 minutes of creative work (writing, art, music, etc.) 5 times per week for 2 weeks',
            duration_minutes=30,
            frequency='5 per week',
            difficulty=4,
            game_achievement_name='Creative Genesis',
            cp_reward=200,
            in_game_perk_unlock='Creative Manifestation (Creation perk boost)',
            stat_bonuses={'special': 5, 'mental': 3},
            real_world_benefits='Enhanced creativity, self-expression, flow states',
            spiritual_reward='Connection to creative source, authentic expression',
            journal_prompts=[
                'What did I create today?',
                'What surprised me in the process?',
                'Where did I get stuck? Where did I flow?'
            ]
        ),

        # Service / Connection
        'compassionate_action': RealWorldPractice(
            practice_id='compassionate_action',
            practice_name='Compassionate Action',
            category='service',
            description='One deliberate act of service or kindness daily for 7 days',
            duration_minutes=15,
            frequency='daily',
            difficulty=3,
            game_achievement_name='Heart of Service',
            cp_reward=200,
            in_game_perk_unlock='Compassionate Aura (Social/healing boost)',
            stat_bonuses={'social': 5, 'special': 3},
            real_world_benefits='Increased connection, reduced isolation, meaning',
            spiritual_reward='Heart opening, connection to others',
            journal_prompts=[
                'What did I do for someone today?',
                'How did it feel?',
                'What did I receive in return?'
            ]
        ),

        # Deep Integration
        'values_clarification': RealWorldPractice(
            practice_id='values_clarification',
            practice_name='Values Clarification',
            category='shadow_work',
            description='1 hour session identifying your core values and examining where you\'re out of alignment',
            duration_minutes=60,
            frequency='once',
            difficulty=6,
            game_achievement_name='Know Thyself',
            cp_reward=150,
            in_game_perk_unlock='Authentic Path (Synergy with all perks)',
            stat_bonuses={'mental': 3, 'special': 4},
            real_world_benefits='Clarity on what matters, reduced internal conflict',
            spiritual_reward='Alignment with authentic self',
            verification_method='journal_entry',
            journal_prompts=[
                'What do I truly value above all else?',
                'Where am I living out of alignment with these values?',
                'What would it look like to live in full alignment?',
                'What fears come up when I consider this?'
            ]
        ),

        # Breakthrough practice
        'hero_journey': RealWorldPractice(
            practice_id='hero_journey',
            practice_name='The Hero\'s Journey',
            category='shadow_work',
            description='Map your life as a hero\'s journey. Identify: Call to adventure, refusal, mentor, trials, abyss, transformation, return. Write it out.',
            duration_minutes=90,
            frequency='once',
            difficulty=8,
            game_achievement_name='Journey Mapped',
            cp_reward=400,
            in_game_perk_unlock='Mythic Resonance (Narrative power)',
            stat_bonuses={'mental': 5, 'special': 8},
            real_world_benefits='Life narrative coherence, meaning-making, empowerment',
            spiritual_reward='Understanding of your unique path, archetypal connection',
            verification_method='journal_entry',
            journal_prompts=[
                'What was my call to adventure?',
                'What trials have I faced?',
                'What is my abyss - my darkest moment?',
                'What treasure did I bring back from the underworld?',
                'How am I returning to serve the world?'
            ]
        )
    }

    def __init__(self, state_manager):
        """Initialize real-world bridge"""
        self.state_manager = state_manager
        self.active_practices = {}
        self.load_practices()

    def load_practices(self):
        """Load active practices from file"""
        try:
            with open('data/real_world_practices.json', 'r') as f:
                data = json.load(f)
                for practice_id, practice_data in data.items():
                    # Reconstruct datetime objects
                    if practice_data.get('last_completed'):
                        practice_data['last_completed'] = datetime.fromisoformat(practice_data['last_completed'])
                    if practice_data.get('completion_date'):
                        practice_data['completion_date'] = datetime.fromisoformat(practice_data['completion_date'])

                    self.active_practices[practice_id] = RealWorldPractice(**practice_data)
        except FileNotFoundError:
            pass  # No practices yet

    def save_practices(self):
        """Save practices to file"""
        data = {
            practice_id: practice.to_dict()
            for practice_id, practice in self.active_practices.items()
        }

        with open('data/real_world_practices.json', 'w') as f:
            json.dump(data, f, indent=2)

    def start_practice(self, practice_id: str) -> RealWorldPractice:
        """
        Start a real-world practice

        Args:
            practice_id: ID of practice from library

        Returns:
            RealWorldPractice object
        """
        if practice_id not in self.PRACTICE_LIBRARY:
            raise ValueError(f"Unknown practice: {practice_id}")

        practice = self.PRACTICE_LIBRARY[practice_id]
        self.active_practices[practice_id] = practice
        self.save_practices()

        return practice

    def complete_session(self, practice_id: str,
                        duration_minutes: Optional[int] = None,
                        journal_entry: Optional[str] = None) -> Dict:
        """
        Record completion of a practice session

        Args:
            practice_id: ID of practice
            duration_minutes: How long (uses default if not provided)
            journal_entry: Optional journal entry

        Returns:
            Dict with results and any unlocks
        """
        if practice_id not in self.active_practices:
            raise ValueError(f"Practice not started: {practice_id}")

        practice = self.active_practices[practice_id]

        # Update stats
        duration = duration_minutes or practice.duration_minutes
        practice.sessions_completed += 1
        practice.total_minutes += duration

        # Update streak
        now = datetime.now()
        if practice.last_completed:
            time_since_last = now - practice.last_completed
            if time_since_last <= timedelta(days=2):  # Within 2 days = streak continues
                practice.current_streak += 1
            else:
                practice.current_streak = 1
        else:
            practice.current_streak = 1

        practice.longest_streak = max(practice.longest_streak, practice.current_streak)
        practice.last_completed = now

        # Check completion criteria
        result = self._check_completion(practice)

        # Save journal if provided
        if journal_entry:
            self._save_journal_entry(practice, journal_entry)

        self.save_practices()

        return result

    def _check_completion(self, practice: RealWorldPractice) -> Dict:
        """Check if practice is complete"""
        result = {
            'practice': practice.practice_name,
            'session_completed': True,
            'total_sessions': practice.sessions_completed,
            'current_streak': practice.current_streak,
            'achievement_unlocked': False,
            'rewards': {}
        }

        # Completion criteria based on frequency
        if practice.frequency == 'daily':
            # Need streak
            required_streak = 7 if '7' in practice.description else 14
            if practice.current_streak >= required_streak and not practice.is_complete:
                practice.is_complete = True
                practice.completion_date = datetime.now()
                result['achievement_unlocked'] = True
                result['rewards'] = self._grant_rewards(practice)

        elif practice.frequency == '5 per week':
            # Need total sessions
            required_sessions = 10  # 2 weeks
            if practice.sessions_completed >= required_sessions and not practice.is_complete:
                practice.is_complete = True
                practice.completion_date = datetime.now()
                result['achievement_unlocked'] = True
                result['rewards'] = self._grant_rewards(practice)

        elif practice.frequency == 'once':
            # Immediate completion
            if not practice.is_complete:
                practice.is_complete = True
                practice.completion_date = datetime.now()
                result['achievement_unlocked'] = True
                result['rewards'] = self._grant_rewards(practice)

        return result

    def _grant_rewards(self, practice: RealWorldPractice) -> Dict:
        """Grant in-game rewards for completing practice"""
        rewards = {
            'achievement': practice.game_achievement_name,
            'cp_reward': practice.cp_reward,
            'stat_bonuses': practice.stat_bonuses,
            'perk_unlock': practice.in_game_perk_unlock,
            'real_benefit': practice.real_world_benefits,
            'spiritual_reward': practice.spiritual_reward
        }

        # Create achievement in database
        from ..core.models import Achievement
        achievement = Achievement(
            id=0,
            name=practice.game_achievement_name,
            tier='gold',  # Real-world achievements are always gold+
            trigger_condition=f'real_world_practice:{practice.practice_id}',
            reward_value=practice.cp_reward,
            earned_date=datetime.now(),
            description=f'Completed: {practice.description}',
            icon='🌟'
        )

        self.state_manager.award_achievement(achievement)

        # Add CP to jumper
        jumper = self.state_manager.load_jumper()
        jumper.total_cp_earned += practice.cp_reward
        self.state_manager.save_jumper(jumper)

        return rewards

    def _save_journal_entry(self, practice: RealWorldPractice, entry: str):
        """Save a journal entry for a practice"""
        journal_file = 'data/practice_journal.jsonl'

        journal_entry = {
            'practice_id': practice.practice_id,
            'practice_name': practice.practice_name,
            'timestamp': datetime.now().isoformat(),
            'session_number': practice.sessions_completed,
            'entry': entry
        }

        with open(journal_file, 'a') as f:
            f.write(json.dumps(journal_entry) + '\n')

    def get_active_practices(self) -> List[RealWorldPractice]:
        """Get all active (not complete) practices"""
        return [p for p in self.active_practices.values() if not p.is_complete]

    def get_completed_practices(self) -> List[RealWorldPractice]:
        """Get all completed practices"""
        return [p for p in self.active_practices.values() if p.is_complete]

    def get_practice_suggestions(self, jumper_state) -> List[str]:
        """Suggest practices based on current game state"""
        suggestions = []

        # Get active perks and drawbacks
        perks = self.state_manager.get_active_perks(jumper_state.id, 'jumper')

        # Suggest meditation if mental/precog perks
        if any('precog' in p.synergy_tags or 'mental' in p.synergy_tags for p in perks):
            if 'daily_meditation' not in self.active_practices:
                suggestions.append('daily_meditation')

        # Always suggest shadow work
        if 'shadow_journaling' not in self.active_practices:
            suggestions.append('shadow_journaling')

        # Physical if combat perks
        if any('combat' in p.synergy_tags or 'physical' in p.synergy_tags for p in perks):
            if 'body_temple' not in self.active_practices:
                suggestions.append('body_temple')

        # Energy work for anyone
        if 'qi_cultivation' not in self.active_practices:
            suggestions.append('qi_cultivation')

        return suggestions

    def generate_practice_prompt(self, practice: RealWorldPractice,
                                 completion_data: Dict) -> str:
        """
        Generate Claude prompt for narrating practice completion

        Args:
            practice: The completed practice
            completion_data: Results from complete_session

        Returns:
            Prompt for deep narration
        """
        prompt = f"""
The protagonist has completed a real-world practice that bridges game and reality.

PRACTICE COMPLETED: {practice.practice_name}
{practice.description}

Real-world benefit: {practice.real_world_benefits}
Spiritual reward: {practice.spiritual_reward}

Sessions completed: {practice.sessions_completed}
Current streak: {practice.current_streak} days

IN-GAME REWARDS:
- Achievement: {practice.game_achievement_name}
- CP gained: +{practice.cp_reward}
- Perk unlocked: {practice.in_game_perk_unlock or 'None'}
- Stat bonuses: {practice.stat_bonuses}

NARRATION TASK:
This is a REAL accomplishment. The player actually DID this practice in real life.
The in-game power they're receiving reflects ACTUAL personal growth.

Show the moment of unlocking this power not as external gain, but as recognition
of what they've already developed. The power was earned through practice, not
granted by fiat.

Make this meaningful. Make this resonant. Show how the practice transformed them,
and how that transformation manifests as in-game power.

This is where game becomes reality. Where reality becomes power.

Write beautifully. Celebrate their growth.
"""
        return prompt
