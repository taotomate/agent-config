---
name: sdd-telemetry-backfill
description: Performs historical token and cost auditing across all conversation threads in the brain. Identifies projects and estimates real vs shadow costs. Trigger: "backfill telemetry", "token archaeology", "audit history".
version: "1.1"
author: gentleman-programming
license: MIT
model_tier: fast
---

## Context & Triggers
**When to use this skill:**
- To audit historical token usage across old conversations.
- To estimate shadow cost savings from using free/local models.
- Triggers: "backfill telemetry", "token archaeology", "audit history".

## Prerequisites
- [ ] Access to `~/.gemini/antigravity/brain/` with conversation overview files.
- [ ] Write access to `~\.gemini\antigravity\scratch\telemetry_log_historical.json`.
- [ ] Python script `backfill_telemetry.py` available in the execution path.

## Execution Phases

> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase. 
> Instead, the agent will print the exact payload (JSON, code block, or parameters) it planned to execute, and will wait for explicit human approval.

### 1. Scan Brain Directories
- Recursively scan all directories in `~/.gemini/antigravity/brain/`

### 2. Parse Conversation Overviews
- For each directory, read `overview.txt`
- Extract `USER_EXPLICIT` and `MODEL` source content

### 3. Attribute to Project
- Detect project association from command logs (`sdd-init`, `/sdd-new`) or context keywords

### 4. Calculate Shadow Cost
- Compare Flash/Small models against GPT-4o-mini as the equivalence baseline

### 5. Persist Results
- Update `~\.gemini\antigravity\scratch\telemetry_log_historical.json` with the batch results

## Guardrails (Critical Rules)
- **ALWAYS** run via the `backfill_telemetry.py` script — never attempt inline manual parsing.
- **ALWAYS** preserve existing entries in the historical log — append, never overwrite.
- **NEVER** skip directories that don't have `overview.txt` — report them as skipped.

## Data Structures / Examples & Commands

### Execution Command
```bash
python backfill_telemetry.py --brain-path ~/.gemini/antigravity/brain/
```

### Output Format (telemetry_log_historical.json)
```json
[
  {"project": "my-app", "conversations": 12, "total_tokens": 150000, "real_cost": 0.0, "shadow_cost": 0.75},
  {"project": "unknown", "conversations": 3, "total_tokens": 25000, "real_cost": 0.0, "shadow_cost": 0.12}
]
```

## Troubleshooting
- *No brain directory found*: Verify Antigravity is installed at `~/.gemini/antigravity/`. If empty, nothing to backfill.
- *Script not found*: Locate `backfill_telemetry.py` in the project's execution/ directory or ask the orchestrator for the path.
