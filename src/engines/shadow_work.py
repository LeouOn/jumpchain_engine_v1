"""
Shadow Work System - Integration of psychological depth
Drawbacks become opportunities for shadow integration
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json


@dataclass
class ShadowAspect:
    """A drawback as psychological shadow work"""

    # Game mechanics
    drawback_name: str
    cp_value: int
    surface_description: str

    # Psychological depth
    shadow_meaning: str  # What this represents in the psyche
    integration_path: str  # How to work with this
    real_world_parallel: str  # Connection to actual life
    archetypal_pattern: str  # Jungian archetype (Shadow, Anima/Animus, etc.)

    # Progress tracking
    awareness_level: int = 0  # 0-10: How conscious
    integration_level: int = 0  # 0-10: How integrated
    breakthrough_moments: List[str] = field(default_factory=list)
    journal_entries: List[Dict] = field(default_factory=list)

    # Rewards for integration
    integration_rewards: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'drawback_name': self.drawback_name,
            'cp_value': self.cp_value,
            'surface_description': self.surface_description,
            'shadow_meaning': self.shadow_meaning,
            'integration_path': self.integration_path,
            'real_world_parallel': self.real_world_parallel,
            'archetypal_pattern': self.archetypal_pattern,
            'awareness_level': self.awareness_level,
            'integration_level': self.integration_level,
            'breakthrough_moments': self.breakthrough_moments,
            'journal_entries': self.journal_entries,
            'integration_rewards': self.integration_rewards
        }


class ShadowWorkSystem:
    """Manage shadow work integration"""

    # Predefined shadow aspects for common drawbacks
    SHADOW_LIBRARY = {
        'Powerful Enemy': ShadowAspect(
            drawback_name='Powerful Enemy',
            cp_value=300,
            surface_description='A dangerous foe hunts you relentlessly',
            shadow_meaning='The parts of yourself in conflict. The inner critic. Self-sabotage patterns.',
            integration_path='Face the enemy not with violence, but understanding. What does it want? What does it represent? Can you make peace with this part of yourself?',
            real_world_parallel='Your inner critic, self-limiting beliefs, or self-sabotage patterns',
            archetypal_pattern='The Shadow - rejected aspects seeking integration'
        ),

        'Amnesia': ShadowAspect(
            drawback_name='Amnesia',
            cp_value=200,
            surface_description='You forget your past, your previous jumps',
            shadow_meaning='Disconnection from your history, your roots, your accumulated wisdom. Fear of truly knowing yourself.',
            integration_path='Reconstruct your story. Journal. Remember. The past shapes but doesn\'t define you.',
            real_world_parallel='Disowned parts of your history, unprocessed trauma, or reluctance to face your full story',
            archetypal_pattern='The Lost Self - fragmentation seeking wholeness'
        ),

        'Wanted': ShadowAspect(
            drawback_name='Wanted',
            cp_value=300,
            surface_description='Authorities hunt you. You are an outlaw.',
            shadow_meaning='Rebellion against authority. Fear of standing in your power. The part that refuses to conform.',
            integration_path='Examine: Are you rebelling for freedom or from fear? Can you honor your authentic self without destructive rebellion?',
            real_world_parallel='Your relationship with authority, rules, and your own authentic power',
            archetypal_pattern='The Rebel - seeking authentic autonomy'
        ),

        'Weakness': ShadowAspect(
            drawback_name='Weakness',
            cp_value=400,
            surface_description='You are physically frail, vulnerable',
            shadow_meaning='Vulnerability shame. Fear of being seen as weak. Compensatory perfectionism.',
            integration_path='Strength isn\'t absence of weakness. True power includes vulnerability. Can you be both strong AND fragile?',
            real_world_parallel='Your relationship with vulnerability, imperfection, and human limitation',
            archetypal_pattern='The Wounded Healer - strength through acknowledged weakness'
        ),

        'Addiction': ShadowAspect(
            drawback_name='Addiction',
            cp_value=400,
            surface_description='You struggle with compulsive behavior',
            shadow_meaning='Unmet needs seeking expression through maladaptive means. Spiritual hunger misdirected.',
            integration_path='What is the addiction really trying to give you? Safety? Connection? Peace? Can you meet that need directly?',
            real_world_parallel='Your actual compulsions, coping mechanisms, or ways you numb difficult feelings',
            archetypal_pattern='The Seeker - hunger for wholeness'
        ),

        'Arrogance': ShadowAspect(
            drawback_name='Arrogance',
            cp_value=200,
            surface_description='You are overconfident, dismissive of others',
            shadow_meaning='Compensation for deep inadequacy feelings. Fragile ego protection. Fear of equality.',
            integration_path='True confidence doesn\'t need arrogance. Can you be capable WITHOUT diminishing others?',
            real_world_parallel='Your relationship with ego, self-worth, and how you relate to others',
            archetypal_pattern='The Inflated Ego - insecurity masked as superiority'
        ),

        'Isolation': ShadowAspect(
            drawback_name='Isolation',
            cp_value=300,
            surface_description='You are cut off from companions, alone',
            shadow_meaning='Fear of intimacy. Walls built for protection that became prisons. Trust wounds.',
            integration_path='Isolation protects you from hurt, but also from love. Can you risk connection?',
            real_world_parallel='Your walls, your fear of being truly seen, your trust issues',
            archetypal_pattern='The Hermit - withdrawal seeking safety'
        ),

        'Berserker': ShadowAspect(
            drawback_name='Berserker',
            cp_value=300,
            surface_description='You lose control in combat, become violent',
            shadow_meaning='Repressed rage. Controlled persona with violent shadow. Power fear.',
            integration_path='The rage is not the enemy. It\'s energy. Can you feel it without being consumed? Can you channel it consciously?',
            real_world_parallel='Your anger, your repressed aggression, your fear of your own intensity',
            archetypal_pattern='The Beast Within - repressed primal energy'
        ),

        'Pacifist': ShadowAspect(
            drawback_name='Pacifist',
            cp_value=200,
            surface_description='You cannot harm anyone, even in self-defense',
            shadow_meaning='Repressed aggression. Fear of your own power to cause harm. Conflict avoidance.',
            integration_path='Healthy boundaries sometimes require force. Can you be peaceful AND powerful? Can you protect without guilt?',
            real_world_parallel='Your difficulty with healthy anger, boundaries, or standing your ground',
            archetypal_pattern='The Saint - power denied'
        ),

        'Obsession': ShadowAspect(
            drawback_name='Obsession',
            cp_value=300,
            surface_description='You fixate on a goal to the exclusion of all else',
            shadow_meaning='Narrow focus as escape from overwhelming complexity. Control through limitation.',
            integration_path='Your obsession protects you from chaos, but also from life. Can you care deeply without losing yourself?',
            real_world_parallel='Your tendencies toward fixation, inability to let go, or need for control',
            archetypal_pattern='The Monomaniac - safety through narrowing'
        )
    }

    def __init__(self, state_manager):
        """Initialize shadow work system"""
        self.state_manager = state_manager

    def create_shadow_aspect(self, drawback_name: str, custom: bool = False,
                            **kwargs) -> ShadowAspect:
        """
        Create a shadow aspect from a drawback

        Args:
            drawback_name: Name of the drawback
            custom: If True, create custom shadow aspect with kwargs
            **kwargs: Custom shadow aspect parameters

        Returns:
            ShadowAspect object
        """
        if not custom and drawback_name in self.SHADOW_LIBRARY:
            # Use predefined
            return self.SHADOW_LIBRARY[drawback_name]
        else:
            # Create custom
            return ShadowAspect(
                drawback_name=drawback_name,
                **kwargs
            )

    def record_breakthrough(self, shadow_aspect: ShadowAspect,
                           description: str,
                           awareness_gain: int = 1,
                           integration_gain: int = 0):
        """
        Record a breakthrough moment

        Args:
            shadow_aspect: The shadow aspect
            description: What was realized
            awareness_gain: Increase in awareness (0-10)
            integration_gain: Increase in integration (0-10)
        """
        shadow_aspect.breakthrough_moments.append({
            'timestamp': datetime.now().isoformat(),
            'description': description,
            'awareness_before': shadow_aspect.awareness_level,
            'integration_before': shadow_aspect.integration_level
        })

        shadow_aspect.awareness_level = min(10, shadow_aspect.awareness_level + awareness_gain)
        shadow_aspect.integration_level = min(10, shadow_aspect.integration_level + integration_gain)

        # Check for integration rewards
        self._check_integration_rewards(shadow_aspect)

    def add_journal_entry(self, shadow_aspect: ShadowAspect, entry: str):
        """Add a journal entry for shadow work"""
        shadow_aspect.journal_entries.append({
            'timestamp': datetime.now().isoformat(),
            'entry': entry,
            'awareness_level': shadow_aspect.awareness_level,
            'integration_level': shadow_aspect.integration_level
        })

    def _check_integration_rewards(self, shadow_aspect: ShadowAspect):
        """Check if integration unlocks rewards"""
        # Thresholds for rewards
        if shadow_aspect.awareness_level >= 5 and 'awareness_5' not in shadow_aspect.integration_rewards:
            shadow_aspect.integration_rewards['awareness_5'] = {
                'type': 'perk_evolution',
                'description': f'Increased awareness of {shadow_aspect.drawback_name} shadow',
                'bonus': 'Related perks gain +1 evolution stage'
            }

        if shadow_aspect.integration_level >= 7 and 'integration_7' not in shadow_aspect.integration_rewards:
            shadow_aspect.integration_rewards['integration_7'] = {
                'type': 'drawback_mitigation',
                'description': f'Partial integration of {shadow_aspect.drawback_name}',
                'bonus': 'Drawback mechanical effects reduced by 50%'
            }

        if shadow_aspect.integration_level >= 10 and 'integration_10' not in shadow_aspect.integration_rewards:
            shadow_aspect.integration_rewards['integration_10'] = {
                'type': 'transcendence',
                'description': f'Complete integration of {shadow_aspect.drawback_name}',
                'bonus': 'Drawback becomes a strength. Keep CP, lose penalty. Unlock "Shadow Master" achievement.'
            }

    def generate_shadow_prompt(self, shadow_aspect: ShadowAspect,
                               situation: str) -> str:
        """
        Generate prompt for LLM to explore shadow aspect

        Args:
            shadow_aspect: The shadow being worked with
            situation: Current in-game situation

        Returns:
            Prompt for deep narration
        """
        prompt = f"""
