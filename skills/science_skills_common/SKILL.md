---
model_tier: inherited
name: science-skills-common
description: >-
  Shared Python package for Science Skills, currently containing http_client --
  a unified HTTP client with rate limiting, retries, and exponential backoff.
  Not a standalone agent skill. Do not invoke directly.
---

## Execution Phases


**DRY-RUN RULE:** Before executing any destructive or external operation, first perform a dry-run to preview what will happen. Show the user what actions would be taken, then ask for confirmation before proceeding.
### 1. Preparation Phase
- Load references and verify prerequisites
- Resolve target scope

### 2. Action Phase
- Execute the main workflow (original content below preserves existing steps)

### 3. Verification Phase
- Verify output matches expected results

## Context & Triggers
**When to use this skill:**
- Triggers: "science_skills_common", "use science_skills_common"


# Science Skills Common

This is a shared Python package, not an agent skill. Skills import it as:

```python
from science_skills.science_skills_common import http_client
```

Each skill declares this as a dependency in its inline `uv` script header, so it
is installed automatically on first use.

This SKILL.md file is included so that standard skill installers automatically
discover and install this package alongside the skills that depend on it.


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash

