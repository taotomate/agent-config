---
model_tier: inherited
name: uv
description: >-
  Checks whether the uv Python package manager is installed and installs it if
  missing. Ensures uv is on PATH. Use when another skill requires uv as a
  prerequisite.
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
- Triggers: "uv", "use uv"


# uv (Python Package Manager)

`uv` is a fast Python package manager used by Science Skills to run their Python
CLI scripts. Many skills depend on `uv` being installed and on PATH.

Ensure `uv` is available before running any skill that depends on it.


## Setup

1.  Check if `uv` is already available: `uv --version` If this succeeds, `uv` is
    ready — skip the remaining steps.
2.  Check whether `uv` is installed at its default location but not on PATH:
    `"$HOME/.local/bin/uv" --version` If this succeeds, skip to step 4.
3.  If uv is not installed do both these steps in order:
    (a) Tell the user that uv is a tool for creating a consistent and reliable
        Python environment used for running the Science Skills, and that you
        need to install it now.
    (b) Install `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`
4.  Add `uv` to PATH and verify (run as a single command): `export
    PATH="$HOME/.local/bin:$PATH" && uv --version`

After setup, bare `uv` commands should work without repeating the export.


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash

