# Jumpchain Engine V1

A persistent, multi-LLM powered jumpchain game engine with state management, companion AI, background simulation, and gamification.

## Features

- **Persistent State**: SQLite database stores all progress, perks, companions, and world state
- **Multi-LLM Architecture**: Specialized models for different tasks:
  - **Narration** (Claude Sonnet 4.5): Main story and dialogue
  - **Calculation** (DeepSeek R1): CP optimization, synergy detection
  - **Background Simulation** (Qwen 2.5): Off-screen events, NPC actions
  - **Companion AI** (Gemma 2): Companion personalities and responses
- **Automated Power Synergy Detection**: Discovers and suggests creative perk combinations
- **Dynamic World Simulation**: Background events continue even when you're not acting
- **Gamification System**: Bronze/Silver/Gold/Platinum achievements with CP rewards
- **Companion System**: Persistent companions with personalities, goals, and relationship tracking
- **Jump Document Parser**: Automatically parse jumpchain PDFs for perks, items, scenarios

## Architecture

```
jumpchain-engine/
├── config/               # Configuration files
│   ├── settings.yaml     # LLM endpoints, gameplay settings
│   └── achievements.json # Achievement definitions
├── data/                 # Data directory
│   ├── jumpchain.db      # SQLite database
│   └── jump_docs/        # Jump document PDFs
├── src/
│   ├── core/             # Core game logic
│   │   ├── models.py     # Data models
│   │   └── state_manager.py  # Database operations
│   ├── engines/          # AI engines
│   │   ├── calculation.py    # Mechanics calculations
│   │   ├── background_sim.py # Background simulation
│   │   ├── companion_ai.py   # Companion generation
│   │   ├── narration.py      # Main narration
│   │   └── world_builder.py  # World population
│   ├── parsers/          # Document parsers
│   ├── rewards/          # Achievement system
│   └── ui/               # User interface
└── schema.sql            # Database schema

```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd jumpchain_engine_v1
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure LLM endpoints**:
   Edit `config/settings.yaml` to set your LLM API endpoints and keys.

4. **Initialize database**:
   ```bash
   python scripts/init_database.py
   ```

## Quick Start

```bash
# Start the engine
python -m src.ui.cli

# Or use the main script (once implemented)
python jumpchain.py start
```

## Configuration

### LLM Endpoints

Edit `config/settings.yaml` to configure your LLM endpoints:

```yaml
llm_endpoints:
  narration:
    model: "claude-sonnet-4-5"
    endpoint: "http://localhost:5000/v1/chat/completions"
    api_key: ""  # Or set CLAUDE_API_KEY environment variable
```

For local LLMs (Strix Halo, etc.), point endpoints to your local inference server.

### Gameplay Settings

```yaml
gameplay:
  tone: "serious_comedy"  # serious_comedy, dark, heroic, absurdist
  difficulty: "balanced"  # easy, balanced, hard, brutal
  base_cp: 1000
  companion_cp: 600
```

## Usage Examples

### Starting a New Jump

```python
from src.core.state_manager import StateManager
from src.engines.world_builder import WorldBuilder

# Initialize
state = StateManager()
builder = WorldBuilder()

# Build world from jump doc
world = builder.build_world("Worm", "data/jump_docs/worm.pdf")
state.save_world_state(world)
```

### Processing a Turn

```python
from src.core.orchestrator import TurnOrchestrator

orchestrator = TurnOrchestrator()

# Player action
action = "Use PtV to find optimal infiltration route into Coil's base"

# Process turn (calculates mechanics, generates background events, companion responses, narration)
result = orchestrator.process_turn(action)

print(result['narration'])
```

### Checking Synergies

```python
from src.engines.calculation import CalculationEngine

calc = CalculationEngine()
perks = state.get_active_perks(jumper_id=1, owner_type='jumper')

synergies = calc.detect_synergies(perks)
for syn in synergies:
    print(f"{' + '.join(syn.perks)} = {syn.multiplier}x")
    print(f"  {syn.description}")
```

## Database Schema

The engine uses SQLite with the following key tables:

- `jumper`: Core character state (CP, location, etc.)
- `perks`: All perks with synergy tags and mechanics
- `companions`: Companion state with personalities
- `world_state`: Current jump world state
- `background_events`: Off-screen events log
- `rewards`: Earned achievements
- `turn_log`: Complete turn history for replay

## Development Roadmap

### Phase 1: Foundation ✅
- [x] Database schema
- [x] State Manager
- [x] Data models
- [x] Configuration system

### Phase 2: Core Mechanics (In Progress)
- [ ] Calculation Engine
- [ ] Jump doc parser
- [ ] Basic turn loop
- [ ] CLI interface

### Phase 3: AI Integration
- [ ] Companion AI module
- [ ] Background Simulator
- [ ] Narration Engine
- [ ] LLM orchestration

### Phase 4: World Building
- [ ] WorldBuilder module
- [ ] Wiki scraper
- [ ] Timeline generation

### Phase 5: Gamification
- [ ] Achievement detection
- [ ] Reward system
- [ ] Progression tracking

### Phase 6: Polish
- [ ] UI improvements
- [ ] Testing suite
- [ ] Balance tuning
- [ ] Documentation

## Contributing

This is a personal project, but suggestions and feedback are welcome!

## License

MIT License (or your preferred license)

## Acknowledgments

- Built for testing AI agentic workflows
- Inspired by the jumpchain community
- Powered by multiple specialized LLMs working in concert
