---
name: conversation-distillation
description: 'Performs high-level technical distillation (Senior Architect mode),
  prioritizing the "What" and the "Why". Filters technical noise and back-and-forth,
  consolidating only the final decisions and their architectural rationale. Trigger:
  "distill thread", "technical distillation", "extract context", "create dossier".
  '
version: "3.1"
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: conversation-distillation/SKILL.md
model_tier: high
---

## Context & Triggers
**When to use this skill:**
- When the user asks to distill, summarize, or create an architectural dossier of the current conversation.
- Triggers: "distill thread", "technical distillation", "extract context", "create dossier".


## Execution Phases


### 1. Diagnosis Phase
- Identify the `<topic_name>` to distill based on the conversation, or ask the user if not obvious.
- Extract the main intent ("Why"): the dossier MUST focus on the original purpose.

### 2. Action Phase
- **Delegate to Unified Distiller**: Execute the central distillation tool:
  ```bash
  python D:\Engram_SDD\Proj-Distill\distill.py --conversation-id <conversation_id> --topic <topic_name>
  ```
- The script will automatically process the conversation in layers, build references, preserve trade-offs, and write the file to `~\.gemini\antigravity\knowledge\`, also persisting it to Engram.

### 3. Verification Phase
- Read the output or review the generated markdown file.
- **Artifact Creation**: Create a markdown artifact (`.md`) to present the script's returned content to the user so they can review and validate it.

## Guardrails (Critical Rules)
- **Philosophy - Intent over Noise:** Do not list mechanical changes, but explain decisions and trade-offs ("X was chosen because Y"). Discard debugging back-and-forth.
- **For Future Self:** The content must be written assuming someone will pick up the project in 6 months without needing to re-read the original chat.
- **Output Identity:** The artifact must start with `Distilled by: Cloud LLM via Antigravity`.
- **Absolute Paths:** Referenced file paths must ALWAYS be absolute.
- **Mermaid Diagrams:** Required for visualizing architecture decisions within the dossier.

## Data Structures / Examples & Commands

**Execution Command:**
```bash
python D:\Engram_SDD\Proj-Distill\distill.py --conversation-id <conversation_id> --topic <topic_name>
```

## ⚠️ Migration Residue (Evolution Feedback)
*(Successfully migrated from v2.0 to IaC v1.2, keeping the "Noise Cancellation" and "Purpose First" philosophies intact)*

## Troubleshooting

- **`distill.py` not found**: The referenced script no longer exists in the repository. Either restore it or update the skill to use the Synapse skill or an alternative distillation method.
- **No conversation ID available**: Ask the user explicitly for the conversation ID or session reference.
- **Output file not generated**: Check stderr output from the script. Verify the topic name is valid and the conversation ID is correct.
