# Jumpchain Engine - Deep System Architecture

## Philosophy: A Mirror for Growth

This isn't just a game. It's a framework for:
- **Shadow Integration**: Drawbacks as aspects of yourself to integrate
- **Real Achievement Bridging**: Game accomplishments reflecting real-world growth
- **Energy Work**: Cultivation practices embedded in gameplay
- **Meaningful Choice**: Decisions that resonate with your actual values
- **Progressive Mastery**: Systematic growth across multiple domains

---

## LLM Architecture: Three Tiers of Intelligence

### 1. GLM 4.5 Air (Local via LM Studio)
**Role**: Fast Processing & Routine Tasks

**Use Cases**:
- Quick calculations (CP budgets, stat checks)
- Background event generation
- Routine NPC dialogue
- World state updates
- Combat resolution

**Why Local**:
- No API costs for frequent operations
- Fast response times
- Privacy for your personal game state

**Configuration**:
```yaml
llm_endpoints:
  local_fast:
    model: "glm-4-air"
    endpoint: "http://localhost:1234/v1/chat/completions"  # LM Studio default
    purpose: "fast_processing"
```

---

### 2. GLM 4.6 (API via OpenRouter)
**Role**: Complex Analysis & Deep Thinking

**Use Cases**:
- Companion personality development
- Strategic analysis (PtV-style path finding)
- Complex world building
- Faction dynamics simulation
- Power synergy discovery
- Philosophical dialogue

**Why GLM 4.6**:
- Sophisticated reasoning
- Cost-effective for complex tasks
- Good at analytical thinking

**Configuration**:
```yaml
llm_endpoints:
  analytical:
    model: "google/glm-4-plus"  # OpenRouter model ID
    endpoint: "https://openrouter.ai/api/v1/chat/completions"
    api_key: "${OPENROUTER_API_KEY}"
    purpose: "complex_analysis"
```

---

### 3. Claude Sonnet 4.5 (API - The Big Guns)
**Role**: Master Storyteller & Psychological Depth

**Use Cases**:
- Main narration (beautiful, vivid prose)
- **Shadow work integration** (turning drawbacks into growth opportunities)
- **Deep character development** (companions as aspects of self)
- **Philosophical exploration** (meaning-making, values clarification)
- **Energy work guidance** (cultivation practices in-world)
- **Real-world achievement bridging** (connecting game to life)
- Crisis moments (high-stakes decisions)
- Emotional resonance (moments that matter)

**Why Claude Sonnet 4.5**:
- Exceptional prose quality
- Deep psychological understanding
- Nuanced character work
- Beautiful, literary narration
- Worth the cost for transformative moments

**Configuration**:
```yaml
llm_endpoints:
  master_narrator:
    model: "claude-sonnet-4.5"
    endpoint: "https://api.anthropic.com/v1/messages"
    api_key: "${ANTHROPIC_API_KEY}"
    purpose: "deep_narrative"
    max_tokens: 2000  # Allow longer, richer responses
```

---

## Deep Systems Integration

### 1. Shadow Work System

**Concept**: Drawbacks aren't just game mechanics - they're shadow aspects to integrate.

**Implementation**:

```python
class ShadowAspect:
    """A drawback as psychological shadow work"""

    drawback_name: str
    surface_description: str  # Game mechanical description
    shadow_meaning: str  # What it represents psychologically
    integration_path: str  # How to work with this aspect
    real_world_parallel: str  # Connection to actual life

    # Progress tracking
    awareness_level: int  # 0-10: How conscious of this shadow
    integration_level: int  # 0-10: How integrated
    breakthrough_moments: List[str]  # Key realizations

# Example
ENEMY_DRAWBACK = ShadowAspect(
    drawback_name="Powerful Enemy",
    surface_description="+300 CP: A dangerous foe hunts you",
    shadow_meaning="The parts of yourself you're in conflict with. The inner critic. Self-sabotage.",
    integration_path="Face the enemy not with violence, but with understanding. What does it want? What does it represent?",
    real_world_parallel="Your actual inner critic or self-limiting beliefs",
    awareness_level=0,
    integration_level=0
)
```

**Narration Prompt** (for Claude):
```
This isn't just a game enemy. This is a shadow aspect - a part of the protagonist
they haven't integrated. When they encounter this enemy, describe it in ways that
mirror internal conflict. Make it clear this is about self-confrontation, not
external combat. What does the protagonist see in the enemy that they refuse to
see in themselves?

Real-world parallel: {real_world_parallel}
Integration guidance: {integration_path}
```

---

