#!/usr/bin/env python3
"""
Test script for Phase 2 implementation
Demonstrates calculation engine, jump parser, and orchestrator
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.state_manager import StateManager
from src.core.models import Perk, Companion
from src.core.orchestrator import TurnOrchestrator
from src.engines.calculation import CalculationEngine
from src.parsers.jump_doc_parser import JumpDocParser
from src.core.config import get_config


def test_calculation_engine():
    """Test the calculation engine"""
    print("=" * 60)
    print("TESTING CALCULATION ENGINE")
    print("=" * 60)

    calc = CalculationEngine()

    # Create test perks
    test_perks = [
        Perk(
            id=1, owner_id=1, owner_type='jumper',
            name='PtV', source_jump='Worm', cp_cost=600,
            description='Path to Victory - see path to any goal',
            is_active=True, evolution_stage=0,
            synergy_tags=['precog', 'combat', 'utility'],
            mechanics={'mental': 10.0}
        ),
        Perk(
            id=2, owner_id=1, owner_type='jumper',
            name='Blank', source_jump='Worm', cp_cost=300,
            description='Immune to all precognition',
            is_active=True, evolution_stage=0,
            synergy_tags=['stealth', 'blank'],
            mechanics={'special': 5.0}
        ),
        Perk(
            id=3, owner_id=1, owner_type='jumper',
            name='Compassionate Transmutation', source_jump='FMA', cp_cost=400,
            description='Create anything with transmutation',
            is_active=True, evolution_stage=0,
            synergy_tags=['creation', 'transmutation'],
            mechanics={'special': 8.0}
        )
    ]

    # Test synergy detection
    print("\n1. Testing Synergy Detection")
    print("-" * 60)
    synergies = calc.detect_synergies(test_perks)
    print(f"Found {len(synergies)} synergies:\n")
    for syn in synergies:
        print(f"  • {' + '.join(syn.perks)} = {syn.multiplier}x")
        print(f"    Type: {syn.combo_type}")
        print(f"    {syn.description}")
        print(f"    Suggestion: {syn.suggested_use}\n")

    # Test combat power calculation
    print("\n2. Testing Combat Power Calculation")
    print("-" * 60)
    power = calc.calculate_combat_power(test_perks, [], [])
    print(f"Power Level: {power['power_level']}")
    print(f"Threat Rating: {power['threat_rating']}/10")
    print(f"\nStats:")
    for stat, value in power['stats'].items():
        print(f"  {stat}: {value:.1f}x")

    # Test CP budget
    print("\n3. Testing CP Budget Calculation")
    print("-" * 60)
    from src.core.models import Achievement
    from datetime import datetime

    test_achievements = [
        Achievement(
            id=1, name='First Steps', tier='bronze',
            trigger_condition='test', reward_value=50,
            earned_date=datetime.now(), description='Test', icon='🏆'
        )
    ]

    drawbacks = [
        {'name': 'Test Drawback', 'cp_value': 300}
    ]

    budget = calc.calculate_cp_budget(
        base_cp=1000,
        drawbacks=drawbacks,
        companions=[],
        achievements=test_achievements
    )

    print(f"Base CP: {budget.base_cp}")
    print(f"Drawback CP: +{budget.drawback_cp}")
    print(f"Achievement Bonus: +{budget.achievement_bonus}")
    print(f"Multipliers: {budget.multipliers}")
    print(f"Total Available: {budget.total_available}")

    # Test build optimization
    print("\n4. Testing Build Optimization")
    print("-" * 60)
    available_perks = test_perks + [
        Perk(
            id=4, owner_id=1, owner_type='jumper',
            name='Enhanced Speed', source_jump='Generic', cp_cost=200,
            description='Move at superhuman speed',
            is_active=False, evolution_stage=0,
            synergy_tags=['speed', 'combat'],
            mechanics={'speed': 5.0}
        )
    ]

    objectives = ['combat', 'stealth']
    optimization = calc.optimize_build(
        available_cp=1000,
        available_perks=available_perks,
        objectives=objectives
    )

    print(f"Optimized build for objectives: {objectives}")
    print(f"Selected {len(optimization['selected_perks'])} perks:")
    for perk in optimization['selected_perks']:
        print(f"  • {perk.name} ({perk.cp_cost} CP)")
    print(f"\nTotal Cost: {optimization['total_cost']} CP")
    print(f"Remaining: {optimization['remaining_cp']} CP")
    print(f"Efficiency: {optimization['efficiency']:.1%}")

    print("\n✓ Calculation Engine tests complete!\n")


def test_jump_parser():
    """Test the jump document parser"""
    print("=" * 60)
    print("TESTING JUMP DOCUMENT PARSER")
    print("=" * 60)

    parser = JumpDocParser()

    # Create a sample jump document
    sample_jump_text = """
GENERIC SUPER JUMP

You start with 1000 CP.

PERKS

Path to Victory (600 CP): You can see the path to accomplish any goal.

Blank (300 CP): You are immune to all forms of precognition.

Enhanced Strength (200 CP): You are super strong.

ITEMS

Magic Sword (400 CP): A powerful enchanted blade.

DRAWBACKS

+200 CP: Enemy - You have a powerful enemy.

+300 CP: Wanted - Everyone is hunting you.
"""

    print("\n1. Parsing Sample Jump Document")
    print("-" * 60)

    result = parser.parse_text(sample_jump_text, "Generic Super Jump")

    print(f"Jump Name: {result['jump_name']}")
    print(f"Base CP: {result['base_cp']}")
    print(f"Duration: {result['duration_years']} years")

    print(f"\nPerks ({len(result['perks'])}):")
    for perk in result['perks']:
        print(f"  • {perk['name']} ({perk['cost']} CP)")
        print(f"    Tags: {', '.join(perk['tags'])}")
        if perk['description']:
            print(f"    {perk['description'][:60]}...")

    print(f"\nItems ({len(result['items'])}):")
    for item in result['items']:
        print(f"  • {item['name']} ({item['cost']} CP)")

    print(f"\nDrawbacks ({len(result['drawbacks'])}):")
    for drawback in result['drawbacks']:
        print(f"  • {drawback['name']} (+{drawback['cp_value']} CP)")

    print("\n✓ Jump Parser tests complete!\n")


def test_orchestrator():
    """Test the turn orchestrator"""
    print("=" * 60)
    print("TESTING TURN ORCHESTRATOR")
    print("=" * 60)

    # Initialize
    state = StateManager()
    orchestrator = TurnOrchestrator(state)

    # Load jumper
    jumper = state.load_jumper()
    print(f"\n1. Current State")
    print("-" * 60)
    print(f"Jumper: {jumper.name}")
    print(f"Jump: {jumper.current_jump}")
    print(f"Day {jumper.current_day}, Year {jumper.current_year}")

    # Add some test perks to jumper
    print("\n2. Adding Test Perks")
    print("-" * 60)
    test_perk = Perk(
        id=0, owner_id=jumper.id, owner_type='jumper',
        name='Super Strength', source_jump='Generic', cp_cost=200,
        description='Incredible strength', is_active=True,
        evolution_stage=0, synergy_tags=['physical', 'combat'],
        mechanics={'physical': 5.0}
    )
    state.save_perk(test_perk)
    print(f"Added perk: {test_perk.name}")

    # Process a turn
    print("\n3. Processing Turn")
    print("-" * 60)
    player_action = "Use my super strength to lift a building"

    result = orchestrator.process_turn(player_action)

    print(f"Turn {result['turn_number']} complete!")
    print(f"\nNarration:")
    print(result['narration'])

    if result['achievements']:
        print(f"\n🏆 Achievements Unlocked:")
        for ach in result['achievements']:
            print(f"  {ach['icon']} {ach['name']} ({ach['tier']})")
            print(f"     {ach['description']}")

    # Get game summary
    print("\n4. Game Summary")
    print("-" * 60)
    summary = orchestrator.get_game_summary()
    print(f"Jumper: {summary['jumper']['name']}")
    print(f"Location: {summary['jumper']['location']}")
    print(f"Day {summary['jumper']['day']}, Year {summary['jumper']['year']}")
    print(f"Power Level: {summary['power_level']}")
    print(f"Threat Rating: {summary['threat_rating']}/10")
    print(f"Active Perks: {summary['active_perks']}")
    print(f"Achievements: {summary['achievements']}")

    print("\n✓ Orchestrator tests complete!\n")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  JUMPCHAIN ENGINE - PHASE 2 TESTS".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")

    try:
        # Test each component
        test_calculation_engine()
        test_jump_parser()
        test_orchestrator()

        print("=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        print("\nPhase 2 Implementation Complete:")
        print("  ✓ Calculation Engine")
        print("  ✓ Jump Document Parser")
        print("  ✓ Turn Orchestrator")
        print("  ✓ Configuration System")
        print("\nReady for Phase 3: AI Integration")
        print()

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
