---
name: sdd-local-distiller
description: >
  Performs chat distillation via local LLMs (Qwen/LM Studio).
  Trigger: "destilar local", "compresión local", "local distiller".
license: MIT
metadata:
  author: TaoTomate
  generator_model: gemini-1.5-pro
  upstream_source: local_custom_skill
  upstream_date: N/A
  local_sync_date: 2026-06-15
  version: "1.0"
---

## Purpose
Speed up the distillation process and ensure privacy by using local compute instead of cloud-based synthesis.

## Unified Execution Protocol (v3.0)

1. **Delegate to Unified Distiller**: Run the central distillation tool using the local provider:
   `python D:\Engram_SDD\Proj-Distill\distill.py --conversation-id <conversation_id> --topic <topic_name> --force-provider local`
2. **Review Output**: The script will automatically process the conversation in layers, build references, preserve trade-offs, write the markdown file to `C:\Users\user\.gemini\antigravity\knowledge\`, and save it to Engram.
3. **Artifact Creation**: Create a markdown artifact with the full content returned by the script.

## Output Requirements
- **Identity**: Start with `Distilled by: Local LLM via Antigravity`.
- **Absolute Paths**: Mandatory for all file references.
- **Mermaid Diagrams**: Required for architecture visualization.
