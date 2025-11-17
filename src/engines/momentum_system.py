"""
Momentum & Boost System
Track daily tasks, weekly goals, virtues, impact, and compound bonuses
Build sustainable positive momentum in both game and life
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
from enum import Enum


class VirtueType(Enum):
    """Core virtues to track"""
    COURAGE = "courage"
    WISDOM = "wisdom"
    TEMPERANCE = "temperance"
    JUSTICE = "justice"
    COMPASSION = "compassion"
    DILIGENCE = "diligence"
    HONESTY = "honesty"
    HUMILITY = "humility"


class ImpactCategory(Enum):
    """Categories of real-world impact"""
    LEARNING = "learning"  # Gaining knowledge, skills
    CREATING = "creating"  # Making things, art, code
    CONNECTING = "connecting"  # Building relationships
    SERVING = "serving"  # Helping others
    HEALING = "healing"  # Self-care, therapy, growth
    TEACHING = "teaching"  # Sharing knowledge
    PROTECTING = "protecting"  # Standing up, boundaries
    CELEBRATING = "celebrating"  # Gratitude, joy, beauty


@dataclass
class DailyTask:
    """A daily task that builds momentum"""
    task_id: str
    name: str
    description: str
    category: ImpactCategory
    virtue_alignment: List[VirtueType]

    # Requirements
    duration_minutes: int
    difficulty: int  # 1-10

    # Rewards
    base_cp: int
    stat_bonuses: Dict[str, int]
    virtue_points: Dict[str, int]  # Which virtues this builds

    # Streak bonuses
    streak_multiplier: float = 0.1  # +10% per day streak
    max_streak_bonus: float = 2.0  # Cap at 2x

    # Progress
    completions_today: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    total_completions: int = 0
    last_completed: Optional[datetime] = None

    def to_dict(self) -> Dict:
        return {
            'task_id': self.task_id,
            'name': self.name,
            'description': self.description,
            'category': self.category.value,
            'virtue_alignment': [v.value for v in self.virtue_alignment],
            'duration_minutes': self.duration_minutes,
            'difficulty': self.difficulty,
            'base_cp': self.base_cp,
            'stat_bonuses': self.stat_bonuses,
            'virtue_points': self.virtue_points,
            'streak_multiplier': self.streak_multiplier,
            'max_streak_bonus': self.max_streak_bonus,
            'completions_today': self.completions_today,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'total_completions': self.total_completions,
            'last_completed': self.last_completed.isoformat() if self.last_completed else None
        }


@dataclass
class WeeklyGoal:
    """A weekly goal for sustained progress"""
    goal_id: str
    name: str
    description: str
    category: ImpactCategory

    # Requirements
    target_completions: int  # How many times this week
    required_tasks: List[str]  # Which daily tasks count

    # Rewards
    completion_cp: int
    stat_bonuses: Dict[str, int]
    special_unlock: Optional[str] = None

    # Progress
    current_week_completions: int = 0
    total_weeks_completed: int = 0
    current_week_start: Optional[datetime] = None

    def to_dict(self) -> Dict:
        return {
            'goal_id': self.goal_id,
            'name': self.name,
            'description': self.description,
            'category': self.category.value,
            'target_completions': self.target_completions,
            'required_tasks': self.required_tasks,
            'completion_cp': self.completion_cp,
            'stat_bonuses': self.stat_bonuses,
            'special_unlock': self.special_unlock,
            'current_week_completions': self.current_week_completions,
            'total_weeks_completed': self.total_weeks_completed,
            'current_week_start': self.current_week_start.isoformat() if self.current_week_start else None
        }


@dataclass
class VirtueProgress:
    """Track progress in a virtue"""
    virtue: VirtueType
    level: int = 0  # 0-10
    points: int = 0  # Points toward next level
    points_per_level: int = 100

    # Bonuses unlocked
    unlocked_bonuses: List[str] = field(default_factory=list)

    def add_points(self, points: int) -> Dict:
        """Add virtue points and check for level up"""
        self.points += points
        result = {'leveled_up': False, 'new_level': self.level, 'bonuses_unlocked': []}

        while self.points >= self.points_per_level and self.level < 10:
            self.points -= self.points_per_level
            self.level += 1
            result['leveled_up'] = True
            result['new_level'] = self.level

            # Check for new bonuses
            bonus = self._get_level_bonus(self.level)
            if bonus:
                self.unlocked_bonuses.append(bonus)
                result['bonuses_unlocked'].append(bonus)

        return result

    def _get_level_bonus(self, level: int) -> Optional[str]:
        """Get bonus for reaching a level"""
        bonuses = {
            3: f"{self.virtue.value}_novice",  # Small bonus
            5: f"{self.virtue.value}_practitioner",  # Medium bonus
            7: f"{self.virtue.value}_adept",  # Large bonus
            10: f"{self.virtue.value}_master"  # Maximum bonus
        }
        return bonuses.get(level)

    def to_dict(self) -> Dict:
        return {
            'virtue': self.virtue.value,
            'level': self.level,
            'points': self.points,
            'unlocked_bonuses': self.unlocked_bonuses
        }


@dataclass
class ImpactLog:
    """Log of real-world impact"""
    timestamp: datetime
    category: ImpactCategory
    description: str
    magnitude: int  # 1-10
    evidence: Optional[str] = None  # Photo, journal entry, etc.

    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp.isoformat(),
            'category': self.category.value,
            'description': self.description,
            'magnitude': self.magnitude,
            'evidence': self.evidence
        }


class MomentumSystem:
    """Manage momentum, virtues, impact, and compound bonuses"""

    # Predefined daily tasks
    DAILY_TASKS_LIBRARY = {
        'morning_meditation': DailyTask(
            task_id='morning_meditation',
            name='Morning Meditation',
            description='20 minutes of meditation to start the day',
            category=ImpactCategory.HEALING,
            virtue_alignment=[VirtueType.TEMPERANCE, VirtueType.WISDOM],
            duration_minutes=20,
            difficulty=3,
            base_cp=10,
            stat_bonuses={'mental': 1, 'special': 1},
            virtue_points={'temperance': 5, 'wisdom': 3}
        ),

        'exercise': DailyTask(
            task_id='exercise',
            name='Physical Exercise',
            description='30 minutes of intentional movement',
            category=ImpactCategory.HEALING,
            virtue_alignment=[VirtueType.DILIGENCE, VirtueType.TEMPERANCE],
            duration_minutes=30,
            difficulty=4,
            base_cp=15,
            stat_bonuses={'physical': 2, 'durability': 1},
            virtue_points={'diligence': 5, 'temperance': 3}
        ),

        'creative_work': DailyTask(
            task_id='creative_work',
            name='Creative Creation',
            description='30 minutes of creative work (writing, art, music, code)',
            category=ImpactCategory.CREATING,
            virtue_alignment=[VirtueType.DILIGENCE, VirtueType.WISDOM],
            duration_minutes=30,
            difficulty=4,
            base_cp=15,
            stat_bonuses={'mental': 1, 'special': 2},
            virtue_points={'diligence': 5, 'wisdom': 3}
        ),

        'learning': DailyTask(
            task_id='learning',
            name='Deliberate Learning',
            description='30 minutes of focused study or skill development',
            category=ImpactCategory.LEARNING,
            virtue_alignment=[VirtueType.WISDOM, VirtueType.DILIGENCE],
            duration_minutes=30,
            difficulty=3,
            base_cp=12,
            stat_bonuses={'mental': 2},
            virtue_points={'wisdom': 5, 'diligence': 3}
        ),

        'act_of_kindness': DailyTask(
            task_id='act_of_kindness',
            name='Act of Kindness',
            description='Do something kind for someone else',
            category=ImpactCategory.SERVING,
            virtue_alignment=[VirtueType.COMPASSION, VirtueType.JUSTICE],
            duration_minutes=15,
            difficulty=2,
            base_cp=10,
            stat_bonuses={'social': 2},
            virtue_points={'compassion': 5, 'justice': 2}
        ),

        'gratitude_practice': DailyTask(
            task_id='gratitude_practice',
            name='Gratitude Practice',
            description='Write 3 things you\'re grateful for',
            category=ImpactCategory.CELEBRATING,
            virtue_alignment=[VirtueType.WISDOM, VirtueType.HUMILITY],
            duration_minutes=10,
            difficulty=1,
            base_cp=8,
            stat_bonuses={'mental': 1},
            virtue_points={'wisdom': 3, 'humility': 5}
        ),

        'teach_share': DailyTask(
            task_id='teach_share',
            name='Teach or Share',
            description='Teach something or share knowledge with others',
            category=ImpactCategory.TEACHING,
            virtue_alignment=[VirtueType.COMPASSION, VirtueType.WISDOM],
            duration_minutes=20,
            difficulty=5,
            base_cp=18,
            stat_bonuses={'mental': 1, 'social': 2},
            virtue_points={'compassion': 4, 'wisdom': 6}
        ),

        'boundary_setting': DailyTask(
            task_id='boundary_setting',
            name='Healthy Boundary',
            description='Set or maintain a healthy boundary',
            category=ImpactCategory.PROTECTING,
            virtue_alignment=[VirtueType.COURAGE, VirtueType.HONESTY],
            duration_minutes=10,
            difficulty=6,
            base_cp=20,
            stat_bonuses={'mental': 2},
            virtue_points={'courage': 6, 'honesty': 4}
        ),

        'deep_conversation': DailyTask(
            task_id='deep_conversation',
            name='Deep Connection',
            description='Have a meaningful conversation with someone',
            category=ImpactCategory.CONNECTING,
            virtue_alignment=[VirtueType.HONESTY, VirtueType.COMPASSION],
            duration_minutes=30,
            difficulty=5,
            base_cp=15,
            stat_bonuses={'social': 3},
            virtue_points={'honesty': 4, 'compassion': 4}
        ),

        'truth_telling': DailyTask(
            task_id='truth_telling',
            name='Speak Your Truth',
            description='Say something true that feels risky to say',
            category=ImpactCategory.CONNECTING,
            virtue_alignment=[VirtueType.COURAGE, VirtueType.HONESTY],
            duration_minutes=15,
            difficulty=7,
            base_cp=25,
            stat_bonuses={'mental': 2, 'social': 1},
            virtue_points={'courage': 7, 'honesty': 6}
        )
    }

    # Weekly goals
    WEEKLY_GOALS_LIBRARY = {
        'consistent_practice': WeeklyGoal(
            goal_id='consistent_practice',
            name='Consistent Practice',
            description='Complete morning meditation 5 days this week',
            category=ImpactCategory.HEALING,
            target_completions=5,
            required_tasks=['morning_meditation'],
            completion_cp=50,
            stat_bonuses={'mental': 5, 'special': 3},
            special_unlock='Meditation Master bonus (+10% to all mental stats)'
        ),

        'creative_momentum': WeeklyGoal(
            goal_id='creative_momentum',
            name='Creative Momentum',
            description='Create something every day for 7 days',
            category=ImpactCategory.CREATING,
            target_completions=7,
            required_tasks=['creative_work'],
            completion_cp=75,
            stat_bonuses={'special': 5},
            special_unlock='Flow State perk (enter creative flow easier)'
        ),

        'physical_cultivation': WeeklyGoal(
            goal_id='physical_cultivation',
            name='Physical Cultivation',
            description='Exercise 5 days this week',
            category=ImpactCategory.HEALING,
            target_completions=5,
            required_tasks=['exercise'],
            completion_cp=60,
            stat_bonuses={'physical': 5, 'durability': 3}
        ),

        'service_week': WeeklyGoal(
            goal_id='service_week',
            name='Week of Service',
            description='Do 5 acts of kindness this week',
            category=ImpactCategory.SERVING,
            target_completions=5,
            required_tasks=['act_of_kindness'],
            completion_cp=50,
            stat_bonuses={'social': 5},
            special_unlock='Heart Opening perk (deeper connections)'
        ),

        'courage_week': WeeklyGoal(
            goal_id='courage_week',
            name='Week of Courage',
            description='Speak truth or set boundaries 3 times this week',
            category=ImpactCategory.PROTECTING,
            target_completions=3,
            required_tasks=['boundary_setting', 'truth_telling'],
            completion_cp=100,
            stat_bonuses={'mental': 5, 'social': 3},
            special_unlock='Authentic Power perk (stand in your truth)'
        )
    }

    def __init__(self, state_manager):
        """Initialize momentum system"""
        self.state_manager = state_manager
        self.active_tasks: Dict[str, DailyTask] = {}
        self.active_goals: Dict[str, WeeklyGoal] = {}
        self.virtue_progress: Dict[VirtueType, VirtueProgress] = {}
        self.impact_logs: List[ImpactLog] = []

        # Initialize all virtues
        for virtue in VirtueType:
            self.virtue_progress[virtue] = VirtueProgress(virtue=virtue)

        self.load_state()

    def load_state(self):
        """Load momentum state from file"""
        try:
            with open('data/momentum_state.json', 'r') as f:
                data = json.load(f)

                # Load tasks
                for task_id, task_data in data.get('tasks', {}).items():
                    task_data['category'] = ImpactCategory(task_data['category'])
                    task_data['virtue_alignment'] = [VirtueType(v) for v in task_data['virtue_alignment']]
                    if task_data.get('last_completed'):
                        task_data['last_completed'] = datetime.fromisoformat(task_data['last_completed'])
                    self.active_tasks[task_id] = DailyTask(**task_data)

                # Load goals
                for goal_id, goal_data in data.get('goals', {}).items():
                    goal_data['category'] = ImpactCategory(goal_data['category'])
                    if goal_data.get('current_week_start'):
                        goal_data['current_week_start'] = datetime.fromisoformat(goal_data['current_week_start'])
                    self.active_goals[goal_id] = WeeklyGoal(**goal_data)

                # Load virtues
                for virtue_name, virtue_data in data.get('virtues', {}).items():
                    virtue = VirtueType(virtue_name)
                    self.virtue_progress[virtue] = VirtueProgress(
                        virtue=virtue,
                        level=virtue_data['level'],
                        points=virtue_data['points'],
                        unlocked_bonuses=virtue_data['unlocked_bonuses']
                    )

        except FileNotFoundError:
            pass  # Fresh start

    def save_state(self):
        """Save momentum state to file"""
        data = {
            'tasks': {tid: task.to_dict() for tid, task in self.active_tasks.items()},
            'goals': {gid: goal.to_dict() for gid, goal in self.active_goals.items()},
            'virtues': {v.value: prog.to_dict() for v, prog in self.virtue_progress.items()}
        }

        with open('data/momentum_state.json', 'w') as f:
            json.dump(data, f, indent=2)

    def activate_task(self, task_id: str) -> DailyTask:
        """Activate a daily task"""
        if task_id not in self.DAILY_TASKS_LIBRARY:
            raise ValueError(f"Task {task_id} not found in library")

        task = self.DAILY_TASKS_LIBRARY[task_id]
        self.active_tasks[task_id] = task
        self.save_state()
        return task

    def activate_goal(self, goal_id: str) -> WeeklyGoal:
        """Activate a weekly goal"""
        if goal_id not in self.WEEKLY_GOALS_LIBRARY:
            raise ValueError(f"Goal {goal_id} not found in library")

        goal = self.WEEKLY_GOALS_LIBRARY[goal_id]
        goal.current_week_start = datetime.now()
        self.active_goals[goal_id] = goal
        self.save_state()
        return goal

    def complete_task(self, task_id: str, duration_minutes: Optional[int] = None) -> Dict:
        """
        Complete a daily task

        Returns:
            Dict with rewards, streak info, virtue progress
        """
        if task_id not in self.active_tasks:
            raise ValueError(f"Task {task_id} not active")

        task = self.active_tasks[task_id]
        now = datetime.now()

        # Update streak
        if task.last_completed:
            time_since = now - task.last_completed
            if time_since <= timedelta(days=2):  # Within 2 days = streak continues
                task.current_streak += 1
            else:
                task.current_streak = 1
        else:
            task.current_streak = 1

        task.longest_streak = max(task.longest_streak, task.current_streak)
        task.completions_today += 1
        task.total_completions += 1
        task.last_completed = now

        # Calculate rewards with streak bonus
        streak_multiplier = min(
            1.0 + (task.current_streak * task.streak_multiplier),
            task.max_streak_bonus
        )

        cp_reward = int(task.base_cp * streak_multiplier)
        stat_bonuses = {k: int(v * streak_multiplier) for k, v in task.stat_bonuses.items()}

        # Award virtue points
        virtue_results = {}
        for virtue_name, points in task.virtue_points.items():
            virtue = VirtueType(virtue_name)
            adjusted_points = int(points * streak_multiplier)
            result = self.virtue_progress[virtue].add_points(adjusted_points)
            virtue_results[virtue_name] = result

        # Check weekly goals
        goal_completions = self._check_weekly_goals(task_id)

        # Save state
        self.save_state()

        return {
            'task_completed': task.name,
            'streak': task.current_streak,
            'streak_multiplier': streak_multiplier,
            'cp_reward': cp_reward,
            'stat_bonuses': stat_bonuses,
            'virtue_progress': virtue_results,
            'weekly_goals_progress': goal_completions,
            'total_completions': task.total_completions
        }

    def _check_weekly_goals(self, task_id: str) -> List[Dict]:
        """Check if task completion progresses weekly goals"""
        now = datetime.now()
        results = []

        for goal in self.active_goals.values():
            # Check if we're in a new week
            if goal.current_week_start:
                days_since_start = (now - goal.current_week_start).days
                if days_since_start >= 7:
                    # Week ended, reset
                    goal.current_week_completions = 0
                    goal.current_week_start = now

            # Check if this task counts for this goal
            if task_id in goal.required_tasks:
                goal.current_week_completions += 1

                # Check completion
                if goal.current_week_completions >= goal.target_completions:
                    completion_result = self._complete_weekly_goal(goal)
                    results.append(completion_result)

        return results

    def _complete_weekly_goal(self, goal: WeeklyGoal) -> Dict:
        """Complete a weekly goal"""
        goal.total_weeks_completed += 1
        goal.current_week_completions = 0
        goal.current_week_start = datetime.now()

        return {
            'goal_completed': goal.name,
            'cp_reward': goal.completion_cp,
            'stat_bonuses': goal.stat_bonuses,
            'special_unlock': goal.special_unlock,
            'total_completions': goal.total_weeks_completed
        }

    def log_impact(self, category: ImpactCategory, description: str,
                   magnitude: int, evidence: Optional[str] = None) -> Dict:
        """
        Log real-world impact

        Args:
            category: Type of impact
            description: What you did
            magnitude: How significant (1-10)
            evidence: Optional proof/reflection

        Returns:
            Dict with bonus rewards
        """
        impact = ImpactLog(
            timestamp=datetime.now(),
            category=category,
            description=description,
            magnitude=magnitude,
            evidence=evidence
        )

        self.impact_logs.append(impact)

        # Calculate rewards based on magnitude
        cp_bonus = magnitude * 5  # 5-50 CP
        virtue_bonus = magnitude * 2

        # Determine which virtues this impacts
        virtue_mapping = {
            ImpactCategory.LEARNING: [VirtueType.WISDOM, VirtueType.DILIGENCE],
            ImpactCategory.CREATING: [VirtueType.WISDOM, VirtueType.DILIGENCE],
            ImpactCategory.CONNECTING: [VirtueType.COMPASSION, VirtueType.HONESTY],
            ImpactCategory.SERVING: [VirtueType.COMPASSION, VirtueType.JUSTICE],
            ImpactCategory.HEALING: [VirtueType.TEMPERANCE, VirtueType.WISDOM],
            ImpactCategory.TEACHING: [VirtueType.COMPASSION, VirtueType.WISDOM],
            ImpactCategory.PROTECTING: [VirtueType.COURAGE, VirtueType.JUSTICE],
            ImpactCategory.CELEBRATING: [VirtueType.WISDOM, VirtueType.HUMILITY]
        }

        virtue_results = {}
        for virtue in virtue_mapping.get(category, []):
            result = self.virtue_progress[virtue].add_points(virtue_bonus)
            virtue_results[virtue.value] = result

        # Save
        self._save_impact_log()
        self.save_state()

        return {
            'impact_logged': description,
            'magnitude': magnitude,
            'cp_bonus': cp_bonus,
            'virtue_progress': virtue_results
        }

    def _save_impact_log(self):
        """Save impact logs to file"""
        with open('data/impact_log.jsonl', 'a') as f:
            for impact in self.impact_logs:
                f.write(json.dumps(impact.to_dict()) + '\n')
        self.impact_logs = []  # Clear after saving

    def get_compound_bonuses(self) -> Dict:
        """
        Calculate compound bonuses from all systems

        Returns:
            Dict with all active bonuses and multipliers
        """
        bonuses = {
            'cp_multiplier': 1.0,
            'stat_multipliers': {},
            'special_bonuses': []
        }

        # Virtue bonuses
        for virtue, progress in self.virtue_progress.items():
            for bonus in progress.unlocked_bonuses:
                bonuses['special_bonuses'].append(bonus)

                # Apply bonus effects
                if 'master' in bonus:
                    bonuses['cp_multiplier'] *= 1.25  # 25% boost for master level
                elif 'adept' in bonus:
                    bonuses['cp_multiplier'] *= 1.15  # 15% for adept
                elif 'practitioner' in bonus:
                    bonuses['cp_multiplier'] *= 1.10  # 10% for practitioner

        # Streak bonuses
        for task in self.active_tasks.values():
            if task.current_streak >= 7:
                bonuses['special_bonuses'].append(f'{task.name} - 7 day streak!')
            if task.current_streak >= 30:
                bonuses['special_bonuses'].append(f'{task.name} - 30 day streak!!')
                bonuses['cp_multiplier'] *= 1.1

        # Weekly goal completion bonuses
        for goal in self.active_goals.values():
            if goal.total_weeks_completed >= 4:
                bonuses['special_bonuses'].append(f'{goal.name} - 1 month complete!')
            if goal.total_weeks_completed >= 12:
                bonuses['special_bonuses'].append(f'{goal.name} - 3 months!')
                bonuses['cp_multiplier'] *= 1.15

        return bonuses

    def get_momentum_summary(self) -> Dict:
        """Get complete momentum summary"""
        return {
            'active_tasks': len(self.active_tasks),
            'active_goals': len(self.active_goals),
            'virtues': {
                v.value: {
                    'level': prog.level,
                    'points': prog.points,
                    'bonuses': len(prog.unlocked_bonuses)
                }
                for v, prog in self.virtue_progress.items()
                if prog.level > 0
            },
            'streaks': {
                task_id: task.current_streak
                for task_id, task in self.active_tasks.items()
                if task.current_streak > 0
            },
            'compound_bonuses': self.get_compound_bonuses()
        }
