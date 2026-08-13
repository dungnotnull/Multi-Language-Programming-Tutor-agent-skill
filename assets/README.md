# Assets Directory

**Purpose:** Static resources, system diagrams, schemas, and templates used in skill outputs

## Structure

This directory contains static resources that the skill uses in generating outputs or that are included in packaged skill files.

## Asset Categories

### Templates
- `parsons_templates.json` - Parson's problem templates by language and difficulty
- `worked_example_templates/` - Worked example templates by concept
- `code_tracing_templates/` - Code tracing exercise templates
- `project_templates/` - Project milestone templates by domain
- `error_databases/` - Language-specific error message databases

### Example Banks
- `language_examples/` - Curated code examples by language
  - `python_examples.json` - Python examples by concept
  - `javascript_examples.json` - JavaScript examples by concept
  - `java_examples.json` - Java examples by concept
  - `cpp_examples.json` - C++ examples by concept
  - `rust_examples.json` - Rust examples by concept
  - `go_examples.json` - Go examples by concept

### Concept Maps
- `concept_maps/` - Cross-language concept mapping resources
  - `control_flow_map.json` - Control flow across languages
  - `data_structures_map.json` - Data structure implementations
  - `paradigm_comparison.json` - Programming paradigm comparisons

### Schemas
- `schemas/` - JSON schemas for validation
  - `input_schema.json` - Skill input validation schema
  - `output_schema.json` - Skill output validation schema
  - `diagnostic_schema.json` - Diagnostic result schema
  - `milestone_schema.json` - Milestone tracking schema

### Diagrams
- `diagrams/` - System architecture and flow diagrams
  - `agent_flow.png` - Agent execution flow diagram
  - `teaching_pipeline.png` - Teaching methodology pipeline
  - `assessment_flow.png` - Diagnostic assessment flow

### Configuration Files
- `language_support.json` - Supported languages and their features
- `difficulty_progression.json` - Difficulty level definitions
- `milestone_definitions.json` - Project milestone definitions

## Usage Guidelines

Asset files should:
1. Be version-controlled and stable
2. Include clear documentation of structure
3. Use appropriate file formats (JSON for data, Markdown for text)
4. Be validated against schemas where applicable
5. Include comments for complex structures

## JSON Structure Guidelines

For JSON assets:
1. Use consistent naming conventions (camelCase for keys)
2. Include type information in comments or documentation
3. Validate against schemas in `/assets/schemas/`
4. Use null sparingly and document allowed values
5. Include examples in documentation

## Template Guidelines

Templates should:
1. Use clear placeholder syntax (e.g., `{{variable_name}}`)
2. Include metadata about difficulty, language, concepts
3. Be validated for correct syntax
4. Include usage examples in comments
5. Support localization where appropriate

## Asset Versioning

Assets follow semantic versioning:
- Major version: Breaking structure changes
- Minor version: Additive changes
- Patch version: Bug fixes and improvements

Version information should be tracked in asset metadata.
