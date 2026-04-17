# oh-my-hermes — Self-Hosting & Recursive Dogfooding Model v1

## 1. Purpose
Define whether **oh-my-hermes can be used to build oh-my-hermes itself**, and if so, under what governance constraints.

This layer answers:
- whether self-hosting is valid for this product
- how recursive dogfooding should work without collapsing control
- what may evolve autonomously during self-development
- what boundaries must remain fixed

---

## 2. Core conclusion
**Yes — omh should develop omh.**

But it must do so as **governed recursive dogfooding**, not as unconstrained self-modification.

The right principle is:

**omh may be both the harness under test and the harness in use, but never without an explicit governance boundary between those two roles.**

---

## 3. Why self-hosting is the right direction
If omh cannot participate in its own development, an important product claim stays unproven.

Because the product claims to be:
- an autonomous harness
- capable of supervised execution
- capable of review, recovery, acceptance, and self-evolution
- capable of improving under real project pressure

The strongest dogfood pressure is therefore:

**Can omh improve omh while preserving product law?**

If yes, the product becomes much more credible.
If no, the product is still only partially real.

---

## 4. Core design distinction
Self-hosting introduces two roles that must not be merged.

### Role A — Active operator
The currently trusted omh instance that is supervising work.

Responsibilities:
- choose mode
- maintain source of truth
- apply review discipline
- decide promotion / defer / escalate
- decide whether changes are accepted into official product history

### Role B — Subject under change
The next candidate state of omh being designed, edited, reviewed, and tested.

Responsibilities:
- receive proposed changes
- produce candidate artifacts
- pass verification and review
- earn promotion into accepted product state

Design rule:
**The operator may use the product to improve itself, but the currently accepted operator state and the candidate changed state must remain conceptually distinct.**

---

## 5. The correct self-hosting model
The correct model is not:
- single undifferentiated self-editing
- instant self-redefinition
- continuous silent mutation

The correct model is:

## Governed recursive dogfooding
Meaning:
1. the accepted omh state supervises work on a candidate omh state
2. execution evidence is collected from real self-use
3. evolution candidates are generated from that evidence
4. promotion happens only at milestone boundaries or explicit governed review points
5. accepted product law is updated only after review and canonical history update

This preserves both:
- real self-improvement pressure
- product identity stability

---

## 6. What self-hosting should improve
Self-hosting is especially valuable for improving:

### 1. Execution discipline
- packet quality
- review loops
- retry / diagnosis logic
- recovery sequencing

### 2. Governance discipline
- promotion thresholds
- evidence interpretation
- milestone judgment
- user-decision boundaries

### 3. Control-plane clarity
- mode visibility
- state truth alignment
- acceptance semantics
- separation between harness and project

### 4. Operator burden reduction
- recurring ambiguity removal
- recurring review-gap removal
- recurring recovery-gap removal

These are exactly the areas where real self-use produces the strongest evidence.

---

## 7. What self-hosting must never do silently
Self-hosting must never silently change:
- what “done” means
- what real acceptance means
- when the user must be interrupted
- what counts as contract-level product truth
- whether milestone discipline applies
- whether historical product law remains legible

This follows directly from the constitution and evolution-governance rules.

Design rule:
**Self-hosting increases evidence pressure, not contract override rights.**

---

## 8. Recommended default operating posture
The default posture for self-hosting should be:

## Governance-Hardening Mode
Reason:
During self-development, the primary question is usually not merely “can the product produce output?”
The primary question is:

**Is the product strong enough to govern its own improvement under real pressure?**

So self-hosting should start from:
- stronger governance attention
- stronger review discipline
- stronger evidence interpretation
- stronger milestone formalization

Then shift as needed:
- uncertainty-dominant work -> Exploration Mode
- coherent finish work -> Delivery Mode
- instability-dominant work -> Recovery Mode

---

## 9. Self-hosting risk model
Self-hosting creates specific failure modes.

### Failure mode 1 — Recursive drift
The system keeps changing itself from local observations without clear promotion boundaries.

### Failure mode 2 — Self-approval collapse
The system effectively becomes judge, implementer, and approver of the same unreviewed change.

