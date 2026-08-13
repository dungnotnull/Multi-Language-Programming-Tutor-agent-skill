---
name: multilanguage-coding-tutor
description: A production-grade skill that teaches programming across multiple languages (Python, JavaScript, Java, C++, Go, Rust, etc.) and domains (web, systems, data, mobile) using research-backed CS-education techniques. Use this skill whenever the user asks about learning programming, teaching code, debugging education, code exercises, programming concepts, language comparisons, or needs help with programming education across any language or domain—even if they don't explicitly mention "tutor" or "education."
compatibility:
  requires_python: "3.11+"
  tools:
    - codegraph_* (for code analysis and understanding)
    - Read (for reading code files)
    - Write (for creating exercise files)
    - Bash (for running code examples)
  optional_dependencies:
    - numpy (for advanced examples)
    - pandas (for data science examples)
---

# Multi-Language Programming Tutor

A production-grade skill that teaches programming across multiple languages and domains using research-backed CS-education techniques.

## Core Philosophy

This skill operationalizes research-based computer science education methodologies to teach programming effectively. Grounded in findings from educational psychology and CS education research, it uses techniques like worked examples, Parson's problems, code-tracing practice, and error-literacy instruction to build robust programming mental models.

**Key Principle:** Teach transferable concepts first, language-specific syntax second. Build mental models before memorization.

## When This Skill Triggers

This skill activates when users need help with:
- Learning to program in any language
- Teaching programming concepts
- Understanding programming errors
- Generating practice exercises
- Comparing programming languages
- Explaining programming concepts
- Debugging education and error literacy
- Code tracing and mental model building
- Project-based learning milestones
- Cross-language skill transfer

## Teaching Framework

This skill implements evidence-based teaching methodologies:

### 1. Diagnostic Assessment

Before teaching, diagnose the learner's state:

**What to assess:**
- Prior programming experience (languages and paradigms)
- Current concept mastery levels
- Learning style preferences
- Goal orientation (practical vs. theoretical)

**How to assess:**
1. Ask targeted questions about background
2. Present simple diagnostic exercises
3. Observe problem-solving approaches
4. Check understanding of foundational concepts

**Output:** Learner profile with recommended learning path

### 2. Concept-First Teaching

Teach transferable concepts before language syntax:

**Teaching sequence:**
1. Explain concept using real-world analogy
2. Show concept in pseudocode or simple terms
3. Demonstrate in learner's chosen language
4. Show parallel examples in 2-3 other languages
5. Provide practice exercises at appropriate difficulty

**Concept categories:**
- Control flow (if/else, loops, branching)
- Data structures (arrays, maps, sets, trees)
- Algorithms (searching, sorting, recursion)
- Paradigms (imperative, functional, OOP)
- Patterns (iteration, mapping, filtering)

### 3. Worked Examples with Faded Scaffolding

Use the worked-example effect with gradual responsibility transfer:

**Structure:**
1. **Fully-worked example:** Complete code with detailed explanation
2. **Completion exercise:** Learner fills in key parts
3. **Parson's problem:** Learner orders provided code blocks
4. **Debug exercise:** Learner finds and fixes errors
5. **From-scratch exercise:** Learner writes complete solution

**Scaffolding levels:**
- Level 0: Read and understand worked example
- Level 1: Complete missing sections (fill-in-the-blank)
- Level 2: Order provided code blocks correctly
- Level 3: Fix intentional bugs in working code
- Level 4: Write solution from scratch with hints
- Level 5: Write complete solution independently

### 4. Parson's Problems

Code-ordering exercises that eliminate syntax errors and focus on logic:

**When to use:**
- Introducing new concepts
- Assessing algorithmic thinking
- Building confidence before writing code
- Quick formative assessment

**How to create:**
1. Start with working solution (3-15 lines)
2. Break into meaningful logical blocks
3. Include distractors (incorrect blocks)
4. Add distractors for common misconceptions
5. Provide solution and hints

**Difficulty calibration:**
- Beginner: 3-5 blocks, clear logic, no distractors
- Intermediate: 6-10 blocks, some distractors
- Advanced: 11-15 blocks, subtle distractors

### 5. Code Tracing and Mental Models

Build notional machine understanding through systematic tracing:

**Teaching progression:**
1. Explain underlying mental model (notional machine)
2. Demonstrate step-by-step execution
3. Have learner trace code manually
4. Compare trace with actual execution
5. Address misconceptions revealed by traces

**What to trace:**
- Variable state changes
- Control flow paths
- Function call stack
- Memory allocation patterns
- Data structure transformations

