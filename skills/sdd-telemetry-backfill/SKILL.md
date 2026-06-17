-----
name: sdd-telemetry-backfill
description: >
  Performs historical token and cost auditing across all conversation threads in the brain.
  Identifies projects and estimates real vs shadow costs.
  Trigger: "backfill telemetry", "arqueología de tokens", "auditar historial".
license: MIT
metadata:
  author: gentleman-programming
  version: "1.0"
---

## Rules
1. **Recursivity**: Scan all directories in `~/.gemini/antigravity/brain/`.
2. **Parsing**: Extract content from `USER_EXPLICIT` and `MODEL` sources in `overview.txt`.
3. **Attribution**: Detect project based on command logs (`sdd-init`, `/sdd-new`) or context keywords.
4. **Equivalence**: Compare Flash/Small models against `GPT-4o-mini` for the Shadow Cost.
5. **Output**: Update `C:\Users\user\.gemini\antigravity\scratch\telemetry_log_historical.json`.

## Usage
Run the `backfill_telemetry.py` script.
