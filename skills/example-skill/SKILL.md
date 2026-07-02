---
model_tier: inherited
name: example-skill
description: This skill should be used when the user asks to "demonstrate skills", "show skill format", "create a skill template", or discusses skill development patterns. Provides a reference template for creating Claude Code plugin skills.
version: 1.0.0
---

## Context & Triggers
**When to use this skill:**
- Trigger: <describe_when_to_use>

## Execution Phases



**DRY-RUN RULE:** Before executing any destructive or external operation, first perform a dry-run to preview what will happen. Show the user what actions would be taken, then ask for confirmation before proceeding.
> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase.
> Instead, the agent will print the exact payload (JSON, code block, or parameters) it planned to execute, and will wait for explicit human approval.
### 1. Preparation Phase
- Load references and verify prerequisites
- Resolve target scope

### 2. Action Phase
- Execute the main workflow (original content below preserves existing steps)

### 3. Verification Phase
- Verify output matches expected results

## Prerequisites
- [ ] Read access to target files/directories
- [ ] Write access for auto-fix operations



# Example Skill

This skill demonstrates the structure and format for Claude Code plugin skills.

## Overview

Skills are model-invoked capabilities that Claude autonomously uses based on task context. Unlike commands (user-invoked) or agents (spawned by Claude), skills provide contextual guidance that Claude incorporates into its responses.

## When This Skill Applies

This skill activates when the user's request involves:
- Creating or understanding plugin skills
- Skill template or reference needs
- Skill development patterns

## Skill Structure

### Required Files

```
skills/
└── skill-name/
    └── SKILL.md          # Main skill definition (required)
```

### Optional Supporting Files

```
skills/
└── skill-name/
    ├── SKILL.md          # Main skill definition
    ├── README.md         # Additional documentation
    ├── references/       # Reference materials
    │   └── patterns.md
    ├── examples/         # Example files
    │   └── sample.md
    └── scripts/          # Helper scripts
        └── helper.sh
```

## Frontmatter Options

Skills support these frontmatter fields:

- **name** (required): Skill identifier
- **description** (required): Trigger conditions - describe when Claude should use this skill
- **version** (optional): Semantic version number
- **license** (optional): License information or reference

## Writing Effective Descriptions

The description field is crucial - it tells Claude when to invoke the skill.

**Good description patterns:**
```yaml
description: This skill should be used when the user asks to "specific phrase", "another phrase", mentions "keyword", or discusses topic-area.
```

**Include:**
- Specific trigger phrases users might say
- Keywords that indicate relevance
- Topic areas the skill covers

## Skill Content Guidelines

1. **Clear purpose**: State what the skill helps with
2. **When to use**: Define activation conditions
3. **Structured guidance**: Organize information logically
4. **Actionable instructions**: Provide concrete steps
5. **Examples**: Include practical examples when helpful

## Best Practices

- Keep skills focused on a single domain
- Write descriptions that clearly indicate when to activate
- Include reference materials in subdirectories for complex skills
- Test that the skill activates for expected queries
- Avoid overlap with other skills' trigger conditions


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash

