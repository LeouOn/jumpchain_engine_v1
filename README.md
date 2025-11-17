# Jumpchain Engine V1
**A Game That's Also A Mirror For Growth**

A persistent, multi-LLM powered jumpchain game engine that bridges gameplay with real personal development through shadow work, energy cultivation, and transformative narration.

---

## What Makes This Special

This isn't just a game engine. It's a framework for:

- **Shadow Integration** - Drawbacks become opportunities for psychological growth
- **Real-World Bridging** - Complete actual meditation/practices to unlock in-game powers
- **Three-Tier Intelligence** - Choose your depth: quick local responses, analytical thinking, or profound narration
- **Meaningful Choices** - Decisions that resonate with your actual values
- **Progressive Mastery** - Both in-game AND in real life

### The Core Innovation

**Real practices → Real growth → In-game power**

Meditate for 7 days? Unlock "Inner Stillness" perk + 200 CP.
Face your shadow in journaling? Unlock "Shadow Integration" + drawback mitigation.
Do Qi Gong daily? Unlock "Internal Energy" stat.

**The power is earned, not granted.**

---

## Architecture: Three LLMs, User-Orchestrated

### Tier 1: GLM 4.5 Air (Local via LM Studio)
- **Use for**: Quick turns, calculations, testing
- **Cost**: $0 (runs locally)
- **Speed**: Fast
- **Depth**: Functional

### Tier 2: GLM 4.6 (API via OpenRouter)
- **Use for**: Strategic analysis, companion AI, complex thinking
- **Cost**: ~$0.01-0.05 per turn
- **Speed**: Medium
- **Depth**: Intelligent

### Tier 3: Claude Sonnet 4.5 (API - The Big Guns)
- **Use for**: Transformative narration, shadow work, real practice completion
- **Cost**: ~$0.05-0.15 per deep turn
- **Speed**: Slower
- **Depth**: Profound, literary, psychologically rich

**You choose** when to use which model. Quick turn? Local. Deep breakthrough? Claude.

---

## Features

### Persistent State
- SQLite database stores everything
- Full turn history
- Character progression across sessions
- Achievement tracking
- Shadow work journal

### Power Synergy System
- Automatic detection of perk combinations
- Known synergies: PtV + Blank = 15x, PtV + Transmutation = 10x
- Tag-based discovery for new combos
- Combat power calculation with multipliers

### Shadow Work Integration
- 10+ predefined shadow aspects (Enemy, Addiction, Isolation, etc.)
- Integration progress tracking (0-10)
- Breakthrough moment recording
- Guided exercises for each shadow type
- Mechanical benefits for integration (drawback mitigation at 7/10, transcendence at 10/10)

### Real-World Practice Bridge
- 8 predefined practices (meditation, shadow journaling, Qi Gong, etc.)
- Streak tracking
- Journal integration
- In-game rewards for real completion
- Beautiful Claude narration for achievements

### Achievement System
- Bronze/Silver/Gold/Platinum tiers
- Synergy detection achievements
- Real-world practice achievements
- Speedrun achievements
- Perfect run achievements

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup LLMs

**LM Studio (Local - Free)**
```bash
# Download from https://lmstudio.ai
# Load GLM 4.5 Air
# Start server (localhost:1234)
# Update config/settings.yaml if needed
```

**OpenRouter (API)**
```bash
export OPENROUTER_API_KEY="your-key"
```

**Anthropic (Claude)**
```bash
export ANTHROPIC_API_KEY="your-key"
```

### 3. Initialize Database
```bash
python scripts/init_database.py
```

### 4. Start Your Journey
```python
from src.core.orchestrator import TurnOrchestrator
from src.engines.llm_client import LLMClient
from src.core.config import get_config

config = get_config()
llm = LLMClient(config)
orchestrator = TurnOrchestrator()

# Quick turn (local, free)
result = orchestrator.process_turn("I meditate on the rooftop")

# Analytical turn (GLM 4.6, ~$0.02)
analysis = llm.analytical_call("Analyze optimal strategy against Coil")

# Deep turn (Claude, ~$0.08)
narration = llm.deep_call("Generate beautiful narration for shadow integration moment")
```

---

## Documentation

- **[DEEP_SYSTEM_ARCHITECTURE.md](docs/DEEP_SYSTEM_ARCHITECTURE.md)** - Philosophy, shadow work, energy systems
- **[USAGE_GUIDE.md](docs/USAGE_GUIDE.md)** - Complete examples, practice integration, cost management
- **[IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md)** - Current development status

---

## Example: Real Practice → In-Game Power

```python
from src.engines.real_world_bridge import RealWorldBridge

bridge = RealWorldBridge(state_manager)

# Start daily meditation practice
meditation = bridge.start_practice('daily_meditation')

# After actually meditating in real life for 20 minutes...
result = bridge.complete_session(
    'daily_meditation',
    duration_minutes=20,
    journal_entry="Faced my fear of inadequacy today..."
)

# After 7 days...
if result['achievement_unlocked']:
    # Achievement: "Master of the Inner World"
    # Reward: 200 CP + "Inner Stillness" perk + Mental Clarity +5
    # Real benefit: Improved focus and emotional regulation

    # Generate beautiful narration with Claude
    narration = generate_practice_completion_narration(meditation, result)
    # "You settle onto the rooftop, cross-legged. The city sprawls below,
    #  but you close your eyes and turn inward. The breath deepens...
    #  This power wasn't granted. It was earned. Through practice.
    #  Through showing up, day after day..."
```

---

## Shadow Work Example

