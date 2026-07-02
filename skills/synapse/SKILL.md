---
name: synapse
description: 'Synapse Distillation Engine. Multi-topic, async map/reduce with quality gates. Backends: ollama, lm-studio, groq, gemini, agent. Triggers: "synapse", "distill experimental", "prueba compress", "destilar hilo", "extraer temas", "crear dossier", "procesar hilos".'
version: "1.1"
author: TaoTomate
model_tier: fast
---

## Context & Triggers

**When to use this skill:**
- When the user wants to distill conversation threads into structured knowledge
- When the user requests topic extraction, claims analysis, or dossier generation
- When processing single or multiple threads from the Antigravity brain
- When comparing against legacy distill results


## Execution Phases

> **[UNIVERSAL DRY-RUN RULE]**
> If the user requests `--dry-run`, print the dossier without saving. Do not call `ingest`.

> **[QUALITY GATE — INTERNALIZED]**
> You MUST read at least chunk 0 of a thread's content before writing claims.
> Each claim's `source_text` MUST be verifiable against actual chunk content.
> Generating claims from 80-char previews is PROHIBITED — it produces false dossiers.
> If you cannot read the chunks (context limit), ask the user to batch in smaller groups.

> **[OUTPUT LANGUAGE RULE]**
> Extraction and synthesis MUST use the same language as the input thread content.
> If the thread is in Spanish, ALL output (claims, topics, dossiers) is in Spanish.
> If the thread mixes languages, use the predominant one.

### 1. Diagnosis Phase

Determine user intent:
- **Single thread**: `synapse task --thread-id <id> --max-chunks N`
- **Multiple threads**: `synapse task --max-threads N --max-chunks N`
- **Status check**: `synapse status`
- **Cross-thread synthesis**: `synapse synthesize --thread-ids <ids>`

Confirm with user:
- How many chunks per thread? (default 3, max 5 for quality)
- How many threads per batch? (default 5 for single-agent, 10 for batches)
- Language preference? (if input is mixed)

### 2. Explore Phase (READ CHUNKS — MANDATORY)

**THIS PHASE IS NOT OPTIONAL. SKIPPING IT VIOLATES THE QUALITY GATE.**

For each thread:
1. Export chunks: `synapse task --thread-id <id> --max-chunks N --output tmp/task.json`
2. Read chunk 0 content from `task.json["extraction"][0]["prompt"]`
3. Identify the user's intent, key discussion points, and conversation flow
4. If N > 1, read remaining chunks sequentially to capture full arc

For batch processing:
1. Export: `synapse task --max-threads N --max-chunks N --output tmp/batch.json`
2. For EACH thread in `batch.json["threads"]`:
   - Read chunk 0 (user's first request) to identify the topic
   - If the chunk has meaningful content, read chunk 1 for depth
   - Do NOT skip threads because "they look similar" or "the preview is short"

### 3. — Phase renamed: Extract Phase (build extraction_results)

After reading the chunks, build `extraction_results`:

```python
extractions = [
    {
        "chunk_id": 0,
        "topic": "Specific Topic Name",  # NOT generic — must reflect actual content
        "claims": [
            {
                "id": "c1_0",
                "content": "Claim text that captures a real point from the conversation",
                "type": "fact|insight|intent|problem|bug|rule|attack|defense",
                "confidence": 0.0-1.0,
                "source_text": "Verbatim or close match FROM THE CHUNK"
            }
        ],
        "relations": [  # optional — for cross-claim relationships
            {
                "id": "r1",
                "source_id": "c1_0",
                "target_id": "c1_1",
                "type": "supports|contradicts|extends|refines",
                "weight": 0.0-1.0,
                "reasoning": "Why these claims relate"
            }
        ]
    },
    ...  # one entry per topic per chunk
]
```

**Validations (mandatory before persisting):**
- `source_text` MUST be a plausible substring or close paraphrase of actual chunk text
- `topic` names must be specific (NOT "General Capabilities", NOT "System Audit" for a jailbreak attempt)
- `type` must be honest — label prompt injection attempts as "attack", not "fact"

### 4. Synthesize Phase (generate dossiers)

For EACH topic, write a full 7-section dossier:

```markdown
### 1. Context & Intent (or Contexto e Intencion)
What is this about? Why did the user bring it up?

### 2. Architecture / Decisions (or Arquitectura / Decisiones)
What decisions were made? What trade-offs discussed?

### 3. Open Topics (or Temas Abiertos)
Questions left unanswered, decisions deferred, unresolved issues, or blocked items.

### 4. Critical Paths (or Caminos Criticos)
Key evidence, findings, blockers, or action items.

### 5. ToDo List (or Lista de Tareas)
Concrete, actionable tasks extracted from the conversation — ordered by priority.

### 6. Visualization (or Visualizacion)
```mermaid
flowchart LR/TD
  ...  # diagram showing relationships
```

### 7. Implementation Hooks (or Hooks de Implementacion)
Actionable next steps, code changes, config updates.
```

Include `synthesis_results` with the 7-section markdown per topic.

### 5. Persist Phase (ingest)

```bash
synapse ingest --input result.json
# or for preview:
synapse ingest --input result.json --dry-run
```

### 6. Audit Phase (quality check)

After ingest, verify:
1. Open the generated dossier file
2. Spot-check 2-3 claims: does the source_text appear in the actual conversation?
3. Is the language consistent? (Spanish thread → Spanish dossier?)
4. Are the topics specific enough to be useful for retrieval?

If quality fails ANY check, delete the dossier, fix the extraction, and re-ingest.

### Quality Decision Tree

```
Is this a single thread or batch?
  ├─ Single: Explore → Extract → Synthesize → Review → Ingest → Audit
  └─ Batch: 
      ├─ Can read ALL chunks? → Full quality per thread
      └─ Context too small for all? → 
          ├─ Reduce batch size (5 threads max) → Full quality
          └─ Ask user: "¿prefieres calidad en pocos o cantidad con previews?"
```

## Guardrails (Reglas Críticas)

1. **NEVER** generate claims without reading at least chunk 0 of the thread.
2. **NEVER** use `status` previews (80 chars) as claim source_text.
3. **NEVER** write a dossier with `fallback_synthesize` (auto-generated from claims only) — always provide `synthesis_results`.
4. **NEVER** translate thread language — if the thread is in Spanish, the dossier is in Spanish.
5. **ALWAYS** validate that `source_text` matches actual chunk content (the `--validate` flag on ingest checks this automatically).
6. **ALWAYS** ask the user before processing batches larger than 10 threads.
7. **IF** you catch yourself about to shortcut quality for speed — STOP. Ask the user how to proceed.

## Validation Hook (in ingest command)

The `--validate` flag checks:
- For each claim, search `source_text` in the chunk content
- If > 50% of claims have no match, REJECT the result
- Report mismatches to the user

Added in `_cmd_ingest`:
```python
if args.validate:
    mismatches = []
    for er in extractions:
        chunk_text = task_chunks.get(er.get("chunk_id", 0), "")
        for c in er.get("claims", []):
            st = c.get("source_text", "")
            if st and st not in chunk_text and not _is_reasonable_paraphrase(st, chunk_text):
                mismatches.append({"claim": c["content"], "source_text": st})
    if mismatches and len(mismatches) > len(all_claims) * 0.5:
        print(json.dumps({"status": "rejected", "mismatches": mismatches}))
        return
```

## Data Structures / Examples & Commands

### Quick Reference

```bash
# Status
cd Proj-Synapse && synapse status

# Single thread with quality
synapse task --thread-id <id> --max-chunks 3 --output task.json
# [Read chunks, extract claims, write result.json]
synapse ingest --input result.json

# Batch with quality (small batches!)
synapse task --max-threads 5 --max-chunks 2 --output batch.json
# [Read each thread's chunks, extract, write result per thread]
synapse ingest --input result_t1.json
synapse ingest --input result_t2.json  # ... one by one

# Cross-thread synthesis
synapse synthesize --thread-ids <id1>,<id2> --output cross.json
# [Process cross-thread patterns, write cross_result.json]
synapse ingest --input cross_result.json --thread-id synthetic
```

### Directory Structure

```
skills/synapse/
├── SKILL.md              # This file
└── references/
    └── cli-commands.md   # Optional: CLI reference

Proj-Synapse/
├── src/
│   ├── cli.py            # Command-line interface
│   ├── reader.py         # Thread reader
│   ├── chunker.py        # Text chunker
│   ├── mapper.py         # Claim extraction (API backend)
│   ├── reducer.py        # Topic graph builder
│   ├── synthesizer.py    # Dossier synthesis (API backend)
│   ├── exporters.py      # File exporters
│   └── models.py         # Data models
├── tests/
└── README.md
```

## Troubleshooting

- **Backend not found**: Verify the backend is installed and running (`ollama list` for local, check API keys for cloud).
- **Empty dossier**: The input threads may lack sufficient conversational depth. Try with longer threads or multiple threads.
- **Quality gate rejects output**: Re-run with `--mode deep` or provide more specific focus. The output may lack supporting evidence for the claims.
- **Python dependency missing**: Run `pip install -r requirements.txt` in the synapse skill directory.
- **Memory not persisting**: Check that `engram` MCP is available. If not, dossiers are still written to disk as fallback.
