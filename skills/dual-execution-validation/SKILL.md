---
name: dual-execution-validation
description: 'Executes technical tasks through cross-validation (Cloud vs Local
  LLM) to compare result fidelity, establish capacity boundaries, and optimize
  token consumption through real-time benchmarking. Trigger: "dual
  execution", "dual validation", "run frontier", "compare with local".
  '
version: "3.1"
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: dual-execution-validation/SKILL.md
model_tier: medium
---

## Context & Triggers
**When to use this skill:**
- When you want to test if a repetitive task (e.g. tests, simple refactors) can be delegated to a local model.
- To validate local model accuracy against cloud models (e.g. GPT/Gemini) on logic problems.
- When processing large volumes of text where token savings are critical.
- Triggers: "dual execution", "dual validation", "run frontier", "compare with local".

## Prerequisites
- [ ] Local model configured and accessible.
- [ ] Know the exact prompt to be used for cross-validation.

## Execution Phases

> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase. 
> Instead, the agent will print the exact payload it planned to execute, and will stop to wait for explicit human approval.

### 1. Diagnosis Phase
- Extract the main intent of the task.
- Prepare the synchronized prompt: formulate EXACTLY the same prompt and context that will be sent to both models.

### 2. Action Phase
- **Local Execution**: Invoke the local model through the corresponding tool or script (e.g. via `ask_local_llm` if the MCP exists, or via Python/bash scripts hitting Ollama).
- **Cloud Execution**: As the orchestrator agent, process the task yourself (using your own engine) and save the result.

### 3. Verification Phase
- Generate an immediate "Comparative Report". Present the evaluation matrix (Verdict) to the user in chat.
- Analyze and declare in the report whether there was "Tunnel Vision" (if the local model ignored the general context, e.g. mixing sections or breaking scopes).

## Guardrails (Critical Rules)
- **Strict Synchronization**: The prompt must be exactly the same for both models. Do not simplify the prompt for the local model.
- **Frontier Detection**: If the local model demonstrates it can match or exceed the test 3 times in a row in a specific category, update the frontier by marking that category as "Safe for Delegation" and save it to Engram.
- **No Local Hallucination**: When evaluating the local model, heavily penalize hallucination or breaking the existing code structure.

## Data Structures / Examples & Commands

**Evaluation Matrix (Verdict)**
Must be presented in Markdown format with this structure:

| Criteria | Cloud (e.g. Gemini Pro) | Local (e.g. Qwen 8B / Hermes) |
|----------|------------------------|------------------------------|
| **Logic** | (1-10) - Depth | (1-10) - Precision |
| **Context** | (1-10) - Global vision | (1-10) - Tunnel vision |
| **Speed** | Time in seconds | Time in seconds |
| **Savings** | 0% (Base cost) | 100% (Tokens saved) |

**Execution Command (Optional if a script exists):**
```bash
# Example of manual comparison test invocation if the shadow test script exists:
python scratch/shadow_test.py
```

## ⚠️ Migration Residue (Evolution Feedback)
*(Successfully migrated from v2.0 to IaC v1.2, formalizing the local vs cloud delegation pipeline within the execution phases)*

## Troubleshooting

- **Local model unreachable**: Verify Ollama is running (`ollama list`). If using an MCP tool, check MCP status.
- **Prompt mismatch**: Ensure the EXACT same prompt string is sent to both models. Use a variable to avoid drift.
- **Tunnel vision detected**: If the local model consistently ignores context, reduce task complexity or mark the category as "Not Safe for Delegation" in the frontier.
