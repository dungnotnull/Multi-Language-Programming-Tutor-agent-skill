# Config Directory

**Purpose:** Dedicated, type-safe configuration management for environment variables, LLM parameters, and system-wide feature flags

## Structure

This directory contains all configuration files for the skill and its subsystems.

## Configuration Files

### Main Configuration
- `config.json` - Main skill configuration file
  - Skill metadata and versioning
  - Feature flags and toggles
  - Default parameter values
  - Module enablement settings

### Environment Configuration
- `env.schema.json` - Environment variable schema definition
- `env.example.json` - Example environment configuration
- `env.defaults.json` - Default environment values

### LLM Configuration
- `llm_params.json` - LLM parameter configurations
  - Model settings (temperature, top_p, max_tokens)
  - Retry logic parameters
  - Timeout configurations
  - Rate limiting settings

### Diagnostic Configuration
- `diagnostic_params.json` - Diagnostic assessment parameters
  - Difficulty calibration settings
  - Mastery threshold definitions
  - Adaptation parameters

### Evaluation Configuration
- `evaluation_params.json` - Evaluation and testing parameters
  - Grading criteria definitions
  - Performance thresholds
  - Test execution settings

### Context Configuration
- `context_params.json` - Context window management
  - Token limit settings
  - Compression thresholds
  - Loading strategies

### Error Handling Configuration
- `error_policies.json` - Error handling policies
  - Retry strategies
  - Fallback behaviors
  - Circuit breaker settings

### Logging Configuration
- `logging_config.json` - Logging system configuration
  - Log level settings
  - Output destinations
  - Format specifications
  - Rotation policies

### Milestone Configuration
- `milestones.json` - Project milestone definitions
  - Milestone hierarchies
  - Prerequisite relationships
  - Achievement criteria

### Language Support Configuration
- `language_support.json` - Supported languages and features
  - Language capabilities
  - Available features per language
  - Language-specific settings

## Configuration Schema

All configuration files should follow this structure:

```json
{
  "$schema": "./config.schema.json",
  "version": "1.0.0",
  "metadata": {
    "name": "configuration_name",
    "description": "Configuration description",
    "last_updated": "2025-01-04"
  },
  "settings": {
    // Configuration key-value pairs
  }
}
```

## Environment Variables

Environment variables are managed through the schema system:

### Required Variables
- `SKILL_MODE` - Operating mode (development, production, testing)
- `LOG_LEVEL` - Logging verbosity (debug, info, warning, error)
- `MAX_TOKENS` - Maximum token budget for operations

### Optional Variables
- `LLM_MODEL` - Default LLM model to use
- `TIMEOUT_SECONDS` - Operation timeout in seconds
- `RETRY_COUNT` - Number of retries for failed operations
- `CACHE_ENABLED` - Enable/disable caching

## Configuration Loading

Configuration is loaded in this order (later overrides earlier):
1. Built-in defaults
2. `env.defaults.json`
3. Environment-specific file (`env.{SKILL_MODE}.json`)
4. Environment variables
5. Runtime overrides

## Validation

All configuration is validated against schemas:
1. Schema validation on load
2. Type checking for all values
3. Range validation for numeric values
4. Enum validation for categorical values
5. Dependency validation between settings

## Feature Flags

Feature flags control optional functionality:

```json
{
  "features": {
    "parsons_problems": true,
    "worked_examples": true,
    "code_tracing": true,
    "error_literacy": true,
    "project_learning": true,
    "cross_language_transfer": true,
    "diagnostics": true,
    "milestone_tracking": true
  }
}
```

## Security Considerations

- Never commit secrets or API keys to config files
- Use environment variables for sensitive data
- Validate all configuration values
- Sanitize error messages to avoid leaking config
- Use read-only configuration after validation

## Development Guidelines

When adding new configuration:
1. Add to appropriate config file
2. Update schema definitions
3. Add validation rules
4. Document in README
5. Add examples to env.example.json
6. Update configuration loading if needed
