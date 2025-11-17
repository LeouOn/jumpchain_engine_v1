#!/usr/bin/env python3
"""
Database initialization script for Jumpchain Engine
Creates the database and sets up initial data
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.state_manager import StateManager
from src.core.models import JumperState


def main():
    """Initialize the database"""
    print("=" * 60)
    print("Jumpchain Engine - Database Initialization")
    print("=" * 60)
    print()

    # Check if database already exists
    db_path = Path("data/jumpchain.db")
    if db_path.exists():
        response = input("Database already exists. Overwrite? (yes/no): ").strip().lower()
        if response != 'yes':
            print("Initialization cancelled.")
            return

        # Backup existing database
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"data/jumpchain_backup_{timestamp}.db"
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"✓ Existing database backed up to: {backup_path}")

        # Remove old database
        db_path.unlink()

    # Create state manager (this will initialize the database)
    print("\nInitializing database...")
    state_manager = StateManager()

    # Create default jumper
    print("Creating default character...")
    jumper = state_manager.load_jumper(jumper_id=1)

    if not jumper:
        # The schema already inserts a default jumper, but let's verify
        print("⚠ Default jumper not found in database")
        print("Creating new jumper...")

        jumper = JumperState(
            id=1,
            name="Jumper",
            age=18,
            current_jump="None",
            total_cp_earned=1000,
            total_cp_spent=0,
            jump_count=0,
            current_year=1,
            current_day=1,
            current_location="Starting Area"
        )
        state_manager.save_jumper(jumper)

    print(f"✓ Default character created: {jumper.name}")

    # Verify database structure
    print("\nVerifying database structure...")
    tables = state_manager.db.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()

    expected_tables = [
        'jumper', 'perks', 'companions', 'items', 'jump_history',
        'world_state', 'active_drawbacks', 'rewards', 'background_events',
        'turn_log'
    ]

    found_tables = [table['name'] for table in tables if table['name'] != 'sqlite_sequence']

    for table in expected_tables:
        if table in found_tables:
            print(f"  ✓ {table}")
        else:
            print(f"  ✗ {table} (MISSING)")

    state_manager.close()

    print()
    print("=" * 60)
    print("Database initialization complete!")
    print("=" * 60)
    print()
    print("You can now run the CLI with:")
    print("  python src/ui/cli.py")
    print()


if __name__ == '__main__':
    main()
