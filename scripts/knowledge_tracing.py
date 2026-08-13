"""
Knowledge Tracing System for Adaptive Learning

Based on research from:
- Corbett, A. T., & Anderson, J. R. (1995). "Knowledge Tracing: Modeling the Acquisition of Procedural Knowledge."
- Koedinger, K. R., & Corbett, A. (2006). "Cognitive Tutors: Technology that Brings Learning Science to the Classroom."

Bayesian Knowledge Tracing (BKT) models skill acquisition over time with four parameters:
- p(L0): Prior probability of knowing the skill
- p(T): Probability of learning the skill from practice
- p(G): Probability of guessing correctly
- p(S): Probability of making a mistake (slipping)
"""

import json
import logging
import time
import math
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random

logger = logging.getLogger(__name__)


class MasteryLevel(Enum):
    """Mastery levels for skills."""
    NOVICE = "novice"       # 0.0 - 0.25
    DEVELOPING = "developing"  # 0.25 - 0.50
    COMPETENT = "competent"    # 0.50 - 0.75
    PROFICIENT = "proficient"  # 0.75 - 0.90
    MASTERED = "mastered"     # 0.90 - 1.00


@dataclass
class SkillParameters:
    """Bayesian Knowledge Tracing parameters for a skill."""
    skill_id: str
    skill_name: str
    p_L0: float  # Prior knowledge probability
    p_T: float   # Learn probability
    p_G: float   # Guess probability
    p_S: float   # Slip probability
    p_mastery: float = 0.0  # Current mastery probability

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'skill_id': self.skill_id,
            'skill_name': self.skill_name,
            'p_L0': self.p_L0,
            'p_T': self.p_T,
            'p_G': self.p_G,
            'p_S': self.p_S,
            'p_mastery': self.p_mastery,
            'mastery_level': self._determine_mastery_level()
        }

    def _determine_mastery_level(self) -> str:
        """Determine mastery level from probability."""
        if self.p_mastery < 0.25:
            return MasteryLevel.NOVICE.value
        elif self.p_mastery < 0.50:
            return MasteryLevel.DEVELOPING.value
        elif self.p_mastery < 0.75:
            return MasteryLevel.COMPETENT.value
        elif self.p_mastery < 0.90:
            return MasteryLevel.PROFICIENT.value
        else:
            return MasteryLevel.MASTERED.value


@dataclass
class ExerciseRecommendation:
    """Recommendation for next exercise."""
    exercise_id: str
    skill_id: str
    difficulty: str
    expected_learning_value: float
    probability_of_success: float
    rationale: str
    alternative_exercises: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'exercise_id': self.exercise_id,
            'skill_id': self.skill_id,
            'difficulty': self.difficulty,
            'expected_learning_value': self.expected_learning_value,
            'probability_of_success': self.probability_of_success,
            'rationale': self.rationale,
            'alternative_exercises': self.alternative_exercises
        }


@dataclass
class LearningAnalytics:
    """Analytics data for a learner."""
    learner_id: str
    skills: Dict[str, SkillParameters]
    exercise_history: List[Dict[str, Any]] = field(default_factory=list)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    time_spent: float = 0.0
    last_updated: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'learner_id': self.learner_id,
            'skills': {k: v.to_dict() for k, v in self.skills.items()},
            'exercise_history': self.exercise_history,
            'performance_metrics': self.performance_metrics,
            'time_spent': self.time_spent,
            'last_updated': self.last_updated
        }


class BayesianKnowledgeTracer:
    """
    Production-grade Bayesian Knowledge Tracing implementation.

    Models skill acquisition over time and enables adaptive exercise selection.
    Based on proven cognitive tutor technology.
    """

    def __init__(self, config_path: str = 'config/config.json'):
        """Initialize the knowledge tracer."""
        self.config = self._load_config(config_path)
        self.skill_database = self._load_skill_database()
        self.learner_models: Dict[str, LearningAnalytics] = {}
        self.exercise_database = self._load_exercise_database()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load config: {e}")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'knowledge_tracing': {
                'enabled': True,
                'mastery_threshold': 0.90,
                'slip_threshold': 0.30,
                'learn_rate_baseline': 0.10,
                'guess_baseline': 0.20
            }
        }

    def _load_skill_database(self) -> Dict[str, Dict]:
        """Load database of programming skills with BKT parameters."""
        return {
            'python_loops': {
                'name': 'Python Loops',
                'category': 'control_flow',
                'p_L0': 0.10,  # Low prior knowledge
                'p_T': 0.15,   # Moderate learnability
                'p_G': 0.20,   # Low guess rate
                'p_S': 0.10    # Low slip rate
            },
            'python_functions': {
                'name': 'Python Functions',
                'category': 'procedural_abstraction',
                'p_L0': 0.05,
                'p_T': 0.10,
                'p_G': 0.15,
                'p_S': 0.15
            },
            'python_conditionals': {
                'name': 'Python Conditionals',
                'category': 'control_flow',
                'p_L0': 0.15,
                'p_T': 0.20,
                'p_G': 0.25,
                'p_S': 0.10
            },
            'python_lists': {
                'name': 'Python Lists',
                'category': 'data_structures',
                'p_L0': 0.08,
                'p_T': 0.12,
                'p_G': 0.18,
                'p_S': 0.12
            },
            'python_dictionaries': {
                'name': 'Python Dictionaries',
                'category': 'data_structures',
                'p_L0': 0.05,
                'p_T': 0.10,
                'p_G': 0.20,
                'p_S': 0.15
            },
            'javascript_loops': {
                'name': 'JavaScript Loops',
                'category': 'control_flow',
                'p_L0': 0.10,
                'p_T': 0.15,
                'p_G': 0.20,
                'p_S': 0.12
            },
            'javascript_functions': {
                'name': 'JavaScript Functions',
                'category': 'procedural_abstraction',
                'p_L0': 0.05,
                'p_T': 0.12,
                'p_G': 0.18,
                'p_S': 0.15
            },
            'javascript_arrays': {
                'name': 'JavaScript Arrays',
                'category': 'data_structures',
                'p_L0': 0.08,
                'p_T': 0.12,
                'p_G': 0.20,
                'p_S': 0.12
            },
            'debugging_syntax': {
                'name': 'Syntax Error Debugging',
                'category': 'debugging',
                'p_L0': 0.15,
                'p_T': 0.08,
                'p_G': 0.25,
                'p_S': 0.10
            },
            'debugging_logic': {
                'name': 'Logic Error Debugging',
                'category': 'debugging',
                'p_L0': 0.05,
                'p_T': 0.10,
                'p_G': 0.15,
                'p_S': 0.20
            },
            'code_tracing': {
                'name': 'Code Tracing',
                'category': 'mental_model',
                'p_L0': 0.10,
                'p_T': 0.15,
                'p_G': 0.15,
                'p_S': 0.15
            }
        }

    def _load_exercise_database(self) -> Dict[str, Dict]:
        """Load database of exercises with skill mappings."""
        return {
            'python_loops_basic': {
                'skill_id': 'python_loops',
                'difficulty': 'beginner',
                'description': 'Basic for loop with range',
                'exercise_type': 'parsons_problem'
            },
            'python_loops_intermediate': {
                'skill_id': 'python_loops',
                'difficulty': 'intermediate',
                'description': 'Nested loops with list manipulation',
                'exercise_type': 'code_tracing'
            },
            'python_functions_basic': {
                'skill_id': 'python_functions',
                'difficulty': 'beginner',
                'description': 'Function with parameters and return',
                'exercise_type': 'worked_example'
            },
            'python_functions_advanced': {
                'skill_id': 'python_functions',
                'difficulty': 'advanced',
                'description': 'Function with *args and **kwargs',
                'exercise_type': 'from_scratch'
            },
            'debugging_syntax': {
                'skill_id': 'debugging_syntax',
                'difficulty': 'intermediate',
                'description': 'Debug syntax errors in code',
                'exercise_type': 'debugging_protocol'
            }
        }

    def initialize_learner(self, learner_id: str) -> LearningAnalytics:
        """
        Initialize a new learner model with default parameters.

        Args:
            learner_id: Unique identifier for learner

        Returns:
            LearningAnalytics with initialized skill parameters
        """
        # Initialize all skills with default parameters
        skills = {}
        for skill_id, skill_data in self.skill_database.items():
            skills[skill_id] = SkillParameters(
                skill_id=skill_id,
                skill_name=skill_data['name'],
                p_L0=skill_data['p_L0'],
                p_T=skill_data['p_T'],
                p_G=skill_data['p_G'],
                p_S=skill_data['p_S'],
                p_mastery=skill_data['p_L0']  # Start with prior knowledge
            )

        learner_model = LearningAnalytics(
            learner_id=learner_id,
            skills=skills
        )

        self.learner_models[learner_id] = learner_model
        return learner_model

    def update_mastery(
        self,
        learner_id: str,
        skill_id: str,
        outcome: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Update mastery probability based on performance.

        Core Bayesian Knowledge Tracing update rule.

        Args:
            learner_id: Learner identifier
            skill_id: Skill being practiced
            outcome: 'correct' or 'incorrect'
            context: Additional context (optional)

        Returns:
            Tuple of (new_mastery_probability, update_metadata)
        """
        if learner_id not in self.learner_models:
            self.initialize_learner(learner_id)

        learner = self.learner_models[learner_id]

        if skill_id not in learner.skills:
            logger.warning(f"Unknown skill_id: {skill_id}")
            return 0.0, {'error': 'Unknown skill'}

        skill = learner.skills[skill_id]

        # BKT update rules
        if outcome == 'correct':
            # Two possibilities: knew it or guessed correctly
            p_knows = (skill.p_T * skill.p_mastery) / \
                      ((skill.p_T * skill.p_mastery) + \
                       ((1 - skill.p_T) * skill.p_G))

            new_mastery = p_knows

        else:  # incorrect
            # Two possibilities: knew it but slipped, or didn't know and didn't guess
            p_knows = ((1 - skill.p_S) * skill.p_mastery) / \
                      (((1 - skill.p_S) * skill.p_mastery) + \
                       ((1 - skill.p_T) * (1 - skill.p_G) * (1 - skill.p_mastery)))

            new_mastery = p_knows

        # Update mastery probability
        old_mastery = skill.p_mastery
        skill.p_mastery = new_mastery

        # Record exercise in history
        learner.exercise_history.append({
            'timestamp': time.time(),
            'skill_id': skill_id,
            'outcome': outcome,
            'old_mastery': old_mastery,
            'new_mastery': new_mastery,
            'change': new_mastery - old_mastery,
            'context': context or {}
        })

        # Update performance metrics
        self._update_performance_metrics(learner, skill_id, outcome)

        return new_mastery, {
            'old_mastery': old_mastery,
            'new_mastery': new_mastery,
            'change': new_mastery - old_mastery,
            'skill_id': skill_id,
            'update_type': 'correct' if outcome == 'correct' else 'incorrect'
        }

    def _update_performance_metrics(
        self,
        learner: LearningAnalytics,
        skill_id: str,
        outcome: str
    ):
        """Update performance metrics for learner."""
        if 'total_attempts' not in learner.performance_metrics:
            learner.performance_metrics['total_attempts'] = 0

        if 'correct_attempts' not in learner.performance_metrics:
            learner.performance_metrics['correct_attempts'] = 0

        learner.performance_metrics['total_attempts'] += 1

        if outcome == 'correct':
            learner.performance_metrics['correct_attempts'] += 1

        # Update overall accuracy
        learner.performance_metrics['overall_accuracy'] = \
            learner.performance_metrics['correct_attempts'] / \
            learner.performance_metrics['total_attempts']

    def predict_performance(
        self,
        learner_id: str,
        skill_id: str,
        exercise_difficulty: str = 'intermediate'
    ) -> float:
        """
        Predict probability of correct performance.

        Args:
            learner_id: Learner identifier
            skill_id: Skill to predict performance on
            exercise_difficulty: Difficulty of exercise

        Returns:
            Probability of correct performance (0.0 to 1.0)
        """
        if learner_id not in self.learner_models:
            self.initialize_learner(learner_id)

        learner = self.learner_models[learner_id]

        if skill_id not in learner.skills:
            return 0.0

        skill = learner.skills[skill_id]

        # Apply difficulty adjustment
        difficulty_adjustment = self._get_difficulty_adjustment(exercise_difficulty)

        # Calculate probability of correct response
        # P(Correct) = P(Knows) * (1 - p_S) + P(Doesn't Know) * p_G
        p_correct = skill.p_mastery * (1 - skill.p_S) + \
                     (1 - skill.p_mastery) * skill.p_G

        # Apply difficulty adjustment
        p_correct_adjusted = max(p_correct - difficulty_adjustment, 0.0)
        p_correct_adjusted = min(p_correct_adjusted, 1.0)

        return p_correct_adjusted

    def _get_difficulty_adjustment(self, difficulty: str) -> float:
        """Get difficulty adjustment factor."""
        adjustments = {
            'beginner': 0.0,
            'intermediate': 0.1,
            'advanced': 0.2,
            'expert': 0.3
        }
        return adjustments.get(difficulty, 0.1)

    def select_optimal_exercise(
        self,
        learner_id: str,
        available_exercises: Optional[List[str]] = None,
        max_exercises: int = 5
    ) -> ExerciseRecommendation:
        """
        Select exercise maximizing expected learning value.

        Uses information gain and zone of proximal development principles.

        Args:
            learner_id: Learner identifier
            available_exercises: List of exercise IDs to consider (optional)
            max_exercises: Maximum number of exercises to evaluate

        Returns:
            ExerciseRecommendation for optimal next exercise
        """
        if learner_id not in self.learner_models:
            self.initialize_learner(learner_id)

        learner = self.learner_models[learner_id]

        # Get exercises to consider
        if available_exercises:
            exercise_ids = [e for e in available_exercises
                          if e in self.exercise_database]
        else:
            exercise_ids = list(self.exercise_database.keys())

        if not exercise_ids:
            return self._create_default_recommendation(learner)

        # Evaluate each exercise
        evaluated = []
        for exercise_id in exercise_ids[:max_exercises]:
            exercise = self.exercise_database[exercise_id]
            skill_id = exercise['skill_id']
            difficulty = exercise['difficulty']

            # Skip mastered skills
            if skill_id in learner.skills:
                mastery = learner.skills[skill_id].p_mastery
                if mastery >= 0.90:  # Mastered
                    continue

            expected_learning = self._calculate_expected_learning_value(
                learner, skill_id, difficulty
            )

            success_probability = self.predict_performance(
                learner_id, skill_id, difficulty
            )

            evaluated.append({
                'exercise_id': exercise_id,
                'skill_id': skill_id,
                'difficulty': difficulty,
                'expected_learning_value': expected_learning,
                'success_probability': success_probability
            })

        if not evaluated:
            return self._create_default_recommendation(learner)

        # Select exercise with highest expected learning value
        # But bias toward exercises in zone of proximal development (0.3-0.7 mastery)
        best = max(evaluated, key=lambda x: self._score_exercise(x))

        # Get alternatives
        alternatives = [e for e in evaluated if e['exercise_id'] != best['exercise_id']]
        alternatives = sorted(alternatives, key=lambda x: x['expected_learning_value'], reverse=True)[:3]

        return ExerciseRecommendation(
            exercise_id=best['exercise_id'],
            skill_id=best['skill_id'],
            difficulty=best['difficulty'],
            expected_learning_value=best['expected_learning_value'],
            probability_of_success=best['success_probability'],
            rationale=self._generate_recommendation_rationale(best, learner),
            alternative_exercises=alternatives
        )

    def _calculate_expected_learning_value(
        self,
        learner: LearningAnalytics,
        skill_id: str,
        difficulty: str
    ) -> float:
        """Calculate expected learning value for an exercise."""
        if skill_id not in learner.skills:
            return 0.5  # Moderate value for unknown skills

        skill = learner.skills[skill_id]

        # Learning value is highest at intermediate mastery levels
        # Zone of proximal development: 0.3 - 0.7 mastery
        mastery = skill.p_mastery

        if 0.3 <= mastery <= 0.7:
            # In zone of proximal development - high value
            base_value = 0.8
        elif mastery < 0.3:
            # Below zone - still high value
            base_value = 0.9
        else:
            # Near mastery - lower value
            base_value = 0.4

        # Adjust for learnability
        learnability = skill.p_T
        adjusted_value = base_value * (1 + learnability)

        return min(adjusted_value, 1.0)

    def _score_exercise(self, exercise_eval: Dict[str, Any]) -> float:
        """Score exercise for selection."""
        # Combine expected learning with zone of proximal development
        learning_value = exercise_eval['expected_learning_value']
        success_prob = exercise_eval['success_probability']

        # Prefer exercises with good balance of learning and success
        # Success probability around 0.5-0.7 is ideal
        if 0.5 <= success_prob <= 0.7:
            success_bonus = 0.2
        elif success_prob < 0.3:
            success_bonus = -0.1  # Too hard
        elif success_prob > 0.9:
            success_bonus = -0.1  # Too easy
        else:
            success_bonus = 0.0

        return learning_value + success_bonus

    def _generate_recommendation_rationale(
        self,
        best_exercise: Dict[str, Any],
        learner: LearningAnalytics
    ) -> str:
        """Generate rationale for exercise recommendation."""
        skill_id = best_exercise['skill_id']
        success_prob = best_exercise['success_probability']

        if skill_id in learner.skills:
            mastery = learner.skills[skill_id].p_mastery
            mastery_level = learner.skills[skill_id]._determine_mastery_level()

            return (f"This exercise targets your {mastery_level} "
                   f"{learner.skills[skill_id].skill_name} skill "
                   f"(current mastery: {mastery:.1%}). "
                   f"Expected success probability: {success_prob:.1%}.")
        else:
            return f"This exercise introduces a new concept. Expected success probability: {success_prob:.1%}."

    def _create_default_recommendation(self, learner: LearningAnalytics) -> ExerciseRecommendation:
        """Create default exercise recommendation."""
        return ExerciseRecommendation(
            exercise_id='default_exercise',
            skill_id='general',
            difficulty='intermediate',
            expected_learning_value=0.5,
            probability_of_success=0.5,
            rationale="Default exercise for continued practice.",
            alternative_exercises=[]
        )

    def get_learner_analytics(
        self,
        learner_id: str
    ) -> Optional[LearningAnalytics]:
        """Get comprehensive analytics for a learner."""
        if learner_id not in self.learner_models:
            return None

        return self.learner_models[learner_id]

    def generate_mastery_report(
        self,
        learner_id: str
    ) -> Dict[str, Any]:
        """
        Generate comprehensive mastery report for learner.

        Args:
            learner_id: Learner identifier

        Returns:
            Complete mastery report with visualizations
        """
        learner = self.get_learner_analytics(learner_id)
        if not learner:
            return {'error': 'Learner not found'}

        # Calculate mastery levels across skills
        mastery_levels = {}
        for skill_id, skill in learner.skills.items():
            mastery_levels[skill_id] = {
                'name': skill.skill_name,
                'mastery_probability': skill.p_mastery,
                'mastery_level': skill._determine_mastery_level(),
                'category': self.skill_database[skill_id]['category']
            }

        # Calculate overall metrics
        total_attempts = learner.performance_metrics.get('total_attempts', 0)
        correct_attempts = learner.performance_metrics.get('correct_attempts', 0)
        overall_accuracy = learner.performance_metrics.get('overall_accuracy', 0.0)

        # Identify strengths and weaknesses
        mastered_skills = [s for s, p in mastery_levels.items() if p['mastery_level'] == 'mastered']
        developing_skills = [s for s, p in mastery_levels.items() if p['mastery_level'] == 'developing']
        novice_skills = [s for s, p in mastery_levels.items() if p['mastery_level'] == 'novice']

        return {
            'learner_id': learner_id,
            'mastery_levels': mastery_levels,
            'strengths': mastered_skills,
            'developing': developing_skills,
            'weaknesses': novice_skills,
            'overall_metrics': {
                'total_exercises': total_attempts,
                'correct_exercises': correct_attempts,
                'overall_accuracy': overall_accuracy,
                'time_spent': learner.time_spent,
                'last_updated': learner.last_updated
            },
            'recommendations': self._generate_learning_recommendations(learner),
            'visualization_data': self._create_visualization_data(mastery_levels)
        }

    def _generate_learning_recommendations(
        self,
        learner: LearningAnalytics
    ) -> List[str]:
        """Generate personalized learning recommendations."""
        recommendations = []

        # Find skills needing practice
        for skill_id, skill in learner.skills.items():
            if skill.p_mastery < 0.30:
                recommendations.append(
                    f"Focus on {skill.skill_name} - needs foundational practice"
                )
            elif 0.30 <= skill.p_mastery < 0.70:
                recommendations.append(
                    f"Continue practicing {skill.skill_name} - in learning zone"
                )

        # Check overall performance
        accuracy = learner.performance_metrics.get('overall_accuracy', 0.0)
        if accuracy < 0.70:
            recommendations.append("Overall accuracy below 70% - review fundamentals")

        return recommendations if recommendations else ["Continuing excellent progress!"]

    def _create_visualization_data(
        self,
        mastery_levels: Dict[str, Dict]
    ) -> Dict[str, Any]:
        """Create data for mastery visualization."""
        return {
            'skill_mastery_chart': [
                {
                    'skill': data['name'],
                    'mastery': data['mastery_probability'],
                    'level': data['mastery_level']
                }
                for skill_id, data in mastery_levels.items()
            ],
            'category_breakdown': self._aggregate_by_category(mastery_levels),
            'progress_over_time': []  # Would populate from exercise history
        }

    def _aggregate_by_category(
        self,
        mastery_levels: Dict[str, Dict]
    ) -> Dict[str, float]:
        """Aggregate mastery by skill category."""
        categories = {}

        for skill_id, data in mastery_levels.items():
            category = self.skill_database[skill_id]['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(data['mastery_probability'])

        return {
            category: sum(values) / len(values)
            for category, values in categories.items()
        }


# Global instance
_knowledge_tracer = None


def get_knowledge_tracer() -> BayesianKnowledgeTracer:
    """Get or create the global knowledge tracer."""
    global _knowledge_tracer
    if _knowledge_tracer is None:
        _knowledge_tracer = BayesianKnowledgeTracer()
    return _knowledge_tracer


# Tool functions for external use

def initialize_learner(learner_id: str) -> Dict[str, Any]:
    """
    Initialize a new learner model.

    Tool wrapper for external use.
    """
    try:
        tracer = get_knowledge_tracer()
        learner = tracer.initialize_learner(learner_id)
        return {
            'success': True,
            'learner': learner.to_dict()
        }
    except Exception as e:
        logger.error(f"Failed to initialize learner: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def update_mastery(
    learner_id: str,
    skill_id: str,
    outcome: str,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Update learner mastery based on performance.

    Tool wrapper for external use.
    """
    try:
        tracer = get_knowledge_tracer()
        new_mastery, metadata = tracer.update_mastery(
            learner_id, skill_id, outcome, context
        )
        return {
            'success': True,
            'new_mastery': new_mastery,
            'metadata': metadata
        }
    except Exception as e:
        logger.error(f"Failed to update mastery: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def predict_performance(
    learner_id: str,
    skill_id: str,
    exercise_difficulty: str = 'intermediate'
) -> Dict[str, Any]:
    """
    Predict performance probability.

    Tool wrapper for external use.
    """
    try:
        tracer = get_knowledge_tracer()
        probability = tracer.predict_performance(
            learner_id, skill_id, exercise_difficulty
        )
        return {
            'success': True,
            'probability': probability
        }
    except Exception as e:
        logger.error(f"Failed to predict performance: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def select_next_exercise(
    learner_id: str,
    available_exercises: Optional[List[str]] = None,
    max_exercises: int = 5
) -> Dict[str, Any]:
    """
    Select optimal next exercise for learner.

    Tool wrapper for external use.
    """
    try:
        tracer = get_knowledge_tracer()
        recommendation = tracer.select_optimal_exercise(
            learner_id, available_exercises, max_exercises
        )
        return {
            'success': True,
            'recommendation': recommendation.to_dict()
        }
    except Exception as e:
        logger.error(f"Failed to select exercise: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def generate_mastery_report(learner_id: str) -> Dict[str, Any]:
    """
    Generate comprehensive mastery report.

    Tool wrapper for external use.
    """
    try:
        tracer = get_knowledge_tracer()
        report = tracer.generate_mastery_report(learner_id)
        return {
            'success': True,
            'report': report
        }
    except Exception as e:
        logger.error(f"Failed to generate report: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == "__main__":
    # Test the knowledge tracing system
    print("Testing Knowledge Tracing System...")

    # Test learner initialization
    learner = initialize_learner('test_learner_1')
    print(f"Learner initialized: {learner['success']}")

    # Test mastery updates
    update1 = update_mastery('test_learner_1', 'python_loops', 'correct')
    print(f"First update: {update1['success']}, new mastery: {update1.get('new_mastery', 0):.2f}")

    update2 = update_mastery('test_learner_1', 'python_loops', 'correct')
    print(f"Second update: {update2['success']}, new mastery: {update2.get('new_mastery', 0):.2f}")

    # Test prediction
    prediction = predict_performance('test_learner_1', 'python_loops', 'intermediate')
    print(f"Performance prediction: {prediction['success']}, probability: {prediction['probability']:.2f}")

    # Test exercise selection
    selection = select_next_exercise('test_learner_1')
    print(f"Exercise selection: {selection['success']}")
    if selection['success']:
        rec = selection['recommendation']
        print(f"Selected: {rec['exercise_id']}")

    # Test mastery report
    report = generate_mastery_report('test_learner_1')
    print(f"Mastery report: {report['success']}")
    if report['success']:
        print(f"Skills tracked: {len(report['report']['mastery_levels'])}")

    print("Knowledge Tracing System test complete!")
