# Agent Instructions (Antigravity Industrial Master V4.1)

> This file is the **Source of Truth** for agent behavior. It is mirrored across `CLAUDE.md` and `GEMINI.md`.
> **Hierarchy**: All operational logic is governed by the [VISION.md](file:///c:/Users/user/.gemini/antigravity/playground/midnight-coronal/src/core/VISION.md) Constitution.

You operate within a 3-layer industrial architecture designed for high-precision autonomous work and continuous self-evolution.

---

## 1. The 3-Layer Framework (Sloanismo)

| Layer | Name | Repository | Responsibilities |
| :--- | :--- | :--- | :--- |
| **L1** | **Directive** | `directives/`, `AGENTS.md` | **Intent**: SOPs and living instructions. Must be read and *updated* as you learn. |
| **L2** | **Orchestration** | **AI Agent (You)** | **Decision**: Tool selection, error routing, and **Self-Annealing** (Fix -> Test -> Update). |
| **L3** | **Execution** | `execution/`, `skills/` | **Action**: Deterministic, stateless Python scripts. Must have `test_*.py` for certification. |

---

## 2. Industrial Protocol (V4.1 Master)

### 🛡️ Taylorismo (Strict Validation)
- **Data Contracts**: Before running L3 scripts, verify the associated `schema.py`. Validate all inputs/outputs.
- **Atomic Validation**: Every script or Skill must include a `validate_input` block to fail-fast on corruption.

### 🔄 Self-Annealing 2.0 (The Learning Loop)
When a tool fails or an API constraint is discovered:
1. **Analyze**: Read stack traces and logs in `.tmp/` or `status`.
2. **Patch**: Fix the L3 script (verify Section 3 for financial stops).
3. **Verify**: Run the associated `test_*.py` to ensure the fix is robust.
4. **Evolve**: Update both the L1 `directive/` AND relevant **Knowledge Items (KIs)**.

### 📦 Sloanismo (Isolation & Hygiene)
- **Dynamic Pathing**: No hardcoded paths (`C:\Users...`). Use `pathlib` relative to project root.
- **File Triage**:
    - **Deliverables**: Final user-facing outputs go to Cloud/Drive or `research_reports/`.
    - **Intermediates**: All temp data goes to `.tmp/`. Treat as volatile and non-persistent.
- **McDonaldized Output**: Every L3 process must return a strict JSON line: 
  `{"status": "success/error", "data": {...}, "error_log": "..."}`

---

## 3. Financial & Safety Safeguards (Volvo Quality)

> [!WARNING]
> **Financial Stop**: If an execution involves **PAID** API credits (Vision, Bulk Search, High-Tier LLMs), **YOU MUST ASK** for user confirmation before retrying a failed loop.

- **Check Registry First**: Consult `registry.json` before creating new functionality to avoid **MUDA** (Waste).
- **Idempotency**: Tools must be safe to re-run without duplicating records or corrupting state.

---

## 4. Operational Workflow (Nexus Integrated)

1. **Receive Intent**: Clear user command or task.
2. **Consult Nexus**: Check `registry.json` for tools and **Knowledge Items (KIs)** for context.
3. **Align Directive**: Read relevant `.md` in `directives/`.
4. **Execute & Monitor**: Run L3 tool.
    - *Success*: Return formatted JSON and finalize deliverables.
    - *Fail*: Enter **Self-Annealing** loop (Fix -> Test -> Update Directive & KI).
5. **Finalize**: Clear `.tmp/` and report status via JSON.

### 🧹 Industrial Hygiene (Maintenance)
- **Proactive Janitoring**: During idle periods or at the start of a session, run the `system-janitor` skill (1-2 times daily) to ensure path integrity and registry consistency.
    - Command: `python d:\Antigravity\skills\system_janitor\scripts\main.py status`

---

## 5. Hardware & Logic Compliance (General Laws)

> [!IMPORTANT]
> Failure to follow these rules is considered **MUDA** (Waste).

- **Hardware Acceleration First**: Always use GPU/CUDA or any available hardware/software acceleration for AI-intensive tasks (Stable Diffusion, Vision, LLMs). Never fallback to slow CPU processing without explicit user authorization.
- **Strict Plan Adherence**: All specifics defined in the **L2 Orchestration Plane** (e.g., `implementation_plan.md`) must be mirrored exactly in the **L3 Execution Checklist** (`task.md`).
- **Data Integrity**: All data tags and metadata must be normalized as per project-specific requirements before starting execution.
- **Transparency**: Technical roadmaps (`task.md`) must reflect the full granularity of the implementation plan. Simplification is prohibited.

---
**Standard Operating Procedure V4.1 finalized.** Operates under the Authority of the Antigravity Constitution.
