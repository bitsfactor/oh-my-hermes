# oh-my-hermes — Evolution Promotion Policy v1

## 1. Purpose
Define **when accumulated evolution evidence should graduate** from backlog observations into accepted product policy.

This layer sits above:
- evolution governance
- evolution evidence evaluation

It answers the product question:

**When does repeated learning become official product behavior?**

---

## 2. Core design problem
A self-improving system fails in two opposite ways if promotion is not designed explicitly.

### Failure mode A — under-promotion
The system keeps learning the same lesson, but never upgrades the product.

Result:
- backlog grows
- repeated friction remains
- learning stays descriptive, not operational

### Failure mode B — over-promotion
The system promotes every strong-looking lesson too quickly.

Result:
- product rules churn
- local project quirks become global policy
- the product becomes unstable and overfit

So the promotion problem is not about whether a candidate is interesting.
It is about whether the product has earned the right to treat it as a rule.

---

## 3. Promotion principle
The default principle should be:

**Promote patterns, not incidents.**

A backlog item should become product policy only when all three are true:
1. the evidence is structurally credible
2. the lesson is reusable beyond the immediate run
3. promotion reduces future ambiguity, failure, or operator burden

This makes promotion a product-discipline act, not a convenience act.

---

## 4. Three-layer learning model
The product learning stack should now be understood as:

1. **Candidate**
   - one interpreted possible lesson
2. **Backlog pattern**
   - repeated or clustered candidates that indicate a stable theme
3. **Promoted rule**
   - an accepted product policy or contract refinement

Key design point:
A candidate is not yet a backlog pattern.
A backlog pattern is not yet a product rule.

Promotion is the transition from level 2 to level 3.

---

## 5. Promotion triggers
A backlog theme should become promotion-eligible when one or more of these occur.

### A. Repetition trigger
The same learning theme recurs across:
- multiple tasks
- multiple phases
- or multiple projects

Meaning:
The signal is no longer anecdotal.

### B. Cost trigger
The same missing rule keeps causing wasted cycles.

Examples of cost:
- repeated retries
- repeated review failures
- repeated unclear acceptance states
- repeated user clarifications
- repeated recovery actions

Meaning:
Even if recurrence count is still modest, the economic cost of not promoting is already visible.

### C. Governance trigger
The same class of candidate keeps landing in `record_only` because the product lacks a more explicit rule.

Meaning:
The system is repeatedly learning something, but governance lacks a container for it.

### D. Operator-friction trigger
The same ambiguity keeps surfacing at the decision-maker layer.

Meaning:
The product is forcing avoidable product decisions to recur.

---

## 6. Promotion thresholds
Promotion should not be binary by default.
Use three thresholds.

### Threshold 1 — retain in backlog
Use when:
- evidence exists
- but recurrence or transferability is still weak

Meaning:
Keep learning, do not formalize yet.

### Threshold 2 — promote to internal policy
Use when:
- pattern is strong
- risk is low or medium
- the change is an internal harness refinement

Meaning:
The product may update its own operating rule.

### Threshold 3 — promote to product contract review
Use when:
- pattern is strong
- scope is broad
- the lesson touches user expectations, acceptance semantics, interruption policy, or delivery contract

Meaning:
Promotion is real, but it belongs at product-governance level, not silent autonomy.

---

## 7. Promotion classes
Recommended promotion classes:

### Class I — Internal operating rule
Examples:
- stronger verification guardrails
- clearer review discipline
- better dependency recovery defaults
- stronger memory hygiene

Default handling:
- may be promoted autonomously when evidence is strong enough

### Class II — Control-plane policy
Examples:
- changed correction thresholds
- changed evidence grading heuristics
- changed promotion thresholds

Default handling:
- stricter review than Class I
- can still be autonomous only when clearly bounded and non-contractual

### Class III — Product contract rule
Examples:
- redefining “done”
- redefining when the user is interrupted
- redefining acceptance or exposure semantics
- redefining how historical work is treated

Default handling:
- never silent promotion
- requires explicit product decision

---

## 8. Promotion evidence package
Before promotion, the system should conceptually be able to state:

- what recurring pattern was observed
- where it recurred
- what cost it created
- why the current product rule was insufficient
- why the proposed promoted rule is reusable
- what risk comes from formalizing it
- whether the promotion changes internal operation or external product contract

This package matters because promotion is more serious than candidate recording.
It is the point where the product begins to redefine itself.

---

## 9. Clustering design
Backlog should not be treated as a flat list.
It should conceptually support clustering by theme.

Recommended cluster types:
- verification gaps
- review gaps
- dependency-recovery gaps
- acceptance-definition gaps
- context-management gaps
- operator-ambiguity gaps
- self-evolution-governance gaps

Why clustering matters:
Promotion should usually happen at the **theme level**, not the individual note level.

A single note is weak.
A cluster is product learning.

---

## 10. Promotion timing
Promotion should happen at deliberate boundaries, not continuously.

Recommended moments:
- milestone completion
- phase completion
- post-incident review boundary
- explicit product-hardening pass

Why:
If promotion happens in the middle of active execution loops, the product can mutate while it is still trying to interpret the current run.

Design rule:
**Learning may be continuous; promotion should be staged.**

---

## 11. Relationship to GitHub milestone discipline
Because this project uses milestone-based GitHub submission, promotion should align with milestone boundaries.

Meaning:
- milestone = product learning checkpoint
- promoted rules should enter Git history at those boundaries
- backlog accumulation can happen continuously
- formal policy promotion should be visible as milestone-grade product evolution

This is important because product memory and product history should stay aligned.

---

## 12. Anti-patterns
The promotion policy should reject these anti-patterns.

### Anti-pattern 1 — Promote because it feels elegant
Elegance is not enough evidence.

### Anti-pattern 2 — Promote because one run was painful
Pain is not the same as product-level recurrence.

### Anti-pattern 3 — Promote implementation convenience into product law
Convenient local behavior should not silently become general policy.

### Anti-pattern 4 — Promote mid-flight
Do not let the product rewrite its own operating law in the middle of unstable execution unless the change is narrowly internal and clearly safe.

---

## 13. Maturity target
A mature oh-my-hermes should eventually be able to do four things distinctly:

1. detect candidate lessons
2. score their evidence
3. cluster them into backlog themes
4. promote only the right themes into product rules

That is the real path from:
- self-editing system
into
- disciplined self-improving product.

---

## 14. Recommended next design layer
After promotion policy, the natural next design problem is:

# Milestone Governance Model

Question:
At each milestone, what exactly must be reviewed, promoted, committed, and pushed so that product evolution stays legible?

Why this is next:
Promotion policy explains **when learning deserves formalization**.
Milestone governance explains **how that formalization enters canonical product history**.

---

## 15. Recommended conclusion
oh-my-hermes should not treat backlog as a graveyard of observations.
It should treat backlog as a **staging area for future product law**.

But promotion must be earned.

That is the design rule that keeps self-improvement from degrading into self-drift.
