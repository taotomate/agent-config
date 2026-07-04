---
name: sdd-telemetry
description: Tracks tokens, execution time, and comparative market value per turn. Trigger: end of every turn or when asking for "telemetría".
version: "1.1"
author: gentleman-programming
license: MIT
model_tier: fast
---

## Context & Triggers
**When to use this skill:**
- At the end of every LLM turn to provide resource consumption feedback.
- When the user asks for telemetry: "telemetría", "cost", "usage", "tokens".
- Appends a cost table to the agent's response and persists to JSON log.


## Execution Phases


### 1. Calculate Turn Stats
- `input_tokens = user_request.length / 4`
- `output_tokens = agent_response.length / 4`
- `duration = end_time - start_time` (in seconds)

### 2. Resolve Pricing
- Read `~\.gemini\antigravity\scratch\pricing_table.json`
- Calculate current cost ($ per 1M tokens) for the model used
- Compute shadow cost against GPT-4o or Claude 3.5 Sonnet as benchmarks

### 3. Append Output Table
- Format the telemetry block and append at the very end of the agent's response

### 4. Persist to Log
- Append the JSON entry to `~\.gemini\antigravity\scratch\telemetry_log.json`

## Guardrails (Critical Rules)
- **ALWAYS** append the telemetry block at the very end of the response — never inline or in the middle.
- **ALWAYS** include both real cost (free tier = $0.0000) and shadow cost (GPT-4o/Claude comparison).
- **NEVER** skip telemetry logging — silence is not an option when the user asked for it.
- **ALWAYS** calculate tokens by character count / 4 as a heuristic — never leave the field blank.

## Data Structures / Examples & Commands

### Output Table Format
```
| Role | Model | Tokens (I/O) | Real Cost | Shadow |
| :--- | :--- | :--- | :--- | :--- |
| 🧠 Orchestrator | {model_cloud} | {in_cloud}k / {out_cloud}k | ${real_cloud} | ${shadow_cloud} |
| 🧪 Distiller | {model_local} (Local) | {in_local}k / {out_local}k | $0.0000 | ${shadow_local} |
| **Total** | | **{total_tokens}k** | **${total_real}** | **${total_shadow}** |
```

### JSON Log Entry (append)
```json
{"timestamp": "ISO-8601", "model": "...", "input_tokens": N, "output_tokens": N, "real_cost": 0.0, "shadow_cost": 0.0}
```

## Troubleshooting
- *pricing_table.json missing*: Telemetry runs with $0 real cost — pricing table is optional for core function.
- *Log file doesn't exist*: Use append mode — the file is created on first write.
