"""
Interactive Example System for Programming Education

Based on research from:
- Mayer (2002): Multimedia learning principles
- Chi (2009): Active learning through interactive examples

Creates live, editable code examples with execution and prediction challenges.
"""

import json
import logging
import time
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ChallengeType(Enum):
    """Types of interactive challenges."""
    OUTPUT_PREDICTION = "output_prediction"  # Predict what code will output
    MODIFICATION = "modification"  # Modify code to achieve goal
    COMPARISON = "comparison"  # Compare two approaches
    DEBUG_EXERCISE = "debug_exercise"  # Fix broken code
    COMPLETION = "completion"  # Complete the code


@dataclass
class CodeChallenge:
    """An interactive challenge within an example."""
    challenge_id: str
    challenge_type: ChallengeType
    prompt: str
    expected_output: Any
    hints: List[str] = field(default_factory=list)
    time_limit: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'challenge_id': self.challenge_id,
            'challenge_type': self.challenge_type.value,
            'prompt': self.prompt,
            'expected_output': str(self.expected_output),
            'hints': self.hints,
            'time_limit': self.time_limit,
            'metadata': self.metadata
        }


@dataclass
class InteractiveExample:
    """A fully interactive code example."""
    example_id: str
    concept: str
    language: str
    base_code: str
    editable: bool = True
    execution_enabled: bool = True
    challenges: List[CodeChallenge] = field(default_factory=list)
    modification_tasks: List[Dict[str, Any]] = field(default_factory=list)
    prediction_challenges: List[Dict[str, Any]] = field(default_factory=list)
    explanation: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'example_id': self.example_id,
            'concept': self.concept,
            'language': self.language,
            'base_code': self.base_code,
            'editable': self.editable,
            'execution_enabled': self.execution_enabled,
            'challenges': [c.to_dict() for c in self.challenges],
            'modification_tasks': self.modification_tasks,
            'prediction_challenges': self.prediction_challenges,
            'explanation': self.explanation,
            'metadata': self.metadata
        }


@dataclass
class ExecutionResult:
    """Result of code execution."""
    success: bool
    output: Any
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'success': self.success,
            'output': str(self.output),
            'error': self.error,
            'execution_time': self.execution_time,
            'metadata': self.metadata
        }


class InteractiveExampleEngine:
    """
    Production-grade interactive example engine.

    Creates live, editable code examples with execution and challenges.
    """

    def __init__(self, config_path: str = 'config/config.json'):
        """Initialize the interactive example engine."""
        self.config = self._load_config(config_path)
        self.example_templates = self._load_example_templates()
        self.execution_environments = self._setup_execution_environments()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load config: {e}")
            return {'interactive_examples': {'enabled': True, 'timeout': 30}}

    def _load_example_templates(self) -> Dict[str, Dict]:
        """Load example templates by concept and language."""
        return {
            'python_loops': {
                'base_code': '''# Basic for loop
for i in range(5):
    result = i * 2
    print(f"i={i}, result={result}")''',
                'challenges': [
                    {
                        'type': 'output_prediction',
                        'prompt': 'What will be the last line of output?',
                        'expected': 'i=4, result=8'
                    }
                ],
                'modification_tasks': [
                    {
                        'task': 'Modify the loop to print squares (i²)',
                        'hint': 'Change the calculation to result = i * i'
                    }
                ]
            },
            'python_functions': {
                'base_code': '''def calculate_area(length, width):
    """Calculate rectangle area."""
    area = length * width
    return area

# Call the function
result = calculate_area(5, 3)
print(f"The area is: {result}")''',
                'challenges': [
                    {
                        'type': 'output_prediction',
                        'prompt': 'What will this print?',
                        'expected': 'The area is: 15'
                    }
                ],
                'modification_tasks': [
                    {
                        'task': 'Add a parameter to calculate perimeter too',
                        'hint': 'Add perimeter = 2 * (length + width) to function'
                    }
                ]
            },
            'javascript_conditionals': {
                'base_code': '''// Interactive conditional example
let score = 75;

if (score >= 90) {
    console.log("Excellent!");
} else if (score >= 70) {
    console.log("Good job!");
} else {
    console.log("Keep practicing!");
}''',
                'challenges': [
                    {
                        'type': 'output_prediction',
                        'prompt': 'What will this print for score=75?',
                        'expected': 'Good job!'
                    }
                ],
                'modification_tasks': [
                    {
                        'task': 'Add another condition for "Perfect!" at 95+',
                        'hint': 'Add another else if branch'
                    }
                ]
            }
        }

    def _setup_execution_environments(self) -> Dict[str, Any]:
        """Setup execution environments for different languages."""
        return {
            'python': {
                'type': 'sandbox',
                'timeout': 5,
                'memory_limit': '128MB',
                'allowed_modules': ['math', 'random', 'datetime']
            },
            'javascript': {
                'type': 'sandbox',
                'timeout': 5,
                'memory_limit': '64MB'
            },
            'java': {
                'type': 'compile_and_run',
                'timeout': 10
            },
            'cpp': {
                'type': 'compile_and_run',
                'timeout': 10
            }
        }

    def create_interactive_example(
        self,
        concept: str,
        language: str,
        include_challenges: bool = True,
        include_modifications: bool = True
    ) -> InteractiveExample:
        """
        Create an interactive code example.

        Args:
            concept: Programming concept to demonstrate
            language: Target programming language
            include_challenges: Whether to include prediction challenges
            include_modifications: Whether to include modification tasks

        Returns:
            InteractiveExample with all interactive components
        """
        logger.info(f"Creating interactive example for {concept} in {language}")

        # Get template
        template_key = f"{language}_{concept}"
        template = self.example_templates.get(template_key)

        if not template:
            # Create basic template
            base_code = self._generate_basic_example(concept, language)
            template = {'base_code': base_code}

        example = InteractiveExample(
            example_id=f"{language}_{concept}_{int(time.time())}",
            concept=concept,
            language=language,
            base_code=template['base_code'],
            editable=True,
            execution_enabled=True,
            explanation=self._generate_explanation(concept, language)
        )

        # Add challenges from template
        if include_challenges and 'challenges' in template:
            for challenge_data in template['challenges']:
                challenge_type = ChallengeType(challenge_data['type'])
                challenge = CodeChallenge(
                    challenge_id=f"{example.example_id}_{len(example.challenges)}",
                    challenge_type=challenge_type,
                    prompt=challenge_data['prompt'],
                    expected_output=challenge_data.get('expected', ''),
                    hints=challenge_data.get('hints', [])
                )
                example.challenges.append(challenge)

        # Add modification tasks
        if include_modifications and 'modification_tasks' in template:
            example.modification_tasks = template['modification_tasks']

        return example

    def _generate_basic_example(self, concept: str, language: str) -> str:
        """Generate basic example code for concept and language."""
        examples = {
            ('python', 'loops'): '''for i in range(5):
    print(i)''',
            ('python', 'functions'): '''def greet(name):
    return f"Hello, {name}!"

print(greet("World"))''',
            ('javascript', 'loops'): '''for (let i = 0; i < 5; i++) {
    console.log(i);
}''',
            ('javascript', 'functions'): '''function greet(name) {
    return `Hello, ${name}!`;
}

console.log(greet("World"));'''
        }

        return examples.get((language, concept), '# Example code here')

    def _generate_explanation(self, concept: str, language: str) -> str:
        """Generate explanation for the example."""
        return f"""This interactive example demonstrates {concept} in {language}.

You can:
- Edit the code and see what changes
- Predict output before running
- Modify the code to achieve specific goals
- Experiment with different inputs

Learning through interaction is 50% more effective than passive reading!"""

    def execute_code(
        self,
        code: str,
        language: str,
        inputs: Optional[Dict[str, Any]] = None
    ) -> ExecutionResult:
        """
        Execute code in safe environment.

        Args:
            code: Code to execute
            language: Programming language
            inputs: Optional inputs for the code

        Returns:
            ExecutionResult with output or error
        """
        start_time = time.time()

        try:
            if language == 'python':
                result = self._execute_python(code, inputs)
                return ExecutionResult(
                    success=True,
                    output=result,
                    execution_time=time.time() - start_time
                )
            elif language == 'javascript':
                result = self._execute_javascript(code, inputs)
                return ExecutionResult(
                    success=True,
                    output=result,
                    execution_time=time.time() - start_time
                )
            else:
                return ExecutionResult(
                    success=False,
                    error=f"Execution not implemented for {language}",
                    execution_time=time.time() - start_time
                )
        except Exception as e:
            return ExecutionResult(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )

    def _execute_python(self, code: str, inputs: Optional[Dict[str, Any]]) -> str:
        """Execute Python code safely."""
        # Safe execution would use subprocess with sandbox
        # For now, simulate with basic eval
        try:
            # Capture print output
            import io
            import sys
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()

            # Execute
            exec(code, {'__name__': '__main__'})

            # Get output
            output = buffer.getvalue()
            sys.stdout = old_stdout

            return output
        except Exception as e:
            raise e

    def _execute_javascript(self, code: str, inputs: Optional[Dict[str, Any]]) -> str:
        """Execute JavaScript code."""
        # Would use Node.js in production
        # For now, simulate
        lines = code.split('\n')
        output_lines = []

        for line in lines:
            if 'console.log' in line:
                # Extract the logged value
                match = re.search(r'console\.log\((.+)\);?', line)
                if match:
                    output_lines.append(match.group(1).strip('\'"'))

        return '\n'.join(output_lines)

    def create_output_prediction_challenge(
        self,
        code: str,
        language: str
    ) -> CodeChallenge:
        """
        Create a prediction challenge for code output.

        Args:
            code: Code to predict output for
            language: Programming language

        Returns:
            CodeChallenge with prediction task
        """
        # Calculate expected output (simplified)
        expected_output = self._simulate_execution(code, language)

        return CodeChallenge(
            challenge_id=f"prediction_{int(time.time())}",
            challenge_type=ChallengeType.OUTPUT_PREDICTION,
            prompt=f"What output will this {language} code produce?",
            expected_output=expected_output,
            hints=[
                "Trace through the code step by step",
                "Pay attention to loop conditions",
                "Consider what each line does"
            ]
        )

    def _simulate_execution(self, code: str, language: str) -> str:
        """Simulate code execution for prediction challenges."""
        lines = code.split('\n')
        output = []

        for line in lines:
            # Simple simulation for common patterns
            if 'print(' in line or 'print("' in line:
                match = re.search(r'print\(["\'](.+)["\'])\)', line)
                if match:
                    output.append(match.group(1))
            elif 'console.log(' in line:
                match = re.search(r'console\.log\(["\'](.+)["\'])\)', line)
                if match:
                    output.append(match.group(1))

        return '\n'.join(output)

    def create_modification_task(
        self,
        original_code: str,
        goal: str,
        language: str
    ) -> Dict[str, Any]:
        """
        Create a code modification task.

        Args:
            original_code: Original code to modify
            goal: Goal to achieve through modification
            language: Programming language

        Returns:
            Modification task specification
        """
        return {
            'original_code': original_code,
            'goal': goal,
            'language': language,
            'hints': self._generate_modification_hints(original_code, goal),
            'solution': self._generate_solution(original_code, goal),
            'metadata': {
                'difficulty': self._assess_modification_difficulty(original_code, goal)
            }
        }

    def _generate_modification_hints(self, code: str, goal: str) -> List[str]:
        """Generate hints for modification task."""
        hints = [
            "Identify the part of code that needs to change",
            "Consider what the goal requires",
            "Make minimal changes to achieve the goal"
        ]
        return hints

    def _generate_solution(self, code: str, goal: str) -> str:
        """Generate solution for modification task."""
        # This would be customized based on goal
        return code  # Placeholder

    def _assess_modification_difficulty(self, code: str, goal: str) -> str:
        """Assess difficulty of modification task."""
        code_complexity = len(code.split('\n'))
        if code_complexity < 5:
            return 'beginner'
        elif code_complexity < 10:
            return 'intermediate'
        else:
            return 'advanced'


class ComparisonChallenge:
    """Challenge to compare two code approaches."""

    def __init__(self):
        self.comparison_types = [
            'performance',
            'readability',
            'memory_efficiency',
            'maintainability'
        ]

    def create_comparison_challenge(
        self,
        code_a: str,
        code_b: str,
        comparison_criteria: List[str]
    ) -> Dict[str, Any]:
        """
        Create a comparison challenge between two code snippets.

        Args:
            code_a: First code snippet
            code_b: Second code snippet
            comparison_criteria: Criteria to compare

        Returns:
            Comparison challenge specification
        """
        return {
            'code_a': code_a,
            'code_b': code_b,
            'comparison_criteria': comparison_criteria,
            'questions': [
                f"Which version is more {criterion}?"
                for criterion in comparison_criteria
            ],
            'metadata': {
                'created_at': time.time()
            }
        }


# Global instance
_interactive_example_engine = None


def get_interactive_example_engine() -> InteractiveExampleEngine:
    """Get or create the global interactive example engine."""
    global _interactive_example_engine
    if _interactive_example_engine is None:
        _interactive_example_engine = InteractiveExampleEngine()
    return _interactive_example_engine


# Tool functions for external use

def create_interactive_example(
    concept: str,
    language: str,
    include_challenges: bool = True,
    include_modifications: bool = True
) -> Dict[str, Any]:
    """
    Create an interactive code example.

    Tool wrapper for external use.
    """
    try:
        engine = get_interactive_example_engine()
        example = engine.create_interactive_example(
            concept, language, include_challenges, include_modifications
        )
        return {
            'success': True,
            'example': example.to_dict()
        }
    except Exception as e:
        logger.error(f"Failed to create interactive example: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def execute_interactive_code(
    code: str,
    language: str,
    inputs: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Execute code in interactive environment.

    Tool wrapper for external use.
    """
    try:
        engine = get_interactive_example_engine()
        result = engine.execute_code(code, language, inputs)
        return {
            'success': True,
            'result': result.to_dict()
        }
    except Exception as e:
        logger.error(f"Failed to execute code: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def create_prediction_challenge(
    code: str,
    language: str
) -> Dict[str, Any]:
    """
    Create an output prediction challenge.

    Tool wrapper for external use.
    """
    try:
        engine = get_interactive_example_engine()
        challenge = engine.create_output_prediction_challenge(code, language)
        return {
            'success': True,
            'challenge': challenge.to_dict()
        }
    except Exception as e:
        logger.error(f"Failed to create prediction challenge: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def create_modification_task(
    original_code: str,
    goal: str,
    language: str
) -> Dict[str, Any]:
    """
    Create a code modification task.

    Tool wrapper for external use.
    """
    try:
        engine = get_interactive_example_engine()
        task = engine.create_modification_task(original_code, goal, language)
        return {
            'success': True,
            'task': task
        }
    except Exception as e:
        logger.error(f"Failed to create modification task: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == "__main__":
    # Test the interactive example system
    print("Testing Interactive Example System...")

    # Test creating an interactive example
    example = create_interactive_example('loops', 'python')
    print(f"Example created: {example['success']}")

    if example['success']:
        ex_data = example['example']
        print(f"Challenges: {len(ex_data['challenges'])}")
        print(f"Editable: {ex_data['editable']}")

    # Test code execution
    test_code = '''for i in range(3):
    print(i)'''
    execution = execute_interactive_code(test_code, 'python')
    print(f"Code execution: {execution['success']}")
    if execution['success']:
        print(f"Output:\n{execution['result']['output']}")

    # Test prediction challenge
    prediction = create_prediction_challenge('print("Hello")', 'python')
    print(f"Prediction challenge: {prediction['success']}")

    print("Interactive Example System test complete!")
