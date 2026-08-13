"""
Execution hooks for agent and tool execution monitoring.

These hooks provide monitoring, validation, and metrics collection for
agent and tool executions within the skill.
"""

import time
import logging
from typing import Any, Dict, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

from .lifecycle import HookResult, HookContext, HookStatus, hook_registry

logger = logging.getLogger(__name__)


class ExecutionPhase(Enum):
    """Phases of execution."""
    BEFORE = "before"
    AFTER = "after"
    ERROR = "error"


@dataclass
class ExecutionMetrics:
    """Metrics collected during execution."""
    agent_name: str
    start_time: float
    end_time: Optional[float] = None
    duration_ms: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    success: bool = True
    error_type: Optional[str] = None
    cache_hit: bool = False
    retry_count: int = 0

    def finalize(self) -> None:
        """Finalize metrics by calculating duration."""
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000
        self.total_tokens = self.input_tokens + self.output_tokens


@dataclass
class ExecutionState:
    """State tracking for execution lifecycle."""
    active: bool = False
    current_agent: Optional[str] = None
    current_tool: Optional[str] = None
    execution_stack: list = field(default_factory=list)
    metrics: Dict[str, ExecutionMetrics] = field(default_factory=dict)


# Global execution state
_execution_state = ExecutionState()


def before_agent_execution(context: HookContext, **kwargs) -> HookResult:
    """Hook executed before any agent execution.

    Performs input validation, token budget checking, and pre-processing.
    """
    agent_name = kwargs.get('agent_name', 'unknown')
    input_data = kwargs.get('input_data', {})

    logger.info(f"Before agent execution: {agent_name}")

    try:
        # Update execution state
        _execution_state.active = True
        _execution_state.current_agent = agent_name
        _execution_state.execution_stack.append({
            'agent': agent_name,
            'start_time': time.time()
        })

        # Initialize metrics
        metrics = ExecutionMetrics(
            agent_name=agent_name,
            start_time=time.time()
        )
        _execution_state.metrics[agent_name] = metrics

        # Validate input data
        if input_data:
            validation_result = validate_agent_input(agent_name, input_data)
            if not validation_result['valid']:
                logger.warning(f"Input validation failed for {agent_name}: {validation_result['errors']}")
                return HookResult(
                    success=False,
                    status=HookStatus.FAILED,
                    data={'validation_errors': validation_result['errors']},
                    error=Exception("Input validation failed")
                )

        # Check token budget
        token_budget = context.get_config('context.max_tokens_per_request', 150000)
        estimated_tokens = estimate_input_tokens(input_data)

        if estimated_tokens > token_budget * 0.8:  # 80% threshold
            logger.warning(f"Token budget approaching: {estimated_tokens}/{token_budget}")
            # Could trigger context compression here

        # Log execution start
        logger.info(f"Agent {agent_name} execution started (estimated tokens: {estimated_tokens})")

        return HookResult(
            success=True,
            status=HookStatus.SUCCESS,
            data={
                'agent_name': agent_name,
                'estimated_tokens': estimated_tokens,
                'validation_passed': True
            }
        )
    except Exception as e:
        logger.error(f"Before agent execution failed for {agent_name}: {e}", exc_info=True)
        return HookResult(
            success=False,
            status=HookStatus.FAILED,
            error=e,
            error_context={'agent_name': agent_name}
        )


def after_agent_execution(context: HookContext, **kwargs) -> HookResult:
    """Hook executed after any agent completes execution.

    Performs output validation, metrics collection, and post-processing.
    """
    agent_name = kwargs.get('agent_name', 'unknown')
    output_data = kwargs.get('output_data', {})
    execution_metrics = kwargs.get('execution_metrics', {})

    logger.info(f"After agent execution: {agent_name}")

    try:
        # Finalize metrics
        if agent_name in _execution_state.metrics:
            metrics = _execution_state.metrics[agent_name]
            metrics.finalize()
            metrics.success = True

            # Update with provided metrics if available
            if 'input_tokens' in execution_metrics:
                metrics.input_tokens = execution_metrics['input_tokens']
            if 'output_tokens' in execution_metrics:
                metrics.output_tokens = execution_metrics['output_tokens']

        # Validate output
        validation_result = validate_agent_output(agent_name, output_data)
        if not validation_result['valid']:
            logger.warning(f"Output validation failed for {agent_name}: {validation_result['errors']}")

        # Pop from execution stack
        if _execution_state.execution_stack:
            _execution_state.execution_stack.pop()

        if not _execution_state.execution_stack:
            _execution_state.active = False
            _execution_state.current_agent = None

        # Log execution completion
        duration = metrics.duration_ms if agent_name in _execution_state.metrics else 0
        logger.info(f"Agent {agent_name} execution completed in {duration:.2f}ms")

        return HookResult(
            success=True,
            status=HookStatus.SUCCESS,
            data={
                'agent_name': agent_name,
                'duration_ms': duration,
                'tokens_used': metrics.total_tokens if agent_name in _execution_state.metrics else 0,
                'validation_passed': validation_result['valid']
            }
        )
    except Exception as e:
        logger.error(f"After agent execution failed for {agent_name}: {e}", exc_info=True)
        return HookResult(
            success=False,
            status=HookStatus.FAILED,
            error=e,
            error_context={'agent_name': agent_name}
        )


def on_agent_error(context: HookContext, **kwargs) -> HookResult:
    """Hook executed when an agent encounters an error.

    Handles error logging, fallback execution, and recovery strategies.
    """
    agent_name = kwargs.get('agent_name', 'unknown')
    error = kwargs.get('error', Exception('Unknown error'))
    error_context = kwargs.get('context', {})

    logger.error(f"Agent error in {agent_name}: {error}")

    try:
        # Update metrics
        if agent_name in _execution_state.metrics:
            metrics = _execution_state.metrics[agent_name]
            metrics.finalize()
            metrics.success = False
            metrics.error_type = type(error).__name__

        # Determine fallback strategy
        fallback_strategies = context.get_config('error_handling.fallback_strategies.llm_failure.strategies', [])
        fallback_result = None

        if fallback_strategies and context.get_config('error_handling.fallback_enabled', True):
            for strategy in fallback_strategies:
                try:
                    fallback_result = execute_fallback(strategy, agent_name, error, error_context)
                    if fallback_result['success']:
                        logger.info(f"Fallback strategy '{strategy}' succeeded for {agent_name}")
                        break
                except Exception as fallback_error:
                    logger.warning(f"Fallback strategy '{strategy}' failed: {fallback_error}")
                    continue

        # Clean up execution state
        if _execution_state.execution_stack:
            _execution_state.execution_stack.pop()

        if not _execution_state.execution_stack:
            _execution_state.active = False
            _execution_state.current_agent = None

        return HookResult(
            success=fallback_result is not None and fallback_result.get('success', False),
            status=HookStatus.SUCCESS if fallback_result and fallback_result.get('success') else HookStatus.FAILED,
            data={
                'agent_name': agent_name,
                'error_type': type(error).__name__,
                'error_message': str(error),
                'fallback_used': fallback_result.get('strategy') if fallback_result else None,
                'fallback_result': fallback_result
            },
            error=error
        )
    except Exception as e:
        logger.error(f"Error handler failed for {agent_name}: {e}", exc_info=True)
        return HookResult(
            success=False,
            status=HookStatus.FAILED,
            error=e,
            error_context={'agent_name': agent_name, 'original_error': str(error)}
        )


# Validation functions

def validate_agent_input(agent_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate agent input data."""
    errors = []

    # Check required fields based on agent type
    required_fields = get_required_fields_for_agent(agent_name)
    for field in required_fields:
        if field not in input_data or input_data[field] is None:
            errors.append(f"Missing required field: {field}")

    # Type checking
    field_types = get_field_types_for_agent(agent_name)
    for field, expected_type in field_types.items():
        if field in input_data and not isinstance(input_data[field], expected_type):
            errors.append(f"Field '{field}' should be {expected_type.__name__}")

    return {
        'valid': len(errors) == 0,
        'errors': errors
    }


def validate_agent_output(agent_name: str, output_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate agent output data."""
    errors = []

    # Check for required output fields
    if not output_data:
        errors.append("Output data is empty")
        return {'valid': False, 'errors': errors}

    # Check structure based on agent type
    if 'result' not in output_data and 'data' not in output_data and 'output' not in output_data:
        errors.append("Output missing result/data field")

    return {
        'valid': len(errors) == 0,
        'errors': errors
    }


def estimate_input_tokens(input_data: Dict[str, Any]) -> int:
    """Estimate token count for input data."""
    # Rough estimation: 1 token ≈ 4 characters
    text = str(input_data)
    return len(text) // 4


def get_required_fields_for_agent(agent_name: str) -> list:
    """Get required fields for specific agent."""
    field_map = {
        'diagnostic_agent': ['learner_profile'],
        'concept_teacher': ['concept', 'language'],
        'parsons_generator': ['language', 'concept', 'difficulty'],
        'code_tracing': ['language', 'code'],
        'error_explainer': ['error_message', 'language']
    }
    return field_map.get(agent_name, [])


def get_field_types_for_agent(agent_name: str) -> Dict[str, type]:
    """Get field type requirements for specific agent."""
    type_map = {
        'diagnostic_agent': {'learner_profile': dict},
        'concept_teacher': {'concept': str, 'language': str},
        'parsons_generator': {'language': str, 'concept': str, 'difficulty': str},
        'code_tracing': {'language': str, 'code': str},
        'error_explainer': {'error_message': str, 'language': str}
    }
    return type_map.get(agent_name, {})


def execute_fallback(
    strategy: str,
    agent_name: str,
    error: Exception,
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Execute fallback strategy for failed agent."""
    logger.info(f"Executing fallback strategy: {strategy}")

    if strategy == 'use_cached_response':
        # Check if we have a cached response for this input
        return {
            'success': False,
            'strategy': strategy,
            'reason': 'No cached response available'
        }

    elif strategy == 'use_simpler_model':
        # Fall back to a simpler/faster model
        return {
            'success': False,
            'strategy': strategy,
            'reason': 'Simpler model not configured'
        }

    elif strategy == 'return_template_response':
        # Return a template-based response
        return {
            'success': True,
            'strategy': strategy,
            'response': f"Template response for {agent_name} (original error: {str(error)})"
        }

    else:
        return {
            'success': False,
            'strategy': strategy,
            'reason': 'Unknown fallback strategy'
        }


# Register execution hooks
hook_registry.register('before_agent_execution', before_agent_execution, priority=100)
hook_registry.register('after_agent_execution', after_agent_execution, priority=100)
hook_registry.register('on_agent_error', on_agent_error, priority=100)


# Convenience functions

def get_execution_metrics() -> Dict[str, Any]:
    """Get current execution metrics."""
    metrics_summary = {}

    for agent_name, metrics in _execution_state.metrics.items():
        metrics_summary[agent_name] = {
            'duration_ms': metrics.duration_ms,
            'total_tokens': metrics.total_tokens,
            'success': metrics.success,
            'error_type': metrics.error_type
        }

    return {
        'active': _execution_state.active,
        'current_agent': _execution_state.current_agent,
        'execution_stack': _execution_state.execution_stack,
        'metrics': metrics_summary
    }


def reset_execution_state() -> None:
    """Reset execution state (useful for testing)."""
    global _execution_state
    _execution_state = ExecutionState()


if __name__ == "__main__":
    # Test execution hooks
    from .lifecycle import initialize_skill

    print("Testing execution hooks...")

    # Initialize context
    ctx = initialize_skill()

    # Test before execution
    before_result = hook_registry.execute(
        'before_agent_execution',
        ctx,
        agent_name='concept_teacher',
        input_data={'concept': 'loops', 'language': 'python'}
    )
    print(f"Before execution: {before_result.success}")

    # Test after execution
    after_result = hook_registry.execute(
        'after_agent_execution',
        ctx,
        agent_name='concept_teacher',
        output_data={'result': 'Example explanation'},
        execution_metrics={'input_tokens': 100, 'output_tokens': 500}
    )
    print(f"After execution: {after_result.success}")

    # Test error handling
    error_result = hook_registry.execute(
        'on_agent_error',
        ctx,
        agent_name='concept_teacher',
        error=Exception("Test error"),
        context={}
    )
    print(f"Error handling: {error_result.success}")

    # Get metrics
    metrics = get_execution_metrics()
    print(f"Execution metrics: {metrics}")

    print("Execution hooks test complete!")
