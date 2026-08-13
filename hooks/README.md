# Hooks Directory

**Purpose:** Lifecycle management, state synchronization, and event emission hooks

## Overview

Hooks are modular functions that execute at specific points during the skill's lifecycle. They provide a clean way to extend functionality without modifying core logic.

## Hook Types

### Lifecycle Hooks

#### `on_skill_init`
- **Timing:** When the skill is first loaded
- **Purpose:** Initialize global state and resources
- **Parameters:** `config` object
- **Use Cases:**
  - Load configuration files
  - Initialize logging system
  - Set up error handlers
  - Initialize caches

#### `on_session_start`
- **Timing:** When a new teaching session begins
- **Parameters:** `session_context` object
- **Use Cases:**
  - Initialize session state
  - Load learner profile if available
  - Set up session-specific logging
  - Initialize progress tracking

#### `on_session_end`
- **Timing:** When a teaching session concludes
- **Parameters:** `session_summary` object
- **Use Cases:**
  - Save session progress
  - Update learner profile
  - Generate session report
  - Clean up resources

#### `on_skill_shutdown`
- **Timing:** When the skill is being unloaded
- **Parameters:** None
- **Use Cases:**
  - Flush logs and buffers
  - Save persistent state
  - Close connections and resources
  - Generate shutdown report

### Execution Hooks

#### `before_agent_execution`
- **Timing:** Before any agent executes
- **Parameters:** `agent_name`, `input_data`
- **Use Cases:**
  - Input validation
  - Token budget checking
  - Logging execution start
  - Pre-processing input data

#### `after_agent_execution`
- **Timing:** After any agent completes execution
- **Parameters:** `agent_name`, `output_data`, `execution_metrics`
- **Use Cases:**
  - Output validation
  - Result logging
  - Metrics collection
  - Post-processing output data

#### `on_agent_error`
- **Timing:** When an agent encounters an error
- **Parameters:** `agent_name`, `error`, `context`
- **Use Cases:**
  - Error logging
  - Fallback execution
  - Error recovery
  - User notification

### State Management Hooks

#### `on_state_change`
- **Timing:** When any state variable changes
- **Parameters:** `state_key`, `old_value`, `new_value`
- **Use Cases:**
  - State validation
  - State synchronization
  - Trigger dependent updates
  - Audit logging

#### `before_state_persistence`
- **Timing:** Before state is saved to storage
- **Parameters:** `state_object`
- **Use Cases:**
  - Data validation
  - Data transformation
  - Encryption
  - Compression

#### `after_state_load`
- **Timing:** After state is loaded from storage
- **Parameters:** `state_object`
- **Use Cases:**
  - Data validation
  - Migration handling
  - Decompression
  - Decryption

### Event Hooks

#### `on_learner_milestone`
- **Timing:** When a learner achieves a milestone
- **Parameters:** `learner_id`, `milestone_data`
- **Use Cases:**
  - Achievement notification
  - Progress analytics
  - Content adaptation
  - Recommendation generation

#### `on_error_encountered`
- **Timing:** When a learner encounters an error
- **Parameters:** `error_data`, `context`
- **Use Cases:**
  - Error pattern analysis
  - Difficulty adjustment
  - Focused teaching trigger
  - Help generation

#### `on_concept_mastered`
- **Timing:** When a learner demonstrates concept mastery
- **Parameters:** `concept_id`, `mastery_level`
- **Use Cases:**
  - Progress tracking
  - Path optimization
  - Content unlock
  - Recommendation updates

### Teaching Hooks

#### `before_exercise_generation`
- **Timing:** Before generating a practice exercise
- **Parameters:** `exercise_type`, `difficulty`, `concept`
- **Use Cases:**
  - Difficulty calibration
  - Prerequisite checking
  - Personalization application
  - Template selection

#### `after_exercise_completion`
- **Timing:** After learner completes an exercise
- **Parameters:** `exercise_data`, `learner_response`, `result`
- **Use Cases:**
  - Performance tracking
  - Difficulty adjustment
  - Feedback generation
  - Next step planning

#### `on_explanation_request`
- **Timing:** When learner requests additional explanation
- **Parameters:** `topic`, `current_understanding`, `context`
- **Use Cases:**
  - Explanation generation
  - Analogy selection
  - Depth adjustment
  - Format preference

## Hook Implementation

### Hook Function Signature

```python
def hook_name(
    parameters: dict,
    context: HookContext
) -> HookResult:
    """
    Hook function with standardized signature.
    
    Args:
        parameters: Hook-specific parameters
        context: Execution context with state and utilities
    
    Returns:
        HookResult with success flag and optional data
    """
    pass
```

### Hook Registration

Hooks are registered in the hook registry:

```json
{
  "hook_name": {
    "enabled": true,
    "priority": 100,
    "handler": "hooks.module.function_name",
    "conditions": {
      "skill_mode": ["production", "development"],
      "feature_flags": ["feature_name"]
    }
  }
}
```

### Hook Execution Order

Hooks execute in priority order (higher priority first):
1. Priority 0-99: Pre-processing hooks
2. Priority 100-199: Core processing hooks
3. Priority 200-299: Post-processing hooks
4. Priority 300+: Cleanup and logging hooks

## Hook Context

The `HookContext` object provides:
- **state:** Current skill state
- **config:** Skill configuration
- **logger:** Logging interface
- **metrics:** Metrics collection interface
- **utilities:** Common utility functions

## Hook Result

The `HookResult` object contains:
- **success:** Boolean indicating success
- **data:** Optional data to pass to next hook
- **modified:** Boolean indicating if data was modified
- **stop:** Boolean to stop hook chain
- **error:** Error information if failed

## Error Handling in Hooks

Hooks should implement defensive error handling:
```python
try:
    # Hook logic
    return HookResult(success=True, data=result)
except Exception as e:
    logger.error(f"Hook {hook_name} failed: {e}")
    return HookResult(success=True, error=e)  # Don't break chain
```

## Hook Testing

Test hooks should:
1. Test success paths
2. Test error conditions
3. Test parameter validation
4. Test state modifications
5. Test hook chain execution

## Hook Documentation

Each hook should document:
1. Purpose and timing
2. Parameters and their types
3. Return value structure
4. Side effects
5. Error conditions
6. Dependencies on other hooks
