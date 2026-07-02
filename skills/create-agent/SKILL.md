---
model_tier: inherited
name: create-agent
description: 'Create a custom agent (.agent.md) for a specific job.'
argument-hint: What job should this agent do and how?
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
- Triggers: "create-agent", "use create-agent"


Related skill: `agent-customization`. Load and follow **agents.md** for template and principles.

Guide the user to create an `.agent.md`.


## Prerequisites
- [ ] Read access to target files/directories
- [ ] Write access for auto-fix operations


## Extract from Conversation
First, review the conversation history. If the user has been using the agent in a specialized way (e.g., restricting tools, following a specific persona, focusing on certain file types), generalize that into a custom agent. Extract:
- The specialized role or persona being assumed
- Tool preferences (which to use, which to avoid)
- The domain or job scope

## Clarify if Needed
If no clear specialization emerges from the conversation, clarify:
- What job should this agent do?
- When should it be picked over the default agent?
- Which tools should it use (or avoid)?

## Iterate
1. Draft the agent file and save it.
2. Identify the most ambiguous or weak parts and ask about those.
3. Once finalized, summarize what the agent does, suggest example prompts to try it, and propose related customizations to create next.

Remember to follow the `agent-customization` guidelines to create highly effective agents.


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash

