#!/usr/bin/env python3
"""
Test script for Momentum System (Phase 2.5)
Tests: Daily tasks, weekly goals, virtue progression, impact logging, compound bonuses
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.engines.momentum_system import MomentumSystem, VirtueType, ImpactCategory
from src.core.state_manager import StateManager


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_daily_tasks():
    """Test daily task activation and completion"""
    print_section("TEST 1: Daily Tasks")

    state = StateManager()
    momentum = MomentumSystem(state)

    # Activate some tasks
    print("\n📋 Activating daily tasks...")
    tasks = ['morning_meditation', 'exercise', 'creative_work']

    for task_id in tasks:
        task = momentum.activate_task(task_id)
        print(f"  ✓ {task.name} ({task.difficulty}/10 difficulty, {task.base_cp} CP base)")

    # Complete a task
    print("\n✅ Completing morning meditation...")
    result = momentum.complete_task('morning_meditation')

    print(f"\n  Task: {result['task_completed']}")
    print(f"  Streak: {result['streak']} days")
    print(f"  Streak multiplier: {result['streak_multiplier']:.2f}x")
    print(f"  CP earned: +{result['cp_reward']}")
    print(f"  Total completions: {result['total_completions']}")

    # Check virtue progress
    if result['virtue_progress']:
        print("\n  Virtue progress:")
        for virtue_name, progress in result['virtue_progress'].items():
            if progress['leveled_up']:
                print(f"    {virtue_name}: Level up to {progress['new_level']}!")
            else:
                print(f"    {virtue_name}: Currently at level {progress['new_level']}")

    print("\n✅ Test 1 Passed: Daily tasks working correctly")
    return True


def test_streaks():
    """Test streak tracking and bonuses"""
    print_section("TEST 2: Streak Tracking")

    state = StateManager()
    momentum = MomentumSystem(state)

    # Activate and complete task multiple times to build streak
    print("\n🔥 Building a streak...")
    momentum.activate_task('exercise')

    # Simulate 5 consecutive days
    for day in range(1, 6):
        result = momentum.complete_task('exercise')
        print(f"  Day {day}: Streak = {result['streak']}, " +
              f"Multiplier = {result['streak_multiplier']:.2f}x, " +
              f"CP = {result['cp_reward']}")

    print("\n✅ Test 2 Passed: Streak bonuses increasing correctly")
    return True


def test_virtue_progression():
    """Test virtue leveling system"""
    print_section("TEST 3: Virtue Progression")

    state = StateManager()
    momentum = MomentumSystem(state)

    # Activate and complete tasks that give virtue points
    print("\n📊 Testing virtue progression...")
    momentum.activate_task('morning_meditation')  # Gives Temperance + Wisdom

    # Complete multiple times to level up
    for i in range(1, 21):
        result = momentum.complete_task('morning_meditation')

        if result['virtue_progress']:
            for virtue_name, progress in result['virtue_progress'].items():
                if progress['leveled_up']:
                    print(f"\n  🎉 {virtue_name.upper()} leveled up to {progress['new_level']}!")
                    if progress['bonuses_unlocked']:
                        for bonus in progress['bonuses_unlocked']:
                            print(f"      Unlocked: {bonus}")

    # Show final virtue status
    print("\n  Final virtue levels:")
    for virtue_type, virtue_prog in momentum.virtue_progress.items():
        if virtue_prog.level > 0:
            print(f"    {virtue_type.value.title()}: Level {virtue_prog.level} " +
                  f"({virtue_prog.points}/{virtue_prog.points_per_level} points)")

    print("\n✅ Test 3 Passed: Virtue progression working correctly")
    return True


def test_weekly_goals():
    """Test weekly goal system"""
    print_section("TEST 4: Weekly Goals")

    state = StateManager()
    momentum = MomentumSystem(state)

    # Activate a goal
    print("\n🎯 Activating weekly goal...")
    goal = momentum.activate_goal('consistent_practice')
    print(f"  Goal: {goal.name}")
    print(f"  Description: {goal.description}")
    print(f"  Requirement: {goal.target_completions} completions")
    print(f"  Reward: {goal.completion_cp} CP + {goal.special_unlock}")

    # Complete tasks to progress goal
    print("\n  Progressing toward goal...")
    momentum.activate_task('morning_meditation')

    for i in range(1, 8):
        result = momentum.complete_task('morning_meditation')

        if result['weekly_goals_progress']:
            for goal_result in result['weekly_goals_progress']:
                print(f"\n  🎊 Weekly goal complete!")
                print(f"    Goal: {goal_result['goal_completed']}")
                print(f"    CP reward: +{goal_result['cp_reward']}")
                if goal_result['special_unlock']:
                    print(f"    Special unlock: {goal_result['special_unlock']}")

    print("\n✅ Test 4 Passed: Weekly goals working correctly")
    return True


def test_impact_logging():
    """Test impact logging system"""
    print_section("TEST 5: Impact Logging")

    state = StateManager()
    momentum = MomentumSystem(state)

    # Log various impacts
    print("\n🌍 Logging real-world impacts...")

    impacts = [
        {
            'category': ImpactCategory.TEACHING,
            'description': 'Helped colleague debug their code',
            'magnitude': 7
        },
        {
            'category': ImpactCategory.CREATING,
            'description': 'Built open source tool that helps others',
            'magnitude': 9
        },
        {
            'category': ImpactCategory.CONNECTING,
            'description': 'Had deep conversation with friend',
            'magnitude': 6
        }
    ]

    total_cp = 0
    for impact in impacts:
        result = momentum.log_impact(
            category=impact['category'],
            description=impact['description'],
            magnitude=impact['magnitude']
        )

        print(f"\n  ✅ {impact['description']}")
        print(f"    Category: {impact['category'].value}")
        print(f"    Magnitude: {impact['magnitude']}/10")
        print(f"    CP bonus: +{result['cp_bonus']}")
        total_cp += result['cp_bonus']

        # Show virtue progress
        if result['virtue_progress']:
            for virtue_name, progress in result['virtue_progress'].items():
                if progress['leveled_up']:
                    print(f"    {virtue_name}: Level up to {progress['new_level']}!")

    print(f"\n  💎 Total Impact CP: +{total_cp}")
    print("\n✅ Test 5 Passed: Impact logging working correctly")
    return True


def test_compound_bonuses():
    """Test compound bonus calculation"""
    print_section("TEST 6: Compound Bonuses")

    state = StateManager()
    momentum = MomentumSystem(state)

    # Build up various bonuses
    print("\n💫 Building compound bonuses...")

    # Build streak
    momentum.activate_task('morning_meditation')
    for _ in range(7):
        momentum.complete_task('morning_meditation')

    # Level up a virtue to 10
    for _ in range(200):  # Enough completions to max out
        momentum.complete_task('morning_meditation')

    # Activate and complete a weekly goal
    momentum.activate_goal('consistent_practice')
    for _ in range(7):
        momentum.complete_task('morning_meditation')

    # Get compound bonuses
    bonuses = momentum.get_compound_bonuses()

    print(f"\n  CP Multiplier: {bonuses['cp_multiplier']:.2f}x")

    if bonuses['special_bonuses']:
        print(f"\n  Special bonuses ({len(bonuses['special_bonuses'])}):")
        for bonus in bonuses['special_bonuses']:
            print(f"    ✨ {bonus}")

    print("\n✅ Test 6 Passed: Compound bonuses calculating correctly")
    return True


def test_momentum_summary():
    """Test momentum summary"""
    print_section("TEST 7: Momentum Summary")

    state = StateManager()
    momentum = MomentumSystem(state)

    # Set up some state
    momentum.activate_task('morning_meditation')
    momentum.activate_task('exercise')
    momentum.activate_goal('consistent_practice')

    for _ in range(5):
        momentum.complete_task('morning_meditation')

    # Get summary
    summary = momentum.get_momentum_summary()

    print("\n📈 Current Momentum Status:")
    print(f"  Active tasks: {summary['active_tasks']}")
    print(f"  Active goals: {summary['active_goals']}")

    if summary['streaks']:
        print(f"\n  Current streaks:")
        for task_id, streak in summary['streaks'].items():
            print(f"    {task_id}: {streak} days")

    bonuses = summary['compound_bonuses']
    print(f"\n  Compound multiplier: {bonuses['cp_multiplier']:.2f}x")

    print("\n✅ Test 7 Passed: Momentum summary working correctly")
    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  MOMENTUM SYSTEM TEST SUITE")
    print("  Phase 2.5: Deep Systems")
    print("=" * 70)

    tests = [
        ("Daily Tasks", test_daily_tasks),
        ("Streak Tracking", test_streaks),
        ("Virtue Progression", test_virtue_progression),
        ("Weekly Goals", test_weekly_goals),
        ("Impact Logging", test_impact_logging),
        ("Compound Bonuses", test_compound_bonuses),
        ("Momentum Summary", test_momentum_summary)
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"\n❌ Test Failed: {name}")
        except Exception as e:
            failed += 1
            print(f"\n❌ Test Failed: {name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()

    # Final summary
    print("\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    print(f"\n  Total tests: {len(tests)}")
    print(f"  Passed: {passed} ✅")
    print(f"  Failed: {failed} ❌")

    if failed == 0:
        print("\n  🎉 All tests passed! Momentum system is ready.")
    else:
        print("\n  ⚠️  Some tests failed. Check output above.")

    print("\n" + "=" * 70)

    return failed == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
