---
name: [skill-name]
description: [Brief 1-2 line description]
version: 1.0.0
author: [Your Name]
model_tier: [high|medium|fast]
---

## Context & Triggers
**When to use this skill:**
- Detail the specific scenarios where the orchestrator should invoke this skill.
- *Example: "When the user asks to create a GitHub ticket or report a bug."*

## Prerequisites
List of environment conditions that must be met **before** starting.
- [ ] Installed tool (e.g. `gh cli`).
- [ ] Existing specific directories.
- [ ] Configured environment variables.

## Execution Phases
Break down the process into deterministic steps. Leave no room for improvisation.

> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase. 
> Instead, the agent will print the exact payload (JSON, code block, or parameters) it planned to execute, and will wait for explicit human approval.

### 1. Diagnosis Phase
- What to investigate or read before acting (e.g. read `.clauderules` or check for duplicates).
### 2. Action Phase
- The commands or modifications to perform on the code or system.
### 3. Verification Phase
- How to objectively test that the action was successful (e.g. run `npm test`, validate JSON against a schema).

## Guardrails (Critical Rules)
Non-negotiable restrictions for the AI model.
- **DO NOT** [Prohibited behavior or dangerous assumption].
- **ALWAYS** [Strict rule to follow without exception].

## Data Structures / Examples & Commands
Provides rich context for the LLM to avoid format hallucinations.
- Command examples (`bash` or scripts).
- Expected formats (JSON schemas, exact Markdown templates).
- Decision tree if the logic has complex branches.

## Troubleshooting
Quick recovery guide for common and skill-specific errors.
- *If [Error X] occurs, the probable cause is [Cause Y]. Run [Command Z] to resolve.*
