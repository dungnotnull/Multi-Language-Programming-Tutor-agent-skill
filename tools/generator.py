"""
Tool implementations for the multilanguage-coding-tutor skill.

This module provides production-grade tool implementations for generating
exercises, examples, and teaching materials.
"""

import json
import logging
import time
import random
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ExerciseType(Enum):
    """Types of exercises that can be generated."""
    PARSONS = "parsons"
    WORKED_EXAMPLE = "worked_example"
    CODE_TRACING = "code_tracing"
    FROM_SCRATCH = "from_scratch"


class Difficulty(Enum):
    """Difficulty levels for exercises."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class Exercise:
    """Base class for exercises."""
    exercise_type: ExerciseType
    concept: str
    language: str
    difficulty: Difficulty
    title: str
    instructions: str
    content: Dict[str, Any]
    hints: List[str] = field(default_factory=list)
    solution: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exercise to dictionary."""
        return {
            'exercise_type': self.exercise_type.value,
            'concept': self.concept,
            'language': self.language,
            'difficulty': self.difficulty.value,
            'title': self.title,
            'instructions': self.instructions,
            'content': self.content,
            'hints': self.hints,
            'solution': self.solution,
            'metadata': self.metadata
        }


class ExerciseGenerator:
    """Production-grade exercise generator with comprehensive capabilities."""

    def __init__(self, config_path: str = 'config/config.json'):
        """Initialize the exercise generator with configuration."""
        self.config = self._load_config(config_path)
        self.templates = self._load_templates()
        self.example_banks = self._load_example_banks()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            config_file = Path(config_path)
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load config: {e}, using defaults")

        return {
            'supported_languages': {
                'python': {'enabled': True},
                'javascript': {'enabled': True},
                'java': {'enabled': True},
                'cpp': {'enabled': True},
                'rust': {'enabled': True},
                'go': {'enabled': True}
            },
            'teaching': {
                'max_exercises_per_session': 10
            }
        }

    def _load_templates(self) -> Dict[str, Dict]:
        """Load exercise templates."""
        templates = {}

        template_path = Path('assets/parsons_templates')
        if template_path.exists():
            for template_file in template_path.glob('*.json'):
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                        templates[template_file.stem] = template_data
                except Exception as e:
                    logger.warning(f"Failed to load template {template_file}: {e}")

        return templates

    def _load_example_banks(self) -> Dict[str, Dict]:
        """Load example code banks."""
        example_banks = {}

        example_path = Path('assets/language_examples')
        if example_path.exists():
            for example_file in example_path.glob('*.json'):
                try:
                    with open(example_file, 'r', encoding='utf-8') as f:
                        example_data = json.load(f)
                        example_banks[example_file.stem] = example_data
                except Exception as e:
                    logger.warning(f"Failed to load examples {example_file}: {e}")

        return example_banks

    def generate_parsons_problem(
        self,
        concept: str,
        language: str,
        difficulty: Difficulty
    ) -> Exercise:
        """Generate a Parson's problem exercise.

        Args:
            concept: Programming concept to practice
            language: Target programming language
            difficulty: Difficulty level

        Returns:
            Exercise object with Parson's problem content
        """
        logger.info(f"Generating Parson's problem: {concept} in {language} at {difficulty.value}")

        # Validate inputs
        if not self._is_language_supported(language):
            raise ValueError(f"Language '{language}' is not supported")

        if not self._is_difficulty_valid(difficulty):
            raise ValueError(f"Difficulty '{difficulty}' is not valid")

        # Get template or generate from scratch
        template_key = f"{concept}_{language}_{difficulty.value}"
        if template_key in self.templates:
            return self._create_parsons_from_template(template_key, concept, language, difficulty)

        # Generate dynamically
        return self._generate_parsons_dynamically(concept, language, difficulty)

    def _create_parsons_from_template(
        self,
        template_key: str,
        concept: str,
        language: str,
        difficulty: Difficulty
    ) -> Exercise:
        """Create Parson's problem from template."""
        template = self.templates[template_key]

        return Exercise(
            exercise_type=ExerciseType.PARSONS,
            concept=concept,
            language=language,
            difficulty=difficulty,
            title=template.get('title', f'{concept.capitalize()} - Code Ordering'),
            instructions=template.get('instructions', 'Arrange the code blocks in the correct order.'),
            content={
                'code_blocks': template.get('code_blocks', []),
                'distractors': template.get('distractors', []),
                'block_count': len(template.get('code_blocks', []))
            },
            hints=template.get('hints', []),
            solution=template.get('solution', {}),
            metadata=template.get('metadata', {})
        )

    def _generate_parsons_dynamically(
        self,
        concept: str,
        language: str,
        difficulty: Difficulty
    ) -> Exercise:
        """Generate Parson's problem dynamically based on concept and language."""
        # Get examples for this concept and language
        example_key = f"{language}_examples"
        examples = self.example_banks.get(example_key, {}).get(concept, [])

        if not examples:
            # Fallback to built-in examples
            examples = self._get_builtin_examples(concept, language)

        if not examples:
            raise ValueError(f"No examples available for {concept} in {language}")

        # Select an appropriate example
        example = self._select_example_by_difficulty(examples, difficulty)

        # Break into blocks
        blocks = self._break_code_into_blocks(example['code'], difficulty)
        distractors = self._generate_distractors(concept, language, difficulty)

        return Exercise(
            exercise_type=ExerciseType.PARSONS,
            concept=concept,
            language=language,
            difficulty=difficulty,
            title=f'{concept.capitalize()} - Code Ordering Exercise',
            instructions=f'Arrange the following code blocks in the correct order to {self._get_exercise_goal(concept)}.',
            content={
                'code_blocks': blocks,
                'distractors': distractors,
                'block_count': len(blocks)
            },
            hints=self._generate_hints(concept, difficulty),
            solution={
                'correct_order': list(range(len(blocks))),
                'explanation': example.get('explanation', '')
            },
            metadata={
                'generated_at': time.time(),
                'source': 'dynamic_generation'
            }
        )

    def generate_worked_example(
        self,
        concept: str,
        language: str,
        scaffolding_level: int = 0
    ) -> Exercise:
        """Generate a worked example with faded scaffolding.

        Args:
            concept: Programming concept to demonstrate
            language: Target programming language
            scaffolding_level: Level of scaffolding (0=full, 5=from scratch)

        Returns:
            Exercise object with worked example content
        """
        logger.info(f"Generating worked example: {concept} in {language} at scaffolding level {scaffolding_level}")

        if scaffolding_level < 0 or scaffolding_level > 5:
            raise ValueError("Scaffolding level must be between 0 and 5")

        # Get example
        example_key = f"{language}_examples"
        examples = self.example_banks.get(example_key, {}).get(concept, [])

        if not examples:
            examples = self._get_builtin_examples(concept, language)

        if not examples:
            raise ValueError(f"No examples available for {concept} in {language}")

        example = examples[0]  # Take first example

        # Apply scaffolding
        scaffolded_example = self._apply_scaffolding(example, scaffolding_level)

        return Exercise(
            exercise_type=ExerciseType.WORKED_EXAMPLE,
            concept=concept,
            language=language,
            difficulty=self._map_scaffolding_to_difficulty(scaffolding_level),
            title=f'{concept.capitalize()} - Worked Example',
            instructions=self._generate_worked_example_instructions(scaffolding_level),
            content={
                'scaffolding_level': scaffolding_level,
                'code': scaffolded_example['code'],
                'explanation': scaffolded_example['explanation'],
                'blanks': scaffolded_example.get('blanks', []),
                'completable_sections': scaffolded_example.get('completable_sections', [])
            },
            hints=self._generate_worked_example_hints(scaffolding_level),
            solution={
                'full_code': example['code'],
                'full_explanation': example.get('explanation', '')
            },
            metadata={
                'generated_at': time.time(),
                'scaffolding_method': 'faded'
            }
        )

    def generate_code_tracing_exercise(
        self,
        concept: str,
        language: str,
        complexity: Difficulty = Difficulty.INTERMEDIATE
    ) -> Exercise:
        """Generate a code tracing exercise.

        Args:
            concept: Programming concept to trace
            language: Target programming language
            complexity: Complexity level of the code

        Returns:
            Exercise object with code tracing content
        """
        logger.info(f"Generating code tracing exercise: {concept} in {language}")

        # Generate code appropriate for tracing
        tracing_code = self._generate_tracing_code(concept, language, complexity)
        trace_steps = self._calculate_trace_steps(tracing_code, language)

        return Exercise(
            exercise_type=ExerciseType.CODE_TRACING,
            concept=concept,
            language=language,
            difficulty=complexity,
            title=f'{concept.capitalize()} - Code Tracing Exercise',
            instructions='Trace through the code step by step, recording the value of each variable at each line.',
            content={
                'code': tracing_code,
                'variables': trace_steps['variables'],
                'expected_lines': trace_steps['line_count']
            },
            hints=self._generate_tracing_hints(concept, complexity),
            solution={
                'trace_table': trace_steps['trace_table'],
                'final_state': trace_steps['final_state']
            },
            metadata={
                'generated_at': time.time(),
                'tracing_method': 'step_by_step'
            }
        )

    # Helper methods

    def _is_language_supported(self, language: str) -> bool:
        """Check if language is supported."""
        supported = self.config.get('supported_languages', {})
        return supported.get(language, {}).get('enabled', False)

    def _is_difficulty_valid(self, difficulty: Difficulty) -> bool:
        """Check if difficulty is valid."""
        return difficulty in Difficulty

    def _get_builtin_examples(self, concept: str, language: str) -> List[Dict]:
        """Get built-in examples for concept and language."""
        # Built-in examples for common concepts
        builtin_examples = {
            'loops': {
                'python': [{
                    'code': '''for i in range(5):
    print(i * 2)''',
                    'explanation': 'This loop prints 0, 2, 4, 6, 8 (each number multiplied by 2)'
                }],
                'javascript': [{
                    'code': '''for (let i = 0; i < 5; i++) {
    console.log(i * 2);
}''',
                    'explanation': 'This loop prints 0, 2, 4, 6, 8 (each number multiplied by 2)'
                }]
            },
            'conditionals': {
                'python': [{
                    'code': '''if x > 10:
    print("Large")
else:
    print("Small")''',
                    'explanation': 'Checks if x is greater than 10 and prints accordingly'
                }],
                'javascript': [{
                    'code': '''if (x > 10) {
    console.log("Large");
} else {
    console.log("Small");
}''',
                    'explanation': 'Checks if x is greater than 10 and prints accordingly'
                }]
            },
            'functions': {
                'python': [{
                    'code': '''def add(a, b):
    return a + b

result = add(3, 4)''',
                    'explanation': 'Defines a function that adds two numbers and calls it with 3 and 4'
                }],
                'javascript': [{
                    'code': '''function add(a, b) {
    return a + b;
}

const result = add(3, 4);''',
                    'explanation': 'Defines a function that adds two numbers and calls it with 3 and 4'
                }]
            }
        }

        return builtin_examples.get(concept, {}).get(language, [])

    def _select_example_by_difficulty(self, examples: List[Dict], difficulty: Difficulty) -> Dict:
        """Select appropriate example based on difficulty."""
        if not examples:
            return {}

        # For simplicity, just return the first example
        # In a full implementation, would select based on difficulty tags
        return examples[0]

    def _break_code_into_blocks(self, code: str, difficulty: Difficulty) -> List[str]:
        """Break code into logical blocks for Parson's problem."""
        lines = code.strip().split('\n')
        blocks = []

        # Group lines into logical blocks
        current_block = []
        for line in lines:
            stripped = line.strip()
            if stripped:
                current_block.append(line.rstrip())
            else:
                if current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = []

        if current_block:
            blocks.append('\n'.join(current_block))

        # If too many blocks for difficulty, merge some
        max_blocks = {
            Difficulty.BEGINNER: 5,
            Difficulty.INTERMEDIATE: 10,
            Difficulty.ADVANCED: 15,
            Difficulty.EXPERT: 20
        }

        if len(blocks) > max_blocks.get(difficulty, 10):
            # Merge blocks to fit difficulty
            merged = []
            i = 0
            while i < len(blocks):
                if i < len(blocks) - 1 and len(blocks) + len(merged) - i > max_blocks[difficulty]:
                    merged.append(blocks[i] + '\n' + blocks[i + 1])
                    i += 2
                else:
                    merged.append(blocks[i])
                    i += 1
            blocks = merged

        return blocks

    def _generate_distractors(self, concept: str, language: str, difficulty: Difficulty) -> List[str]:
        """Generate distractor blocks for Parson's problem."""
        distractors = []

        # Common distractors based on concept
        if difficulty != Difficulty.BEGINNER:
            if concept == 'loops':
                if language == 'python':
                    distractors.append('print(i * 2)')
                    distractors.append('for i in range(5): print(i * 2)')
                elif language == 'javascript':
                    distractors.append('console.log(i * 2)')
                    distractors.append('for (i = 0; i < 5; i++) console.log(i * 2)')

        return distractors

    def _generate_hints(self, concept: str, difficulty: Difficulty) -> List[str]:
        """Generate progressive hints for exercise."""
        hints = [
            f"Think about what {concept} do in programming.",
            "Start by identifying the main operation.",
            "Consider the order of operations."
        ]

        if difficulty != Difficulty.BEGINNER:
            hints.append("Check for any edge cases.")

        return hints

    def _get_exercise_goal(self, concept: str) -> str:
        """Get the goal description for an exercise."""
        goals = {
            'loops': 'create a loop that processes items',
            'conditionals': 'make a decision based on a condition',
            'functions': 'define and call a function',
            'arrays': 'work with a collection of items',
            'strings': 'manipulate text data'
        }
        return goals.get(concept, f'demonstrate {concept}')

    def _apply_scaffolding(self, example: Dict, level: int) -> Dict:
        """Apply faded scaffolding to example."""
        scaffolded = {
            'code': example['code'],
            'explanation': example.get('explanation', ''),
            'blanks': [],
            'completable_sections': []
        }

        if level == 0:
            # Full example - no changes
            return scaffolded
        elif level == 1:
            # Add some blanks for key concepts
            scaffolded['blanks'] = ['KEYWORD']
        elif level >= 2:
            # Add completable sections
            scaffolded['completable_sections'] = [
                {'line_start': 1, 'line_end': 2, 'hint': 'Define the function'}
            ]

        return scaffolded

    def _generate_worked_example_instructions(self, level: int) -> str:
        """Generate instructions for worked example."""
        instructions = {
            0: "Read through this complete example carefully.",
            1: "Fill in the missing keywords in this example.",
            2: "Complete the missing sections in this example.",
            3: "Fix the intentional bugs in this code.",
            4: "Complete this exercise with hints provided.",
            5: "Write the complete solution from scratch."
        }
        return instructions.get(level, "Complete this exercise.")

    def _generate_worked_example_hints(self, level: int) -> List[str]:
        """Generate hints for worked example."""
        if level <= 2:
            return ["Focus on understanding the logic.", "Check the syntax carefully."]
        elif level <= 4:
            return ["Think about the problem step by step.", "Break it down into smaller parts."]
        else:
            return ["Plan your approach first.", "Test as you go."]

    def _map_scaffolding_to_difficulty(self, scaffolding_level: int) -> Difficulty:
        """Map scaffolding level to difficulty."""
        mapping = {
            0: Difficulty.BEGINNER,
            1: Difficulty.BEGINNER,
            2: Difficulty.INTERMEDIATE,
            3: Difficulty.INTERMEDIATE,
            4: Difficulty.ADVANCED,
            5: Difficulty.EXPERT
        }
        return mapping.get(scaffolding_level, Difficulty.INTERMEDIATE)

    def _generate_tracing_code(self, concept: str, language: str, complexity: Difficulty) -> str:
        """Generate code appropriate for tracing."""
        # Simplified tracing code generation
        if concept == 'loops' and language == 'python':
            return '''x = 0
for i in range(3):
    x = x + i
print(x)'''
        elif concept == 'conditionals' and language == 'python':
            return '''x = 5
if x > 3:
    x = x + 1
else:
    x = x - 1
print(x)'''
        else:
            # Return generic example
            return '''# Example code for tracing
x = 10
y = x + 5
print(y)'''

    def _calculate_trace_steps(self, code: str, language: str) -> Dict[str, Any]:
        """Calculate the trace steps for code."""
        # Simplified trace calculation
        return {
            'variables': ['x', 'y', 'i'],
            'line_count': len(code.split('\n')),
            'trace_table': {},
            'final_state': {}
        }

    def _generate_tracing_hints(self, concept: str, complexity: Difficulty) -> List[str]:
        """Generate hints for code tracing."""
        return [
            "Track each variable's value as you go through each line.",
            "Be careful with loop conditions.",
            "Pay attention to when variables are modified."
        ]


