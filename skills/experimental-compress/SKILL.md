---
name: experimental-compress
description: 'Synapse Distillation Engine (replaces Proj-Distill). Multi-topic, BTW-aware,
  async map/reduce with free cloud tier support. Backends: ollama, lm-studio, groq, gemini.
  Triggers: "prueba compress", "distill experimental", "telemetria de destilacion".
  '
version: "4.1"
author: TaoTomate
generator_model: gemini-2.0-flash
inherited_from: experimental-compress/SKILL.md
migrated_by: synapse-engine
model_tier: fast
---

## Context & Triggers
**When to use this skill:**
- When the user asks to view the progress of chunks processed in the background (`'status'`).
- When the SOTA Sync Point needs to be injected into the current thread (`'reduce'` or `'map' + 'reduce'`).
- Triggers: "prueba compress", "distill experimental", "telemetria de destilacion".


## Execution Phases


### 1. Diagnosis Phase
- Identify the user's intent: Status Check (`status`), Map Extraction (`map`), or Dossier Synthesis (`reduce`).

### 2. Action Phase
- **If Status Check (Telemetry):**
  - Execute the `status` command (see Commands section).
- **If Map Extraction:**
  - Run `map` to extract claims from the thread. Claims are grouped by topic automatically (BTW detection built-in).
  - Supports `--max-chunks` for quick partial mapping.
  - Supports `--backend groq` for fast cloud extraction.
- **If Dossier Synthesis:**
  - Run `reduce` to generate the consolidated dossier from previously mapped claims.
  - Optionally use `--inject-root` to write the dossier to the thread root (visible in Antigravity UI).

### 3. Verification Phase
- **For Status Check:** Read the console stdout and display the report of processed threads, topics, claims, and pending lines.
- **For SOTA Injection:** The `reduce` command returns JSON. Extract the `summary` field (the dossier markdown). Output the *exact* content of that `summary` into the chat immediately.

## Guardrails (Critical Rules)
- **ALWAYS** use the actual chat ID when replacing `<conversation_id>`.
- **NEVER** summarize or hide in an artifact the content of the `summary` returned in `reduce` mode. You must print it exactly as it comes.
- **ALWAYS** execute `reduce` after `map` for complete dossiers.

## Data Structures / Examples & Commands

### Execution Commands

**Status Check (Telemetry):**
```bash
python D:\Engram_SDD\Proj-Synapse\src\cli.py status
```

**Map Extraction (Default - local Ollama):**
```bash
python D:\Engram_SDD\Proj-Synapse\src\cli.py map --thread-id <conversation_id>
```

**Map Extraction (Fast - Groq free tier):**
```bash
python D:\Engram_SDD\Proj-Synapse\src\cli.py map --backend groq --thread-id <conversation_id>
```

**Map Extraction (Partial - first 5 chunks):**
```bash
python D:\Engram_SDD\Proj-Synapse\src\cli.py map --max-chunks 5 --thread-id <conversation_id>
```

**Dossier Synthesis (Default):**
```bash
python D:\Engram_SDD\Proj-Synapse\src\cli.py reduce --thread-id <conversation_id>
```

**Dossier Synthesis (Injected to thread root for UI visibility):**
```bash
python D:\Engram_SDD\Proj-Synapse\src\cli.py reduce --inject-root --thread-id <conversation_id>
```

**Dossier Synthesis (Fast - Groq):**
```bash
python D:\Engram_SDD\Proj-Synapse\src\cli.py reduce --backend groq --thread-id <conversation_id>
```

### Backend Options
| Backend | Flag | Speed | Cost |
|---------|------|-------|------|
| Ollama (local) | `--backend ollama` | Slow | Free |
| LM Studio (local) | `--backend lm-studio` | Medium | Free |
| Groq (cloud) | `--backend groq` | Fast | Free tier |
| Gemini (cloud) | `--backend gemini` | Fast | Free tier |

## Migration Notes
- Replaces the old `Proj-Distill/distill_experimental.py` script.
- Key improvements: multi-topic detection (BTW-aware), cross-thread synthesis, typed claims with relations, portable paths (no hardcoded `C:\Users\user\...`), multiple LLM backends.
- State is stored in `~/.gemini/antigravity/knowledge/synapse_state_<thread_id>.json`.
- Dossiers are written to `~/.gemini/antigravity/knowledge/` by default.

## Troubleshooting

- **Backend not responding**: Verify the backend is running (`ollama list` for local, check API key for cloud). Use a different backend with `--backend`.
- **Thread not found**: Confirm the thread ID or path is correct. The engine expects valid conversation files in the brain directory.
- **Empty output**: The input may have no detectable topics. Check the thread content length and quality.
- **Quality gate failed**: Review the output claims — they may lack supporting evidence or relations. Re-run with more specific focus.
