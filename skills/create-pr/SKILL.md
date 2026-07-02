---
model_tier: inherited
name: create-pr
description: Create a pull request for the current session. Use when the user wants to open a PR with the session's changes.
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
- Triggers: "create-pr", "use create-pr"


<!-- Customize this skill and select save to override its behavior. Delete that copy to restore the built-in behavior. -->

# Create Pull Request

Use the GitHub MCP server to create a pull request — do NOT use the `gh` CLI.

1. Run the compile and hygiene tasks (fixing any errors)
2. If there are any uncommitted changes, use the `/commit` skill to commit them
3. Review all changes in the current session
4. Write a clear, concise PR title with a short area prefix (e.g. "sessions: …", "editor: …")
5. Write a description covering what changed, why, and anything reviewers should know
6. Create the pull request


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash

