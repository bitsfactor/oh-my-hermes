# oh-my-hermes — Product Constitution Model v1

## 1. Purpose
Define the small set of **constitutional rules** that no autonomous learning loop, governance layer, or product evolution path may silently violate.

This model exists to protect product identity while autonomy grows.

It answers:
- what must remain stable even as the product learns
- what may be refined versus what may never drift silently
- where the absolute upper boundary of autonomous evolution sits

---

## 2. Core design idea
Everything below this layer may evolve:
- execution policy
- review policy
- evidence policy
- promotion policy
- milestone governance
- internal operating rules

But not everything may evolve equally.

A constitution exists because a self-improving system otherwise risks confusing:
- adaptability
with
- identity loss

So the constitution is the answer to this question:

**What must remain true for this to still be oh-my-hermes?**

---

## 3. Constitutional role
The constitution is not:
- a backlog
- a policy preference list
- a design note
- a temporary milestone artifact

It is:

**the permanent constraint layer above ordinary product evolution.**

Meaning:
- normal policies may change
- operational heuristics may change
- internal rules may change
- but constitutional rules may only change through explicit product-level decision

This makes the constitution the product’s identity anchor.

---

## 4. First constitutional principle
### Principle 1 — Conversation is the primary interface
The product must remain conversation-first.

Meaning:
- the user interacts with Hermes in natural language
- forms, config files, and internal state may support the system
- but they do not replace conversation as the primary product surface

Why constitutional:
If this changes, the product changes category.
It stops being the system the user asked for.

---

## 5. Second constitutional principle
### Principle 2 — The harness governs execution
The child coding agent does not define completion, product law, or product truth.

Meaning:
- Codex or any future executor may implement
- but the harness determines state, review gates, verification, recovery, and acceptance

Why constitutional:
If this changes, the product stops being a harness and collapses into executor delegation.

---

## 6. Third constitutional principle
### Principle 3 — Real acceptance outranks narration
The product may never treat executor narration or optimistic local signals as the final source of truth when real-surface acceptance is available.

Meaning:
- “says it worked” is never enough
- real user-facing surface verification remains authoritative

Why constitutional:
This is one of the defining differences between a workflow shell and a governed delivery harness.

---

## 7. Fourth constitutional principle
### Principle 4 — Autonomy may refine, but not silently redefine the contract
The system may improve internal operation autonomously.
It may not silently alter:
- what completion means
- what the user should expect
- when the user is interrupted
- what counts as acceptable delivery
- how prior work is treated when direction changes

Why constitutional:
Without this principle, self-improvement becomes self-redefinition.

---

## 8. Fifth constitutional principle
### Principle 5 — Durable state outranks conversational residue
The product must preserve its authoritative operating truth in durable artifacts, not only in transient chat context.

Meaning:
- resume must come from durable state
- governance must be traceable
- product evolution must be auditable

Why constitutional:
Without this, the system becomes non-restartable, non-governable, and non-productized.

---

## 9. Sixth constitutional principle
### Principle 6 — Milestone history is part of product truth
Canonical Git/GitHub history is not just engineering convenience.
It is part of the governed product record.

Meaning:
- major design evolution must become milestone history
- product law should not exist only in local working memory or implicit drift

Why constitutional:
The product is self-improving; therefore its history is part of what users and future operators must be able to trust.

---

## 10. Constitutional boundary test
A proposed change should be tested against one key question:

**Does this refine how oh-my-hermes works, or does it redefine what oh-my-hermes is?**

If it only refines operation:
- normal governance may handle it

If it redefines identity:
- it is constitutional territory
- it requires explicit product-level decision

This test is the fast boundary between normal product evolution and constitutional change.

---

## 11. Constitutional violation classes
Recommended violation classes:

### Class A — Interface violation
The product drifts away from conversation-first operation.

### Class B — Governance violation
The executor or local improvisation overrides the harness as governing authority.

### Class C — Truth-source violation
Narration or weak checks replace real acceptance or durable state.

### Class D — Contract violation
Autonomy silently changes user-facing guarantees.

### Class E — History violation
Milestone-grade product change fails to enter canonical product history.

These are not ordinary defects.
They are identity threats.

---

## 12. Relationship to governance
Normal governance decides:
- can this be auto-applied
- should this stay backlog
- should this be escalated

The constitution decides something deeper:
- is this category of change even eligible for silent evolution at all?

So governance operates **inside** constitutional boundaries.
It does not define them.

---

## 13. Relationship to milestones
Milestones formalize product evolution.
The constitution limits what milestone governance is allowed to formalize without explicit product decision.

Meaning:
- milestones can publish coherent product growth
- but they cannot quietly cross constitutional boundaries

This keeps milestone discipline from becoming a legitimation machine for silent identity drift.

---

## 14. Relationship to self-evolution
A self-improving product needs two powers at once:
1. the power to learn
2. the power to not become something else accidentally

The constitution is what gives it the second power.

Without it, self-evolution becomes open-ended mutation.
With it, self-evolution becomes governed adaptation.

---

## 15. Constitutional change rule
Constitutional rules may change, but only under a stricter standard than ordinary product rules.

Recommended standard:
- explicit user/product-owner decision
- explicit statement of what identity rule changes
- explicit acknowledgement of what prior assumptions are superseded
- explicit milestone-grade publication into canonical history

Meaning:
The constitution is not immutable.
But it is not part of silent autonomous learning.

---

## 16. Minimal constitution of oh-my-hermes
At current maturity, the minimal constitution is:

1. conversation-first product surface
2. harness-governed execution
3. real acceptance over narration
4. no silent contract redefinition
5. durable state as operational truth
6. milestone history as product record

These six rules are enough to preserve identity while the rest of the product evolves.

---

## 17. Recommended next design layer
After the constitution, the next natural layer is:

# Product Operating System Model

Question:
Given the constitution, governance stack, and milestone discipline, what is the complete recurring operating cycle of the product as a living system?

Why this is next:
The constitution defines what must not drift.
The next step is to define the stable ongoing operating loop that lives within those boundaries.

---

## 18. Recommended conclusion
oh-my-hermes should be designed as a self-improving product with a constitution.

That is the right model because autonomy without constitutional boundaries eventually stops being trustworthy.

The constitution is what ensures the product can evolve aggressively without silently ceasing to be itself.
