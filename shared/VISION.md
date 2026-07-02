# VISION.md
<!-- v3.2 | last edited: 2026-06-03 -->

## Why and What This System Is For

Intelligence without accessibility has no real utility.

A system that costs too much to execute too little does not scale, does not help,
and is not worth building. Power is not the goal —
economy of means is.

This framework exists to solve any digitalizable problem,
from the abstract (logic, data, decisions) to the physical
(machines, protocols, implementations). It is not a niche system
— it is general-purpose, designed so that execution cost
is always proportional to the problem it solves.

---

## The Meta-Observation

Studying industrial history reveals a recurring pattern:

1. Someone discovers a more efficient method
2. The method becomes standardized and sustained
3. The efficiency benefit does not go to its creator but to whoever
   controls the process

This is not just history — it is a structural conflict of interest
that reproduces itself in current AI systems.

The per-token pricing model is the clearest example: an agent that
solves something in 500 tokens generates less revenue for the provider than one
that uses 2000. Efficiency goes against the incentive of whoever sells
intelligence. The Taylorist worker had the same problem — the more
efficient they were, the more the standard was tightened and the less
they earned proportionally.

The answer to that conflict is the same as in industry:
document the efficient method, sustain it, and do not rely on
the provider having the same incentives as you.

That is what this system does.

---

## Historical Stages and Their Extrapolation

Each stage solved a concrete problem in its time.
The question for each is: does that problem exist in an agent system?

### 1. Taylorism (~1880, USA)
**Historical problem:** Inefficiency of empirical craft work —
each worker did things their own way, with no standard method.

**Solution:** Time, divide, and standardize every task.
The method no longer lives in the worker's head but becomes
a documented, reproducible protocol.

**Extrapolation:** Agents without strict input/output contracts
improvise. Zod, TypeScript, schemas — they are the Taylorist stopwatch.
They reduce the improvisation window and make behavior predictable.

**Judgment:** Natural. It is the most direct extrapolation of all.

**Concrete application:** Skill design. A well-made skill
documents the efficient method and sustains it. It is not rediscovered
every time.

---

### 2. Fordism (1908-1913, USA)
**Historical problem:** High unit cost and slow manual
assembly.

**Solution:** Linear assembly line, standardized single product,
massive scale.

**Extrapolation:** Fixed sequential pipelines — Agent A passes to B,
B passes to C. Works for CI/CD and predictable automations.

**Judgment:** Natural for simple automation, forced for autonomous
agents. Fordist rigidity is exactly what an intelligent system
must be able to break when the problem requires it.

---

### 3. Sloanism (1920s, USA)
**Historical problem:** Market saturation of the single product
— Ford's Model T did not fit all contexts.

**Solution:** Layered segmentation — different products for
different needs, with shared common base.

**Extrapolation:** Layered architecture L1/L2/L3. Each layer has
distinct responsibilities and they do not mix. Common base,
variable behavior by context.

**Judgment:** Natural. It is the foundation of any extensible
architecture.

---

### 4. Toyotism and Ohnoism (~1948-1975, Japan)
**Historical problem:** Post-war lack of capital and space —
no warehousing possible; produce only what is needed.

**Solution:** Just-in-Time (pull system) and Jidoka — produce on
demand and stop the line at any defect.

**Extrapolation:** Agents do not consume tokens speculatively —
they wait for the signal. Token cost is the exact equivalent
of storage cost. Producing inferences only
on demand saves operational capital identically.

**Judgment:** The most natural of all extrapolations.

**Tension:** Pure Jidoka — stopping everything on error — can break
system resilience. See open problems section.

---

### 5. Volvoism (1970s, Sweden)
**Historical problem:** Alienation and absenteeism of the Fordist worker —
the fixed line destroyed motivation.

**Solution:** Autonomous work cells, high cooperative autonomy,
no rigid central line.

**Extrapolation:** Microservices and decoupled modules that
self-register and solve problems without suffocating central control.

**Judgment:** Forced in its ethical premise (machines do not get alienated),
natural in its architecture. Modular fault tolerance
is a real standard — if one component falls, the rest keeps operating.

---

### 6. Post-Fordism and Flexible Specialization (1970-1980, Global)
**Historical problem:** Rigidity of large corporations during
economic crises — fixed machinery could not be reprogrammed.

**Solution:** Microelectronics to quickly reprogram machinery
by niche.

**Extrapolation:** Dynamic containers (Docker/Kubernetes) —
software-defined infrastructure, adaptable in real time.

**Judgment:** Natural. It directly maps the transition from rigid
hardware to malleable environments.

---

### 7. McDonaldization (1990s, Global)
**Historical problem:** Unpredictable variability in mass services —
every location was different.

**Solution:** Parameterize identical processes. The result is always
the same regardless of who executes it.

**Extrapolation:** Every agent, regardless of its internal logic,
returns exactly the same JSON structure. The
orchestration layer does not rewrite adaptation logic for each agent.

**Judgment:** Natural. It is the key to frictionless system
composition.

---

### 8. Sonyism (1990s, Japan)
**Historical problem:** Commercial obsolescence in high-tech
markets — competitors copied before investment was amortized.

**Solution:** Compress the product lifecycle, ship the next
version before the previous one is copied.

**Extrapolation:** The race between AI labs (OpenAI, Google,
DeepSeek) — ship the next disruptive capability quickly.

**Judgment:** Natural at the macroeconomic AI level, forced within
a local architecture. A proprietary system needs stability,
not radical mutations that break the foundation every few weeks.

---

### 9. Platformism (2010s, Global)
**Historical problem:** Massive fixed costs of physical infrastructure —
Uber has no cars, Airbnb has no hotels.

**Solution:** Intermediation algorithms that connect supply and
demand without owning the assets.

**Extrapolation:** The orchestrator as pure intermediary — does not execute,
assigns. Routes tasks to agents or third-party APIs by context.

**Judgment:** Very natural. It describes exactly how modern
AI orchestration frameworks operate.

---

### 10. Industry 4.0 (2011, Germany)
**Historical problem:** Gap between digital planning and physical
execution — the factory did not monitor itself in real time.

**Solution:** IoT, Big Data, adaptive automation — the factory
becomes a cyber-physical system that monitors and corrects itself.

**Extrapolation:** Agents that monitor their own errors, modify
their source code, and redeploy without human intervention.

**Judgment:** Natural. It is the current state of AI-assisted development
and the ultimate goal of this system.

---

## Open Problems

These tensions were initially unresolved. They are documented
here with their current resolution and what remains pending.

### 1. Parallelism vs. Just-in-Time

**Original tension:** Toyotism demands strict flow control
to avoid accumulating token stock. Industry 4.0 demands concurrent
parallelism to be efficient.

**Resolution:** A 100% synchronous system is idealistic — there can always
be network latency, errors, or denser prompts. The
solution is not runtime coordination but preventive design
of the execution tree: wide and shallow, with as few
sequential dependencies as possible. What cannot be parallelized
is managed with pause and wait. Models are selected by layer:
free tier and local models via Ollama or LM Studio for L3,
paid models only for what small models cannot resolve.

**Pending:** Define the execution tree factorization principle
as an L1 directive at the start of each project.

---

### 2. Ohnoism vs. Resilience

**Original tension:** Stopping everything on error prevents
hallucination propagation. But freezing the entire system for a secondary
failure violates basic resilience.

**Resolution:** The dependency tree with factorized modules.
If a part fails checks or audits, it is retried in
isolation without paralyzing the rest. The delay is bounded to that
factorization. L3 does not decide what impact its failure has — it only
reports. L2 decides what to retry and what to wait for.

**Pending:** Document in `registry.json` the dependencies of each
module so L2 can make that decision with real information.

---

### 3. Digital Taylorism Metrics

**Original tension:** We need to measure agent efficiency but
had not defined the metrics.

**Resolution:** Each LLM signs its output with its identity. In
retrospect, we track which models generate more errors and on
what task types — whether the error is from the model or from the
harness design. Temperature 0 to reduce unwanted variability, but
assuming LLMs are probabilistic and hallucinations
can always occur. Test redundancy and controls are the containment
mechanism, not error elimination.

Metrics to record: tokens consumed per task, latency,
financial cost, error rate by model and task type.

**Pending:** Define the authorship signature format and where
the metric history accumulates.

---

## Closing: Principles Emerging from Open Problems

### Errors Are Expected

The system is not designed to eliminate errors but to contain them,
measure them, and learn from them. An error is not a system failure
— it is information. The authorship signature of each LLM, the tests,
the redundancy of controls — they are not defenses against error,
they are mechanisms to make error useful.

### Antifragility

A robust system resists error. A resilient system recovers from it.
An antifragile system improves because of it.

This is the design goal. Every accounted error adjusts which
model does what task. Every skill failure generates a new test.
Every detected hallucination refines the harness. Controlled exposure
to error is the system's evolution mechanism — not an unwanted
side effect.

### The Execution Tree

Minimize correlation from design — wide, shallow trees
with as few sequential dependencies as possible.
The principle is defined here. How it applies to each specific project
is the responsibility of L1 at the start of that project.