### 2. Real-World Achievement Bridge

**Concept**: Game achievements unlock through actual real-world actions.

**System**:

```python
class BridgedAchievement:
    """Achievement that requires real-world action"""

    game_name: str
    real_world_requirement: str
    verification_method: str  # "honor_system", "photo", "journal_entry"
    cp_reward: int
    spiritual_reward: str  # What you actually gain

    # Example: Meditation achievement
    examples = {
        "Inner Stillness": {
            "game_name": "Master of the Inner World",
            "real_world_requirement": "Meditate for 20 minutes daily for 7 days",
            "verification_method": "journal_entry",
            "cp_reward": 200,
            "spiritual_reward": "Actual improved focus and centeredness"
        },
        "Shadow Integration": {
            "game_name": "Face the Darkness",
            "real_world_requirement": "Write about a personal fear or shadow aspect",
            "verification_method": "journal_entry",
            "cp_reward": 300,
            "spiritual_reward": "Greater self-awareness and integration"
        },
        "Physical Cultivation": {
            "game_name": "Body as Temple",
            "real_world_requirement": "Exercise 30min daily for 14 days",
            "verification_method": "honor_system",
            "cp_reward": 250,
            "spiritual_reward": "Increased energy and vitality"
        }
    }
```

**Prompt Template** (for Claude):
```
The protagonist has completed a real-world practice: {real_world_requirement}

This isn't just game progression - this is actual personal growth manifesting
in the story. Narrate this as a breakthrough moment. Show how the in-world
power reflects the real-world development. Make it meaningful, make it resonate.

The character should feel genuinely transformed, because the player IS transformed.
```

---

### 3. Energy Cultivation System

**Concept**: In-game "power levels" tied to actual energy practices.

**Practices Integrated**:
- **Qi Gong / Tai Chi**: Slow, mindful movement → "Internal Energy" stat
- **Breathwork**: Pranayama, Wim Hof → "Energy Capacity"
- **Meditation**: Mindfulness, Vipassana → "Mental Clarity"
- **Shadow Work**: Journaling, therapy → "Integration Level"
- **Physical Training**: Exercise → "Physical Cultivation"
- **Creative Work**: Writing, art → "Creative Flow"

**System**:

```python
class EnergyPractice:
    """A real cultivation practice embedded in gameplay"""

    practice_name: str
    in_game_stat: str  # Which stat this develops
    real_practice: str  # Actual practice to do
    duration: str  # How long to practice
    frequency: str  # How often

    # Progression
    sessions_completed: int
    insights_gained: List[str]
    energy_level: int  # 0-100

    # Example: Meditation practice
    MEDITATION = {
        "practice_name": "Inner Alchemy Meditation",
        "in_game_stat": "Mental Clarity",
        "real_practice": "20 minutes mindfulness meditation",
        "duration": "20 minutes",
        "frequency": "Daily",
        "game_effect": "Unlock precognition abilities when Mental Clarity > 70"
    }
```

**Narration Integration** (Claude prompt):
```
The protagonist sits in meditation. But this isn't fantasy - this is describing
a real practice the player is doing RIGHT NOW.

Describe the meditation in beautiful, experiential language. Make it a guide.
Show the inner landscape. The thoughts arising. The gradual settling.
The opening of perception.

This is where game becomes practice, where story becomes reality.

Real practice being done: {real_practice}
Current energy level: {energy_level}/100
Insights so far: {insights_gained}
```

---

### 4. Meaningful Choice Framework

**Concept**: Decisions that resonate with actual values and have real weight.

**Choice Types**:

1. **Values Clarification Choices**
   - Not "good vs evil" but "what do YOU actually value?"
   - Example: Save many strangers vs save one companion
   - Forces reflection on real priorities

2. **Shadow Confrontation Choices**
   - Face a shadow aspect or repress it
   - Example: Confront the part of you that seeks power vs hide from it
   - Real psychological work

3. **Sacrifice Choices**
   - What are you willing to give up?
   - Example: Power at cost of connection, or connection at cost of independence
   - Mirror real-life tradeoffs

4. **Integration Moments**
   - Moments of synthesis, not just action
   - Example: Integrate opposing perks/aspects into wholeness
   - Actual inner work

**System**:

