---
model_tier: inherited
name: create-instructions
description: 'Create an instructions file (.instructions.md) for a project rule or convention.'
argument-hint: What rule or convention to enforce?
disable-model-invocation: true
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
- Triggers: "create-instructions", "use create-instructions"


Related skill: `agent-customization`. Load and follow **instructions.md** for template and principles.

Guide the user to create an instructions file.


## Prerequisites
- [ ] Read access to target files/directories
- [ ] Write access for auto-fix operations


## Extract from Conversation
First, review the conversation history. If the user has been correcting the agent's output or asking for specific patterns (e.g., "always use X", "never do Y", "follow this style"), generalize that into a persistent instruction. Extract:
- Corrections or preferences mentioned during the conversation
- Coding patterns the user enforced or requested
- Project-specific conventions referenced

## Clarify if Needed
If no clear rule emerges from the conversation, clarify:
- Should this apply everywhere or only to specific files?
- Which technologies or file types are affected?
- Is this a hard rule or a preference?

Explore the codebase using subagents if you need more context.

## Iterate
1. Draft the instruction and save it.
2. Identify the most ambiguous or weak parts and ask about those.
3. Once finalized, summarize what the instruction enforces, suggest example prompts to see it in action, and propose related customizations to create next.

Remember to follow the `agent-customization` guidelines to create highly effective instructions.


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash

