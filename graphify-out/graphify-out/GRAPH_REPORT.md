# Graph Report - D:\TaoTomate.Dots\agent-config-core  (2026-07-02)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 98 nodes · 162 edges · 15 communities (9 shown, 6 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bd110126`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Agent Orchestration Persistence Modes|Agent Orchestration Persistence Modes]]
- [[_COMMUNITY_SDD Skills Workflow Protocol|SDD Skills Workflow Protocol]]
- [[_COMMUNITY_Skill Markdown Parsing Utilities|Skill Markdown Parsing Utilities]]
- [[_COMMUNITY_Agent Governance Error Handling|Agent Governance Error Handling]]
- [[_COMMUNITY_Agent Config Entry Points|Agent Config Entry Points]]
- [[_COMMUNITY_Skill Registry Audit Framework|Skill Registry Audit Framework]]
- [[_COMMUNITY_Skill Registry Generation Scripts|Skill Registry Generation Scripts]]
- [[_COMMUNITY_Skill Catalog Reporting Tool|Skill Catalog Reporting Tool]]
- [[_COMMUNITY_Skill Audit Validation|Skill Audit Validation]]
- [[_COMMUNITY_File Content Hashing|File Content Hashing]]
- [[_COMMUNITY_Duplicate Skill Detection|Duplicate Skill Detection]]
- [[_COMMUNITY_Skill Recommendations Generator|Skill Recommendations Generator]]
- [[_COMMUNITY_Distillation Protocol|Distillation Protocol]]
- [[_COMMUNITY_Agent Trigger Rules|Agent Trigger Rules]]
- [[_COMMUNITY_Skill Registry Management|Skill Registry Management]]

## God Nodes (most connected - your core abstractions)
1. `Agent Base Instructions` - 20 edges
2. `README - Agent Config` - 19 edges
3. `SDD Workflow Concept` - 12 edges
4. `main()` - 11 edges
5. `scan_directory()` - 10 edges
6. `Governance Protocol` - 10 edges
7. `Changelog` - 8 edges
8. `parse_frontmatter()` - 7 edges
9. `Persistence Contract` - 7 edges
10. `SDD Phase Common Protocol` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Agent Base Instructions` --references--> `skill_catalog.py Tool`  [EXTRACTED]
  agents/base.md → tools/skill_catalog.py
- `README - Agent Config` --references--> `skill_catalog.py Tool`  [EXTRACTED]
  README.md → tools/skill_catalog.py
- `AGENTS.md Entry Point` --references--> `Agent Base Instructions`  [EXTRACTED]
  AGENTS.md → agents/base.md
- `Governance Protocol` --references--> `Auditor Skill`  [EXTRACTED]
  .config/GOVERNANCE_PROTOCOL.md → skills/auditor/SKILL.md
- `Skill Registry` --references--> `skill_catalog.py Tool`  [EXTRACTED]
  .config/skill-registry.md → tools/skill_catalog.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **SDD Persistence Modes (engram / openspec / hybrid / none)** — concept_engram_mode, concept_openspec_mode, concept_hybrid_mode, shared_persistence_contract [EXTRACTED 1.00]
- **SDD Phase Pipeline Skills** — shared_openspec_convention, shared_persistence_contract, shared_sdd_phase_common, concept_sdd_pipeline, concept_return_envelope [EXTRACTED 0.90]
- **Orchestrator Skill Injection Flow** — shared_skill_resolver, concept_skill_registry, concept_compact_rules, concept_l1_orchestrator, shared_sdd_phase_common [EXTRACTED 0.90]
- **Agent Entry Points Loading base.md** — agents_md, claude_md, gemini_md, agents_base_md [EXTRACTED 1.00]
- **SDD Phase Skill Set** — skills_sdd_init_skill_sdd_init, skills_sdd_explore_skill_sdd_explore, skills_sdd_propose_skill_sdd_propose, skills_sdd_spec_skill_sdd_spec, skills_sdd_design_skill_sdd_design, skills_sdd_tasks_skill_sdd_tasks, skills_sdd_apply_skill_sdd_apply, skills_sdd_verify_skill_sdd_verify, skills_sdd_archive_skill_sdd_archive, skills_sdd_onboard_skill_sdd_onboard, concept_sdd_workflow [EXTRACTED 1.00]
- **Failure Handling Flow** — concept_failure_protocol, config_governance_protocol_md, config_error_log_md, shared_errors_learned_md, skills_auditor_skill_auditor [EXTRACTED 0.95]

## Communities (15 total, 6 thin omitted)

### Community 0 - "Agent Orchestration Persistence Modes"
Cohesion: 0.17
Nodes (21): Agent Context Isolation (Cross-session Amnesia), Compact Rules (Skill Injection), Engram Persistence Mode, Gatekeeper (Skill Routing Enforcer), Helpful vs Compliant Bias (RLHF), Hybrid Persistence Mode, L1 Orchestrator, L2 Orchestration Layer (+13 more)

### Community 1 - "SDD Skills Workflow Protocol"
Cohesion: 0.15
Nodes (13): Engram Memory Protocol, SDD Workflow Concept, Engram Artifact Convention, SDD Apply Skill, SDD Archive Skill, SDD Design Skill, SDD Explore Skill, SDD Init Skill (+5 more)

### Community 2 - "Skill Markdown Parsing Utilities"
Cohesion: 0.25
Nodes (11): Any, extract_description(), extract_skill_name(), extract_version(), parse_frontmatter(), Extract YAML frontmatter from a markdown file., Get skill name from frontmatter or fall back to parent directory name., Get version from frontmatter. (+3 more)

### Community 3 - "Agent Governance Error Handling"
Cohesion: 0.39
Nodes (9): Antigravity Agent Wrapper, Agent Base Instructions, Failure Protocol / Black Box, Error Log, Governance Protocol, Errors Learned Log, Model Routing, Go Testing Skill (+1 more)

### Community 4 - "Agent Config Entry Points"
Cohesion: 0.32
Nodes (8): Claude Code Agent Wrapper, Gemini CLI Agent Wrapper, AGENTS.md Entry Point, CLAUDE.md Entry Point, GEMINI.md Entry Point, README - Agent Config, OpenSpec Convention, VISION.md Philosophy

### Community 5 - "Skill Registry Audit Framework"
Cohesion: 0.29
Nodes (8): Changelog, 7 Audit Axioms, Skill Registry, Audit Framework, Skill Style Guide, Trigger Rules, Skill Optimizer Skill, skill_catalog.py Tool

### Community 6 - "Skill Registry Generation Scripts"
Cohesion: 0.36
Nodes (8): Path, archive_duplicates(), generate_registry(), identify_active(), main(), Mark skills that live in the active agent-config directories., Move non-active duplicate skill directories to .skill-archive/., Generate skill-registry.md from scanned skills.

### Community 7 - "Skill Catalog Reporting Tool"
Cohesion: 0.29
Nodes (6): build_version_map(), print_json(), print_report(), Map skill name → list of all found versions across locations., Print human-readable markdown report., Print machine-readable JSON output.

### Community 8 - "Skill Audit Validation"
Cohesion: 0.50
Nodes (4): Skill Audit Report, Skill Template, Validation Framework, Auditor Skill

## Knowledge Gaps
- **23 isolated node(s):** `Agent Trigger Rules`, `Validation Framework`, `L2 Orchestration Layer`, `L3 Execution Layer`, `resolve_model.py (Model Tier Resolution)` (+18 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `README - Agent Config` connect `Agent Config Entry Points` to `Agent Orchestration Persistence Modes`, `SDD Skills Workflow Protocol`, `Agent Governance Error Handling`, `Skill Registry Audit Framework`, `Skill Audit Validation`?**
  _High betweenness centrality (0.219) - this node is a cross-community bridge._
- **Why does `Persistence Contract` connect `Agent Orchestration Persistence Modes` to `Agent Config Entry Points`?**
  _High betweenness centrality (0.168) - this node is a cross-community bridge._
- **Why does `Agent Base Instructions` connect `Agent Governance Error Handling` to `SDD Skills Workflow Protocol`, `Agent Config Entry Points`, `Skill Registry Audit Framework`?**
  _High betweenness centrality (0.140) - this node is a cross-community bridge._
- **What connects `Extract YAML frontmatter from a markdown file.`, `SHA-256 hash of the file content (normalized: strip trailing whitespace per line`, `Get skill name from frontmatter or fall back to parent directory name.` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._