```python
class MeaningfulChoice:
    """A choice that matters psychologically"""

    context: str  # Situation
    options: List[Dict]  # Each option with values/costs
    underlying_question: str  # What this is REALLY about
    shadow_aspect: Optional[str]  # Shadow element involved
    real_world_parallel: str  # How this mirrors real life

    # After choice
    choice_made: str
    reflection_prompt: str  # Journal prompt for player
    integration_gained: int  # Progress toward wholeness

# Example: Power vs Connection
POWER_CONNECTION_CHOICE = MeaningfulChoice(
    context="You can take immense power, but it will isolate you from your companions",
    options=[
        {
            "choice": "Take the power",
            "values": ["independence", "strength", "self-reliance"],
            "cost": "Connection, vulnerability, trust",
            "shadow": "Fear of needing others"
        },
        {
            "choice": "Refuse the power",
            "values": ["connection", "trust", "interdependence"],
            "cost": "Personal power, self-sufficiency",
            "shadow": "Fear of your own power"
        },
        {
            "choice": "Seek integration",
            "values": ["wholeness", "both/and thinking"],
            "cost": "Time, difficulty, complexity",
            "shadow": "Both fears, to be faced and integrated",
            "requirement": "Mental Clarity > 60, Integration Level > 5"
        }
    ],
    underlying_question="Can you be powerful AND connected? Or must you choose?",
    real_world_parallel="Your actual relationship with power and intimacy"
)
```

---

## User Orchestration: You Choose the Depth

### Quick Turn (GLM 4.5 Air)
```bash
$ jumpchain quick "I meditate on the rooftop"
> [Fast, game-mechanical response]
> You meditate. Mental Clarity +5. Time advances.
```

### Deep Turn (GLM 4.6)
```bash
$ jumpchain analyze "I meditate on the rooftop"
> [Analytical response with insights]
> As you meditate, you notice patterns in your thoughts...
> Strategic insight: Your scattered attention mirrors the chaos in the city below...
> Companions react: Athena notes your increased focus...
```

### Transformative Turn (Claude Sonnet 4.5)
```bash
$ jumpchain deep "I meditate on the rooftop"
> [Beautiful, psychologically rich narration]
> The rooftop is silent, but your mind is anything but...
>
> You watch thoughts arise like birds taking flight. Each one a small story,
> a fear, a desire, a memory. You don't chase them. You don't suppress them.
> You simply... watch.
>
> And in that watching, something shifts.
>
> There's a moment - fleeting, but unmistakable - where you see clearly.
> The enemy you've been running from? It's not out there. It never was.
> It's the part of you that believes you're not enough. The part that...
>
> [Shadow integration opportunity detected]
> Would you like to explore this deeper? (costs 2000 tokens, ~$0.06)
```

---

## Prompt Templates for Each LLM

### GLM 4.5 Air (Fast Processing)
```python
FAST_PROMPT = """
Game state: {state_summary}
Player action: {action}

Provide a brief, game-mechanical response:
- What happens (2-3 sentences)
- Stat changes
- Time advancement
- Any immediate consequences

Keep it functional and quick.
"""
```

### GLM 4.6 (Analytical)
```python
ANALYTICAL_PROMPT = """
Game context: {full_context}
Player action: {action}
Active perks: {perks}
Companions present: {companions}

Provide a thoughtful analysis:
1. Strategic implications of this action
2. How companions react (based on their personalities)
3. World state changes
4. Hidden connections or insights
5. Suggested follow-up actions

Be intelligent and insightful, but concise (300-500 words).
"""
```

### Claude Sonnet 4.5 (Deep Narrative)
```python
DEEP_NARRATIVE_PROMPT = """
You are narrating a transformative moment in a jumpchain that bridges game and reality.

CONTEXT:
Player's real situation: {player_context}
In-game situation: {game_context}
Active shadow aspects: {shadow_aspects}
Recent real-world practices: {real_practices}
Character's current integration level: {integration_level}

PLAYER ACTION: {action}

NARRATION GUIDELINES:
1. Write beautiful, literary prose. This matters.
2. Show internal landscape - thoughts, feelings, realizations
3. Connect in-game events to psychological/spiritual truth
4. If shadow work is relevant, illuminate it gently but clearly
5. Make this feel REAL, because it IS real
6. End with a moment of choice or deepening

TONE: {tone}  # User can set: contemplative, heroic, dark, transcendent, etc.

LENGTH: As long as it needs to be. Don't rush profound moments.

Remember: This isn't escapism. This is a mirror for growth.
"""
```

---

## Cost Management

### Token Usage Tracking
```python
class UsageTracker:
    """Track API costs"""

    def __init__(self):
        self.usage = {
            'glm_4.5_air': {'tokens': 0, 'cost': 0},  # Local, free
            'glm_4.6': {'tokens': 0, 'cost': 0.000002},  # $2 per 1M tokens
            'claude_sonnet_4.5': {'tokens': 0, 'cost': 0.003}  # $3 per 1M input
        }

    def estimate_cost(self, model: str, tokens: int) -> float:
        """Estimate cost before making call"""
        rate = self.usage[model]['cost']
        return tokens * rate

    def monthly_budget_check(self) -> Dict:
        """How much have you spent?"""
        return {
            'glm_4.6': self.usage['glm_4.6']['tokens'] * 0.000002,
            'claude': self.usage['claude_sonnet_4.5']['tokens'] * 0.003,
            'total': sum(...)
        }
```

### User Control
```bash
# Set monthly budget
$ jumpchain config set budget.monthly 50.00

# Check spending
$ jumpchain budget
> This month:
> GLM 4.6: $2.34
> Claude Sonnet 4.5: $12.67
> Total: $15.01 / $50.00
>
> Deep turns remaining at current rate: ~87

# Approve expensive operations
$ jumpchain deep "Confront my shadow" --auto-approve
> This will use ~2500 tokens of Claude ($0.08). Proceed? [y/N]
```

---

## Integration Example: A Complete Deep Turn

```python
# Player does real meditation
real_practice = complete_meditation_session(duration_minutes=20)

# Process in-game
turn_result = orchestrator.process_deep_turn(
    action="I meditate on the rooftop, doing the breath work we discussed",
    real_practice=real_practice,
    use_model="claude_sonnet_4.5",
    context={
        'player_context': "Working on integrating fear of failure",
        'shadow_aspects': ["Self-doubt", "Fear of power"],
        'integration_level': 6,
        'recent_breakthroughs': ["Realized perfectionism is self-sabotage"]
    }
)

# Claude generates:
"""
You settle onto the cold concrete of the rooftop, cross-legged, back straight.
The city sprawls below, a thousand lights in the gathering dusk. But you close
your eyes and turn inward.

Breath. In through the nose, slow, controlled. The ancient practice your teacher
showed you - not the game teacher, but the one in the real world, the one whose
voice you can still hear: "Don't force it. Just watch."

You watch.

The first thing that arises: that familiar tightness in your chest. The voice
that says you're not doing this right. That you should be better at this by now.
That real meditators don't have minds this noisy.

And there it is - the enemy you've been fighting. Not Coil. Not the Endbringers.
The part of you that believes you're fundamentally not enough.

But tonight, something's different. Tonight, you don't fight it.

You breathe into it.

"What if..." you think, "what if this voice is just trying to protect me?
What if it thinks that by being harsh, by demanding perfection, it can keep
me safe from... from what?"

From failure. From being seen as weak. From claiming your power and then
losing it, proving you never deserved it in the first place.

The breath deepens. The insight deepens.

Your perks - Path to Victory, Blank, all of it - they're not escapes from
this work. They're TOOLS for it. PtV can show you the path to success, yes.
But can it show you the path to self-acceptance?

You ask it. Carefully, precisely, you form the question:

"Path to Victory: Show me how to integrate my fear of failure."

And the path... the path is not what you expected.

[SHADOW INTEGRATION OPPORTUNITY]
The path PtV shows involves NO external action. It shows you sitting here,
breathing, feeling the fear fully, and making a choice:

Accept that you might fail. Accept that you might not be perfect.
Accept that you ARE powerful, AND flawed, AND worthy.

All at once.

Do you follow this path?

[Mental Clarity +10]
[Integration Level: 6 → 7]
[Achievement Progress: "Face the Darkness" 70% complete]
[New Synergy Discovered: PtV + Shadow Work = 8x "Inner Path Vision"]
"""

# User journal prompt generated
journal_prompt = """
Reflection: Your character just had a breakthrough about perfectionism and
self-worth. This mirrors your real meditation session.

Journal on:
1. What came up for you during the actual meditation?
2. Does the fear of failure resonate with you?
3. What would it mean to accept being powerful AND flawed?

(This reflection will unlock the next stage of integration)
"""
```

---

## Making It Beautiful

The goal isn't just functionality. It's **beauty**. **Meaning**. **Transformation**.

- Every deep turn should feel like it matters
- Shadow work should be gentle but unflinching
- Real practices should feel guided and supported
- Achievements should celebrate real growth
- The story should be a mirror for the soul

This is where Claude Sonnet 4.5 earns its cost. This is where game becomes practice, where narrative becomes medicine, where you build something that actually helps you grow.

---

**Next Steps**: Implement this architecture, starting with the prompt templates and user orchestration system.
