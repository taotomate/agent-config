# Analysis Criteria — Phase 2: Functional Analysis

Detailed criteria for evaluating whether a skill optimally fulfills its purpose.
Used by LLM delegations (high tier) during Phase 2 of skill-optimizer.

## 1. Intent vs Reality

| Question | Problem Indicator |
|----------|----------------------|
| Does the `description` exactly reflect what the `Phases` do? | If there are steps in Phases that the description does not cover |
| Do the `Triggers` cover ALL real invocation scenarios? | If it gets invoked by undocumented triggers |
| Are there overly generic triggers causing incorrect invocations? | If triggers like "error" or "git" without further context |

## 2. Minimal Path

| Question | Problem Indicator |
|----------|----------------------|
| Does each phase produce an output necessary for the next? | If there are phases that only format/repeat |
| Can 2+ phases be collapsed into 1? | If they are linear sequences without branching |
| Are there redundant steps between skills in the same pipeline? | If sdd-spec and sdd-design both have duplicate "load skills" steps |

## 3. Decision Points

| Question | Problem Indicator |
|----------|----------------------|
| Do the guardrails reflect real decisions the LLM must make vs obvious restrictions? | Guardrails like "DO NOT use bad practices" without concrete criteria |
| Where does the LLM add value vs just format output? | If the output is 100% template without analysis |

## 4. Failure Modes

| Question | Problem Indicator |
|----------|----------------------|
| Do the guardrails cover failures documented in errors_learned.md? | If errors_learned.md has entries without a corresponding guardrail |
| Does the skill have a Troubleshooting section? | Missing recovery guide for known errors |

## 5. External Coupling

| Question | Problem Indicator |
|----------|----------------------|
| Does it use CLIs without version pinning? (gh, yt-dlp, ffmpeg) | If the CLI changes and the skill has no fallback |
| Do Prerequisites document external dependencies? | If it calls a CLI not listed in prerequisites |

## 6. Testability

| Question | Problem Indicator |
|----------|----------------------|
| Is the output verifiable without an LLM? | If verification requires "ask the user" |
| Is there an associated test_*.py in execution/? | Execution skills should have tests |

## 7. Token Efficiency

| Question | Problem Indicator |
|----------|----------------------|
| Does the skill prompt contain extensive tutorials? | Skills are instructions, not documentation |
| Are compact rules concise? (< 15 lines) | Long rules indicate they should be a separate reference/ |
