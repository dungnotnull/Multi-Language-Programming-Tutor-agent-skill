# Agents Directory

**Purpose:** Specialized sub-agents for specific teaching and analysis tasks

## Architecture Overview

This directory contains specialized sub-agents that implement specific aspects of the multilanguage coding tutor. Each agent has a focused responsibility and can be invoked independently or as part of a chain.

## Agent Types

### Core Teaching Agents

#### Diagnostic Agent
- **File:** `diagnostic_agent.md`
- **Purpose:** Assess learner's current knowledge, language background, and learning needs
- **Capabilities:**
  - Language/paradigm background assessment
  - Concept mastery evaluation
  - Learning style detection
  - Personalized path recommendation

#### Concept Teaching Agent
- **File:** `concept_teacher.md`
- **Purpose:** Teach transferable programming concepts with language-specific examples
- **Capabilities:**
  - Concept explanation with analogies
  - Multi-language demonstration
  - Practice exercise generation
  - Assessment and feedback

#### Parson's Problems Agent
- **File:** `parsons_agent.md`
- **Purpose:** Generate and validate Parson's problem exercises
- **Capabilities:**
  - Problem generation by difficulty and language
  - Solution validation
  - Hint generation
  - Progress tracking

#### Worked Examples Agent
- **File:** `worked_examples_agent.md`
- **Purpose:** Create worked examples with faded scaffolding
- **Capabilities:**
  - Example selection by concept and difficulty
  - Scaffolding level adjustment
  - Explanation generation
  - Interactive exercise creation

### Debugging & Mental Model Agents

#### Code Tracing Agent
- **File:** `code_tracing_agent.md`
- **Purpose:** Teach code tracing and mental model building
- **Capabilities:**
  - Tracing exercise generation
  - Step-by-step execution visualization
  - Variable state tracking
  - Mental model assessment

#### Error Literacy Agent
- **File:** `error_literacy_agent.md`
- **Purpose:** Teach error message understanding and debugging
- **Capabilities:**
  - Error explanation generation
  - Pattern identification
  - Solution recommendation
  - Prevention strategy teaching

### Project-Based Learning Agents

#### Project Generator Agent
- **File:** `project_generator.md`
- **Purpose:** Generate project-based learning milestones
- **Capabilities:**
  - Domain-specific project creation
  - Milestone breakdown
  - Prerequisite checking
  - Progress tracking

#### Milestone Tracker Agent
- **File:** `milestone_tracker.md`
- **Purpose:** Track and manage learning milestones
- **Capabilities:**
  - Progress visualization
  - Achievement tracking
  - Personalized path adaptation
  - Recommendation generation

### Cross-Language Transfer Agents

#### Concept Mapper Agent
- **File:** `concept_mapper.md`
- **Purpose:** Map concepts between programming languages
- **Capabilities:**
  - Concept equivalence identification
  - Syntax translation
  - Paradigm adaptation
  - Pattern mapping

#### Language Comparison Agent
- **File:** `language_comparison.md`
- **Purpose:** Compare languages and teach transferable skills
- **Capabilities:**
  - Feature comparison
  - Pattern translation
  - Best practice mapping
  - Paradigm explanation

### Evaluation & Analysis Agents

#### Quality Evaluator Agent
- **File:** `quality_evaluator.md`
- **Purpose:** Evaluate the quality of generated content
- **Capabilities:**
  - Content quality assessment
  - Pedagogical effectiveness evaluation
  - Clarity and accuracy checking
  - Improvement recommendation

#### Test Case Generator Agent
- **File:** `test_generator.md`
- **Purpose:** Generate test cases for skill validation
- **Capabilities:**
  - Test prompt creation
  - Expected output generation
  - Edge case identification
  - Coverage analysis

## Agent Execution Pattern

### Chain-of-Thought Routing
```
User Request
    ↓
Router Agent (analyze request)
    ↓
Specialized Agent(s) (execute task)
    ↓
Quality Evaluator (validate output)
    ↓
Response to User
```

### Parallel Execution
Some tasks can be executed in parallel:
- Multiple language examples for concept teaching
- Multiple difficulty levels for exercises
- Multiple domain projects for recommendations

### Sequential Execution
Some tasks require sequential execution:
- Diagnostic → Concept Teaching → Exercise Generation
- Project Selection → Milestone Creation → Progress Tracking

## Agent Communication

Agents communicate through:
1. **Structured Input:** JSON-defined input schemas
2. **Context Passing:** Shared context objects
3. **Result Aggregation:** Combining multiple agent outputs
4. **Error Handling:** Graceful fallbacks and error propagation

## Agent Development Guidelines

When creating a new agent:
1. Define clear purpose and capabilities
2. Specify input/output schemas
3. Document execution patterns
4. Include error handling strategies
5. Add evaluation criteria
6. Create test cases

## Agent Metadata

Each agent file should include:
```markdown
# Agent Name

**Purpose:** One-line description

**Input Schema:** JSON schema for inputs

**Output Schema:** JSON schema for outputs

**Capabilities:**
- Capability 1
- Capability 2

**Dependencies:**
- Required scripts/tools
- Required reference materials
- Required configuration

**Error Handling:**
- Known error conditions
- Fallback strategies

**Evaluation Criteria:**
- Quality metrics
- Success conditions
```
