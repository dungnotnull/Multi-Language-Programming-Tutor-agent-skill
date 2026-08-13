# Scripts Directory

**Purpose:** Automation, database seeding, ingestion, and local setup routines

## Structure

This directory contains executable scripts for deterministic and repetitive tasks that the skill needs to perform.

## Script Categories

### Generation Scripts
- `parsons_generator.py` - Parson's problem exercise generator
- `worked_examples.py` - Worked example generation with faded scaffolding
- `code_tracing.py` - Code tracing exercise generator
- `project_generator.py` - Project-based learning milestone generator
- `concept_mapper.py` - Cross-language concept mapping system
- `error_explainer.py` - Error message explanation system
- `diagnostics.py` - Learner diagnostic and assessment engine

### Evaluation Scripts
- `evaluator.py` - Automated evaluation and grading system
- `benchmark.py` - Performance benchmarking tools

### System Scripts
- `error_handler.py` - Error handling and resilience system
- `logger.py` - Structured logging system
- `context_manager.py` - Context window optimization
- `milestone_tracker.py` - Learning milestone tracking

### Utility Scripts
- `token_counter.py` - Token counting and analysis
- `validator.py` - Input validation and schema checking

## Usage

Scripts in this directory should:
1. Be executable standalone (include `if __name__ == "__main__"` blocks)
2. Have clear command-line interfaces with argparse
3. Include comprehensive docstrings
4. Handle errors gracefully
5. Log operations appropriately
6. Be type-hinted for IDE support

## Dependencies

Scripts may depend on:
- Standard Python 3.11+ library
- Third-party packages listed in project requirements
- Configuration from `/config`
- Reference data from `/references`
- Templates from `/assets`

## Development Guidelines

- Keep scripts focused on single responsibilities
- Use type hints for all function signatures
- Include unit tests in `/tests` directory
- Document CLI usage in docstrings
- Handle configuration loading from `/config`