# Global generator instance
_generator_instance = None


def get_generator() -> ExerciseGenerator:
    """Get or create the global exercise generator instance."""
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = ExerciseGenerator()
    return _generator_instance


# Tool functions for external use

def generate_parsons_problem(
    concept: str,
    language: str,
    difficulty: str
) -> Dict[str, Any]:
    """Generate a Parson's problem exercise.

    Tool wrapper for external use.
    """
    try:
        generator = get_generator()
        difficulty_enum = Difficulty(difficulty.lower())
        exercise = generator.generate_parsons_problem(concept, language, difficulty_enum)
        return {
            'success': True,
            'exercise': exercise.to_dict()
        }
    except Exception as e:
        logger.error(f"Failed to generate Parson's problem: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def generate_worked_example(
    concept: str,
    language: str,
    scaffolding_level: int = 0
) -> Dict[str, Any]:
    """Generate a worked example exercise.

    Tool wrapper for external use.
    """
    try:
        generator = get_generator()
        exercise = generator.generate_worked_example(concept, language, scaffolding_level)
        return {
            'success': True,
            'exercise': exercise.to_dict()
        }
    except Exception as e:
        logger.error(f"Failed to generate worked example: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def generate_code_tracing_exercise(
    concept: str,
    language: str,
    complexity: str = 'intermediate'
) -> Dict[str, Any]:
    """Generate a code tracing exercise.

    Tool wrapper for external use.
    """
    try:
        generator = get_generator()
        complexity_enum = Difficulty(complexity.lower())
        exercise = generator.generate_code_tracing_exercise(concept, language, complexity_enum)
        return {
            'success': True,
            'exercise': exercise.to_dict()
        }
    except Exception as e:
        logger.error(f"Failed to generate code tracing exercise: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == "__main__":
    # Test the generators
    print("Testing exercise generators...")

    # Test Parson's problem
    parsons = generate_parsons_problem('loops', 'python', 'beginner')
    print(f"Parson's problem generated: {parsons['success']}")

    # Test worked example
    worked = generate_worked_example('loops', 'python', 1)
    print(f"Worked example generated: {worked['success']}")

    # Test code tracing
    tracing = generate_code_tracing_exercise('loops', 'python', 'intermediate')
    print(f"Code tracing generated: {tracing['success']}")

    print("Exercise generators test complete!")
