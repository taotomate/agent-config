<!-- v2.1 | last edited: 2026-06-23 -->
# Tool & Model Routing

## Agent vs Script
- If the task is predictable and repeatable → script in `execution/`
- If the task requires decision-making or has variable steps → agent
- If the script does not exist:
  1. Create it in `execution/task_name.py`
  2. Create its `test_task_name.py`
  3. Verify it passes the test before executing
- The model is used to generate the script, not to execute the task

## Models by Layer

### L1 — Planning / Architecture
- Primary: Gemini Pro / Opus
- Fallback: Sonnet
- When: design, architecture, complex analysis

### L2 — Orchestration / Decisions
- Primary: Gemini Flash / Sonnet
- Fallback: Haiku
- When: task routing, error handling, coordination

### L3 — Execution
- Primary: Python script in `execution/`
- Fallback: local models (Ollama / LM Studio) or free tier
- Paid models only if the above options are insufficient

## Model Change on Failure
If a model generates repeated errors on a specific task type,
consult `directives/errors_learned.md` for history
and reassign it to a layer or task where it performs better.
