# Tools Directory

**Purpose:** Rich tool definitions with schemas and execution handlers for agent use

## Overview

Tools are callable functions that agents can dynamically invoke. They provide a standardized interface for common operations, with schema validation and error handling.

## Tool Architecture

### Tool Definition Structure

```json
{
  "name": "tool_name",
  "version": "1.0.0",
  "description": "Tool description",
  "input_schema": {
    "type": "object",
    "properties": {
      "parameter_name": {
        "type": "string",
        "description": "Parameter description"
      }
    },
    "required": ["parameter_name"]
  },
  "output_schema": {
    "type": "object",
    "properties": {
      "result": {
        "type": "string",
        "description": "Result description"
      }
    }
  },
  "handler": "tools.module_name.function_name",
  "execution": {
    "type": "synchronous",
    "timeout": 30,
    "retry": {
      "max_attempts": 3,
      "backoff": "exponential"
    }
  }
}
```

## Tool Categories

### Generation Tools

#### `generate_parsons_problem`
- **Purpose:** Generate Parson's problem exercises
- **Input:** language, concept, difficulty
- **Output:** Problem specification, solution, hints
- **Handler:** `scripts/parsons_generator.py`

#### `generate_worked_example`
- **Purpose:** Generate worked examples with scaffolding
- **Input:** concept, language, scaffolding_level
- **Output:** Example code, explanations, exercises
- **Handler:** `scripts/worked_examples.py`

#### `generate_code_tracing_exercise`
- **Purpose:** Generate code tracing exercises
- **Input:** language, complexity, concepts
- **Output:** Exercise code, trace steps, answer key
- **Handler:** `scripts/code_tracing.py`

#### `generate_explanation`
- **Purpose:** Generate explanations for concepts
- **Input:** concept, depth, analogies, examples
- **Output:** Explanation text, examples, visualizations
- **Handler:** `scripts/explanation_generator.py`

### Analysis Tools

#### `analyze_code`
- **Purpose:** Analyze code for patterns and issues
- **Input:** code, language, analysis_type
- **Output:** Analysis results, suggestions, patterns
- **Handler:** `scripts/code_analyzer.py`

#### `explain_error`
- **Purpose:** Explain error messages
- **Input:** error_message, language, context
- **Output:** Explanation, causes, solutions, prevention
- **Handler:** `scripts/error_explainer.py`

#### `assess_mastery`
- **Purpose:** Assess learner's concept mastery
- **Input:** learner_responses, concept_id
- **Output:** Mastery level, gaps, recommendations
- **Handler:** `scripts/diagnostics.py`

#### `compare_languages`
- **Purpose:** Compare programming languages
- **Input:** languages, aspect, detail_level
- **Output:** Comparison table, examples, recommendations
- **Handler:** `scripts/concept_mapper.py`

### Project Tools

#### `generate_project_milestones`
- **Purpose:** Generate project-based learning milestones
- **Input:** domain, language, difficulty_level
- **Output:** Project specification, milestones, resources
- **Handler:** `scripts/project_generator.py`

#### `track_progress`
- **Purpose:** Track learner progress on milestones
- **Input:** learner_id, milestone_data, completion_status
- **Output:** Progress report, achievements, next_steps
- **Handler:** `scripts/milestone_tracker.py`

#### `recommend_next_step`
- **Purpose:** Recommend next learning step
- **Input:** learner_profile, current_progress, goals
- **Output:** Recommendation with rationale, resources
- **Handler:** `scripts/recommender.py`

### Utility Tools

#### `validate_code`
- **Purpose:** Validate code syntax and structure
- **Input:** code, language, validation_rules
- **Output:** Validation result, errors, warnings
- **Handler:** `scripts/validator.py`

#### `count_tokens`
- **Purpose:** Count tokens in text
- **Input:** text, model
- **Output:** Token count, cost estimate
- **Handler:** `scripts/token_counter.py`

#### `format_code`
- **Purpose:** Format code according to language standards
- **Input:** code, language, style_guide
- **Output:** Formatted code, changes made
- **Handler:** `scripts/formatter.py`

#### `load_reference`
- **Purpose:** Load reference materials dynamically
- **Input:** reference_id, sections
- **Output:** Reference content, metadata
- **Handler:** `scripts/reference_loader.py`

### Configuration Tools

#### `load_config`
- **Purpose:** Load configuration values
- **Input:** config_path, keys, defaults
- **Output:** Configuration values
- **Handler:** `config/config_loader.py`

#### `update_config`
- **Purpose:** Update configuration at runtime
- **Input:** config_path, updates, validate
- **Output:** Update confirmation, new config
- **Handler:** `config/config_loader.py`

#### `get_feature_flag`
- **Purpose:** Check if a feature is enabled
- **Input:** feature_name, context
- **Output:** Feature enabled status, config
- **Handler:** `config/feature_flags.py`

### State Management Tools

#### `save_state`
- **Purpose:** Save current skill state
- **Input:** state_data, key, options
- **Output:** Save confirmation, metadata
- **Handler:** `scripts/state_manager.py`

#### `load_state`
- **Purpose:** Load saved skill state
- **Input:** key, options
- **Output:** State data, metadata
- **Handler:** `scripts/state_manager.py`

#### `clear_state`
- **Purpose:** Clear saved skill state
- **Input:** key, options
- **Output:** Clear confirmation
- **Handler:** `scripts/state_manager.py`

### Logging Tools

#### `log_event`
- **Purpose:** Log events with structured data
- **Input:** event_type, data, level
- **Output:** Log confirmation
- **Handler:** `scripts/logger.py`

#### `get_metrics`
- **Purpose:** Retrieve performance metrics
- **Input:** metric_type, time_range, aggregation
- **Output:** Metrics data, statistics
- **Handler:** `scripts/metrics.py`

## Tool Execution

### Synchronous Execution
Most tools execute synchronously:
```python
result = execute_tool(
    tool_name="generate_parsons_problem",
    parameters={
        "language": "python",
        "concept": "loops",
        "difficulty": "intermediate"
    }
)
```

### Asynchronous Execution
Long-running tools can execute asynchronously:
```python
task_id = execute_tool_async(
    tool_name="generate_project_milestones",
    parameters={...}
)
result = await tool_result(task_id)
```

### Batch Execution
Multiple tools can be executed in batch:
```python
results = execute_tools_batch([
    {"tool": "generate_parsons_problem", "params": {...}},
    {"tool": "generate_worked_example", "params": {...}}
])
```

## Tool Error Handling

Tools implement comprehensive error handling:
1. **Input Validation:** Validate against schema
2. **Execution Errors:** Try-catch with logging
3. **Retry Logic:** Configurable retry with backoff
4. **Fallbacks:** Graceful degradation
5. **Error Responses:** Structured error information

## Tool Registration

Tools are registered in the tool registry:
```json
{
  "tools": {
    "tool_name": {
      "enabled": true,
      "version": "1.0.0",
      "schema": "tools/schemas/tool_name.json",
      "handler": "tools/handlers/tool_name.py"
    }
  }
}
```

## Tool Discovery

Agents can discover available tools:
```python
available_tools = discover_tools(
    category="generation",
    language="python"
)
```

## Tool Versioning

Tools follow semantic versioning:
- **Major:** Breaking changes
- **Minor:** Feature additions
- **Patch:** Bug fixes

Tool handlers should maintain backward compatibility within major versions.

## Tool Testing

Tool tests should cover:
1. Valid inputs
2. Invalid inputs
3. Edge cases
4. Error conditions
5. Performance characteristics
6. Integration with other tools

## Tool Documentation

Each tool should document:
1. Purpose and use cases
2. Input schema with examples
3. Output schema with examples
4. Error conditions and handling
5. Performance characteristics
6. Dependencies and requirements
7. Version history
