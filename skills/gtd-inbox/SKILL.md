---
name: gtd-inbox
description: "GTD Inbox processor — SQLite-based personal inbox for importing, classifying, and organizing tasks from WhatsApp, Telegram, bookmarks, and raw files. Covers the Proj-GTD-CSV project workflow."
version: 1.0.0
author: Hermes Agent
model_tier: medium
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [GTD, inbox, classification, sqlite, personal-productivity]
    related_skills: []
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
- Triggers: "gtd-inbox", "use gtd-inbox"



# GTD Inbox Processor

Manage a personal Getting-Things-Done inbox backed by SQLite. Items arrive from multiple sources (WhatsApp chats, Telegram, bookmarks, manual files), get classified by keyword-matching rules, and accumulate in a central inbox for review.


## Prerequisites
- [ ] Read access to target files/directories
- [ ] Write access for auto-fix operations


## Project Location

`D:\Engram_SDD\Proj-GTD-CSV\`

## Architecture

| File | Role |
|------|------|
| `gtd.py` | CLI entry point — all subcommands |
| `db.py` | SQLite connection, schema, queries |
| `schema.sql` | Database schema (items, classification_rules, projects) |
| `ingest.py` | File ingestion + archiving |
| `parsers/whatsapp.py` | WhatsApp chat export parser |
| `parsers/telegram.py` | Telegram export parser |
| `parsers/bookmarks.py` | Bookmark file parser |
| `training.py` | Interactive classification (review + label) |
| `refine.py` | Iterative refinement: auto-classify + review weakest |
| `classifier.py` | Keyword-based classification engine |
| `archive/` | Processed source files moved here |
| `inbox/` | Drop zone for new files to process |

## Commands

```bash
cd D:\Engram_SDD\Proj-GTD-CSV

# Ingest files into inbox
python gtd.py ingest --inbox                    # process all files in inbox/
python gtd.py ingest path/to/file.txt           # specific file
python gtd.py ingest --inbox --keep-source      # don't archive after import

# Classify items
python gtd.py classify                         # interactive (default batch=20)
python gtd.py classify --batch 50

# Refine (auto-classify + review weakest)
python gtd.py refine
python gtd.py refine --batch 100

# List items
python gtd.py list                              # latest classified
python gtd.py list --unclassified               # unclassified only
python gtd.py list --unclassified --limit 50

# Stats
python gtd.py stats

# Export learned rules
python gtd.py export-rules
```

## Workflow

### 1. Ingest
Drop source files into `inbox/` or run `ingest` with specific paths. Files are parsed, content extracted as individual items, and inserted into SQLite. Source files are moved to `archive/` (unless `--keep-source`).

### 2. Classify
Run `classify` to interactively review unclassified items. The classifier suggests categories based on learned rules; the user confirms or corrects.

### 3. Refine
Run `refine` for batch processing: auto-classifies everything possible, then reviews the weakest classifications for manual confirmation.

### 4. Review
Use `list --unclassified` to see pending items and `stats` to track progress.

## Categories

| Category | Meaning |
|----------|---------|
| `next_action` | Concrete next step to take |
| `reference` | Information to keep for later |
| `someday_maybe` | Ideas / maybe later |
| `ambiguous` | Needs manual review — can't auto-classify |

## Database Schema (summary)

- **items** — id, content, source, category, project_name, created_at, classified_at
- **classification_rules** — keyword, category, weight, hits (learned from training)
- **projects** — extracted project names from items

## Pitfalls

- Always run from the project directory (`D:\Engram_SDD\Proj-GTD-CSV\`) — `db.py` resolves the DB relative to CWD.
- The `inbox/` directory may not exist by default; create it if needed before `--inbox`.
- `archive/` subdirectories are named by source (e.g., `2026-06-24-WhatsApp Chat - INBOX GTD 🧰⏳⚡🔝/`).
- Stats show classified vs unclassified counts — if unclassified grows large, run `refine --batch 200`.
- `export-rules` is useful to understand what the classifier has learned and debug misclassifications.

## Verification

```bash
cd D:\Engram_SDD\Proj-GTD-CSV
python gtd.py stats
# Should show total/classified/unclassified counts
```


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash

