---
name: glossary-extractor
description: Specialized process for technical vocabulary extraction, architecture
  jargon, and methodological concepts. Generates MOC files for Obsidian.
version: 1.0.0
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: glossary-extractor/SKILL.md
migrated_by: skill-migrator@1.0.0
model_tier: medium
---

## Context & Triggers
**When to use this skill:**
- On-demand invocation or when discussing methodological and technical architecture concepts.
- When generating MOC (Map of Content) files for Obsidian with hidden JSON metadata.

## Prerequisites
- [ ] The target path must exist: `D:\Voveda\20_Atlas\21_MOCs`.

## Execution Phases

> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase. 
> Instead, the agent will print the exact payload (JSON, code block, or parameters) it planned to execute, and will stop to wait for explicit human approval.

### 1. Diagnosis Phase
- Apply MAXIMUM RECALL strategy: Identify infrastructure tools (APIs, libraries, e.g. TypeScript, Obsidian API), methodology (patterns like MOC, Atomic Notes), and underlying theory.
- If in doubt about a term's simplicity, **INCLUDE IT**. Recall density has priority.
- Alias Unification: Check if different terms mean the same thing to consolidate them using the `aliases` field.

### 2. Action Phase
- Generate the glossary content in Markdown following the Zettelkasten MOC schema.
- The BODY must contain a list of `[[Term Name]]`: Brief definition.
- Embed the hidden JSON block at the end of the file for automated processing.

### 3. Verification Phase
- Save the file to `D:\Voveda\20_Atlas\21_MOCs` with the correct naming convention: `Glossary_[Project/Topic]_[YYYY-MM-DD]_[HHMM].md`.

## Guardrails (Critical Rules)
- **DO NOT** infantilize definitions, always maintain high technical rigor.
- **DO NOT** ignore "simple" infrastructure terms (e.g. API names or base languages).
- **ALWAYS** use the HHMM timestamp in the filename to avoid collisions.
- **NEVER** alter the "title", "content", or "aliases" keys of the structured JSON block.

## Data Structures / Examples & Commands

### Hidden JSON Structure for Obsidian
The generated file must end with this hidden block (wrapped in Obsidian `%%` comments):

```html
%%
JSON_GLOSSARY_START
[
  {
    "title": "Term Name",
    "content": "Dense, technical, and precise definition (no infantilization).",
    "aliases": ["synonym1", "synonym2"],
    "tags": ["#architecture", "#workflow"]
  }
]
JSON_GLOSSARY_END
%%
```

## ⚠️ Migration Residue (Evolution Feedback)
*(All information has been successfully mapped)*
