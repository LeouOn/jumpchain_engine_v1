"""
Basic CLI interface for Jumpchain Engine
"""

import sys
import os

# Add parent directory to path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.core.state_manager import StateManager
from src.core.models import JumperState, Companion, Perk
import json


class JumpchainCLI:
    """Simple command-line interface for Jumpchain Engine"""

    def __init__(self):
        self.state_manager = StateManager()
        self.jumper = None
        self.running = True

    def start(self):
        """Start the CLI"""
        print("=" * 60)
        print("JUMPCHAIN ENGINE V1".center(60))
        print("=" * 60)
        print()

        # Load or create jumper
        self.jumper = self.state_manager.load_jumper()

        if not self.jumper or self.jumper.name == "Jumper":
            print("No existing character found. Let's create one!")
            self.create_character()
        else:
            print(f"Welcome back, {self.jumper.name}!")
            self.show_status()

        print()
        self.main_loop()

    def create_character(self):
        """Create a new character"""
        print()
        name = input("Enter your character name: ").strip() or "Jumper"
        age = input("Enter starting age (default 18): ").strip()
        age = int(age) if age.isdigit() else 18

        self.jumper = JumperState(
            id=1,
            name=name,
            age=age,
            current_jump="None",
            total_cp_earned=1000,
            total_cp_spent=0,
            jump_count=0,
            current_year=1,
            current_day=1,
            current_location="Starting Area"
        )

        self.state_manager.save_jumper(self.jumper)
        print(f"\nCharacter '{name}' created successfully!")

    def show_status(self):
        """Display current character status"""
        print()
        print("─" * 60)
        print(f" Character: {self.jumper.name}")
        print(f" Current Jump: {self.jumper.current_jump}")
        print(f" Location: {self.jumper.current_location}")
        print(f" Day {self.jumper.current_day}, Year {self.jumper.current_year}")
        print(f" Total CP: {self.jumper.total_cp_earned} | Spent: {self.jumper.total_cp_spent} | Available: {self.jumper.available_cp}")
        print(f" Jumps Completed: {self.jumper.jump_count}")
        print("─" * 60)

        # Show active perks
        perks = self.state_manager.get_active_perks(self.jumper.id, 'jumper')
        if perks:
            print(f"\n Active Perks ({len(perks)}):")
            for perk in perks[:5]:  # Show first 5
                print(f"  • {perk.name} ({perk.source_jump})")
            if len(perks) > 5:
                print(f"  ... and {len(perks) - 5} more")

        # Show companions
        companions = self.state_manager.load_companions()
        if companions:
            print(f"\n Companions ({len(companions)}):")
            for comp in companions[:3]:
                print(f"  • {comp.name} (Relationship: {comp.relationship_level}/10)")
            if len(companions) > 3:
                print(f"  ... and {len(companions) - 3} more")

        # Show achievements
        achievements = self.state_manager.get_achievements()
        if achievements:
            print(f"\n Achievements: {len(achievements)}")
            tier_counts = {}
            for ach in achievements:
                tier_counts[ach.tier] = tier_counts.get(ach.tier, 0) + 1
            for tier, count in tier_counts.items():
                print(f"  {tier.capitalize()}: {count}")

    def main_loop(self):
        """Main command loop"""
        print("\nType 'help' for available commands, 'quit' to exit.")

        while self.running:
            try:
                print()
                command = input("> ").strip().lower()

                if not command:
                    continue

                if command == 'quit' or command == 'exit':
                    self.quit()
                elif command == 'help':
                    self.show_help()
                elif command == 'status':
                    self.show_status()
                elif command.startswith('perks'):
                    self.show_perks()
                elif command.startswith('companions'):
                    self.show_companions()
                elif command.startswith('achievements'):
                    self.show_achievements()
                elif command.startswith('add perk'):
                    self.add_perk_wizard()
                elif command.startswith('add companion'):
                    self.add_companion_wizard()
                elif command.startswith('turn'):
                    self.advance_turn()
                elif command.startswith('backup'):
                    self.backup_database()
                else:
                    print(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\nUse 'quit' to exit.")
            except Exception as e:
                print(f"Error: {e}")

    def show_help(self):
        """Show available commands"""
        print()
        print("Available Commands:")
        print("  status              - Show character status")
        print("  perks               - List all perks")
        print("  companions          - List all companions")
        print("  achievements        - List all achievements")
        print("  add perk            - Add a new perk")
        print("  add companion       - Add a new companion")
        print("  turn                - Advance one turn (one day)")
        print("  backup              - Create database backup")
        print("  help                - Show this help")
        print("  quit                - Exit the program")

    def show_perks(self):
        """Show all perks"""
        perks = self.state_manager.get_all_perks(self.jumper.id, 'jumper')

        if not perks:
            print("\nNo perks acquired yet.")
            return

        print(f"\n=== Your Perks ({len(perks)}) ===")
        for i, perk in enumerate(perks, 1):
            status = "✓" if perk.is_active else "✗"
            print(f"{i}. {status} {perk.name} ({perk.source_jump}) - {perk.cp_cost} CP")
            if perk.description:
                print(f"   {perk.description[:80]}{'...' if len(perk.description) > 80 else ''}")

    def show_companions(self):
        """Show all companions"""
        companions = self.state_manager.load_companions(active_only=False)

        if not companions:
            print("\nNo companions yet.")
            return

        print(f"\n=== Your Companions ({len(companions)}) ===")
        for i, comp in enumerate(companions, 1):
            status = "Active" if comp.is_active else "Inactive"
            print(f"{i}. {comp.name} ({status})")
            print(f"   Origin: {comp.origin} | From: {comp.source_jump}")
            print(f"   Relationship: {comp.relationship_level}/10")
            print(f"   CP: {comp.cp_spent}/{comp.cp_budget}")
            if comp.perks:
                print(f"   Perks: {len(comp.perks)}")

    def show_achievements(self):
        """Show all achievements"""
        achievements = self.state_manager.get_achievements()

        if not achievements:
            print("\nNo achievements earned yet.")
            return

        print(f"\n=== Achievements ({len(achievements)}) ===")
        by_tier = {'bronze': [], 'silver': [], 'gold': [], 'platinum': []}

        for ach in achievements:
            by_tier[ach.tier].append(ach)

        for tier in ['platinum', 'gold', 'silver', 'bronze']:
            tier_achs = by_tier[tier]
            if tier_achs:
                print(f"\n{tier.upper()}:")
                for ach in tier_achs:
                    print(f"  {ach.icon} {ach.name}")
                    print(f"     {ach.description}")
                    print(f"     Reward: {ach.reward_value}")

    def add_perk_wizard(self):
        """Wizard to add a new perk"""
        print("\n=== Add New Perk ===")
        name = input("Perk name: ").strip()
        if not name:
            print("Cancelled.")
            return

        source = input("Source jump: ").strip() or self.jumper.current_jump
        cost_str = input("CP cost: ").strip()
        cost = int(cost_str) if cost_str.isdigit() else 0

        description = input("Description (optional): ").strip()

        tags_str = input("Synergy tags (comma-separated, optional): ").strip()
        tags = [t.strip() for t in tags_str.split(',')] if tags_str else []

        perk = Perk(
            id=0,  # Will be auto-assigned
            owner_id=self.jumper.id,
            owner_type='jumper',
            name=name,
            source_jump=source,
            cp_cost=cost,
            description=description,
            is_active=True,
            evolution_stage=0,
            synergy_tags=tags,
            mechanics={}
        )

        self.state_manager.save_perk(perk)

        # Update jumper CP
        self.jumper.total_cp_spent += cost
        self.state_manager.save_jumper(self.jumper)

        print(f"\n✓ Perk '{name}' added successfully!")

    def add_companion_wizard(self):
        """Wizard to add a new companion"""
        print("\n=== Add New Companion ===")
        name = input("Companion name: ").strip()
        if not name:
            print("Cancelled.")
            return

        origin = input("Origin: ").strip()
        source = input("Source jump: ").strip() or self.jumper.current_jump

        companion = Companion(
            id=0,  # Will be auto-assigned
            name=name,
            origin=origin,
            source_jump=source,
            cp_budget=600,
            cp_spent=0,
            relationship_level=5,
            is_active=True,
            personality_profile={},
            current_activity="Idle"
        )

        self.state_manager.save_companion(companion)
        print(f"\n✓ Companion '{name}' added successfully!")

    def advance_turn(self):
        """Advance one turn"""
        self.jumper = self.state_manager.advance_turn()
        print(f"\n⏩ Advanced to Day {self.jumper.current_day}, Year {self.jumper.current_year}")

    def backup_database(self):
        """Create a backup of the database"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"data/jumpchain_backup_{timestamp}.db"

        self.state_manager.backup(backup_path)
        print(f"\n✓ Database backed up to: {backup_path}")

    def quit(self):
        """Exit the program"""
        print("\nSaving and exiting...")
        self.state_manager.close()
        self.running = False
        print("Goodbye!")


def main():
    """Entry point"""
    cli = JumpchainCLI()
    cli.start()


if __name__ == '__main__':
    main()
