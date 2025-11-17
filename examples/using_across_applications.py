"""
Example: Using the Jumpchain Engine systems across different applications

This shows how the modular design allows reuse in:
- Personal dashboard apps
- Habit tracking systems
- Creative writing tools
- Learning management systems
- Therapeutic journaling apps
- etc.
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.engines.llm_providers import (
    UniversalLLMClient, ZAIProvider, LMStudioProvider,
    OpenRouterProvider, AnthropicProvider
)
from src.engines.momentum_system import MomentumSystem, ImpactCategory
from src.engines.shadow_work import ShadowWorkSystem
from src.engines.real_world_bridge import RealWorldBridge
from src.core.state_manager import StateManager


# ============================================================================
# EXAMPLE 1: Personal Growth Dashboard
# ============================================================================

def personal_growth_dashboard():
    """
    A daily dashboard showing:
    - Current streaks
    - Virtue progress
    - Weekly goal status
    - Impact log summary
    """
    print("=" * 60)
    print("PERSONAL GROWTH DASHBOARD".center(60))
    print("=" * 60)

    state = StateManager()
    momentum = MomentumSystem(state)
    bridge = RealWorldBridge(state)

    # Activate some tasks
    momentum.activate_task('morning_meditation')
    momentum.activate_task('exercise')
    momentum.activate_task('creative_work')
    momentum.activate_task('act_of_kindness')

    # Activate a goal
    momentum.activate_goal('consistent_practice')

    # Complete a task
    result = momentum.complete_task('morning_meditation')

    print(f"\n✅ {result['task_completed']}")
    print(f"   Streak: {result['streak']} days (multiplier: {result['streak_multiplier']:.2f}x)")
    print(f"   CP earned: +{result['cp_reward']}")
    print(f"   Total completions: {result['total_completions']}")

    # Show virtue progress
    print("\n📊 Virtue Progress:")
    for virtue_name, progress in result['virtue_progress'].items():
        if progress['leveled_up']:
            print(f"   🎉 {virtue_name.upper()} leveled up to {progress['new_level']}!")
            for bonus in progress['bonuses_unlocked']:
                print(f"      Unlocked: {bonus}")

    # Show summary
    summary = momentum.get_momentum_summary()
    print(f"\n📈 Momentum Summary:")
    print(f"   Active tasks: {summary['active_tasks']}")
    print(f"   Active goals: {summary['active_goals']}")

    if summary['streaks']:
        print(f"\n🔥 Current Streaks:")
        for task_id, streak in summary['streaks'].items():
            print(f"   {task_id}: {streak} days")

    # Compound bonuses
    bonuses = summary['compound_bonuses']
    print(f"\n💫 Compound Bonuses:")
    print(f"   CP Multiplier: {bonuses['cp_multiplier']:.2f}x")
    if bonuses['special_bonuses']:
        for bonus in bonuses['special_bonuses']:
            print(f"   ✨ {bonus}")


# ============================================================================
# EXAMPLE 2: Habit Tracker with AI Coaching
# ============================================================================

def habit_tracker_with_ai():
    """
    Habit tracker that uses AI to:
    - Provide encouragement
    - Suggest next actions
    - Reflect on progress
    """
    print("\n" + "=" * 60)
    print("AI-POWERED HABIT TRACKER".center(60))
    print("=" * 60)

    # Setup LLM client with fallback
    llm_client = UniversalLLMClient()

    # Add providers
    llm_client.add_provider('local', LMStudioProvider())
    llm_client.add_provider('z.ai', ZAIProvider(api_key="your-key"))

    # Set fallback order (local first, then Z.AI)
    llm_client.set_fallback_order(['local', 'z.ai'])

    # Setup momentum
    state = StateManager()
    momentum = MomentumSystem(state)

    # Get summary
    summary = momentum.get_momentum_summary()

    # Generate AI insight
    prompt = f"""
    The user has:
    - {summary['active_tasks']} active daily tasks
    - Current streaks: {summary['streaks']}
    - Compound bonus multiplier: {summary['compound_bonuses']['cp_multiplier']}x

    Provide brief, encouraging feedback and suggest what they should focus on today.
    Keep it under 100 words.
    """

    try:
        response = llm_client.call(prompt, provider='local', max_tokens=200)
        print(f"\n🤖 AI Coach says:")
        print(f"   {response.content}")
        print(f"\n   [Using: {response.provider}, {response.tokens_used} tokens, ${response.cost_usd:.4f}]")
    except Exception as e:
        print(f"\n⚠️ AI unavailable: {e}")


# ============================================================================
# EXAMPLE 3: Creative Writing Assistant
# ============================================================================

def creative_writing_assistant():
    """
    Use the system to:
    - Track writing sessions
    - Build creative momentum
    - Get AI feedback on work
    """
    print("\n" + "=" * 60)
    print("CREATIVE WRITING ASSISTANT".center(60))
    print("=" * 60)

    state = StateManager()
    momentum = MomentumSystem(state)

    # Activate creative task
    task = momentum.activate_task('creative_work')

    print(f"\n📝 Task: {task.name}")
    print(f"   {task.description}")
    print(f"   Difficulty: {task.difficulty}/10")
    print(f"   Reward: {task.base_cp} CP base")

    # Complete writing session
    result = momentum.complete_task('creative_work', duration_minutes=45)

    print(f"\n✅ Session Complete!")
    print(f"   Time: 45 minutes")
    print(f"   Streak: {result['streak']} days")
    print(f"   CP earned: +{result['cp_reward']} (with {result['streak_multiplier']:.2f}x streak bonus)")

    # Check weekly goal
    if result['weekly_goals_progress']:
        for goal_result in result['weekly_goals_progress']:
            print(f"\n🎯 Weekly Goal Complete: {goal_result['goal_completed']}")
            print(f"   Bonus CP: +{goal_result['cp_reward']}")
            if goal_result['special_unlock']:
                print(f"   🌟 Unlocked: {goal_result['special_unlock']}")

    # AI feedback (using Z.AI for deeper analysis)
    llm_client = UniversalLLMClient()
    llm_client.add_provider('z.ai', ZAIProvider(api_key="your-key"))
    llm_client.set_fallback_order(['z.ai'])

    prompt = f"""
    A writer just completed a {result['streak']} day writing streak.
    They've written for 45 minutes today.

    Provide brief, inspiring encouragement (2-3 sentences).
    """

    try:
        response = llm_client.call(
            prompt,
            model="glm-4.6",  # Use more powerful model for creativity
            temperature=0.8,
            max_tokens=150
        )
        print(f"\n✨ Inspiration:")
        print(f"   {response.content}")
    except:
        print("\n✨ Keep the momentum going! Every day of practice builds your craft.")


# ============================================================================
# EXAMPLE 4: Impact Tracker (Doing Good in the World)
# ============================================================================

def impact_tracker():
    """
    Track real-world impact and see compound benefits
    """
    print("\n" + "=" * 60)
    print("IMPACT TRACKER - DOING GOOD".center(60))
    print("=" * 60)

    state = StateManager()
    momentum = MomentumSystem(state)

    # Log various impacts
    impacts = [
        {
            'category': ImpactCategory.TEACHING,
            'description': 'Helped colleague debug their code for 30 minutes',
            'magnitude': 6
        },
        {
            'category': ImpactCategory.SERVING,
            'description': 'Volunteered at food bank',
            'magnitude': 8
        },
        {
            'category': ImpactCategory.CREATING,
            'description': 'Built open source tool that helps others',
            'magnitude': 9
        },
        {
            'category': ImpactCategory.CONNECTING,
            'description': 'Had deep conversation with friend going through hard time',
            'magnitude': 7
        }
    ]

    print("\n📝 Logging impacts...")

    total_cp = 0
    for impact in impacts:
        result = momentum.log_impact(
            category=impact['category'],
            description=impact['description'],
            magnitude=impact['magnitude']
        )

        print(f"\n✅ {impact['description']}")
        print(f"   Magnitude: {impact['magnitude']}/10")
        print(f"   CP bonus: +{result['cp_bonus']}")
        total_cp += result['cp_bonus']

        # Show virtue progress
        for virtue_name, progress in result['virtue_progress'].items():
            if progress['leveled_up']:
                print(f"   🎉 {virtue_name.upper()} → Level {progress['new_level']}!")

    print(f"\n💎 Total Impact CP: +{total_cp}")
    print(f"\n🌍 You're making a difference. Keep going.")


# ============================================================================
# EXAMPLE 5: Therapeutic Journaling with Shadow Work
# ============================================================================

def therapeutic_journaling():
    """
    Combine journaling with shadow work integration
    """
    print("\n" + "=" * 60)
    print("THERAPEUTIC JOURNALING".center(60))
    print("=" * 60)

    state = StateManager()
    shadow = ShadowWorkSystem(state)

    # Working with a shadow
    enemy = shadow.SHADOW_LIBRARY['Powerful Enemy']

    print(f"\n🌑 Shadow Aspect: {enemy.drawback_name}")
    print(f"   Surface: {enemy.surface_description}")
    print(f"   Deeper: {enemy.shadow_meaning}")
    print(f"   Path: {enemy.integration_path}")

    # Get exercise
    exercise = shadow.generate_integration_exercise(enemy)

    print(f"\n📋 Today's Exercise: {exercise['exercise']['name']}")
    print(f"   {exercise['exercise']['instructions']}")
    print(f"   Duration: {exercise['exercise']['duration']}")

    # Simulate doing the exercise and journaling
    journal_entry = """
    Looked in the mirror today. Really looked.

    The self-judgment is... intense. "Not good enough" plays on repeat.
    But I'm starting to see it's not TRUTH - it's just a voice. A scared voice.

    What if this inner critic is trying to protect me by keeping me small?
    "If you don't try, you can't fail." That's the logic.

    But that's not living. That's just... not dying.

    I want to live. Even if it means risking failure.
    """

    print(f"\n📝 Journal Entry:")
    print(journal_entry)

    # Record breakthrough
    shadow.record_breakthrough(
        enemy,
        description="Recognized the inner critic's protective intent. Beginning to differentiate voice from truth.",
        awareness_gain=2,
        integration_gain=1
    )

    shadow.add_journal_entry(enemy, journal_entry)

    print(f"\n📊 Shadow Progress:")
    print(f"   Awareness: {enemy.awareness_level}/10")
    print(f"   Integration: {enemy.integration_level}/10")
    print(f"   Next milestone: {shadow._next_milestone(enemy)}")

    # AI reflection (using Claude for depth)
    llm_client = UniversalLLMClient()
    llm_client.add_provider('claude', AnthropicProvider(api_key="your-key"))

    prompt = shadow.generate_shadow_prompt(
        enemy,
        "You just completed the mirror work exercise and journaled about it."
    )

    try:
        response = llm_client.call(
            prompt,
            provider='claude',
            model='claude-sonnet-4-5',
            max_tokens=500,
            temperature=0.8
        )

        print(f"\n🪞 Reflection:")
        print(response.content)
        print(f"\n   [Cost: ${response.cost_usd:.3f} - Worth it for this depth]")
    except:
        print("\n🪞 This is powerful work. You're seeing clearly. Keep going.")


# ============================================================================
# EXAMPLE 6: Complete Integration - All Systems Working Together
# ============================================================================

def complete_integration_example():
    """
    Show everything working together
    """
    print("\n" + "=" * 60)
    print("COMPLETE INTEGRATION EXAMPLE".center(60))
    print("=" * 60)

    # Initialize all systems
    state = StateManager()
    llm_client = UniversalLLMClient()
    momentum = MomentumSystem(state)
    shadow = ShadowWorkSystem(state)
    bridge = RealWorldBridge(state)

    # Setup LLM providers
    llm_client.add_provider('local', LMStudioProvider())
    llm_client.add_provider('z.ai', ZAIProvider(api_key="your-key"))
    llm_client.add_provider('claude', AnthropicProvider(api_key="your-key"))
    llm_client.set_fallback_order(['local', 'z.ai', 'claude'])

    print("\n🎮 Systems initialized:")
    print("   ✅ LLM Client (3 providers)")
    print("   ✅ Momentum System")
    print("   ✅ Shadow Work")
    print("   ✅ Real-World Bridge")

    # Simulated day
    print("\n📅 Simulating a complete day...")

    # 1. Morning meditation (real practice)
    print("\n🧘 Morning: Meditation")
    meditation = bridge.start_practice('daily_meditation')
    # User does actual meditation...
    result = bridge.complete_session('daily_meditation', duration_minutes=20)

    if result['achievement_unlocked']:
        print(f"   🌟 Achievement: {result['rewards']['achievement']}")

    # 2. Daily task completion with momentum
    print("\n💪 Midday: Exercise")
    ex_result = momentum.complete_task('exercise')
    print(f"   Streak: {ex_result['streak']} days")
    print(f"   CP: +{ex_result['cp_reward']}")

    # 3. Creative work
    print("\n✍️ Afternoon: Creative Work")
    cr_result = momentum.complete_task('creative_work')
    print(f"   Streak: {cr_result['streak']} days")

    # 4. Act of kindness
    print("\n❤️ Evening: Act of Kindness")
    momentum.complete_task('act_of_kindness')

    # 5. Impact logging
    print("\n🌍 Impact Log")
    impact = momentum.log_impact(
        category=ImpactCategory.CREATING,
        description="Built this amazing modular system to help others",
        magnitude=9
    )
    print(f"   Magnitude: 9/10")
    print(f"   CP bonus: +{impact['cp_bonus']}")

    # 6. Shadow work
    print("\n🌑 Shadow Work: Brief Check-in")
    enemy = shadow.SHADOW_LIBRARY['Powerful Enemy']
    shadow.add_journal_entry(enemy, "Noticed the critic today, but didn't engage. Progress.")

    # 7. Get compound bonuses
    print("\n💫 Compound Bonuses Summary")
    bonuses = momentum.get_compound_bonuses()
    print(f"   Total CP Multiplier: {bonuses['cp_multiplier']:.2f}x")
    print(f"   Special Bonuses: {len(bonuses['special_bonuses'])}")

    # 8. AI summary of the day
    print("\n🤖 AI Summary (using local model)")

    summary_prompt = f"""
    Summarize this person's day:
    - Meditated 20 minutes
    - Exercised
    - Did creative work
    - Acted with kindness
    - Built something that helps others (magnitude 9/10)
    - Worked on shadow integration

    Current multiplier: {bonuses['cp_multiplier']}x

    Give brief encouragement (2-3 sentences).
    """

    try:
        response = llm_client.call(summary_prompt, provider='local', max_tokens=150)
        print(f"   {response.content}")
    except:
        print("   You showed up for yourself and others today. That matters.")

    # 9. Usage summary
    print("\n📊 LLM Usage Summary:")
    usage = llm_client.get_usage_summary()
    for provider, stats in usage.items():
        if stats['calls'] > 0:
            print(f"   {provider}: {stats['calls']} calls, ${stats['cost_usd']:.4f}")


# ============================================================================
# MAIN - Run Examples
# ============================================================================

def main():
    """Run all examples"""
    examples = [
        ("Personal Growth Dashboard", personal_growth_dashboard),
        ("Habit Tracker with AI", habit_tracker_with_ai),
        ("Creative Writing Assistant", creative_writing_assistant),
        ("Impact Tracker", impact_tracker),
        ("Therapeutic Journaling", therapeutic_journaling),
        ("Complete Integration", complete_integration_example)
    ]

    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  JUMPCHAIN ENGINE - CROSS-APPLICATION EXAMPLES".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")

    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  {len(examples) + 1}. Run all examples")
    print(f"  0. Exit")

    try:
        choice = int(input("\nChoose an example (0-{}): ".format(len(examples) + 1)))

        if choice == 0:
            print("Goodbye!")
            return
        elif choice == len(examples) + 1:
            # Run all
            for name, func in examples:
                func()
                input("\nPress Enter to continue...")
        elif 1 <= choice <= len(examples):
            examples[choice - 1][1]()
        else:
            print("Invalid choice")

    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == '__main__':
    main()
