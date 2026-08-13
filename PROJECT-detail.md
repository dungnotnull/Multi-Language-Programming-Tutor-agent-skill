# PROJECT-detail.md — Multi-Language Programming Tutor

## 1. Problem Statement

A skill that teaches programming across multiple languages (Python, JavaScript, Java, C++, Go, Rust, etc.) and domains (web, systems, data, mobile), using research-backed CS-education techniques such as worked examples, code-tracing practice, and error-message literacy.

## 2. Target Users

Describe the primary user personas for this skill (fill in based on real usage once built): e.g., students, professionals, hobbyists, or practitioners in the relevant domain.

## 3. Functional Specification

### 3.1 Core Capabilities

- Diagnose learner's current language/paradigm background
- Teach transferable programming concepts before language-specific syntax
- Use worked examples and Parson's-problem-style code-ordering exercises
- Teach code-tracing and mental-model building for debugging
- Explain compiler/interpreter error messages pedagogically (error literacy)
- Design project-based milestones per domain (web app, CLI tool, systems program)
- Support cross-language transfer (e.g., Python to Rust ownership concepts)

### 3.2 Key Methodologies & Frameworks Applied

- **Parson's Problems (code-ordering) technique**
- **Worked-example effect and faded-scaffolding**
- **Notional machine / mental-model building for programming (du Boulay)**
- **Error-message literacy pedagogy**
- **Project-Based Learning (PBL) for programming**

Each framework above should be operationalized as a concrete step, checklist, or template inside the skill's SKILL.md and reference files once this scaffold is turned into a runnable skill (see `DEVELOPMENT-TASK-BY-PHASES.md`).

### 3.3 Expected Input

Typical user requests this skill should handle (fill in with real example prompts during development and testing).

### 3.4 Expected Output Format

Define the structured output format(s) this skill should produce (e.g., structured report, checklist, scored recommendation, memo). Align with the methodologies above so outputs are consistent and auditable.

## 4. Out of Scope / Guardrails

General guardrails apply — remain factual, avoid unsupported certainty, and encourage professional consultation where the topic genuinely warrants it.

## 5. Knowledge Base Dependency

This skill's reasoning quality depends on the research foundations catalogued in `SECOND-BRAIN-KNOWLEDGE-PAPER.md`. When building the actual skill (SKILL.md + references/), extract the operational principles from each paper into concrete reference files rather than leaving them as a flat reading list.

## 6. Success Criteria

- Output correctly applies the named methodologies rather than generic reasoning.
- Output is well-structured and consistent across repeated runs on similar inputs.
- Domain-appropriate guardrails/disclaimers are respected in every response.
- Test prompts (see `DEVELOPMENT-TASK-BY-PHASES.md`, Phase 5) produce outputs a subject-matter-competent reviewer would rate as sound.
