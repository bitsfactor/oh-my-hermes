# oh-my-hermes — Product Modes Model v1

## 1. Purpose
Define the top-level **operating postures** of oh-my-hermes.

This layer answers:
- in what distinct modes the product should operate
- how the same product behaves differently under different mission conditions
- what changes across modes and what must remain invariant

This is the missing layer between:
- a stable operating system
and
- practical use on real projects

---

## 2. Core design question
The product is now defined as:
- a governed autonomous harness
- with a product operating system
- with milestone discipline
- with a constitutional layer
- with a decision-maker control surface

The next question is:

**What posture should the product take in different real operating contexts?**

Because the same system should not behave identically when:
- exploring an uncertain path
- driving a delivery to completion
- recovering from runtime failure
- hardening its own governance

So the modes model defines the product’s deliberate posture shifts.

---

## 3. Design principle
Modes should change:
- emphasis
- tolerance
- escalation posture
- interpretation of uncertainty
- promotion aggressiveness

Modes should **not** change:
- constitutional rules
- source-of-truth rules
- milestone discipline
- the requirement for real acceptance when acceptance is part of the requested deliverable

This is the core design principle:

**Modes change posture, not identity.**

---

## 4. The four canonical modes

### Mode 1 — Exploration Mode
Purpose:
Reduce uncertainty and discover viable paths.

Best used when:
- the product or project frontier is unclear
- multiple approaches are plausible
- cheap experimentation can reduce risk
- architectural understanding is still forming

Primary bias:
- learning over closure

Allowed posture:
- more branch experiments
- more provisional backlog capture
- lower promotion aggressiveness
- higher tolerance for unresolved debt that does not corrupt contract meaning

Risk:
If overused, the system can drift into endless exploration without delivery.

---

### Mode 2 — Delivery Mode
Purpose:
Drive a bounded goal to real completion.

Best used when:
- the target is already coherent
- the system should optimize for finishing
- acceptance criteria are frozen enough to execute against

Primary bias:
- closure over optional exploration

Allowed posture:
- tighter task sequencing
- stronger insistence on review gates and acceptance
- lower tolerance for open-ended design detours
- preference for continue_with_debt over exploratory branching when semantics are unchanged

Risk:
If overused too early, the system may force closure before uncertainty is actually reduced.

---

### Mode 3 — Recovery Mode
Purpose:
Restore a blocked or unstable execution path to a safe operating baseline.

Best used when:
- transport or environment failures dominate
- acceptance is blocked by runtime defects
- the current path is unstable enough that normal delivery pressure is counterproductive

Primary bias:
- regain reliability before forward progress

Allowed posture:
- stronger diagnosis focus
- narrower change surfaces
- heavier bias toward isolating root cause
- lower tolerance for unrelated progress claims

Risk:
If overused, the system can become too conservative and stop re-entering productive delivery motion.

---

### Mode 4 — Governance-Hardening Mode
Purpose:
Improve the harness product itself rather than primarily deliver external work.

Best used when:
- repeated signals show missing product law
- the control plane is weaker than the execution pressure demands
- a design layer needs formalization before more scale makes sense

Primary bias:
- strengthen the machine over immediate throughput

Allowed posture:
- higher attention to evidence, promotion, and milestone formalization
- stronger backlog clustering and interpretation
- more product-law work, less external feature pressure

Risk:
If overused, the product can become introspective and under-serve live delivery work.

---

## 5. Mode selection rule
The product should select mode based on the dominant operating problem.

### If the dominant problem is uncertainty
-> Exploration Mode

### If the dominant problem is finishing a coherent target
-> Delivery Mode

### If the dominant problem is instability or blockage
-> Recovery Mode

### If the dominant problem is insufficient product governance or control strength
-> Governance-Hardening Mode

This keeps the system from using a single posture for every situation.

---

## 6. What changes across modes
The following dimensions may vary by mode.

### 1. Uncertainty tolerance
- high in Exploration
- low in Delivery
- moderate in Recovery
- selective in Governance-Hardening

