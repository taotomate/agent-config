---
model_tier: inherited
name: act-on-feedback
description: Act on user feedback attached to the current session. Use when the user submits feedback on the session's changes via the Submit Feedback button.
---

## Execution Phases



**DRY-RUN RULE:** Before executing any destructive or external operation, first perform a dry-run to preview what will happen. Show the user what actions would be taken, then ask for confirmation before proceeding.
> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase.
> Instead, the agent will print the exact payload (JSON, code block, or parameters) it planned to execute, and will wait for explicit human approval.
### 1. Preparation Phase
- Load references and verify prerequisites
- Resolve target scope

### 2. Action Phase
- Execute the main workflow (original content below preserves existing steps)

### 3. Verification Phase
- Verify output matches expected results

## Context & Triggers
**When to use this skill:**
- TODO: Add specific triggers for this skill
- Triggers: "act-on-feedback", "use act-on-feedback"


<!-- Customize this skill and select save to override its behavior. Delete that copy to restore the built-in behavior. -->

# Act on Feedback

The user has provided feedback on the current session's changes. Their feedback comments have been attached to this message.

1. Review all attached feedback comments carefully
2. Understand the intent behind each piece of feedback
3. Make the requested changes to address the feedback
4. Verify your changes are consistent with the rest of the codebase


## Prerequisites
- [ ] Read access to target files/directories
- [ ] Write access for auto-fix operations



## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash

