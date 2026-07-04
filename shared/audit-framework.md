---
author: TaoTomate
generator_model: mimo-auto
version: 1.0.0
inherited_from: custom — derived from first-principles analysis of agent configuration systems
---

# Audit Framework — First-Principles Agent Configuration Auditor

## Purpose

A domain-agnostic framework for auditing any agent configuration system (AGENTS.md, shared conventions, skills, SDD artifacts, or any future structure). Two layers: axioms define what "valid" means; premises define what must be true for rules to hold.

## Level 0 — Purpose (the invariant question)

Before auditing, answer: **What is the purpose of this system?**

The question never changes. The answer does — it shifts with project, moment, and environment. The answer calibrates which axioms matter most and what thresholds to apply.

```
Same question, different contexts:

"What is the purpose of AGENTS.md?"
  → "Give an agent identity and behavioral rules"
  → "Orchestrate an SDD pipeline with persistence"
  → "Coordinate multiple models with cross-session memory"

Each answer reweights the axioms differently.
```

The purpose is NOT an axiom. It is the lens through which axioms are evaluated. Without it, the audit produces technically correct but irrelevant findings.

---

## Layer 1 — Axioms (7)

Seven necessary conditions for a valid system. Organized by scope: internal, external, and bridge (crosses both).

A system satisfying all seven has no coverage holes. This does NOT guarantee optimality — it guarantees completeness of the validity space. Optimality additionally requires proportionality to context, which changes over time.

### Internal Axioms (toward inside)

Properties of the system's own structure.

| Axiom | Definition | Violation example |
|--------|-----------|-------------------|
| **Consistency** | No part contradicts another part | Rule A says "always X", Rule B says "never X" |
| **Economy** | Every component exists for a provable reason; no waste | Unused rules, premature abstractions, instructions the agent ignores |
| **Traceability** | Every effect has a traceable cause; every artifact has an owner | Anonymous decisions, orphaned files, "who wrote this?" |

### External Axioms (toward outside)

Properties of the system's relationship with its environment.

| Axiom | Definition | Violation example |
|--------|-----------|-------------------|
| **Correctness** | The system does what it claims to do | Rules say "enforce TDD" but no test runner is configured |
| **Completeness** | Everything required exists and is reachable | Referenced file doesn't exist, missing fallback path |
| **Degradability** | Partial failure does not collapse the whole | Engram down → entire SDD pipeline breaks |

### Bridge Axiom (crosses both)

| Axiom | Definition | Violation example |
|--------|-----------|-------------------|
| **Evolvability** | The system adapts to environmental change without breaking internal or external contracts | Skills reference models that no longer exist; rules designed for a stack the project no longer uses |

### Internal/External Pairing Pattern

```
Internal (toward inside)        External (toward outside)
─────────────────────────────   ─────────────────────────────
Consistency                ↔    Correctness
Economy                    ↔    Completeness
Traceability               ↔    Degradability
```

The bridge axiom (Evolvability) monitors that internal properties stay aligned with external reality as both change over time.

### Proportionality (not an axiom — a measurement)

A system can satisfy all seven axioms and still be suboptimal or over-optimized. Proportionality measures whether the system's complexity matches its context:

```
All axioms satisfied + proportionality = optimal
All axioms satisfied - proportionality = suboptimal or over-optimized
```

Proportionality is context-dependent and time-dependent. It cannot be a fixed axiom because what's "proportional" changes. It is evaluated by the auditor after the seven axioms pass.

---

## Layer 2 — Premises (12)

Operational rules derived from axioms. Each premise expresses one axiom in actionable language. These are what an auditor actually checks.

### Derived from Internal Axioms

| # | Premise | Derived from | Question |
|---|---------|-------------|----------|
| P1 | **Every node has a single owner** | Traceability | Who is the authoritative source of each piece of information? |
| P3 | **No information lives in two sites** | Consistency, Economy | Is the same truth duplicated or referenced? |
| P4 | **Every instruction is executable** | Traceability | Can the agent actually comply, or is it wishful thinking? |
| P5 | **Every component has a provable reason to exist** | Economy | Does each line, rule, or section earn its place? |
| P6 | **Dependencies point downward** | Economy | Does the orchestrator reference, or reimplement? |

### Derived from External Axioms

| # | Premise | Derived from | Question |
|---|---------|-------------|----------|
| P2 | **Every reference must resolve** | Completeness | Does each invoked thing exist and is it accessible? |
| P7 | **State reflects reality** | Correctness | Does the file say what the system actually does? |
| P9 | **Activation is correct** | Correctness | Do rules apply when they should, and only when they should? |
| P12 | **Output matches intent** | Correctness | Does what the system produces match what its rules say it should produce? |

### Derived from Bridge Axiom

| # | Premise | Derived from | Question |
|---|---------|-------------|----------|
| P8 | **Every failure has a fallback** | Degradability, Evolvability | What degrades when a dependency is missing? |
| P10 | **Every node knows how to update itself** | Evolvability | When something changes, is there a clear process to propagate the change? |
| P11 | **Versions are traceable** | Evolvability | Do I know what version of each piece I have and when it dates from? |

### Premise Map to Axioms

```
Axiom          Premises that express it
──────────────  ──────────────────────────────
Consistency     P3, P7
Economy         P3, P5, P6
Traceability    P1, P4
Correctness     P7, P9, P12
Completeness    P2, P8
Degradability   P8, P9
Evolvability    P8, P10, P11
```

---

## Severity Classification

Every finding is classified by severity AND scope (internal/external):

| Severity | Internal finding | External finding |
|----------|-----------------|------------------|
| **CRITICAL** | System contradicts itself; no owner for critical artifact | Referenced dependency doesn't exist; output doesn't match intent |
| **WARNING** | Premature abstraction; redundant information | Drift from reality; activation applies to wrong scope |
| **SUGGESTION** | Could be more economical; traceability could improve | Could be more proportional to context |

### Severity calibration

Severity is NOT fixed per axiom — it depends on Level 0 (purpose):

```
Purpose: "orchestrate SDD pipeline"
  → P2 (references resolve) = CRITICAL (broken pipeline)
  → P5 (economy) = WARNING (token waste)
  → P11 (versions) = SUGGESTION (nice to have)

Purpose: "give agent identity"
  → P2 (references resolve) = WARNING (agent degrades gracefully)
  → P5 (economy) = CRITICAL (every rule must earn its place)
  → P11 (versions) = SUGGESTION
```

---

## Audit Execution Protocol

### Step 0: Resolve Purpose

```
1. Read the target system
2. Answer: "What is the purpose of this system?"
3. Answer: "Which axioms are most critical for that purpose?"
4. Calibrate severity thresholds based on answers
```

### Step 1: Structural Scan (premises P1-P6)

Check internal premises: ownership, redundancy, executability, economy, dependency direction.

### Step 2: Referential Integrity (premises P2, P8-P9)

Check that every reference resolves, every failure has a fallback, activation is correct.

### Step 3: Behavioral Verification (premises P7, P12)

Check that state matches reality and output matches intent.

### Step 4: Evolution Readiness (premises P10-P11)

Check versioning and update paths.

### Step 5: Proportionality Assessment

After all axioms pass, assess: is the system proportional to its context? Flag sub-optimization or over-optimization.

### Step 6: Report

Output findings grouped by severity, with scope (internal/external) and the premise that was violated.

---

## Usage

This framework is domain-agnostic. Apply it to:

- AGENTS.md and its dependency tree
- Individual SKILL.md files
- OpenSpec artifacts
- Shared convention files
- Any future configuration structure

The axioms and premises don't change. The purpose (Level 0) and severity calibration change per audit target.

## Audit Examples

- [Gentle-AI audit](audits/gentle-ai-audit.md) — external open-source project (Gentleman-Programming/gentle-ai)
- [agent-config audit](audits/agent-config-audit.md) — personal dotfiles derived from Gentle-AI
