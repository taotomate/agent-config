---
name: code-reviewer-python
description: 'Migrated skill: code-reviewer-python'
version: 1.0.0
author: unknown
generator_model: unknown
model_tier: medium
inherited_from: D:\todas-las-skills-llm\skills\code-reviewer-python\SKILL.md
migrated_by: skill-optimizer@3.2.0
---

## Context & Triggers
**When to use this skill:**
- TODO: Add specific triggers for this skill
- Triggers: "code-reviewer-python", "use code-reviewer-python"



# Code Reviewer - Python
Load this skill whenever you are acting as a Code Reviewer and the files being reviewed are Python files (`.py`).

## Prerequisites
- [ ] Read access to target files/directories
- [ ] Write access for auto-fix operations

## Execution Phases

> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase.
> Instead, the agent will print the exact payload it planned to execute, and will wait for explicit human approval.

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

## Guardrails (Critical Rules)
- **ALWAYS** reject the code if you find:
  - Hardcoded secrets or credentials
  - Empty try/except blocks (silent error handling)
  - Code duplication (violates DRY)
  - `print()` in production code (should use `logger`)
- **ALWAYS** reject the code if:
  - Missing type hints on public functions
  - Bare `except:` without specific exception
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash

## Data Structures / Examples & Commands

### Response Format
The first line of your response must be exactly one of:
- `STATUS: PASSED`
- `STATUS: FAILED`

If `FAILED`, list the issues in this format:
`<file>:<line> - <rule violated> - <issue>`