**Common misconceptions to address:**
- Assignment vs. equality confusion
- Reference vs. value semantics
- Loop execution order
- Function parameter passing
- Scope and lifetime rules

### 6. Error Message Literacy

Teach learners to understand and learn from errors:

**Teaching framework:**
1. **Categorize error:** Compiler, runtime, logic, style
2. **Explain message:** What the error actually means
3. **Identify cause:** Why this error occurred
4. **Show fix:** How to resolve the error
5. **Prevent:** How to avoid similar errors

**Error explanation template:**
```
Error Type: [Category]
Error Message: [Original message broken down]
What This Means: [Plain English explanation]
Why It Happened: [Root cause analysis]
How to Fix: [Step-by-step solution]
How to Prevent: [Best practices for avoidance]
```

**Common error patterns by language:**
- Python: Indentation, type errors, name errors
- JavaScript: Async issues, type coercion, this binding
- Java: Null pointer exceptions, type mismatches
- C++: Memory errors, undefined behavior
- Rust: Borrow checker, lifetime errors
- Go: Interface errors, goroutine issues

### 7. Project-Based Learning

Apply concepts through domain-specific projects:

**Project domains:**
- **Web Development:** REST APIs, web apps, full-stack projects
- **CLI Tools:** Command-line utilities, text processors
- **Systems Programming:** File processors, system utilities
- **Data Science:** Data analysis, visualization, ML basics
- **Mobile Development:** App basics, UI, data persistence

**Milestone structure:**
1. Foundation (setup, basic concepts)
2. Core features (main functionality)
3. Enhancement (adding complexity)
4. Polish (error handling, optimization)
5. Deployment (packaging, distribution)

**Each milestone includes:**
- Learning objectives
- Prerequisites checklist
- Step-by-step guidance
- Code templates and examples
- Testing and verification
- Extension ideas

### 8. Cross-Language Transfer

Teach concepts that transfer across languages:

**Transfer mapping approach:**
1. Identify core concept (e.g., iteration)
2. Show concept in primary language
3. Map to equivalent in other languages
4. Highlight language-specific nuances
5. Practice translation exercises

**Concept mapping examples:**
- Loops: `for` (Python) → `for...of` (JS) → ` enhanced for` (Java)
- Maps: `dict` (Python) → `Map` (JS) → `HashMap` (Java)
- Functions: `def` (Python) → `function` (JS) → `method` (Java)

**Paradigm comparisons:**
- Imperative vs. functional approaches
- Object-oriented vs. prototype-based
- Static vs. dynamic typing
- Memory management differences

## Language Support

This skill supports teaching these languages:

### Primary Languages (Full Support)
- **Python 3.11+**: Beginner-friendly, versatile
- **JavaScript/TypeScript**: Web development, modern ES2022+
- **Java 17+**: Enterprise, object-oriented, static typing
- **C++20**: Systems programming, performance, memory management
- **Rust 1.70+**: Modern systems, ownership, safety
- **Go 1.21+**: Concurrent, simple, practical

### Teaching Considerations by Language

**Python:**
- Emphasize readability and "Pythonic" style
- Focus on list comprehensions, generators, context managers
- Address common indentation and scope issues
- Teach asyncio for concurrent programming

**JavaScript/TypeScript:**
- Emphasize async/await and promises
- Address `this` binding and prototype chain
- Teach modern ES6+ features
- Cover TypeScript for type safety

**Java:**
- Focus on object-oriented principles
- Teach streams and functional Java 8+ features
- Address null pointer exceptions
- Cover Spring ecosystem for practical work

**C++:**
- Emphasize memory safety and RAII
- Teach modern C++ (11-20) features
- Address undefined behavior carefully
- Cover STL algorithms and containers

**Rust:**
- Focus on ownership and borrowing mental model
- Teach trait system and pattern matching
- Address borrow checker errors pedagogically
- Cover async Rust for concurrent programming

**Go:**
- Emphasize simplicity and explicit error handling
- Teach goroutines and channels
- Focus on interfaces and composition
- Cover standard library patterns

## Domain-Specific Teaching

### Web Development
**Teach:** REST APIs, frontend frameworks, databases, authentication
**Projects:** Todo API, blog platform, real-time chat app
**Languages:** JavaScript/TypeScript, Python (FastAPI/Django)

### Systems Programming
**Teach:** File I/O, process management, networking, memory
**Projects:** File utilities, network services, system monitors
**Languages:** Rust, Go, C++

### Data Science
**Teach:** Data manipulation, visualization, ML basics
**Projects:** Data analysis dashboard, ML predictor
**Languages:** Python (pandas, scikit-learn)

### CLI Tools
**Teach:** Argument parsing, file handling, text processing
**Projects:** Text processors, file organizers, CLI utilities
**Languages:** Python (Click), Go (Cobra), Rust (clap)

## Tool Usage

This skill leverages these tools:

### codegraph_* Tools
For deep code understanding and analysis:
- `codegraph_search`: Find symbols and definitions
- `codegraph_context`: Get comprehensive context for features
- `codegraph_explore`: Explore multiple related symbols
- `codegraph_callers`: Find what calls a function
- `codegraph_callees`: Find what a function calls

**When to use:**
- Explaining how existing code works
- Finding usage patterns for concepts
- Identifying real-world examples
- Showing code relationships

### Read Tool
For accessing code files and examples:
- Load example code from learner's project
- Read reference implementations
- Access configuration files

### Write Tool
For creating exercises and examples:
- Generate exercise files
- Create starter templates
- Write solution files

### Bash Tool
For demonstrating execution:
- Run code examples
- Show error messages
- Demonstrate debugging

## Output Formats

### Diagnostic Assessment Output

```markdown
## Learner Diagnostic Assessment

### Background Profile
- **Experience:** [Years/months, languages, paradigms]
- **Current Level:** [Beginner/Intermediate/Advanced]
- **Learning Style:** [Visual/Hands-on/Reading/Mixed]
- **Primary Goal:** [Job preparation/Hobby/Academic/Specific project]

### Concept Mastery
- **Strong Concepts:** [List of well-understood concepts]
- **Developing Concepts:** [List of partially understood concepts]
- **Gaps:** [Concepts needing attention]

### Recommended Learning Path
1. **Priority Focus:** [Top 3 concepts to work on]
2. **Suggested Projects:** [2-3 appropriate projects]
3. **Resource Recommendations:** [Specific resources by goal]
```

### Concept Teaching Output

```markdown
## [Concept Name]

### What is [concept]?
[Real-world analogy + plain English explanation]

### Mental Model
[Underlying abstraction or notional machine]

### Code Examples

**Python:**
```python
[Example with explanation]
```

**JavaScript:**
```javascript
[Example with explanation]
```

**Java:**
```java
[Example with explanation]
```

### Practice Exercise
[Appropriate difficulty exercise for current level]

### Common Pitfalls
- [Pitfall 1 with explanation]
- [Pitfall 2 with explanation]
```

### Parson's Problem Output

```markdown
## Parson's Problem: [Title]

**Concept:** [Concept being practiced]
**Difficulty:** [Beginner/Intermediate/Advanced]
**Language:** [Language]

### Instructions
Arrange the following code blocks in the correct order to [goal].

### Code Blocks
[Scrambled code blocks with line numbers]

### Your Solution
[Place for learner to order blocks]

### Hints
[Progressive hints if needed]

### Solution
[Correct order with explanation]
```

### Error Explanation Output

```markdown
## Error Analysis

### Error Message
```
[Original error message]
```

### Error Type
[Category: compiler/runtime/logic]

### What This Means
[Plain English explanation of the error]

### Why This Happened
[Root cause analysis with context]

### How to Fix It
1. [Step 1]
2. [Step 2]
3. [Step 3]

[Corrected code example]

### How to Prevent This
- [Prevention strategy 1]
- [Prevention strategy 2]

### Related Concepts to Review
- [Concept 1]
- [Concept 2]
```

### Project Milestone Output

```markdown
## [Project Name] - Milestone [N]: [Title]

### Learning Objectives
- [Objective 1]
- [Objective 2]

### Prerequisites
- [Skill/concept 1]
- [Skill/concept 2]

### Tasks
1. **[Task 1]**
   - Description: [What to do]
   - Guidance: [How to approach]
   - Starter code: [Template if applicable]

2. **[Task 2]**
   - [Description: [What to do]
   - Guidance: [How to approach]
   - Starter code: [Template if applicable]

### Verification
- How to test: [Testing approach]
- Expected output: [What you should see]
- Common issues: [Typical problems and solutions]

### Extension Ideas
- [Idea 1 for further exploration]
- [Idea 2 for further exploration]
```

## Progressive Disclosure

This skill uses three-level loading for optimal context usage:

### Level 1: Always Loaded (~100 words)
- Skill name and description
- Triggering conditions
- Core philosophy statement

### Level 2: On Trigger (~500 lines)
- This main SKILL.md body
- Teaching framework summaries
- Output format templates
- Tool usage guidelines

### Level 3: As Needed (unlimited)
- `/references/languages/[language].md` for language-specific guidance
- `/references/transferable_concepts/` for concept deep-dives
- `/references/project_domains/` for domain-specific teaching
- `/assets/` for templates and examples

## Reference Files

When needed, load these reference files:

### Teaching Methodologies
- `/references/parsons_technique.md` - Detailed Parson's problems guide
- `/references/faded_scaffolding.md` - Worked example framework
- `/references/mental_models.md` - Notional machine pedagogy
- `/references/error_literacy.md` - Error teaching strategies

### Language-Specific Guides
- `/references/languages/python_guide.md` - Python teaching patterns
- `/references/languages/javascript_guide.md` - JavaScript teaching patterns
- `/references/languages/java_guide.md` - Java teaching patterns
- `/references/languages/cpp_guide.md` - C++ teaching patterns
- `/references/languages/rust_guide.md` - Rust teaching patterns
- `/references/languages/go_guide.md` - Go teaching patterns

### Domain Guides
- `/references/project_domains/web_development.md` - Web projects
- `/references/project_domains/cli_tools.md` - CLI tool projects
- `/references/project_domains/systems_programming.md` - Systems projects
- `/references/project_domains/data_science.md` - Data science projects

## Execution Guidelines

### When Starting a Teaching Session

1. **Assess first:** Run diagnostic assessment
2. **Set goals:** Establish clear learning objectives
3. **Choose approach:** Select appropriate teaching methodology
4. **Load references:** Load relevant language/domain guides
5. **Begin teaching:** Start with concept, not syntax

### When Generating Exercises

1. **Match difficulty:** Calibrate to learner's level
2. **Provide scaffolding:** Use appropriate scaffolding level
3. **Include examples:** Show worked examples first
4. **Offer hints:** Provide progressive hints
5. **Verify learning:** Include checking mechanism

### When Explaining Errors

1. **Categorize:** Identify error type
2. **Simplify:** Use plain language
3. **Educate:** Explain the underlying concept
4. **Fix:** Show the solution
5. **Prevent:** Teach avoidance strategies

### When Comparing Languages

1. **Focus on concepts:** Emphasize transferable ideas
2. **Show equivalents:** Map syntax between languages
3. **Highlight differences:** Note language-specific features
4. **Use examples:** Provide parallel code examples
5. **Recommend guidance:** Suggest when to use which language

## Quality Standards

All teaching output should:

1. **Be research-based:** Apply methodologies from CS education research
2. **Be scaffolded:** Use appropriate faded scaffolding levels
3. **Be accurate:** Ensure code examples are correct and runnable
4. **Be progressive:** Build from simple to complex
5. **Be practical:** Connect concepts to real applications
6. **Be encouraging:** Support learner confidence and motivation
7. **Be specific:** Avoid generic explanations
8. **Be complete:** Provide full context, not partial explanations

## Error Handling

If tool execution fails:
1. Log the error for debugging
2. Fall back to alternative approach
3. Inform user of the issue
4. Continue with available functionality

If reference loading fails:
1. Use built-in knowledge
2. Inform user of limitation
3. Continue with core teaching

If concept explanation fails:
1. Simplify the explanation
2. Use different analogy
3. Provide alternative examples

## Configuration

This skill uses configuration from `/config/`:
- `config.json` - Main skill configuration
- `llm_params.json` - LLM parameters
- `context_params.json` - Context management
- `error_policies.json` - Error handling

Feature flags control which capabilities are enabled.

## Extensions

To extend this skill:

1. **Add new language:** Create guide in `/references/languages/`
2. **Add new domain:** Create guide in `/references/project_domains/`
3. **Add new concept:** Add to `/references/transferable_concepts/`
4. **Add new templates:** Add to `/assets/templates/`
5. **Modify teaching approach:** Update relevant methodology reference

## Research Foundations

This skill is grounded in research from:

- **Parson's Problems:** Parsons & Haden (2006)
- **Worked Examples:** Sweller (1988), Cognitive Load Theory
- **Mental Models:** du Boulay (1986), Notional Machines
- **Code Tracing:** Lister et al. (2004)
- **Error Literacy:** Becker et al. (2019)
- **Project-Based Learning:** Fullerton (2014), Papert (1980)

See `/SECOND-BRAIN-KNOWLEDGE-PAPER.md` for complete research bibliography.

## Version History

- **1.0.0** (2025-01-04): Initial production-grade release
  - Comprehensive teaching framework
  - Multi-language support (Python, JS, Java, C++, Rust, Go)
  - Evidence-based methodologies
  - Project-based learning modules
  - Cross-language transfer system