### 2. Escalation threshold
- lower in Recovery for hard blockers
- lower in Governance-Hardening for contract-level drift
- higher in Exploration for reversible ambiguity
- moderate in Delivery when delivery semantics are already frozen

### 3. Experiment appetite
- highest in Exploration
- low in Delivery
- very low in Recovery
- moderate in Governance-Hardening when testing product-law alternatives

### 4. Promotion aggressiveness
- low in Exploration
- moderate in Delivery
- low in Recovery
- highest in Governance-Hardening for internal product refinements with strong evidence

### 5. Debt tolerance
- high in Exploration when semantics are safe
- moderate in Delivery
- low in Recovery for stability-threatening debt
- low in Governance-Hardening when debt reflects missing product law

---

## 7. What must remain invariant across modes
No mode may override the constitution.

Therefore these invariants remain fixed:
- conversation-first product surface
- harness-governed execution and truth
- real acceptance outranking narration
- no silent contract redefinition
- durable state as operational truth
- milestone history as governed product record

This is why modes are safe.
They only shift operational posture inside constitutional boundaries.

---

## 8. Mode transitions
Mode transitions should be explicit, not accidental.

### Recommended transition triggers
- uncertainty falls enough to leave Exploration and enter Delivery
- runtime instability rises enough to leave Delivery and enter Recovery
- repeated governance gaps rise enough to leave Delivery or Exploration and enter Governance-Hardening
- governance improvements complete enough to return from Governance-Hardening to Delivery or Exploration

Design rule:
**A mode transition is a product-level posture decision, not an implementation side effect.**

---

## 9. Mode failure patterns
The system should recognize characteristic failure modes.

### Exploration failure
- endless branch experiments
- no convergence
- low formalization

### Delivery failure
- pushing closure through unresolved uncertainty
- repeated late replan pressure
- acceptance surprises

### Recovery failure
- endless diagnosis without re-entry
- fixation on local blockers with no restored trajectory

### Governance-Hardening failure
- too much inward focus
- weak external value delivery
- theory accumulation without renewed execution pressure

This matters because every mode has a predictable pathological form.

---

## 10. Control-panel relationship
The control panel should expose mode explicitly.

A decision-maker should always be able to see:
- current mode
- why the system is in that mode
- what bias that mode introduces
- what would trigger a mode change

This makes the product steerable at the right abstraction layer.

---

## 11. Product OS relationship
The Product Operating System defines the recurring outer loop.
The Modes Model defines the posture in which that operating system currently runs.

So:
- Product OS = ongoing machine cycle
- Product Modes = current behavioral stance of that machine

This distinction is essential.
Without modes, the Product OS is structurally correct but behaviorally flat.

---

## 12. Applying to the API project
For a real sample project such as an API backend, the main practical result is:

### You can start applying oh-my-hermes now
because the system now has distinct postures.

Recommended initial application pattern:
- begin in **Governance-Hardening Mode** when the harness itself still needs strengthening from real pressure
- use **Exploration Mode** for uncertain architectural forks
- switch into **Delivery Mode** when a slice is coherent enough to finish
- use **Recovery Mode** when runtime or transport instability blocks honest progress

This is the design step that turns the harness from “usable in principle” into “usable with deliberate posture.”

---

## 13. Recommended immediate interpretation
Before this modes layer, applying oh-my-hermes to a real API project was possible but still posture-ambiguous.

After this modes layer, application becomes clearer because the product can now distinguish:
- learning posture
- finishing posture
- stabilization posture
- self-hardening posture

That is enough to justify real dogfood application in the API project.

---

## 14. Recommended next design layer
After Product Modes Model, the next natural layer is:

# API-Project Adoption Model

Question:
How should a real API project be onboarded into oh-my-hermes step by step so that the product controls the project without collapsing sample-project and harness-product boundaries?

Why this is next:
Now that the product has modes, the next question is not abstract governance anymore.
It is the practical adoption architecture for the first real project.

---

## 15. Recommended conclusion
oh-my-hermes should support a small number of explicit operating modes.

That is what makes the harness truly applicable to a real project: not just because it has policies, but because it can adopt the right posture for the current kind of work.