### Failure mode 3 — Product/project merge
Work on omh and work in a sample project become operationally indistinguishable.

### Failure mode 4 — Governance theater
The system claims self-governance, but changes are still really just ad hoc edits with nicer words.

### Failure mode 5 — Introspection trap
The product becomes too focused on refining itself and under-delivers on external project value.

The model must explicitly resist all five.

---

## 10. Required safety boundaries
For recursive dogfooding to be valid, these boundaries must exist.

### Boundary 1 — Accepted state vs candidate state
There must always be a meaningful distinction between:
- the currently accepted omh state
- the candidate modified omh state

### Boundary 2 — Evidence before promotion
Self-use observations must first appear as evidence or candidates, not immediate law.

### Boundary 3 — Milestone promotion
Promotion into accepted product history should normally happen at milestone boundaries.

### Boundary 4 — Independent review pressure
The system should preserve real review distance wherever possible.
Even if the same harness is involved, review logic must not collapse into unchecked self-assertion.

### Boundary 5 — Canonical history update
Accepted self-improvement must enter canonical Git history as an explicit product-state change.

These boundaries are what make self-hosting credible rather than circular.

---

## 11. Operational model for recursive development
Recommended operational loop:

1. run omh on omh work under Governance-Hardening Mode
2. collect execution evidence from real self-use
3. classify lessons as candidate / backlog / escalation
4. implement bounded improvements to candidate omh state
5. run review and verification against that candidate state
6. decide promotion at milestone boundary
7. publish accepted change into canonical history
8. continue from the newly accepted state

This creates a controlled recursive ladder:

**use -> learn -> refine -> review -> promote -> become the new operator baseline**

That is the correct self-evolution shape.

---

## 12. Relationship to auto-evolution
Self-hosting does not mean unlimited auto-upgrade.

Instead, it means self-use becomes the richest source of evolution evidence.

So the relationship is:
- self-hosting generates stronger evidence
- evolution governance classifies it
- promotion policy decides when it becomes rule
- milestone governance decides when it becomes official history

This preserves the earlier architectural split:
- discovery
- governance
- materialization

Self-hosting strengthens the pipeline.
It does not bypass it.

---

## 13. Relationship to sample projects
Sample projects remain necessary.

Reason:
A product cannot prove itself only on itself.
It must also survive pressure from external real work.

So the right stack is:
- **external dogfood**: omh drives projects like xapi-image-backend
- **internal dogfood**: omh drives improvements to omh itself

These two pressures should reinforce each other.

Design rule:
**Self-hosting sharpens the harness internally; sample projects validate whether that sharpening transfers outward.**

---

## 14. Product-level interpretation
This means the next stage of omh is not merely:
- “build the harness first, then maybe use it later”

It is:
- **build the harness by already using the harness in a governed way**

That is a more truthful product path.
Because omh is supposed to be a living autonomous operating system, not a static design package waiting for later activation.

---

## 15. Recommended immediate policy
Recommended immediate policy for this repo:

1. treat omh as eligible to operate on omh
2. keep self-hosting in Governance-Hardening Mode by default
3. treat all self-observed improvements as candidates first
4. require milestone-legible promotion into accepted history
5. do not allow self-hosting to silently rewrite contract-level law

This is the minimal policy set that makes recursive development both useful and governable.

---

## 16. Recommended next design layer
After Self-Hosting & Recursive Dogfooding Model, the next natural layer is:

# API-Project Adoption Model

Question:
How should omh onboard a real API project while simultaneously preserving a clean relationship between:
- external project delivery
- internal self-hosted product evolution

Why this is next:
Now the product has both:
- operating postures
- a recursive self-development model

So the next missing layer is the adoption architecture that coordinates:
- omh on omh
- omh on real external projects
without collapsing them into one undifferentiated workflow.

---

## 17. Recommended conclusion
**Yes — omh should be used while building omh.**

But the correct form is not free recursive self-modification.
The correct form is:

**governed recursive dogfooding**

That is how omh becomes a real autonomous product without losing product law, historical legibility, or operator trust.