You are narrating a moment of psychological depth in a transformative jumpchain.

SHADOW ASPECT BEING EXPLORED:
{shadow_aspect.drawback_name}

Surface (game mechanical): {shadow_aspect.surface_description}
Deeper meaning: {shadow_aspect.shadow_meaning}
Real-world parallel: {shadow_aspect.real_world_parallel}
Archetypal pattern: {shadow_aspect.archetypal_pattern}

Integration path: {shadow_aspect.integration_path}

Current progress:
- Awareness: {shadow_aspect.awareness_level}/10
- Integration: {shadow_aspect.integration_level}/10

Previous breakthroughs:
{self._format_breakthroughs(shadow_aspect)}

CURRENT SITUATION:
{situation}

NARRATION GUIDELINES:
1. Show this drawback manifesting, but illuminate its shadow nature
2. Don't hit the reader over the head - be subtle, literary
3. Create an opportunity for breakthrough if they're ready
4. Connect the in-game manifestation to the psychological truth
5. End with a moment of choice or deepening awareness

Remember: This is not just a story. This is a mirror. This is medicine.

Write beautifully. Write truthfully. Show them something about themselves.
"""
        return prompt

    def _format_breakthroughs(self, shadow_aspect: ShadowAspect) -> str:
        """Format breakthrough moments for prompt"""
        if not shadow_aspect.breakthrough_moments:
            return "None yet - this is their first encounter with this shadow."

        formatted = []
        for moment in shadow_aspect.breakthrough_moments[-3:]:  # Last 3
            formatted.append(f"- {moment['description']}")

        return "\n".join(formatted)

    def generate_integration_exercise(self, shadow_aspect: ShadowAspect) -> Dict:
        """
        Generate a real-world integration exercise

        Args:
            shadow_aspect: The shadow to work with

        Returns:
            Exercise dict with instructions
        """
        # Exercise templates based on shadow type
        exercises = {
            'The Shadow': {
                'name': 'Mirror Work',
                'instructions': 'Sit with a mirror. Look into your own eyes. What do you see? What do you judge? Can you witness without condemning?',
                'duration': '10 minutes',
                'journal_prompt': 'What parts of myself am I most critical of? What would happen if I accepted them?'
            },
            'The Lost Self': {
                'name': 'Timeline Reconstruction',
                'instructions': 'Map your life in 5-year segments. What happened? Who were you? What did you lose? What did you gain?',
                'duration': '30 minutes',
                'journal_prompt': 'What parts of my history have I disowned? What happens when I reclaim them?'
            },
            'The Rebel': {
                'name': 'Authority Inventory',
                'instructions': 'List every authority you rebel against. Then ask: What authentic need is this rebellion protecting?',
                'duration': '20 minutes',
                'journal_prompt': 'Where is my rebellion serving my freedom? Where is it just fear?'
            },
            'The Wounded Healer': {
                'name': 'Vulnerability Practice',
                'instructions': 'Share something you\'re struggling with. With a friend, therapist, or journal. Let yourself be seen in weakness.',
                'duration': 'One honest conversation',
                'journal_prompt': 'What do I fear will happen if I show my weakness? What actually happened when I did?'
            }
        }

        pattern = shadow_aspect.archetypal_pattern.split(' - ')[0]  # Get archetype name
        exercise = exercises.get(pattern, {
            'name': 'Shadow Journal',
            'instructions': f'Write about: {shadow_aspect.integration_path}',
            'duration': '15 minutes',
            'journal_prompt': f'How does {shadow_aspect.drawback_name} show up in my real life?'
        })

        return {
            'shadow_aspect': shadow_aspect.drawback_name,
            'exercise': exercise,
            'current_level': shadow_aspect.integration_level,
            'next_milestone': self._next_milestone(shadow_aspect)
        }

    def _next_milestone(self, shadow_aspect: ShadowAspect) -> str:
        """Get next integration milestone"""
        if shadow_aspect.integration_level < 5:
            return "Reach Integration 5: Begin seeing this pattern in daily life"
        elif shadow_aspect.integration_level < 7:
            return "Reach Integration 7: Partial mitigation - drawback penalty reduced 50%"
        elif shadow_aspect.integration_level < 10:
            return "Reach Integration 10: Complete transcendence - drawback becomes strength"
        else:
            return "Fully integrated. This shadow has become light."
