# oh-my-hermes — Evolution Governance Model v1

## 1. Purpose
Define the **design model** for how oh-my-hermes should evolve itself without collapsing product governance.

This is the layer above implementation.
It answers:
- what counts as self-evolution
- what may be auto-applied
- what must remain recorded only
- what must be escalated to the user

---

## 2. Core design shift
The product should no longer be thought of as merely:
- an autonomous executor
- plus a memory system
- plus a patch mechanism

It should now be thought of as a **governed self-improving control system**.

That means self-evolution is not a side effect.
It is a first-class control-plane function.

---

## 3. Three-layer evolution architecture

### Layer A — Discovery
Purpose:
- detect that execution revealed a reusable improvement

Output:
- an evolution candidate

Key idea:
The runtime should separate **observing an improvement** from **applying an improvement**.

### Layer B — Governance
Purpose:
- classify the improvement by product risk
- decide whether it is safe to auto-apply

Output:
One of three outcomes:
- `auto_upgrade_allowed`
- `record_only`
- `user_decision_required`

Key idea:
This layer is the policy boundary between autonomy and product control.

### Layer C — Materialization
Purpose:
- either patch the skill/package
- or record the improvement durably
- or escalate it for user decision

Output:
- accepted product refinement
- backlog item
- user decision item

Key idea:
The system must never confuse **candidate discovered** with **product changed**.

---

## 4. Product boundary
The most important design boundary is:

### Internal product refinement
Safe to auto-apply when bounded.

Examples:
- clearer workflow rules
- stronger review logic
- better memory hygiene
- improved dependency recovery behavior
- tighter runtime contracts

### Product-direction change
Not safe to auto-apply.

Examples:
- changing what completion means
- changing acceptance standards
- changing user interruption policy
- changing treatment of historical work
- changing delivery semantics

Design rule:
**Autonomy may refine the machine, but may not silently redefine the product contract.**

---

## 5. Canonical evolution state machine
Recommended state machine:

1. `candidate_detected`
2. `candidate_classified`
3. one of:
   - `auto_applied`
   - `recorded_only`
   - `awaiting_user_decision`
4. `superseded` or `retained` later

This creates a clean audit model:
- discovered
- judged
- materialized
- later superseded if needed

---

## 6. Source-of-truth model
Self-evolution should have **two distinct truths**.

### Machine truth
Lives in durable control-plane artifacts.
Purpose:
- resume
- traceability
- automation safety

### Product truth
Lives in the skill/package and its memory.
Purpose:
- define what the product currently is
- define why it evolved

Design rule:
A product change is real only when both are aligned:
1. governance outcome exists
2. durable product artifact reflects that outcome

---

## 7. Why candidate artifacts matter
The candidate artifact is not an implementation detail.
It is a design necessity.

Without it, the system collapses three different moments into one:
- discovery
- judgment
- application

That creates three risks:
1. silent product drift
2. no audit trail for why a change happened
3. no clean place to stop when confidence is low

So the candidate artifact should be treated as:
**the handshake object between runtime learning and product governance.**

---

## 8. Default governance posture
Recommended default posture:
**conservative autonomy**

Meaning:
- if bounded and clearly internal -> auto-apply
- if useful but underspecified -> record only
- if contract-affecting -> ask user

This is the right balance because the product goal is not maximum mutation speed.
The product goal is:
**maximum autonomous improvement without silent contract drift.**

---

## 9. Maturity model

### Maturity 1 — Auto-log
The system can record improvements.

### Maturity 2 — Auto-upgrade artifact
The system can patch bounded product artifacts.

### Maturity 3 — Governed self-evolution
The system can decide whether to patch, record, or escalate.

### Maturity 4 — Evidence-backed evolution
The system can explain why a change was safe, based on execution evidence.

### Maturity 5 — Pattern extraction
The system can consolidate repeated backlog items into higher-level product refinements.

Current target design:
**Maturity 4**

Meaning:
The next design priority is not “more patching.”
It is:
**stronger evidence semantics for why a candidate should change the product.**

---

## 10. Next design problem
The next major design layer should be:

# Evolution Evidence Model

Question:
What evidence is strong enough for oh-my-hermes to treat a runtime observation as a product-worthy refinement?

Recommended answer:
Every evolution candidate should eventually carry:
- source context
- repeatedness or rarity
- affected policy area
- risk level
- confidence level
- recommended action
- relationship to existing accepted rules

That becomes the bridge from:
- ad hoc improvement recording
into
- disciplined product learning

---

## 11. Recommended conclusion
The system should now be designed as:

**conversation-driven autonomous harness**
+
**governed self-evolution control plane**

That is the correct product identity.

The next design step is therefore:
**not more execution plumbing, but a formal evolution evidence model.**
