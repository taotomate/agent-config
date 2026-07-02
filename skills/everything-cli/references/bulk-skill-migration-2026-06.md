# Bulk Skill Migration — 2026-06

## Context
Migrated 15 legacy v1.0 skills to modern format (DRY-RUN, Guardrails, Prerequisites, Context & Triggers).

## What Was Migrated
- bitwarden-cli, computer-use, yuanbao, dogfood (repo skills)
- sdd-apply, sdd-archive, sdd-design, sdd-explore, sdd-init, sdd-local-distiller, sdd-propose, sdd-spec, sdd-tasks, sdd-verify, sdd-onboard (TaoTomate skills)

## Migration Template

```yaml
---
name: <name>
description: <original description>
version: <original version>
author: <original author>
model_tier: <original tier or "medium">
migrated_by: skill-optimizer@2.0.2
---

## Context & Triggers
**When to use this skill:**
- TODO: Add specific triggers for <name>
- Triggers: "<name>", "use <name>"

## Prerequisites
- [ ] Read access to target files/directories
- [ ] Write access for auto-fix operations

## Execution Phases

> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase.
> Instead, the agent will print the exact payload (JSON, code block, or parameters) it planned to execute, and will wait for explicit human approval.

### 1. Preparation Phase
- Load references and verify prerequisites
- Resolve target scope

### 2. Action Phase
- Execute the main workflow
- Follow the steps defined in the original content below

### 3. Verification Phase
- Verify output matches expected results
- Generate completion report

## Original Content
<original SKILL.md body preserved verbatim>

## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** generate report before any change
- **ALWAYS** verify target directory exists before scanning — if missing, abort with clear error
- **ALWAYS** handle unreadable SKILL.md gracefully — skip with warning, don't crash the batch

## Troubleshooting
- *If prerequisites are missing*: Install required tools before proceeding
- *If dry-run mode*: Only generate reports, do not write changes
```

## Structural Analysis Checks
For each skill, verify presence of:
1. Frontmatter (`---` at start)
2. DRY-RUN rule (under Execution Phases)
3. Guardrails section
4. Context & Triggers
5. Prerequisites
6. Execution Phases
7. Data Structures / Examples / Original Content

**Legacy detection**: `not has_dry_run and not has_guardrails` → needs migration

## Result
All 15 skills scored 1.00 after migration. Backups saved as `.v1-backup` files alongside each SKILL.md.
