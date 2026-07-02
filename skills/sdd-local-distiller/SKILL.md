---
name: sdd-local-distiller
description: 'Performs chat distillation via local LLMs (Qwen/LM Studio). Trigger:
  "destilar local", "compresión local", "local distiller".

  '
license: MIT
version: "1.1"
author: gentleman-programming
model_tier: fast
---

## Purpose
Speed up the distillation process and ensure privacy by using local compute instead of cloud-based synthesis.

> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase.
> Instead, the agent will print the exact payload (JSON, code block, or parameters) it planned to execute, and will wait for explicit human approval.

## Unified Execution Protocol (v3.0)

1. **Delegate to Unified Distiller**: Run the central distillation tool using the local provider:
   `python D:\Engram_SDD\Proj-Distill\distill.py --conversation-id <conversation_id> --topic <topic_name> --force-provider local`
2. **Review Output**: The script will automatically process the conversation in layers, build references, preserve trade-offs, write the markdown file to `~\.gemini\antigravity\knowledge\`, and save it to Engram.
3. **Artifact Creation**: Create a markdown artifact with the full content returned by the script.

## Output Requirements
- **Identity**: Start with `Distilled by: Local LLM via Antigravity`.
- **Absolute Paths**: Mandatory for all file references.
- **Mermaid Diagrams**: Required for architecture visualization.

## Guardrails (Critical Rules)

- NEVER use cloud-based LLMs for distillation when this skill is invoked — always use `--force-provider local`.
- ALWAYS create a markdown artifact with the full script output for user review.
- If `distill.py` is not found or fails, report the error — do not attempt inline distillation.

## Troubleshooting

- **`distill.py` not found**: The referenced script (`Proj-Distill/distill.py`) may have been removed. Use the Synapse skill or an alternative distillation method.
- **Local model unreachable**: Verify LM Studio or Ollama is running on the expected port.
- **Empty output**: The conversation may be too short or lack extractable structure.
