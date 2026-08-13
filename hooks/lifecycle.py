"""
Production-grade lifecycle hooks for the multilanguage-coding-tutor skill.

This module provides hooks that execute at specific points during the skill's
lifecycle, including initialization, session management, and shutdown.

All hooks include comprehensive error handling, logging, and graceful degradation.
"""

import logging
import sys
import json
import time
from pathlib import Path
from typing import Any, Dict, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import traceback

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('multilanguage_coding_tutor.log')
    ]
)

logger = logging.getLogger(__name__)


class HookStatus(Enum):
    """Status of hook execution."""
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    PARTIAL = "partial"


@dataclass
class HookResult:
    """Result of hook execution with comprehensive error tracking."""
    success: bool
    status: HookStatus
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[Exception] = None
    error_context: Optional[Dict[str, Any]] = None
    execution_time_ms: float = 0.0
    modified: bool = False
    stop_chain: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'success': self.success,
            'status': self.status.value,
            'data': self.data,
            'error': str(self.error) if self.error else None,
            'error_context': self.error_context,
            'execution_time_ms': self.execution_time_ms,
            'modified': self.modified,
            'stop_chain': self.stop_chain,
            'metadata': self.metadata
        }


@dataclass
class HookContext:
    """Context object passed to all hooks containing skill state and utilities."""
    state: Dict[str, Any] = field(default_factory=dict)
    config: Dict[str, Any] = field(default_factory=dict)
    logger: logging.Logger = field(default_factory=lambda: logger)
    metrics: Dict[str, Any] = field(default_factory=dict)

    # Utility functions
    def get_state(self, key: str, default: Any = None) -> Any:
        """Get state value with default."""
        return self.state.get(key, default)

    def set_state(self, key: str, value: Any) -> None:
        """Set state value."""
        self.state[key] = value

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get config value with default."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value if value is not None else default


class HookRegistry:
    """Registry for managing skill hooks with priority-based execution."""

    def __init__(self):
        self._hooks: Dict[str, list] = {}
        self._hook_metadata: Dict[str, Dict[str, Any]] = {}

    def register(
        self,
        hook_name: str,
        handler: Callable,
        priority: int = 100,
        enabled: bool = True,
        conditions: Optional[Dict[str, Any]] = None
    ) -> None:
        """Register a hook with metadata and execution priority."""
        if hook_name not in self._hooks:
            self._hooks[hook_name] = []

        hook_entry = {
            'handler': handler,
            'priority': priority,
            'enabled': enabled,
            'conditions': conditions or {},
            'metadata': {
                'registered_at': time.time(),
                'call_count': 0
            }
        }

        self._hooks[hook_name].append(hook_entry)
        # Sort by priority (higher priority first)
        self._hooks[hook_name].sort(key=lambda x: x['priority'], reverse=True)

        logger.info(f"Registered hook '{hook_name}' with priority {priority}")

    def execute(self, hook_name: str, context: HookContext, **kwargs) -> HookResult:
        """Execute all registered hooks for a given hook name in priority order."""
        if hook_name not in self._hooks:
            return HookResult(
                success=True,
                status=HookStatus.SKIPPED,
                data={'message': f'No hooks registered for {hook_name}'}
            )

        final_result = HookResult(
            success=True,
            status=HookStatus.SUCCESS,
            data={}
        )

        for hook_entry in self._hooks[hook_name]:
            if not hook_entry['enabled']:
                continue

            # Check conditions
            if not self._check_conditions(hook_entry['conditions'], context):
                continue

            start_time = time.time()
            handler = hook_entry['handler']

            try:
                result = handler(context=context, **kwargs)

                # Update metadata
                hook_entry['metadata']['call_count'] += 1

                # Merge results
                if isinstance(result, HookResult):
                    final_result.execution_time_ms += (time.time() - start_time) * 1000

                    if not result.success:
                        final_result.success = False
                        final_result.status = HookStatus.PARTIAL

                    final_result.data.update(result.data)
                    final_result.modified = final_result.modified or result.modified

                    if result.stop_chain:
                        logger.info(f"Hook chain stopped by '{hook_name}' handler")
                        break
                    elif result.error:
                        final_result.error_context = {
                            'hook_name': hook_name,
                            'handler': handler.__name__,
                            'error': result.error
                        }

            except Exception as e:
                execution_time = (time.time() - start_time) * 1000
                logger.error(f"Hook '{hook_name}' failed: {e}", exc_info=True)

                final_result.success = False
                final_result.status = HookStatus.FAILED
                final_result.error = e
                final_result.error_context = {
                    'hook_name': hook_name,
                    'handler': handler.__name__,
                    'traceback': traceback.format_exc()
                }
                final_result.execution_time_ms += execution_time

                # Continue executing remaining hooks unless configured otherwise
                # (graceful degradation)

        return final_result

    def _check_conditions(self, conditions: Dict[str, Any], context: HookContext) -> bool:
        """Check if hook execution conditions are met."""
        if not conditions:
            return True

        # Check skill mode
        if 'skill_mode' in conditions:
            current_mode = context.get_config('skill.mode', 'development')
            if current_mode not in conditions['skill_mode']:
                return False

        # Check feature flags
        if 'feature_flags' in conditions:
            for flag in conditions['feature_flags']:
                if not context.get_config(f'features.{flag}.enabled', False):
                    return False

        return True


# Global hook registry
hook_registry = HookRegistry()


def load_config(config_path: str = 'config/config.json') -> Dict[str, Any]:
    """Load configuration from file with comprehensive error handling."""
    try:
        config_file = Path(config_path)
        if not config_file.exists():
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return get_default_config()

        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        logger.info(f"Loaded configuration from {config_path}")
        return config
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config file: {e}")
        return get_default_config()
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return get_default_config()


def get_default_config() -> Dict[str, Any]:
    """Get default configuration when config loading fails."""
    return {
        'skill': {
            'name': 'multilanguage-coding-tutor',
            'version': '1.0.0',
            'mode': 'development'
        },
        'features': {},
        'supported_languages': {
            'python': {'enabled': True},
            'javascript': {'enabled': True},
            'java': {'enabled': True},
            'cpp': {'enabled': True},
            'rust': {'enabled': True},
            'go': {'enabled': True}
        },
        'context': {
            'max_tokens_per_request': 150000,
            'compression_threshold': 0.8
        },
        'error_handling': {
            'retry_attempts': 3,
            'fallback_enabled': True
        },
        'logging': {
            'level': 'info',
            'structured': True
        }
    }


# Lifecycle Hook Implementations

def on_skill_init(context: HookContext, **kwargs) -> HookResult:
    """Hook executed when the skill is first loaded.

    Initializes global state, resources, and systems.
    """
    logger.info("Initializing multilanguage-coding-tutor skill")

    try:
        # Load configuration
        config = load_config()
        context.config.update(config)

        # Initialize skill state
        context.set_state('initialized_at', time.time())
        context.set_state('version', config.get('skill', {}).get('version', '1.0.0'))
        context.set_state('session_count', 0)

        # Initialize caches
        context.set_state('code_example_cache', {})
        context.set_state('exercise_cache', {})
        context.set_state('concept_cache', {})

        # Validate feature flags
        enabled_features = []
        for feature_name, feature_config in config.get('features', {}).items():
            if feature_config.get('enabled', False):
                enabled_features.append(feature_name)
        context.set_state('enabled_features', enabled_features)

        logger.info(f"Skill initialized successfully with {len(enabled_features)} features enabled")

        return HookResult(
            success=True,
            status=HookStatus.SUCCESS,
            data={
                'version': context.get_state('version'),
                'enabled_features': enabled_features,
                'supported_languages': list(config.get('supported_languages', {}).keys())
            }
        )
    except Exception as e:
        logger.error(f"Skill initialization failed: {e}", exc_info=True)
        return HookResult(
            success=False,
            status=HookStatus.FAILED,
            error=e,
            error_context={'phase': 'initialization'}
        )


def on_session_start(context: HookContext, **kwargs) -> HookResult:
    """Hook executed when a new teaching session begins.

    Initializes session-specific state and prepares for learner interaction.
    """
    session_id = kwargs.get('session_id', f"session_{int(time.time())}")
    logger.info(f"Starting session: {session_id}")

    try:
        # Initialize session state
        session_state = {
            'session_id': session_id,
            'started_at': time.time(),
            'learner_profile': kwargs.get('learner_profile', {}),
            'current_language': kwargs.get('language', 'python'),
            'current_domain': kwargs.get('domain', 'general'),
            'teaching_history': [],
            'exercise_count': 0,
            'concept_mastery': {},
            'error_encounters': []
        }

        context.set_state('current_session', session_state)
        context.set_state('session_count', context.get_state('session_count', 0) + 1)

        logger.info(f"Session {session_id} started successfully")

        return HookResult(
            success=True,
            status=HookStatus.SUCCESS,
            data={
                'session_id': session_id,
                'language': session_state['current_language'],
                'domain': session_state['current_domain']
            }
        )
    except Exception as e:
        logger.error(f"Session start failed: {e}", exc_info=True)
        return HookResult(
            success=False,
            status=HookStatus.FAILED,
            error=e,
            error_context={'session_id': session_id}
        )


def on_session_end(context: HookContext, **kwargs) -> HookResult:
    """Hook executed when a teaching session concludes.

    Saves session progress, generates reports, and cleans up resources.
    """
    session = context.get_state('current_session', {})
    session_id = session.get('session_id', 'unknown')
    logger.info(f"Ending session: {session_id}")

    try:
        # Calculate session metrics
        duration = time.time() - session.get('started_at', time.time())
        exercise_count = session.get('exercise_count', 0)
        teaching_history = session.get('teaching_history', [])

        session_summary = {
            'session_id': session_id,
            'duration_seconds': duration,
            'exercise_count': exercise_count,
            'concepts_covered': list(session.get('concept_mastery', {}).keys()),
            'errors_encountered': len(session.get('error_encounters', [])),
            'teaching_methods_used': list(set(h.get('method', 'unknown') for h in teaching_history))
        }

        # Save session summary to history
        if 'session_history' not in context.state:
            context.set_state('session_history', [])
        session_history = context.get_state('session_history', [])
        session_history.append(session_summary)
        context.set_state('session_history', session_history)

        # Clear current session state
        context.set_state('current_session', {})

        logger.info(f"Session {session_id} ended: {exercise_count} exercises completed")

        return HookResult(
            success=True,
            status=HookStatus.SUCCESS,
            data=session_summary
        )
    except Exception as e:
        logger.error(f"Session end failed: {e}", exc_info=True)
        return HookResult(
            success=False,
            status=HookStatus.FAILED,
            error=e,
            error_context={'session_id': session_id}
        )


def on_skill_shutdown(context: HookContext, **kwargs) -> HookResult:
    """Hook executed when the skill is being unloaded.

    Flushes logs, saves persistent state, and performs cleanup.
    """
    logger.info("Shutting down multilanguage-coding-tutor skill")

    try:
        # Gather statistics
        total_sessions = context.get_state('session_count', 0)
        session_history = context.get_state('session_history', [])

        total_exercises = sum(s.get('exercise_count', 0) for s in session_history)
        total_duration = sum(s.get('duration_seconds', 0) for s in session_history)

        shutdown_summary = {
            'version': context.get_state('version', 'unknown'),
            'total_sessions': total_sessions,
            'total_exercises': total_exercises,
            'total_duration_seconds': total_duration,
            'shutdown_at': time.time()
        }

        # Flush any remaining logs
        for handler in logger.handlers:
            handler.flush()

        logger.info(f"Skill shutdown complete: {total_sessions} sessions, {total_exercises} exercises")

        return HookResult(
            success=True,
            status=HookStatus.SUCCESS,
            data=shutdown_summary
        )
    except Exception as e:
        logger.error(f"Skill shutdown failed: {e}", exc_info=True)
        return HookResult(
            success=False,
            status=HookStatus.FAILED,
            error=e,
            error_context={'phase': 'shutdown'}
        )


def on_skill_init_safe(context: HookContext, **kwargs) -> HookResult:
    """Safe version of skill initialization that always succeeds.

    Used as a fallback if the main initialization fails.
    """
    logger.warning("Using safe initialization fallback")

    context.set_state('initialized_at', time.time())
    context.set_state('safe_mode', True)

    return HookResult(
        success=True,
        status=HookStatus.SUCCESS,
        data={'mode': 'safe', 'message': 'Skill initialized in safe mode'}
    )


# Register lifecycle hooks
hook_registry.register('on_skill_init', on_skill_init, priority=100)
hook_registry.register('on_skill_init', on_skill_init_safe, priority=50)  # Fallback
hook_registry.register('on_session_start', on_session_start, priority=100)
hook_registry.register('on_session_end', on_session_end, priority=100)
hook_registry.register('on_skill_shutdown', on_skill_shutdown, priority=100)


# Convenience functions for external use

def initialize_skill() -> HookContext:
    """Initialize the skill and return the context."""
    context = HookContext()
    result = hook_registry.execute('on_skill_init', context)

    if not result.success:
        logger.warning("Skill initialization had issues, using fallback")
        # Fallback initialization will be triggered by priority system

    return context


def start_session(context: HookContext, **session_kwargs) -> HookResult:
    """Start a new teaching session."""
    return hook_registry.execute('on_session_start', context, **session_kwargs)


def end_session(context: HookContext) -> HookResult:
    """End the current teaching session."""
    return hook_registry.execute('on_session_end', context)


def shutdown_skill(context: HookContext) -> HookResult:
    """Shutdown the skill."""
    return hook_registry.execute('on_skill_shutdown', context)


if __name__ == "__main__":
    # Test the lifecycle hooks
    print("Testing lifecycle hooks...")

    # Test initialization
    ctx = initialize_skill()
    print(f"Initialized: {ctx.get_state('version')}")

    # Test session lifecycle
    session_result = start_session(ctx, session_id="test_session", language="python")
    print(f"Session started: {session_result.data}")

    end_result = end_session(ctx)
    print(f"Session ended: {end_result.data}")

    # Test shutdown
    shutdown_result = shutdown_skill(ctx)
    print(f"Shutdown: {shutdown_result.data}")

    print("Lifecycle hooks test complete!")
