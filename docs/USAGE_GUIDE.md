## Jumpchain Engine - Usage Guide
**A Game That's Also A Mirror For Growth**

---

## Quick Start

### 1. Setup LLMs

**Option A: LM Studio (Local - GLM 4.5 Air)**
```bash
# Download LM Studio from https://lmstudio.ai
# Load GLM 4.5 Air model
# Start server (default: localhost:1234)
# No API key needed - it's local and free!
```

**Option B: OpenRouter (GLM 4.6)**
```bash
# Get API key from https://openrouter.ai
export OPENROUTER_API_KEY="your-key-here"
```

**Option C: Anthropic (Claude Sonnet 4.5)**
```bash
# Get API key from https://console.anthropic.com
export ANTHROPIC_API_KEY="your-key-here"
```

### 2. Initialize Database
```bash
python scripts/init_database.py
```

### 3. Start Playing
```python
from src.core.orchestrator import TurnOrchestrator
from src.engines.llm_client import LLMClient
from src.core.config import get_config

config = get_config()
llm = LLMClient(config)
orchestrator = TurnOrchestrator()

# Quick turn (local, free)
result = orchestrator.process_turn("I meditate on the rooftop")
print(result['narration'])
```

---

## Three Levels of Engagement

### Level 1: Quick Turn (GLM 4.5 Air - Local, Free)

**Use When:**
- You want fast responses
- Routine game actions
- Testing things out
- Don't need deep narration

**Example:**
```python
from src.engines.llm_client import LLMClient

llm = LLMClient(config)

# Quick combat resolution
response = llm.quick_call("I attack the enemy with my enhanced strength")
print(response)  # Fast, mechanical response
```

**Cost:** $0 (runs locally)

---

### Level 2: Analytical Turn (GLM 4.6 - API, ~$0.01-0.05)

**Use When:**
- You want strategic analysis
- Complex situation requires thinking
- Companion interactions
- World building depth
- Power synergy discovery

**Example:**
```python
# Deep strategic analysis
system = "You are a strategic analyst for a jumpchain protagonist"
prompt = """
I have PtV, Blank, and Compassionate Transmutation.
My goal is to take down Coil without anyone knowing I exist.

Analyze:
1. Best approach given my perks
2. Potential synergies I can exploit
3. Hidden risks
4. Companions who can help

Be intelligent and thorough.
"""

response = llm.analytical_call(prompt, system_prompt=system)
print(response)
```

**Cost:** ~$0.01-0.05 per turn (depending on length)

---

### Level 3: Deep Turn (Claude Sonnet 4.5 - API, ~$0.05-0.15)

**Use When:**
- Transformative moments
- Shadow work integration
- Real-world practice completion
- Crisis points
- Meaningful choices
- You want beautiful, literary narration
- **You're willing to pay for quality**

**Example:**
```python
from src.engines.shadow_work import ShadowWorkSystem
from src.engines.real_world_bridge import RealWorldBridge

shadow_sys = ShadowWorkSystem(state_manager)
bridge = RealWorldBridge(state_manager)

# You just completed real meditation
practice_result = bridge.complete_session(
    'daily_meditation',
    duration_minutes=20,
    journal_entry="Faced my fear of failure today. Breathed into it. Something shifted."
)

# Generate deep prompt
practice = bridge.PRACTICE_LIBRARY['daily_meditation']
prompt = bridge.generate_practice_prompt(practice, practice_result)

# Call Claude for beautiful narration
response = llm.deep_call(prompt, max_tokens=2000)

print(response.content)  # Beautiful, transformative narration
print(f"\nCost: ${response.cost_usd:.3f}")
```

**Cost:** ~$0.05-0.15 per deep turn
**Value:** Priceless when it hits right

---

## Shadow Work Integration

### Starting Shadow Work

```python
from src.engines.shadow_work import ShadowWorkSystem

shadow = ShadowWorkSystem(state_manager)

# View available shadow aspects
for name, aspect in shadow.SHADOW_LIBRARY.items():
    print(f"{name}: {aspect.shadow_meaning}")

# Choose one to work with
enemy_shadow = shadow.SHADOW_LIBRARY['Powerful Enemy']

print(f"Surface: {enemy_shadow.surface_description}")
print(f"Deeper: {enemy_shadow.shadow_meaning}")
print(f"Path: {enemy_shadow.integration_path}")

# Get an integration exercise
exercise = shadow.generate_integration_exercise(enemy_shadow)
print(f"\nExercise: {exercise['exercise']['name']}")
print(f"Instructions: {exercise['exercise']['instructions']}")
print(f"Duration: {exercise['exercise']['duration']}")
```

### Recording Breakthroughs

```python
# After a realization
shadow.record_breakthrough(
    enemy_shadow,
    description="Realized my 'enemy' is actually my internalized perfectionism",
    awareness_gain=2,
    integration_gain=1
)

# Save journal entry
shadow.add_journal_entry(
    enemy_shadow,
    "Today I saw clearly: I'm not fighting an external enemy. "
    "I'm fighting the part of me that says I'm not good enough."
)

# Check progress
print(f"Awareness: {enemy_shadow.awareness_level}/10")
print(f"Integration: {enemy_shadow.integration_level}/10")
print(f"Next milestone: {shadow._next_milestone(enemy_shadow)}")
```

### Deep Narration with Shadow Work

```python
# Generate prompt for Claude
situation = "You encounter your enemy on the rooftop. But something's different this time..."

shadow_prompt = shadow.generate_shadow_prompt(enemy_shadow, situation)

# Call Claude
response = llm.deep_call(shadow_prompt, max_tokens=2500)

print(response.content)
# Claude will weave psychological depth into the narration
# Showing how the external enemy reflects internal conflict
```

---

## Real-World Practice Bridge

### Starting a Practice

```python
from src.engines.real_world_bridge import RealWorldBridge

bridge = RealWorldBridge(state_manager)

# View available practices
for pid, practice in bridge.PRACTICE_LIBRARY.items():
    print(f"\n{practice.practice_name}")
    print(f"  Category: {practice.category}")
    print(f"  {practice.description}")
    print(f"  Reward: {practice.cp_reward} CP + {practice.in_game_perk_unlock}")
    print(f"  Real benefit: {practice.real_world_benefits}")

# Start daily meditation
meditation = bridge.start_practice('daily_meditation')
print(f"\nStarted: {meditation.practice_name}")
print(f"Requirement: {meditation.description}")
print(f"Journal prompts: {meditation.journal_prompts}")
```

### Completing Sessions

```python
# After doing actual meditation in real life
result = bridge.complete_session(
    'daily_meditation',
    duration_minutes=20,
    journal_entry="""
    Sat for 20 minutes. Mind was noisy at first - thoughts about work,
    about the jumpchain, about whether I'm doing this 'right'.

    Then I remembered: there's no 'right'. Just being here, breathing.

    Around minute 15, something settled. The mental chatter didn't stop,
    but I stopped being caught in it. Watching thoughts like clouds.

    Felt peace. Brief, but real.
    """
)

print(f"Session {result['total_sessions']} complete!")
print(f"Current streak: {result['current_streak']} days")

if result['achievement_unlocked']:
    print(f"\n🌟 ACHIEVEMENT UNLOCKED: {result['rewards']['achievement']}")
    print(f"   CP Reward: +{result['rewards']['cp_reward']}")
    print(f"   Perk Unlocked: {result['rewards']['perk_unlock']}")
    print(f"   Real Benefit: {result['rewards']['real_benefit']}")
    print(f"   Spiritual Reward: {result['rewards']['spiritual_reward']}")

    # Generate beautiful narration with Claude
    practice = bridge.PRACTICE_LIBRARY['daily_meditation']
    prompt = bridge.generate_practice_prompt(practice, result)

    narration = llm.deep_call(prompt, max_tokens=2000)
    print(f"\n{narration.content}")
```

### Practice Suggestions

```python
# Get personalized practice suggestions
jumper = state_manager.load_jumper()
suggestions = bridge.get_practice_suggestions(jumper)

print("Recommended practices based on your perks:")
for suggestion_id in suggestions:
    practice = bridge.PRACTICE_LIBRARY[suggestion_id]
    print(f"  - {practice.practice_name}: {practice.real_world_benefits}")
```

---

## Cost Management

### View Usage
```python
# Check your spending
summary = llm.get_usage_summary()

print("LLM Usage Summary:")
print(f"  Local (GLM 4.5 Air): {summary.get('glm-4-air', {}).get('call_count', 0)} calls - $0")
print(f"  Analytical (GLM 4.6): {summary.get('google/glm-4-plus', {}).get('call_count', 0)} calls - ${summary.get('google/glm-4-plus', {}).get('total_cost_usd', 0):.2f}")
print(f"  Deep (Claude): {summary.get('claude-sonnet-4-5', {}).get('call_count', 0)} calls - ${summary.get('claude-sonnet-4-5', {}).get('total_cost_usd', 0):.2f}")
print(f"\nTotal Spent: ${summary['total_cost']:.2f}")
```

### Estimate Before Calling
```python
# Estimate cost before expensive operation
estimated_tokens = 2500
cost = llm.estimate_cost('master_narrator', estimated_tokens)

print(f"This will cost approximately ${cost:.3f}")

# Manual confirmation for expensive calls
if cost > 0.10:
    response = input("Proceed? [y/N]: ")
    if response.lower() != 'y':
        print("Cancelled")
        exit()
```

---

## Example: Complete Deep Session

```python
"""
A complete session showing all systems working together:
1. Shadow work
2. Real practice
3. Multi-tiered LLM calls
4. Meaningful progression
"""

from src.core.orchestrator import TurnOrchestrator
from src.engines.llm_client import LLMClient
from src.engines.shadow_work import ShadowWorkSystem
from src.engines.real_world_bridge import RealWorldBridge
from src.core.config import get_config

# Initialize
config = get_config()
state_manager = StateManager()
llm = LLMClient(config)
shadow_sys = ShadowWorkSystem(state_manager)
bridge = RealWorldBridge(state_manager)

# 1. Player does real meditation (20 minutes in real life)
print("🧘 You meditate for 20 minutes...")
input("Press Enter when you've completed your meditation...")

# 2. Log the practice
practice_result = bridge.complete_session(
    'daily_meditation',
    duration_minutes=20,
    journal_entry="Faced my fear of inadequacy during meditation today..."
)

print(f"✓ Session logged. Streak: {practice_result['current_streak']} days")

# 3. If shadow work is active
enemy_shadow = shadow_sys.SHADOW_LIBRARY['Powerful Enemy']
if enemy_shadow.awareness_level > 3:
    # Quick analytical check for insights
    analysis_prompt = f"""
    The protagonist just meditated and faced their fear of inadequacy.
    Their 'Powerful Enemy' shadow aspect (inner critic) is at awareness {enemy_shadow.awareness_level}/10.

    What insight might arise from today's practice?
    Keep it brief (2-3 sentences).
    """

    insight = llm.analytical_call(analysis_prompt)
    print(f"\n💡 Insight: {insight}")

    # Record breakthrough
    shadow_sys.record_breakthrough(
        enemy_shadow,
        description=insight,
        awareness_gain=1
    )

# 4. If practice unlocked achievement - DEEP NARRATION
if practice_result['achievement_unlocked']:
    print("\n🌟 Achievement Unlocked! Generating deep narration...\n")

    # Build comprehensive context
    practice = bridge.PRACTICE_LIBRARY['daily_meditation']
    shadow_prompt = shadow_sys.generate_shadow_prompt(
        enemy_shadow,
        "You feel the new power settling into your being..."
    )
    practice_prompt = bridge.generate_practice_prompt(practice, practice_result)

    # Combine contexts
    deep_prompt = f"""
    {practice_prompt}

    ADDITIONAL CONTEXT (Shadow Work):
    {shadow_prompt}

    Weave these together: The real practice. The shadow integration. The power unlocking.
    Make it beautiful, true, and transformative.
    """

    # Call Claude (this costs ~$0.08)
    if llm.confirm_expensive_call('master_narrator', 2500):
        narration = llm.deep_call(deep_prompt, max_tokens=2500)

        print(narration.content)
        print(f"\n[Cost: ${narration.cost_usd:.3f}]")
        print(f"[Tokens: {narration.tokens_used}]")
    else:
        print("(Deep narration skipped - cost not approved)")

# 5. Update game state
jumper = state_manager.load_jumper()
print(f"\n📊 Character Update:")
print(f"   Total CP: {jumper.total_cp_earned}")
print(f"   Achievements: {len(state_manager.get_achievements())}")
print(f"   Shadow Integration: {enemy_shadow.integration_level}/10")
```

---

## Best Practices

### When to Use Each Tier

**GLM 4.5 Air (Local):**
- Testing
- Quick exploration
- Routine combat
- Simple calculations
- "What would happen if..."
- **Anytime you don't need depth**

**GLM 4.6 (Analytical):**
- Strategic planning
- Companion interactions
- Power synergy analysis
- World building details
- Complex situations
- **When you need smart, not beautiful**

**Claude Sonnet 4.5 (Deep):**
- Shadow work breakthroughs
- Real practice completion
- Major story beats
- Crisis moments
- Character revelations
- **When it needs to MATTER**

### Cost-Saving Tips

1. **Use local first** - Test with GLM 4.5 Air
2. **Batch deep turns** - Save transformative moments, then do them together
3. **Real practice = worth it** - When you actually DID the meditation, the Claude narration earns its cost
4. **Budget monthly** - Set a limit ($20-50/month) and stay conscious
5. **Quality over quantity** - Better to have 5 deep, meaningful turns than 50 shallow ones

---

## Monthly Budget Example

**Casual Play ($10/month):**
- Unlimited local turns (GLM 4.5 Air)
- ~200 analytical turns (GLM 4.6)
- ~10-15 deep turns (Claude)
- Focus deep turns on real practice completions

**Committed Play ($30/month):**
- Unlimited local
- ~500 analytical turns
- ~30-40 deep turns
- Weekly shadow work sessions with Claude
- All real practices get deep narration

**Transformative Play ($50/month):**
- Full depth experience
- Every meaningful moment gets Claude
- Shadow work as primary focus
- Real practices become the game

**The Point:**
This isn't about min-maxing costs. It's about **choosing where depth matters**.

---

## The Philosophy

This system is designed to be:

1. **A Mirror** - Your character's journey reflects yours
2. **A Practice** - Real meditation unlocks real (and game) powers
3. **A Teacher** - Shadow work integrated into gameplay
4. **A Celebration** - Achievement narrations honor actual growth
5. **A Choice** - You orchestrate the depth

Use it well. Grow with it. Let it be both game and medicine.

---

Next: Read `docs/DEEP_SYSTEM_ARCHITECTURE.md` for the philosophical foundation.
