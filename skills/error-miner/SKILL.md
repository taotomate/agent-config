---
name: error-miner
description: Analyzes thread transcripts for manual interventions or protocol deviations, and appends them objectively to error_log.md.
version: 1.1.0
author: TaoTomate
generator_model: nemotron-3-ultra-free
inherited_from: error-miner/SKILL.md
migrated_by: skill-optimizer@1.0.0
model_tier: medium
---

## Context & Triggers
**When to use this skill:**
- At the end of a session where the human intervened to correct a hallucination or protocol deviation.
- When the user asks to audit or mine the history for errors.
- Triggers: "mine errors", "close thread and mine", "postmortem", "audit history"


## Execution Phases


### 1. Diagnosis Phase
- Scan the transcript for: omitted commands, violated rules, routing skips, manual interventions.
- If no errors are detected, report "No deviations found" and finish.

### 2. Action Phase
- For each error detected, generate a structured block with a timestamp (`YYYYMMDDHHMMSS`).
- Append the block to the end of `shared/global_error_log.md` using append (`>>` in bash, `Add-Content` in PowerShell).
- Do NOT read the existing file — use stateless append with a timestamp.

### 3. Verification Phase
- Confirm the block was appended (check the last line of the file).
- If the append failed, report the error without retrying.

## Guardrails (Critical Rules)
- **NEVER** use defensive LLM biases (e.g. "ambiguous prompt" or "user tricked me").
- **ALWAYS** describe the technical failure as-is: what command was omitted, what rule was violated, why routing was not followed.
- **ALWAYS** use stateless append (do not read the existing file — generate ID by timestamp).
- **NEVER** rewrite the file — use `>>` or `Add-Content`.
- **ALWAYS** include all 10 fields of the log block (project, phase, model, context, violated rule, erroneous action, effect, root cause, resolution).

## Data Structures / Examples & Commands

### Log Block
```markdown
## Error #{YYYYMMDDHHMMSS}
- **Project / Workspace:** [Project name or repository]
- **Active Phase:** [What the agent was doing]
- **Model:** [Name of the LLM model that failed]
- **Failure Context:** [Original command or user intent, verbatim]
- **Violated Rule:** [What protocol or directive was ignored]
- **Erroneous Action:** [What the agent tried to do instead of following the rule]
- **Effect / Symptom:** [How you noticed the error]
- **Root Cause:** [Technical failure or architectural bias]
- **Resolution:** [How the user intervened or how it was fixed]
```

### Commands
```powershell
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$logPath = "D:\TaoTomate.Dots\agent-config\shared\global_error_log.md"
$content = @"

## Error #$timestamp
- **Project / Workspace:** ...
- **Active Phase:** ...
- **Model:** ...
- **Failure Context:** ...
- **Violated Rule:** ...
- **Erroneous Action:** ...
- **Effect / Symptom:** ...
- **Root Cause:** ...
- **Resolution:** ...
"@
Add-Content -Path $logPath -Value $content -Encoding UTF8
```

## Troubleshooting
- *No errors detected but the user knows there are some*: Review the transcript line by line looking for manual interventions (the user said "no", "fix", "that's wrong").
- *Append failed*: Verify write permissions on `shared/global_error_log.md`. Do not retry.
