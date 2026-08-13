# References Directory

**Purpose:** Domain knowledge, prompt base-templates, and raw context guidelines for RAG/agent grounding

## Structure

This directory contains reference materials loaded into context as needed by the skill and its agents.

## Reference Categories

### Teaching Methodology References
- `parsons_technique.md` - Parson's Problems implementation guide
- `faded_scaffolding.md` - Worked example and scaffolding framework
- `mental_models.md` - Notional machine and mental model building
- `error_literacy.md` - Error message teaching methodology
- `diagnostic_framework.md` - Learner assessment framework
- `milestone_framework.md` - Project-based milestone system

### Language-Specific References
- `languages/` - Language-specific teaching guides
  - `python_guide.md` - Python teaching patterns and common issues
  - `javascript_guide.md` - JavaScript/TypeScript teaching patterns
  - `java_guide.md` - Java teaching patterns and best practices
  - `cpp_guide.md` - C++ teaching patterns and concepts
  - `rust_guide.md` - Rust ownership and borrowing pedagogy
  - `go_guide.md` - Go concurrency and patterns
  - `mobile_guide.md` - Mobile development (Swift/Kotlin) patterns

### Domain-Specific References
- `project_domains/` - Domain-specific project guides
  - `web_development.md` - Web development project milestones
  - `cli_tools.md` - CLI tool development projects
  - `systems_programming.md` - Systems programming projects
  - `data_science.md` - Data science project patterns
  - `mobile_development.md` - Mobile app development projects

### Transferable Concepts References
- `transferable_concepts/` - Language-agnostic concept guides
  - `control_flow.md` - Control flow structures across languages
  - `data_structures.md` - Data structures and their implementations
  - `algorithms.md` - Algorithmic thinking and patterns
  - `paradigms.md` - Programming paradigms comparison
  - `patterns.md` - Design patterns across languages

### Technical References
- `optimization.md` - Context window and performance optimization
- `monitoring.md` - Logging and monitoring practices
- `error_handling.md` - Production error handling strategies
- `testing.md` - Testing methodology for skill outputs

## Usage Guidelines

Reference files should:
1. Be focused and comprehensive (300+ lines warrant sub-files)
2. Include table of contents for navigation
3. Use clear headings and hierarchical structure
4. Include examples and templates
5. Reference research sources where applicable
6. Be cited from SKILL.md with clear guidance on when to load

## Progressive Disclosure

Reference files support the skill's progressive disclosure system:
- **Level 1:** SKILL.md metadata (always in context)
- **Level 2:** SKILL.md body (loaded when skill triggers)
- **Level 3:** Reference files (loaded as needed)

## File Naming Convention

Use descriptive, lowercase names with underscores:
- `teaching_method_name.md` for teaching techniques
- `language_name_guide.md` for language guides
- `domain_name.md` for domain references
