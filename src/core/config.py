"""
Configuration loader for Jumpchain Engine
Handles loading settings from YAML and JSON files
"""

import yaml
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for Jumpchain Engine"""

    def __init__(self, config_dir: str = "config"):
        """
        Initialize configuration

        Args:
            config_dir: Directory containing config files
        """
        self.config_dir = Path(config_dir)
        self.settings = {}
        self.achievements = {}

        # Load configurations
        self.load_settings()
        self.load_achievements()

    def load_settings(self):
        """Load settings from settings.yaml"""
        settings_path = self.config_dir / "settings.yaml"

        if not settings_path.exists():
            logger.warning(f"Settings file not found: {settings_path}, using defaults")
            self.settings = self._default_settings()
            return

        try:
            with open(settings_path, 'r') as f:
                self.settings = yaml.safe_load(f)
            logger.info(f"Loaded settings from {settings_path}")
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            self.settings = self._default_settings()

        # Override with environment variables
        self._apply_env_overrides()

    def load_achievements(self):
        """Load achievement definitions from achievements.json"""
        ach_path = self.config_dir / "achievements.json"

        if not ach_path.exists():
            logger.warning(f"Achievements file not found: {ach_path}")
            self.achievements = {'achievements': []}
            return

        try:
            with open(ach_path, 'r') as f:
                self.achievements = json.load(f)
            logger.info(f"Loaded {len(self.achievements.get('achievements', []))} achievement definitions")
        except Exception as e:
            logger.error(f"Error loading achievements: {e}")
            self.achievements = {'achievements': []}

    def _default_settings(self) -> Dict:
        """Return default settings"""
        return {
            'llm_endpoints': {
                'narration': {
                    'model': 'claude-sonnet-4-5',
                    'endpoint': 'http://localhost:5000/v1/chat/completions',
                    'api_key': ''
                },
                'calculation': {
                    'model': 'deepseek-r1',
                    'endpoint': 'http://localhost:5001/v1/chat/completions',
                    'api_key': ''
                },
                'background': {
                    'model': 'qwen-2.5-72b',
                    'endpoint': 'http://localhost:5002/v1/chat/completions',
                    'api_key': ''
                },
                'companions': {
                    'model': 'gemma-2-27b',
                    'endpoint': 'http://localhost:5003/v1/chat/completions',
                    'api_key': ''
                }
            },
            'database': {
                'path': 'data/jumpchain.db',
                'backup_interval': 10,
                'auto_backup': True
            },
            'gameplay': {
                'tone': 'serious_comedy',
                'auto_save': True,
                'difficulty': 'balanced',
                'days_per_turn': 1,
                'base_cp': 1000,
                'companion_cp': 600
            },
            'rewards': {
                'bronze_multiplier': 1.05,
                'silver_multiplier': 1.10,
                'gold_multiplier': 1.25,
                'platinum_multiplier': 1.50,
                'track_speedruns': True,
                'track_synergies': True,
                'track_perfect_runs': True
            },
            'narration': {
                'max_length_words': 500,
                'include_companion_dialogue': True,
                'show_mechanics': False,
                'hint_at_background': True
            },
            'background_simulation': {
                'enabled': True,
                'events_per_turn': 2,
                'crisis_chance': 0.05,
                'opportunity_chance': 0.10
            },
            'companion_ai': {
                'enabled': True,
                'autonomous_actions': True,
                'relationship_evolution': True,
                'memory_depth': 20
            },
            'world_building': {
                'auto_populate': True,
                'wiki_scraping': True,
                'timeline_generation': True
            },
            'ui': {
                'interface': 'cli',
                'colors': True,
                'animations': False
            },
            'debug': {
                'verbose_logging': False,
                'show_llm_prompts': False,
                'show_calculation_details': False
            }
        }

    def _apply_env_overrides(self):
        """Apply environment variable overrides"""
        # Check for API keys in environment
        env_mappings = {
            'CLAUDE_API_KEY': ['llm_endpoints', 'narration', 'api_key'],
            'DEEPSEEK_API_KEY': ['llm_endpoints', 'calculation', 'api_key'],
            'QWEN_API_KEY': ['llm_endpoints', 'background', 'api_key'],
            'GEMMA_API_KEY': ['llm_endpoints', 'companions', 'api_key'],
        }

        for env_var, path in env_mappings.items():
            value = os.environ.get(env_var)
            if value:
                # Navigate to the right place in settings dict
                current = self.settings
                for key in path[:-1]:
                    if key not in current:
                        current[key] = {}
                    current = current[key]
                current[path[-1]] = value

    def get(self, *keys, default=None) -> Any:
        """
        Get a configuration value by path

        Args:
            *keys: Path to the value (e.g., 'gameplay', 'tone')
            default: Default value if not found

        Returns:
            Configuration value
        """
        current = self.settings
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current

    def get_llm_config(self, llm_type: str) -> Dict:
        """
        Get LLM configuration for a specific type

        Args:
            llm_type: 'narration', 'calculation', 'background', or 'companions'

        Returns:
            Dict with model, endpoint, api_key
        """
        return self.get('llm_endpoints', llm_type, default={})

    def get_achievement_config(self, achievement_id: str) -> Optional[Dict]:
        """
        Get achievement configuration by ID

        Args:
            achievement_id: Achievement ID

        Returns:
            Achievement config dict or None
        """
        for ach in self.achievements.get('achievements', []):
            if ach.get('id') == achievement_id:
                return ach
        return None

    def get_all_achievements(self) -> List[Dict]:
        """Get all achievement configurations"""
        return self.achievements.get('achievements', [])

    def get_reward_multiplier(self, tier: str) -> float:
        """
        Get reward multiplier for achievement tier

        Args:
            tier: 'bronze', 'silver', 'gold', or 'platinum'

        Returns:
            Multiplier value
        """
        key = f'{tier}_multiplier'
        return self.get('rewards', key, default=1.0)

    def is_debug_mode(self) -> bool:
        """Check if any debug mode is enabled"""
        debug = self.get('debug', default={})
        return any(debug.values()) if isinstance(debug, dict) else False

    def save_settings(self, settings_path: Optional[str] = None):
        """
        Save current settings to file

        Args:
            settings_path: Optional path to save to
        """
        if settings_path is None:
            settings_path = self.config_dir / "settings.yaml"

        try:
            with open(settings_path, 'w') as f:
                yaml.dump(self.settings, f, default_flow_style=False)
            logger.info(f"Saved settings to {settings_path}")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")


# Global config instance
_config = None


def get_config() -> Config:
    """Get global configuration instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config


def reload_config():
    """Reload configuration from files"""
    global _config
    _config = Config()
    return _config
