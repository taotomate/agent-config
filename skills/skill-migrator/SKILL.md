---
name: skill-migrator
description: Meta-tool for migrating legacy skills to the new state-machine standard (IaC v1.2), supporting individual and batch mode with residue analysis. Includes a post-migration phase that updates the skill-registry automatically.
version: 1.1.0
author: TaoTomate
generator_model: nemotron-3-ultra-free
inherited_from: skill-migrator/SKILL.md
migrated_by: skill-migrator@1.1.0
model_tier: fast
---

## Context & Triggers
**When to use this skill:**
- When refactoring legacy skills (v1.0 architecture) toward the new deterministic state-machine format (IaC v1.2+).
- To apply a migration process in bulk across an entire directory.
- Triggers: "migrate skill", "refactor old skill", "apply skill-migrator", "update skill architecture".

## Prerequisites
- [ ] The target architecture template (`agent-config/shared/template_skill.md`) must exist and be readable by the agent.
- [ ] The agent must have read and write permissions on the target file (`target: path`) or target directory (`batch: path`).
- [ ] The agent must not have active restrictions preventing it from overwriting Markdown files or generating new structures.

## Execution Phases

> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase. 
> Instead, the agent will print the exact payload (JSON, code block, or parameters) it planned to execute, and will wait for explicit human approval.

### 1. Diagnosis Phase
- Identify the requested execution mode: Individual (`target: path/to/skill`) or Batch (`batch: path/to/dir/`).
- If Batch mode, perform a glob scan of all `SKILL.md` files within the indicated directory.
- **Complexity Filter (Active Guardrail):** Superficially analyze each target skill's content before intervening.
  - If the skill delegates aggressively to sub-agents, invokes external scripts (e.g. `node script.js`, `python script.py`), or belongs to the orchestration suite (`sdd-*`): **MARK AS SKIPPED**.
  - If Batch mode, report the skip and continue with the next. If Individual mode, **abort immediately** and request a human rewrite it manually.

### 2. Action Phase
- For each skill passing the filter, apply **Semantic Mapping** to the new template:
  - What was previously *When to use / Triggers* ➔ Move to `Context & Triggers`.
  - Implicit environment requirements ➔ Move to `Prerequisites`.
  - *Workflow / Steps* ➔ Distribute logically among `Execution Phases` (Diagnosis, Action, Verification).
  - *Critical Rules* ➔ Convert into prohibitions/obligations in `Guardrails (Critical Rules)`.
  - *Code Examples / Bash Commands* ➔ Strictly encapsulate in `Data Structures / Examples & Commands`.
- **Traceability Injection:** Inject the **Traceability Seal** into the new skill's YAML frontmatter (see Data Structures section).
- **Dry-Run Rule Injection:** Inject the universal Dry-Run rule block under the Execution Phases title (see Data Structures).
- **Residue Analysis (Lost & Found):** Compare the full original text with the mapped text. Any block or concept that does not logically fit into the new mold MUST be appended at the end of the new file under the heading `## ⚠️ Migration Residue (Evolution Feedback)`.
- Overwrite the old `SKILL.md` with the new content.

### 3. Verification Phase
- If executed in Batch mode, present a console summary table indicating:
  - `Successfully Migrated Skills` vs `Skipped Skills (With complexity reason)`.
- If executed in Individual mode, suggest the human invoke the newly migrated skill with the `--dry-run` flag to validate the agent can parse it correctly without executing destructive actions.

### 4. Post-Migration Phase: Update Registry
- **Only if NOT `--dry-run` mode** and at least one skill was successfully migrated:
  - Invoke the `skill-registry` skill via the `skill` tool to regenerate `.atl/skill-registry.md` with the updated skills.
  - Show confirmation: "Registry updated: X user skills indexed."
- If `--dry-run` mode: skip this phase and report: "[DRY-RUN] Registry not updated (simulation)."

## Guardrails (Critical Rules)
- **NEVER** silently delete code examples, commands, or documentation links from a skill. If you cannot place them in the correct section, forcibly move them to the Migration Residue block.
- **ALWAYS** inject the literal `--dry-run` rule into the skills you migrate.
- **NEVER** modify or attempt to auto-migrate skills that trigger the Complexity Filter. The heuristic cannot refactor external Node or Python scripts.
- **ALWAYS** include the exact traceability seal in the YAML frontmatter; without it, the migration is null and the file will be considered corrupt by the registry.

## Data Structures / Examples & Commands

### Traceability Seal (Frontmatter Injection)
You must inject these fields into the YAML header, replacing the brackets with the current session's dynamic data:
```yaml
generator_model: [the raw LLM model you use, e.g. gemini-1.5-pro]
inherited_from: [Absolute or relative path of the original SKILL.md file]
migrated_by: skill-migrator@1.0.0
```

### Dry-Run Rule Injection
Copy and insert this block exactly as-is, right below the `## Execution Phases` title in the skill you are migrating:

```markdown
> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase. 
> Instead, the agent will print the exact payload (JSON, code block, or parameters) it planned to execute, and will stop to wait for explicit human approval.
```

## Troubleshooting
- *If a severe context loss occurs and the skill is emptied:* The orchestrator should stop, restore the original file from its source, and request the human process that skill manually.
- *If Batch mode crashes:* Ensure recursive read permissions on the target folder, and check logs for which specific skill caused the exception to skip it in the next cycle.
