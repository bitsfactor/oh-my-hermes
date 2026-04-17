# oh-my-hermes — Product Control Panel Model v1

## 1. Purpose
Define the **decision-maker control surface** for oh-my-hermes.

This layer answers:
- what a human product owner should be able to see
- what they should be able to steer
- what they should *not* need to see
- how to preserve conversation-first operation while still exposing meaningful control

This is not an implementation UI spec.
It is the design model for the product’s top-level steering surface.

---

## 2. Core design idea
Now that oh-my-hermes has:
- a constitutional layer
- a governance stack
- a milestone discipline
- a product operating system

it needs a human-facing steering abstraction.

The key design question is:

**How does a decision-maker observe and steer the product without falling into implementation detail?**

That is what the control panel model defines.

---

## 3. Control-panel principle
The control panel should not expose the machine in raw form.
It should expose the machine at the **right abstraction level**.

Meaning:
- no file-churn view by default
- no executor transcript view by default
- no low-level runtime noise by default
- no obligation to inspect internal scripts, packets, or state files

Instead, the control panel should answer product questions such as:
- What state is the system in?
- What is blocked?
- What is being learned?
- What requires my decision?
- What changed at the last milestone?

So the control panel is not an engineer console.
It is a **product steering surface for a governed autonomous system**.

---

## 4. What the control panel is for
The control panel exists for four jobs.

### Job 1 — situational awareness
Let the operator understand the current state of the product.

### Job 2 — bounded intervention
Let the operator steer product direction when constitutional or contract-level judgment is required.

### Job 3 — confidence management
Let the operator judge whether the product is healthy, drifting, blocked, or under-governed.

### Job 4 — milestone awareness
Let the operator see what has become official product law and what remains provisional.

---

## 5. Core control-panel surfaces
The control panel should expose five primary surfaces.

### 1. Mission surface
What is the product currently trying to accomplish?

Examples:
- active product focus
- active sample-project validation target
- current milestone frontier

This answers:
**What is the system pointed at right now?**

### 2. Health surface
What is the state of the product as an operating system?

Examples:
- healthy
- blocked
- learning but unstable
- backlog-heavy
- decision-gated

This answers:
**Is the system operationally healthy?**

### 3. Governance surface
What decisions are pending, what is autonomous, and what is outside autonomous authority?

Examples:
- auto-governable items
- deferred items
- user decision queue
- constitutional boundary alerts

This answers:
**What can the product decide on its own, and what must come to me?**

### 4. Learning surface
What has the system been learning about itself?

Examples:
- top backlog themes
- promoted rules
- repeated friction signals
- recently formalized product law

This answers:
**How is the product evolving?**

### 5. History surface
What changed at the last milestone, and what is now canonical?

Examples:
- latest milestone summary
- latest promoted policies
- latest constitutional interpretations
- current baseline commit / release meaning

This answers:
**What is officially true now?**

---

## 6. What the control panel should not expose by default
The control panel should not default to:
- raw execution transcripts
- patch diffs
- packet internals
- low-level process logs
- line-by-line implementation evidence
- internal tool chatter

Those may exist behind drill-down layers.
But they are not the primary product surface.

Design rule:
**The default view should expose governed state, not implementation residue.**

---

## 7. Canonical operator questions
A correct control panel should make these questions cheap to answer.

1. What state is the product in right now?
2. What is blocked?
3. What needs my decision?
4. What changed recently?
5. What did the system learn?
6. What is still only backlog, not product law?
7. Is the product still operating within constitutional boundaries?

If these questions are hard to answer, the control panel is wrong.

---

## 8. Control classes
The decision-maker should have only a small number of top-level control classes.

### Class A — Direction controls
Examples:
- choose current priority
- select which frontier matters now
- approve contract-level shifts

### Class B — Governance controls
Examples:
- approve or reject product-direction changes
- relax or tighten promotion posture
- trigger milestone formalization

### Class C — Recovery controls
Examples:
- pause a drifting evolution path
- require replan
- force backlog instead of promotion
- freeze constitutional review

### Class D — Publication controls
Examples:
- accept milestone publication
- defer milestone closure
- require clearer product summary before publication

This keeps operator control meaningful but sparse.

---

## 9. Conversation-first control model
Because oh-my-hermes is conversation-first, the control panel should not be understood as a dashboard first.

The deeper model is:

**conversation is the front door, control panel is the durable operator view behind it**

Meaning:
- the user may still steer primarily by talking
- but the system should internally organize those decisions into stable control surfaces
- the control model should be representable in conversation, not dependent on GUI assumptions

This preserves constitutional consistency with the conversation-first product identity.

---

## 10. Recommended summary shape
At any moment, a high-quality control panel should be able to summarize the product in five lines:

1. **Mission** — what the system is trying to do
2. **State** — healthy / blocked / unstable / gated
3. **Governance** — what is autonomous vs awaiting decision
4. **Learning** — what the system is currently discovering
5. **History** — what the last milestone made official

This is the minimal operator-grade summary contract.

---

## 11. Failure modes of a bad control panel
The model should reject these failure modes.

### Failure 1 — Implementation trap
The operator must parse low-level details to know what is happening.

### Failure 2 — Illusion of control
The panel exposes many knobs but none correspond to real governance boundaries.

### Failure 3 — Hidden decision debt
Important product-direction decisions remain invisible until too late.

### Failure 4 — No learning visibility
The product evolves, but the operator cannot tell how or why.

### Failure 5 — No constitutional visibility
The product may be drifting across identity boundaries without any visible signal.

---

## 12. Relationship to the Product Operating System
The Product Operating System defines how the product runs.
The Control Panel Model defines how a human product owner sees and steers that running system.

So:
- Product OS = machine operating cycle
- Control Panel = human steering surface for that cycle

This separation matters because observability and steerability are not the same as execution.

---

## 13. Relationship to milestones
At milestone boundaries, the control panel should be the place where the decision-maker can see:
- what became official
- what stayed backlog
- what moved closer to constitutional territory
- what the next frontier is

That makes milestone closure legible without exposing raw implementation churn.

---

## 14. Current recommendation
At the current maturity of oh-my-hermes, the control panel should prioritize:
1. health visibility
2. governance visibility
3. learning visibility
4. milestone visibility
5. constitutional-boundary visibility

This is more important right now than deep operational controls.
Because the product is still consolidating its governing logic.

---

## 15. Recommended next design layer
After the Product Control Panel Model, the next natural design layer is:

# Product Modes Model

Question:
What top-level operating modes should oh-my-hermes support, and how should the same product behave differently across exploration, delivery, recovery, and governance-heavy contexts?

Why this is next:
Once the operator view exists, the next design question is how the product should intentionally change posture under different mission conditions.

---

## 16. Recommended conclusion
oh-my-hermes should expose a sparse, governance-aligned control panel for decision-makers.

That is the correct design because the user should steer product direction and trust boundaries—
not micromanage internal machinery.
