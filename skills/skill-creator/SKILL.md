---
name: skill-creator
description: 'Creates new AI service skills following the Service Skills spec. Trigger:
  When user asks to create a new skill, add service instructions, or document patterns
  for AI.
  '
license: Apache-2.0
version: "1.1"
author: gentleman-programming
generator_model: gemini-1.5-pro
inherited_from: skill-creator/SKILL.md
migrated_by: skill-migrator@1.0.0
model_tier: high
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Context & Triggers
**When to use this skill:**
- A pattern is used repeatedly and the AI requires explicit instructions.
- Project-specific conventions differ from general recommended practices.
- Complex workflows require step-by-step instructions.
- When decision trees can help the AI choose the correct approach.


## Execution Phases


### 1. Diagnosis Phase
- Evaluate whether a skill is really needed: If documentation already exists, create a reference. If trivial, do not create the skill.
- Determine the name following the naming convention (`{technology}`, `{project}-{component}`, `{action}-{target}`).

### 2. Action Phase
- Write the main `SKILL.md` using the template.
- Include clear critical patterns, minimal code examples, and copy-paste commands.
- Decide the location of accessory files: `assets/` for templates or JSON schemas; `references/` for local documentation references.

### 3. Verification Phase
- Ensure the frontmatter is complete (lowercase identifier, description with triggers, version, author).
- Add the new skill to the `CONSTITUTION.md` registry using the skills table.

### Validation
Before marking the skill as complete, verify:

**Input Validation:**
- Skill name follows naming convention (`{technology}`, `{project}-{component}`, `{action}-{target}`)
- No duplicate skill exists in `skills/` directory

**Output Validation:**
- SKILL.md has valid frontmatter with all required fields
- SKILL.md body is under 450 tokens (style guide budget)
- No TODO placeholders remain
- `references/` directory contains only local files (no URLs)

## Guardrails (Critical Rules)
- **NEVER** add a "Keywords" section (the agent searches frontmatter, not the body).
- **NEVER** use web URLs in `references/`, use local paths exclusively.
- **NEVER** duplicate existing documentation content; use links and references.
- **ALWAYS** start with the most critical patterns and use tables for decision trees.

## Data Structures / Examples & Commands

### Skill Naming Convention
- **Generic:** `{technology}` (e.g. `pytest`, `typescript`)
- **Project-specific:** `{project}-{component}` (e.g. `myapp-api`)
- **Workflow:** `{action}-{target}` (e.g. `skill-creator`, `jira-task`)

### Directory Structure
```text
skills/{skill-name}/
├── SKILL.md              # Required - main file
├── assets/               # Optional - templates, schemas
└── references/           # Optional - links to local documentation
```

### Basic SKILL.md Template
```markdown
---
name: {skill-name}
description: '{What it does. Trigger: keywords for invocation.}'
version: "1.0.0"
author: {your-name}
generator_model: {model-used}
inherited_from: {origin-path}
model_tier: {high|medium|fast}
---

## Context & Triggers
**When to use this skill:**
- {situation 1}
- {situation 2}

## Prerequisites
- [ ] {requirement 1}

## Execution Phases


### 1. {Phase Name}
{description}

### 2. {Phase Name}
{description}

### 3. Verification Phase
{how to confirm success}

## Guardrails (Critical Rules)

- {rule 1}
- {rule 2}

## Data Structures / Examples & Commands

{key formats, tables, and CLI commands}

## Troubleshooting

- **{Problem}**: {solution}
- **{Problem}**: {solution}
```

### Registration in CONSTITUTION.md
```markdown
| `{skill-name}` | {Description} | [SKILL.md](skills/{skill-name}/SKILL.md) |
```

## Troubleshooting

- **Template doesn't pass skill-optimizer**: The template above is aligned with what skill-optimizer v2.0.2 checks. Ensure all sections are filled: frontmatter (version, model_tier, author, generator_model, inherited_from), DRY-RUN rule, Guardrails, Data Structures, and Troubleshooting.
- **model_tier not set**: Choose from `high` (architecture/design skills), `medium` (implementation/analysis), or `fast` (mechanical/utility). If unsure, use `medium`.
- **UNIVERSAL DRY-RUN missing**: The rule MUST appear under `## Execution Phases` before any step. Paste the exact block from the template above.
- **Template reference missing**: See `_shared/template_skill.md` for the complete reference template with all fields.

## ⚠️ Migration Residue (Evolution Feedback)
*(All information has been successfully mapped)*