```python
from src.engines.shadow_work import ShadowWorkSystem

shadow = ShadowWorkSystem(state_manager)

# Working with the 'Powerful Enemy' drawback as shadow
enemy = shadow.SHADOW_LIBRARY['Powerful Enemy']

# Surface: "A dangerous foe hunts you"
# Deeper: "The inner critic. Self-sabotage. Parts of yourself in conflict."
# Path: "Face the enemy with understanding, not violence."

# Get integration exercise
exercise = shadow.generate_integration_exercise(enemy)
# "Mirror Work: Look into your own eyes. What do you judge?
#  Can you witness without condemning?"

# After doing the exercise...
shadow.record_breakthrough(
    enemy,
    description="Realized my 'enemy' is my internalized perfectionism",
    awareness_gain=2,
    integration_gain=1
)

# Progress: 5/10 awareness, 3/10 integration
# At 7/10: Drawback penalty reduced 50%
# At 10/10: Drawback becomes a strength, keep the CP
```

---

## Project Structure

```
jumpchain_engine_v1/
├── config/
│   ├── settings.yaml              # LLM endpoints, gameplay settings
│   └── achievements.json          # Achievement definitions
├── data/
│   ├── jumpchain.db              # SQLite database
│   ├── llm_usage.json            # Cost tracking
│   ├── real_world_practices.json # Practice progress
│   └── practice_journal.jsonl    # Journal entries
├── docs/
│   ├── DEEP_SYSTEM_ARCHITECTURE.md  # Philosophy & design
│   └── USAGE_GUIDE.md                # Complete usage examples
├── src/
│   ├── core/
│   │   ├── models.py              # Data models
│   │   ├── state_manager.py      # Database interface
│   │   ├── config.py              # Configuration loader
│   │   └── orchestrator.py       # Main game loop
│   ├── engines/
│   │   ├── calculation.py         # Synergy detection, power calculation
│   │   ├── llm_client.py         # Multi-LLM client
│   │   ├── shadow_work.py        # Shadow integration system
│   │   └── real_world_bridge.py  # Practice → game bridge
│   ├── parsers/
│   │   └── jump_doc_parser.py    # Parse jumpchain PDFs
│   └── ui/
│       └── cli.py                 # Terminal interface
├── scripts/
│   ├── init_database.py           # Setup script
│   └── test_phase2.py            # Testing
└── schema.sql                     # Database schema
```

---

## Testing

```bash
# Test core mechanics
python scripts/test_phase2.py

# All tests should pass:
# ✓ Calculation Engine (synergy detection, power calculation)
# ✓ Jump Parser (PDF parsing, perk extraction)
# ✓ Turn Orchestrator (turn processing, achievements)
# ✓ Configuration (settings loading)
```

---

## Cost Management

### Monthly Budget Examples

**Casual ($10/month):**
- Unlimited local turns
- ~200 analytical turns
- ~10-15 deep turns
- Focus Claude on real practices

**Committed ($30/month):**
- ~500 analytical turns
- ~30-40 deep turns
- Weekly shadow work with Claude
- All practices get deep narration

**Transformative ($50/month):**
- Full depth experience
- Every meaningful moment gets Claude
- Shadow work as primary focus
- Game becomes practice

### Track Your Spending
```python
llm = LLMClient(config)
summary = llm.get_usage_summary()
print(f"Total spent this month: ${summary['total_cost']:.2f}")
```

---

## Philosophy

From the [Deep System Architecture](docs/DEEP_SYSTEM_ARCHITECTURE.md):

> This isn't just a game. It's a framework for:
> - Shadow Integration: Drawbacks as aspects to integrate
> - Real Achievement Bridging: Game accomplishments reflect real growth
> - Energy Work: Cultivation practices embedded in gameplay
> - Meaningful Choice: Decisions that resonate with actual values
> - Progressive Mastery: Systematic growth across multiple domains

**The goal isn't escapism. The goal is using game structure to support real development.**

---

## Implementation Status

**Phase 1: Foundation** ✅ COMPLETE
- Database, models, state management
- Configuration system
- CLI interface

**Phase 2: Core Mechanics** ✅ COMPLETE
- Calculation engine (synergies, power tiers, CP budgets)
- Jump document parser
- Turn orchestrator
- Achievement system

**Phase 2.5: Deep Systems** ✅ COMPLETE
- Three-tier LLM client (local, analytical, deep)
- Shadow work integration
- Real-world practice bridge
- Cost tracking and management

**Phase 3: Full Integration** (In Progress)
- Polish deep narration prompts
- Expand shadow work library
- Add more real-world practices
- Comprehensive testing with actual use

---

## Contributing

This is a personal development project, but I'm happy to discuss:
- Additional shadow work patterns
- Real-world practice ideas
- Synergy combinations
- Narrative techniques

---

## License

MIT License - Use it, modify it, grow with it.

---

## Acknowledgments

Built for exploring:
- How games can support real personal development
- Multi-agent AI coordination
- Shadow integration through narrative
- The bridge between virtual and real growth

**May you find both power and wisdom in your journey.**

---

## Next Steps

1. Read [DEEP_SYSTEM_ARCHITECTURE.md](docs/DEEP_SYSTEM_ARCHITECTURE.md) for the philosophy
2. Read [USAGE_GUIDE.md](docs/USAGE_GUIDE.md) for detailed examples
3. Set up your LLM endpoints
4. Start a practice (meditation, shadow journaling, Qi Gong)
5. Let the game mirror your growth

**This is where game becomes practice. Where practice becomes power.**
