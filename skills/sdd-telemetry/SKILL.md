---
name: sdd-telemetry
description: >
  Tracks tokens, execution time, and comparative market value.
  Trigger: End of every turn or when asking for "telemetría".
license: MIT
metadata:
  author: gentleman-programming
  version: "1.0"
---

## Purpose
Provide the user with real-time feedback on resource consumption and efficiency compared to top-tier models.

## Operating Instructions

1. **Calculate Turn Stats**:
   - `input_tokens = user_request.length / 4`
   - `output_tokens = agent_response.length / 4`
   - `duration = end_time - start_time` (in seconds)

2. **Comparative Pricing**:
   - Read `C:\Users\user\.gemini\antigravity\scratch\pricing_table.json`.
   - Calculate current cost ($ per 1M tokens).
   - Compare with `GPT-4o` or `Claude 3.5 Sonnet` as benchmarks.

3. **Output Format**:
   - Append a block like this at the very end of your response:

   | Role | Model | Tokens (I/O) | Real Cost | Shadow |
| :--- | :--- | :--- | :--- | :--- |
| 🧠 Orchestrator | {model_cloud} | {in_cloud}k / {out_cloud}k | ${real_cloud} | ${shadow_cloud} |
| 🧪 Distiller | {model_local} (Local) | {in_local}k / {out_local}k | $0.0000 | ${shadow_local} |
| **Total** | | **{total_tokens}k** | **${total_real}** | **${total_shadow}** |

4. **Persistence**:
   - Append the JSON entry to `C:\Users\user\.gemini\antigravity\scratch\telemetry_log.json`.
