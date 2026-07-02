---
model_tier: inherited
name: string-database
description: >
  Query the STRING database for protein-protein interactions (PPIs), functional
  enrichment, and homology. Use when the user asks about interactions between
  specific proteins, interaction evidence, confidence scores, protein
  interaction partners, or pathway enrichments.
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
- Triggers: "string_database", "use string_database"



# STRING Database Skill

This skill allows you to query the STRING database programmatically using a
bundled Python CLI wrapper.

## Prerequisites

1.  **`uv`**: Read the `uv` skill and follow its Setup instructions to ensure
    `uv` is installed and on PATH.
2.  **User Notification**: If LICENSE_NOTIFICATION.txt does not already exist in
    this skill directory then (1) prominently notify the user to check the terms
    at https://string-db.org/cgi/access, then (2) create the file recording the
    notification text and timestamp.

## Core Rules

1.  **MANDATORY: Ask for Species First:** The STRING API requires NCBI Taxon
    IDs. **You MUST NOT guess or assume a species.** If the user does not
    explicitly state a species or Taxon ID, you MUST stop and ask: "Which
    species are you interested in? I need the NCBI Taxon ID to proceed." Even
    for well-known proteins like TP53, BRCA1, or MDM2 that are commonly
    associated with human studies, you MUST still ask — do not default to Human.
2.  **Never print output to stdout:** The `--output <file.tsv>` is required.
    Never read large outputs into context. Instead use jq, python or file
    operations (`grep`, `head`) to process large output.
3.  **Map Identifiers first:** If you only have common gene names (e.g.,
    'TP53'), map them to STRING IDs first as this guarantees much faster server
    responses. Use the `map` command for this.
4.  **Notification**: If this skill is used, ensure this is mentioned in the
    output.

## Tool Execution

The CLI is at `scripts/string_cli.py` and should be run using `uv run`:

```bash
uv run scripts/string_cli.py <command> [options] --output /tmp/out.tsv
```

## Feature Domains (Progressive Disclosure)

Read the following reference files based on the user's request:

*   **[Mapping Identifiers](references/mapping.md)** - Map common protein names
    to STRING IDs.
*   **[Interactions & Network](references/interactions.md)** - Find interacting
    proteins, network topologies, mediators, homology, and visual network
    images.
*   **[Enrichment & Functional Annotations](references/enrichment.md)** -
    Analyze pathway enrichment (GO, KEGG, Pfam), PPI significance, or find all
    proteins associated with a specific term (e.g. Melanoma).
*   **[Values/Ranks Enrichment](references/valuesranks.md)** - Submit full
    experimental datasets (e.g., logFC, p-values) for rank-based enrichment
    analysis using the async background API.

To begin, read the reference file most appropriate to the current task to
discover the correct CLI command.


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash

