"""
Self-Explanation System for Programming Education

Based on research from:
- Renkl, A. (2002). "Worked-Out Examples: Instructional Explanations Support Learning by Self-Explanations."
- Chi, M. T. H., et al. (1989). "Self-Explanations: How Students Study and Use Examples."

Effect sizes: d = 0.89 for learning gains when self-explanations are used properly.
"""

import json
import logging
import time
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re

logger = logging.getLogger(__name__)


class ExplanationQuality(Enum):
    """Quality levels for self-explanations."""
    EXCELLENT = "excellent"  # 4: Comprehensive, accurate, detailed
    GOOD = "good"  # 3: Accurate, reasonably detailed
    ADEQUATE = "adequate"  # 2: Partially accurate, minimal detail
    INADEQUATE = "inadequate"  # 1: Inaccurate or missing
    NOT_ATTEMPTED = "not_attempted"  # 0: No explanation provided


class ScaffoldingLevel(Enum):
    """Scaffolding levels for self-explanation prompts."""
    SENTENCE_STEMS = 0  # Provide sentence starters
    GUIDED_PROMPTS = 1  # Provide specific questions
    STRUCTURED = 2  # Provide structured template
    HINTS = 3  # Provide hints only
    MINIMAL = 4  # Minimal guidance
    INDEPENDENT = 5  # No scaffolding


@dataclass
class ExplanationPrompt:
    """A self-explanation prompt with multiple components."""
    before_step: str
    after_step: str
    principle_check: str
    prediction: str
    metacognitive: str

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return {
            'before_step': self.before_step,
            'after_step': self.after_step,
            'principle_check': self.principle_check,
            'prediction': self.prediction,
            'metacognitive': self.metacognitive
        }


@dataclass
class ExplanationAssessment:
    """Assessment of learner's self-explanation."""
    quality: ExplanationQuality
    completeness_score: float  # 0.0 to 1.0
    accuracy_score: float  # 0.0 to 1.0
    depth_score: float  # 0.0 to 1.0
    transfer_potential: float  # 0.0 to 1.0
    feedback: str
    strengths: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    rubric_details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'quality': self.quality.value,
            'completeness_score': self.completeness_score,
            'accuracy_score': self.accuracy_score,
            'depth_score': self.depth_score,
            'transfer_potential': self.transfer_potential,
            'feedback': self.feedback,
            'strengths': self.strengths,
            'improvements': self.improvements,
            'rubric_details': self.rubric_details
        }


@dataclass
class ConceptExplanation:
    """A self-explanation for a specific programming concept."""
    concept_id: str
    learner_explanation: str
    target_concept: str
    scaffolding_used: ScaffoldingLevel
    time_taken_seconds: float
    prompts: List[str]
    assessment: Optional[ExplanationAssessment] = None
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'concept_id': self.concept_id,
            'learner_explanation': self.learner_explanation,
            'target_concept': self.target_concept,
            'scaffolding_used': self.scaffolding_used.value,
            'time_taken_seconds': self.time_taken_seconds,
            'prompts': self.prompts,
            'assessment': self.assessment.to_dict() if self.assessment else None,
            'timestamp': self.timestamp
        }


class SelfExplanationEngine:
    """
    Production-grade self-explanation system for programming education.

    Implements research-backed self-explanation strategies with:
    - Targeted prompt generation
    - Quality assessment
    - Adaptive scaffolding
    - Progressive difficulty
    """

    def __init__(self, config_path: str = 'config/config.json'):
        """Initialize the self-explanation engine with configuration."""
        self.config = self._load_config(config_path)
        self.concept_database = self._load_concept_database()
        self.prompt_templates = self._load_prompt_templates()
        self.quality_rubric = self._load_quality_rubric()
        self.explanation_history = {}

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except Exception as e:
            logger.warning(f"Failed to load config: {e}, using defaults")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'self_explanation': {
                'enabled': True,
                'min_explanation_length': 10,
                'max_explanation_length': 500,
                'quality_threshold': 0.7,
                'adaptive_scaffolding': True
            }
        }

    def _load_concept_database(self) -> Dict[str, Dict]:
        """Load database of programming concepts with explanation requirements."""
        return {
            'loops': {
                'key_principles': ['iteration', 'condition', 'update', 'termination'],
                'common_misconceptions': ['loops execute once always', 'condition checked after body'],
                'transfer_concepts': ['while_loops', 'for_loops', 'recursion'],
                'explanation_requirements': {
                    'must_mention': ['iteration', 'condition'],
                    'should_mention': ['update', 'termination'],
                    'bonus_mentions': ['efficiency', 'use_cases']
                }
            },
            'functions': {
                'key_principles': ['abstraction', 'parameters', 'return_values', 'scope'],
                'common_misconceptions': ['functions modify originals', 'return is optional'],
                'transfer_concepts': ['methods', 'lambdas', 'closures'],
                'explanation_requirements': {
                    'must_mention': ['abstraction', 'parameters'],
                    'should_mention': ['return_values', 'scope'],
                    'bonus_mentions': ['reusability', 'side_effects']
                }
            },
            'arrays': {
                'key_principles': ['indexed_storage', 'sequential_access', 'memory_layout'],
                'common_misconceptions': ['arrays start at index 1', 'arrays are fixed size always'],
                'transfer_concepts': ['lists', 'vectors', 'dynamic_arrays'],
                'explanation_requirements': {
                    'must_mention': ['indexed_storage', 'zero_indexed'],
                    'should_mention': ['sequential_access', 'memory_contiguous'],
                    'bonus_mentions': ['complexity', 'alternatives']
                }
            },
            'recursion': {
                'key_principles': ['base_case', 'recursive_case', 'stack_frame'],
                'common_misconceptions': ['recursion is infinite', 'base_case optional'],
                'transfer_concepts': ['iteration', 'divide_conquer'],
                'explanation_requirements': {
                    'must_mention': ['base_case', 'recursive_case'],
                    'should_mention': ['stack', 'call_stack'],
                    'bonus_mentions': ['tail_recursion', 'stack_overflow']
                }
            },
            'conditionals': {
                'key_principles': ['boolean_logic', 'branching', 'execution_flow'],
                'common_misconceptions': ['elseif is required', 'conditions check all cases'],
                'transfer_concepts': ['switch_cases', 'ternary_operators'],
                'explanation_requirements': {
                    'must_mention': ['boolean_evaluation', 'branching'],
                    'should_mention': ['execution_flow', 'conditions_order'],
                    'bonus_mentions': ['short_circuit', 'nested_conditions']
                }
            },
            'variables': {
                'key_principles': ['storage', 'typing', 'scope', 'assignment'],
                'common_misconceptions': ['variables store expressions', 'assignment is equality'],
                'transfer_concepts': ['constants', 'references', 'pointers'],
                'explanation_requirements': {
                    'must_mention': ['storage', 'assignment'],
                    'should_mention': ['scope', 'naming'],
                    'bonus_mentions': ['type_system', 'memory_location']
                }
            }
        }

    def _load_prompt_templates(self) -> Dict[str, List[str]]:
        """Load prompt templates for different scaffolding levels."""
        return {
            'before_step': [
                "Before we execute this line, what do you think will happen?",
                "Looking at this code, what do you expect this line to do?",
                "Predict the result of executing this line.",
                "What does this line accomplish in the overall program?"
            ],
            'after_step': [
                "Now that we've executed this line, why did we get that result?",
                "Explain in your own words what just happened.",
                "Why does this code produce this specific output?",
                "What programming principle is being demonstrated here?"
            ],
            'principle_check': [
                "What programming concept or principle is being used in this code?",
                "Can you identify the key concept being applied here?",
                "Which fundamental programming rule is this example following?",
                "What pattern does this code demonstrate?"
            ],
            'prediction': [
                "What would happen if we changed this part of the code?",
                "How would the output change if we modified this value?",
                "Predict the result if we removed this line.",
                "What would break if we changed this condition?"
            ],
            'metacognitive': [
                "Does this explanation make complete sense to you? What's unclear?",
                "On a scale of 1-5, how well do you understand this concept?",
                "What aspect of this do you find most confusing?",
                "Can you think of a real-world analogy for this concept?"
            ]
        }

    def _load_quality_rubric(self) -> Dict[str, Dict]:
        """Load quality assessment rubric."""
        return {
            'completeness': {
                'excellent': {'min_mentions': 4, 'detail_level': 'high'},
                'good': {'min_mentions': 3, 'detail_level': 'medium'},
                'adequate': {'min_mentions': 2, 'detail_level': 'basic'},
                'inadequate': {'min_mentions': 1, 'detail_level': 'minimal'}
            },
            'accuracy': {
                'excellent': {'correct_concepts': 1.0, 'no_misconceptions': True},
                'good': {'correct_concepts': 0.8, 'minor_misconceptions': 1},
                'adequate': {'correct_concepts': 0.6, 'minor_misconceptions': 2},
                'inadequate': {'correct_concepts': 0.4, 'major_misconceptions': True}
            },
            'depth': {
                'excellent': {'mechanism_explained': True, 'why_included': True, 'connections_made': True},
                'good': {'mechanism_explained': True, 'why_included': True, 'connections_made': False},
                'adequate': {'mechanism_explained': True, 'why_included': False, 'connections_made': False},
                'inadequate': {'mechanism_explained': False, 'why_included': False, 'connections_made': False}
            },
            'transfer': {
                'excellent': {'generalizable_principle': True, 'applications': 3},
                'good': {'generalizable_principle': True, 'applications': 2},
                'adequate': {'generalizable_principle': True, 'applications': 1},
                'inadequate': {'generalizable_principle': False, 'applications': 0}
            }
        }

    def generate_prompts_for_step(
        self,
        concept: str,
        code_step: str,
        scaffolding_level: ScaffoldingLevel = ScaffoldingLevel.GUIDED_PROMPTS
    ) -> ExplanationPrompt:
        """
        Generate targeted self-explanation prompts for a code step.

        Args:
            concept: Programming concept being taught
            code_step: Specific code line or block being explained
            scaffolding_level: Level of guidance to provide

        Returns:
            ExplanationPrompt with targeted questions
        """
        concept_info = self.concept_database.get(concept, {})
        principles = concept_info.get('key_principles', [])
        misconceptions = concept_info.get('common_misconceptions', [])

        # Select appropriate prompts based on scaffolding level
        if scaffolding_level == ScaffoldingLevel.SENTENCE_STEMS:
            return self._generate_sentence_stem_prompts(concept, code_step, principles)
        elif scaffolding_level == ScaffoldingLevel.GUIDED_PROMPTS:
            return self._generate_guided_prompts(concept, code_step, principles)
        elif scaffolding_level == ScaffoldingLevel.STRUCTURED:
            return self._generate_structured_prompts(concept, code_step, principles)
        elif scaffolding_level == ScaffoldingLevel.HINTS:
            return self._generate_hint_prompts(concept, code_step, principles)
        else:
            return self._generate_minimal_prompts(concept, code_step)

    def _generate_sentence_stem_prompts(
        self,
        concept: str,
        code_step: str,
        principles: List[str]
    ) -> ExplanationPrompt:
        """Generate prompts with sentence stems for completion."""
        return ExplanationPrompt(
            before_step=f"This line of code {code_step} will ______________ because ______________.",
            after_step=f"The result we got happened because ______________, which demonstrates ______________.",
            principle_check=f"The programming principle being used here is ______________, which means ______________.",
            prediction=f"If we changed this code to ______________, then the output would ______________ because ______________.",
            metacognitive=f"I understand this concept [well/somewhat/not at all] because ______________."
        )

    def _generate_guided_prompts(
        self,
        concept: str,
        code_step: str,
        principles: List[str]
    ) -> ExplanationPrompt:
        """Generate guided prompts with specific questions."""
        principle_focus = principles[0] if principles else "this concept"

        return ExplanationPrompt(
            before_step=f"Before executing '{code_step}', what do you think will happen? Consider how {principle_focus} works.",
            after_step=f"Now that we've executed this step, explain why we got this result. What does this show about {concept}?",
            principle_check=f"Which of these principles is being demonstrated: {', '.join(principles)}? Explain your choice.",
            prediction=f"What would happen to the output if we removed or changed this line? Be specific.",
            metacognitive=f"On a scale of 1-5, how well do you understand this? What specifically is clear or unclear?"
        )

    def _generate_structured_prompts(
        self,
        concept: str,
        code_step: str,
        principles: List[str]
    ) -> ExplanationPrompt:
        """Generate structured template prompts."""
        return ExplanationPrompt(
            before_step=f"STEP 1: Prediction - What will '{code_step}' do?\nSTEP 2: Reasoning - Why do you think this?",
            after_step=f"STEP 1: Observation - What actually happened?\nSTEP 2: Explanation - Why did this occur?",
            principle_check=f"Identify the programming principle used and explain how it applies to '{code_step}'.",
            prediction=f"Hypothesis: If we modified this code to ______________, then ______________ because ______________.",
            metacognitive=f"Reflection: I [fully/partially/minimally] understand this because ______________."
        )

    def _generate_hint_prompts(
        self,
        concept: str,
        code_step: str,
        principles: List[str]
    ) -> ExplanationPrompt:
        """Generate minimal hint prompts."""
        return ExplanationPrompt(
            before_step=f"What will '{code_step}' accomplish?",
            after_step=f"Why did this code produce this result?",
            principle_check=f"What programming concept is being used here?",
            prediction=f"How would changing this affect the output?",
            metacognitive=f"How confident are you in your understanding (1-5)?"
        )

    def _generate_minimal_prompts(
        self,
        concept: str,
        code_step: str
    ) -> ExplanationPrompt:
        """Generate minimal prompts for independent learners."""
        return ExplanationPrompt(
            before_step=f"Explain what this code will do.",
            after_step=f"Explain why this code produced this result.",
            principle_check=f"What principle is being demonstrated?",
            prediction=f"What if we changed this?",
            metacognitive=f"How well do you understand this?"
        )

    def assess_explanation(
        self,
        explanation: str,
        target_concept: str,
        code_context: Optional[str] = None
    ) -> ExplanationAssessment:
        """
        Assess the quality of a learner's self-explanation.

        Uses multi-dimensional rubric based on research findings.

        Args:
            explanation: Learner's explanation text
            target_concept: Concept being explained
            code_context: Optional code context for assessment

        Returns:
            ExplanationAssessment with quality ratings and feedback
        """
        if not explanation or len(explanation.strip()) < 10:
            return self._create_inadequate_assessment("Explanation too short or missing")

        concept_info = self.concept_database.get(target_concept, {})
        requirements = concept_info.get('explanation_requirements', {})
        misconceptions = concept_info.get('common_misconceptions', [])

        # Assess each dimension
        completeness = self._assess_completeness(explanation, requirements)
        accuracy = self._assess_accuracy(explanation, target_concept, misconceptions)
        depth = self._assess_depth(explanation, requirements)
        transfer = self._assess_transfer(explanation, concept_info)

        # Calculate overall quality
        overall_score = (
            completeness * 0.3 +
            accuracy * 0.4 +
            depth * 0.2 +
            transfer * 0.1
        )

        quality = self._determine_quality_level(overall_score)

        # Generate feedback
        feedback = self._generate_feedback(quality, completeness, accuracy, depth, transfer)
        strengths = self._identify_strengths(explanation, requirements)
        improvements = self._identify_improvements(explanation, requirements, misconceptions)

        return ExplanationAssessment(
            quality=quality,
            completeness_score=completeness,
            accuracy_score=accuracy,
            depth_score=depth,
            transfer_potential=transfer,
            feedback=feedback,
            strengths=strengths,
            improvements=improvements,
            rubric_details={
                'word_count': len(explanation.split()),
                'sentence_count': len(re.split(r'[.!?]+', explanation)),
                'key_terms_found': self._find_key_terms(explanation, target_concept),
                'structure_analysis': self._analyze_structure(explanation)
            }
        )

    def _assess_completeness(
        self,
        explanation: str,
        requirements: Dict[str, List[str]]
    ) -> float:
        """Assess explanation completeness (0.0 to 1.0)."""
        must_mention = requirements.get('must_mention', [])
        should_mention = requirements.get('should_mention', [])
        bonus_mentions = requirements.get('bonus_mentions', [])

        explanation_lower = explanation.lower()

        # Count mentions
        must_count = sum(1 for term in must_mention if term in explanation_lower)
        should_count = sum(1 for term in should_mention if term in explanation_lower)
        bonus_count = sum(1 for term in bonus_mentions if term in explanation_lower)

        # Calculate score
        must_score = must_count / len(must_mention) if must_mention else 1.0
        should_score = should_count / len(should_mention) if should_mention else 0.0
        bonus_score = bonus_count / len(bonus_mentions) if bonus_mentions else 0.0

        # Weighted calculation (must-mention most important)
        completeness = (must_score * 0.6 + should_score * 0.3 + bonus_score * 0.1)
        return min(completeness, 1.0)

    def _assess_accuracy(
        self,
        explanation: str,
        concept: str,
        common_misconceptions: List[str]
    ) -> float:
        """Assess explanation accuracy (0.0 to 1.0)."""
        explanation_lower = explanation.lower()

        # Check for misconceptions
        misconception_count = sum(
            1 for misconception in common_misconceptions
            if misconception.lower() in explanation_lower
        )

        # Penalize misconceptions
        misconception_penalty = misconception_count * 0.3

        # Check for accurate concept usage
        concept_info = self.concept_database.get(concept, {})
        accurate_indicators = [
            'correctly', 'accurately', 'properly', 'appropriately',
            'because', 'therefore', 'thus', 'means that'
        ]

        accuracy_indicators = sum(
            1 for indicator in accurate_indicators
            if indicator in explanation_lower
        )

        accuracy_bonus = min(accuracy_indicators * 0.1, 0.3)

        accuracy = 1.0 - misconception_penalty + accuracy_bonus
        return max(min(accuracy, 1.0), 0.0)

    def _assess_depth(
        self,
        explanation: str,
        requirements: Dict[str, List[str]]
    ) -> float:
        """Assess explanation depth (0.0 to 1.0)."""
        # Check for mechanistic explanations
        mechanism_keywords = [
            'works by', 'functions', 'operates', 'executes',
            'because', 'causes', 'results in', 'leads to'
        ]

        # Check for "why" explanations
        why_keywords = [
            'because', 'since', 'due to', 'reason', 'therefore',
            'purpose', 'designed to', 'intended to'
        ]

        # Check for connections
        connection_keywords = [
            'similar to', 'like', 'unlike', 'compared to',
            'relates to', 'connection', 'relates'
        ]

        explanation_lower = explanation.lower()

        mechanism_score = min(sum(1 for kw in mechanism_keywords if kw in explanation_lower) * 0.2, 0.4)
        why_score = min(sum(1 for kw in why_keywords if kw in explanation_lower) * 0.25, 0.35)
        connection_score = min(sum(1 for kw in connection_keywords if kw in explanation_lower) * 0.25, 0.25)

        depth_score = mechanism_score + why_score + connection_score
        return min(depth_score, 1.0)

    def _assess_transfer(
        self,
        explanation: str,
        concept_info: Dict
    ) -> float:
        """Assess transfer potential (0.0 to 1.0)."""
        # Check for generalizable principles
        generalizable_keywords = [
            'in general', 'typically', 'usually', 'commonly',
            'principle', 'rule', 'pattern', 'applies to'
        ]

        # Check for application mentions
        application_keywords = [
            'can be used', 'application', 'use case', 'example',
            'applies', 'works when', 'useful for'
        ]

        explanation_lower = explanation.lower()

        generalizable = any(kw in explanation_lower for kw in generalizable_keywords)
        applications = sum(1 for kw in application_keywords if kw in explanation_lower)

        transfer_score = (0.5 if generalizable else 0.0) + min(applications * 0.15, 0.5)
        return min(transfer_score, 1.0)

    def _determine_quality_level(self, overall_score: float) -> ExplanationQuality:
        """Determine quality level from overall score."""
        if overall_score >= 0.9:
            return ExplanationQuality.EXCELLENT
        elif overall_score >= 0.75:
            return ExplanationQuality.GOOD
        elif overall_score >= 0.6:
            return ExplanationQuality.ADEQUATE
        elif overall_score >= 0.3:
            return ExplanationQuality.INADEQUATE
        else:
            return ExplanationQuality.NOT_ATTEMPTED

    def _generate_feedback(
        self,
        quality: ExplanationQuality,
        completeness: float,
        accuracy: float,
        depth: float,
        transfer: float
    ) -> str:
        """Generate constructive feedback based on assessment."""
        feedback_templates = {
            ExplanationQuality.EXCELLENT: "Excellent explanation! You've demonstrated comprehensive understanding.",
            ExplanationQuality.GOOD: "Good explanation with solid understanding. Minor improvements possible.",
            ExplanationQuality.ADEQUATE: "Adequate explanation covering basics. Room for deeper understanding.",
            ExplanationQuality.INADEQUATE: "Explanation needs significant improvement. Key concepts missing.",
            ExplanationQuality.NOT_ATTEMPTED: "No explanation provided. Please explain in your own words."
        }

        base_feedback = feedback_templates[quality]

        # Add specific suggestions
        suggestions = []
        if completeness < 0.7:
            suggestions.append("Include more key concepts in your explanation.")
        if accuracy < 0.7:
            suggestions.append("Review the concept to avoid misconceptions.")
        if depth < 0.7:
            suggestions.append("Explain WHY things work, not just WHAT works.")
        if transfer < 0.7:
            suggestions.append("Consider how this concept applies in different contexts.")

        if suggestions:
            base_feedback += " Suggestions: " + "; ".join(suggestions)

        return base_feedback

    def _identify_strengths(
        self,
        explanation: str,
        requirements: Dict[str, List[str]]
    ) -> List[str]:
        """Identify strengths in the explanation."""
        strengths = []
        explanation_lower = explanation.lower()

        # Check for key concept mentions
        must_mention = requirements.get('must_mention', [])
        found_concepts = [term for term in must_mention if term in explanation_lower]
        if found_concepts:
            strengths.append(f"Correctly identified key concepts: {', '.join(found_concepts)}")

        # Check for mechanistic explanations
        if any(kw in explanation_lower for kw in ['because', 'works by', 'functions']):
            strengths.append("Provided mechanistic explanation")

        # Check for appropriate length
        word_count = len(explanation.split())
        if 20 <= word_count <= 100:
            strengths.append("Appropriate explanation length")

        return strengths

    def _identify_improvements(
        self,
        explanation: str,
        requirements: Dict[str, List[str]],
        misconceptions: List[str]
    ) -> List[str]:
        """Identify areas for improvement."""
        improvements = []
        explanation_lower = explanation.lower()

        # Check for missing must-mention concepts
        must_mention = requirements.get('must_mention', [])
        missing_concepts = [term for term in must_mention if term not in explanation_lower]
        if missing_concepts:
            improvements.append(f"Consider including: {', '.join(missing_concepts)}")

        # Check for misconceptions
        found_misconceptions = [
            m for m in misconceptions
            if m.lower() in explanation_lower
        ]
        if found_misconceptions:
            improvements.append(f"Avoid common misconceptions: {', '.join(found_misconceptions)}")

        # Check for explanation length
        word_count = len(explanation.split())
        if word_count < 15:
            improvements.append("Expand your explanation with more detail")
        elif word_count > 150:
            improvements.append("Consider condensing your explanation")

        # Check for depth
        if not any(kw in explanation_lower for kw in ['because', 'therefore', 'reason']):
            improvements.append("Include reasoning (why/how) in your explanation")

        return improvements

    def _find_key_terms(self, explanation: str, concept: str) -> List[str]:
        """Find key programming terms in explanation."""
        concept_info = self.concept_database.get(concept, {})
        principles = concept_info.get('key_principles', [])

        explanation_lower = explanation.lower()
        found_terms = [principle for principle in principles if principle in explanation_lower]

        return found_terms

    def _analyze_structure(self, explanation: str) -> Dict[str, Any]:
        """Analyze the structure of the explanation."""
        sentences = re.split(r'[.!?]+', explanation)
        words = explanation.split()

        return {
            'sentence_count': len([s for s in sentences if s.strip()]),
            'avg_sentence_length': len(words) / max(len(sentences), 1),
            'has_connectors': any(conn in explanation.lower() for conn in ['because', 'therefore', 'however', 'thus']),
            'has_examples': any(example in explanation.lower() for example in ['example', 'for instance', 'such as']),
            'question_count': explanation.count('?')
        }

    def _create_inadequate_assessment(self, reason: str) -> ExplanationAssessment:
        """Create assessment for inadequate explanation."""
        return ExplanationAssessment(
            quality=ExplanationQuality.INADEQUATE,
            completeness_score=0.0,
            accuracy_score=0.0,
            depth_score=0.0,
            transfer_potential=0.0,
            feedback=f"Explanation inadequate: {reason}",
            strengths=[],
            improvements=["Provide a complete explanation in your own words"],
            rubric_details={'reason': reason}
        )

    def create_self_explanation_exercise(
        self,
        concept: str,
        worked_example: str,
        scaffolding_level: ScaffoldingLevel = ScaffoldingLevel.GUIDED_PROMPTS
    ) -> Dict[str, Any]:
        """
        Create a complete self-explanation exercise from a worked example.

        Args:
            concept: Programming concept being taught
            worked_example: Complete worked example code
            scaffolding_level: Level of guidance to provide

        Returns:
            Complete exercise with prompts and assessment
        """
        # Break example into steps
        steps = self._parse_example_into_steps(worked_example)

        # Generate prompts for each step
        exercise_steps = []
        for i, step in enumerate(steps):
            prompts = self.generate_prompts_for_step(concept, step, scaffolding_level)
            exercise_steps.append({
                'step_number': i + 1,
                'code_step': step,
                'prompts': prompts.to_dict(),
                'expected_elements': self._get_expected_explanation_elements(concept)
            })

        return {
            'concept': concept,
            'worked_example': worked_example,
            'scaffolding_level': scaffolding_level.value,
            'steps': exercise_steps,
            'overall_instructions': self._generate_overall_instructions(concept),
            'assessment_rubric': self._generate_assessment_rubric(concept)
        }

    def _parse_example_into_steps(self, example: str) -> List[str]:
        """Parse worked example into logical steps."""
        lines = example.strip().split('\n')
        steps = []

        current_step = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                current_step.append(line.rstrip())
                if line.rstrip().endswith(':') or stripped in ['def', 'class', 'if', 'for', 'while']:
                    if current_step:
                        steps.append('\n'.join(current_step))
                        current_step = []

        if current_step:
            steps.append('\n'.join(current_step))

        return steps if steps else [example.strip()]

    def _get_expected_explanation_elements(self, concept: str) -> Dict[str, List[str]]:
        """Get expected elements for a good explanation."""
        concept_info = self.concept_database.get(concept, {})
        return {
            'must_include': concept_info.get('explanation_requirements', {}).get('must_mention', []),
            'should_include': concept_info.get('explanation_requirements', {}).get('should_mention', []),
            'bonus_include': concept_info.get('explanation_requirements', {}).get('bonus_mentions', [])
        }

    def _generate_overall_instructions(self, concept: str) -> str:
        """Generate overall instructions for the self-explanation exercise."""
        return f"""Self-Explanation Exercise: {concept}

Instructions:
1. Go through each step of the worked example
2. For each step, provide your explanation in your own words
3. Answer the prompts as completely as possible
4. Focus on WHY things work, not just WHAT they do
5. Make connections to what you already know

Research shows that self-explanation can improve learning by 89% - take your time and explain thoroughly!"""

    def _generate_assessment_rubric(self, concept: str) -> Dict[str, Any]:
        """Generate assessment rubric for the exercise."""
        return {
            'completeness': {
                'excellent': 'All required concepts explained in detail',
                'good': 'Most required concepts explained',
                'adequate': 'Some required concepts mentioned',
                'inadequate': 'Few or no required concepts'
            },
            'accuracy': {
                'excellent': 'No misconceptions, all concepts accurate',
                'good': 'Minor inaccuracies, no major misconceptions',
                'adequate': 'Some inaccuracies present',
                'inadequate': 'Major misconceptions present'
            },
            'depth': {
                'excellent': 'Explains mechanisms and reasoning',
                'good': 'Explains why things work',
                'adequate': 'Describes what happens',
                'inadequate': 'Superficial or incorrect'
            },
            'transfer': {
                'excellent': 'Identifies generalizable principles',
                'good': 'Makes some connections to other contexts',
                'adequate': 'Limited transfer insights',
                'inadequate': 'No transfer potential shown'
            }
        }


# Global instance
_self_explanation_engine = None


def get_self_explanation_engine() -> SelfExplanationEngine:
    """Get or create the global self-explanation engine instance."""
    global _self_explanation_engine
    if _self_explanation_engine is None:
        _self_explanation_engine = SelfExplanationEngine()
    return _self_explanation_engine


# Tool functions for external use

def create_self_explanation_exercise(
    concept: str,
    worked_example: str,
    scaffolding_level: int = 1
) -> Dict[str, Any]:
    """
    Create a self-explanation exercise from a worked example.

    Tool wrapper for external use.
    """
    try:
        engine = get_self_explanation_engine()
        scaffolding = ScaffoldingLevel(scaffolding_level)
        exercise = engine.create_self_explanation_exercise(concept, worked_example, scaffolding)
        return {
            'success': True,
            'exercise': exercise
        }
    except Exception as e:
        logger.error(f"Failed to create self-explanation exercise: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def assess_learner_explanation(
    explanation: str,
    target_concept: str,
    code_context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Assess a learner's self-explanation quality.

    Tool wrapper for external use.
    """
    try:
        engine = get_self_explanation_engine()
        assessment = engine.assess_explanation(explanation, target_concept, code_context)
        return {
            'success': True,
            'assessment': assessment.to_dict()
        }
    except Exception as e:
        logger.error(f"Failed to assess explanation: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def generate_explanation_prompts(
    concept: str,
    code_step: str,
    scaffolding_level: int = 1
) -> Dict[str, Any]:
    """
    Generate targeted self-explanation prompts.

    Tool wrapper for external use.
    """
    try:
        engine = get_self_explanation_engine()
        scaffolding = ScaffoldingLevel(scaffolding_level)
        prompts = engine.generate_prompts_for_step(concept, code_step, scaffolding)
        return {
            'success': True,
            'prompts': prompts.to_dict()
        }
    except Exception as e:
        logger.error(f"Failed to generate prompts: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == "__main__":
    # Test the self-explanation system
    print("Testing Self-Explanation System...")

    # Test prompt generation
    prompts = generate_explanation_prompts('loops', 'for i in range(5):', 1)
    print(f"Prompts generated: {prompts['success']}")

    # Create a sample exercise
    example = """
for i in range(5):
    print(i * 2)
"""
    exercise = create_self_explanation_exercise('loops', example)
    print(f"Exercise created: {exercise['success']}")

    # Test assessment
    learner_explanation = "This loop iterates 5 times because range(5) generates numbers 0-4. Each iteration multiplies the number by 2 and prints it."
    assessment = assess_learner_explanation(learner_explanation, 'loops')
    print(f"Assessment complete: {assessment['success']}")
    if assessment['success']:
        print(f"Quality: {assessment['assessment']['quality']}")
        print(f"Completeness: {assessment['assessment']['completeness_score']:.2f}")

    print("Self-Explanation System test complete!")
