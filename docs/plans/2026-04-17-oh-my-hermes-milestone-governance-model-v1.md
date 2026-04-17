# oh-my-hermes — Milestone Governance Model v1

## 1. Purpose
Define how **milestones govern product evolution** in oh-my-hermes.

This layer answers:
- what a milestone means in this product
- what must be reviewed at a milestone boundary
- what must be promoted, deferred, or escalated
- what must enter canonical GitHub history

This is the design layer that connects:
- ongoing autonomous learning
- governed product change
- durable public project history

---

## 2. Core design idea
A milestone should not be treated as merely:
- “some work got done”
- “time to commit”
- “a convenient git checkpoint”

It should be treated as:

**the canonical governance boundary where local learning becomes official product history.**

That is the right abstraction because oh-my-hermes is not just shipping code.
It is shipping:
- execution policy
- governance policy
- learning policy
- product contract

So milestone boundaries are where the product decides what is now officially true.

---

## 3. What a milestone is
A milestone is a **coherent product-state transition**.

A good milestone has all three:
1. a design theme
2. a governance judgment
3. a canonical history update

Examples:
- runtime contract established
- self-evolution governance established
- evidence model established
- promotion policy established
- milestone governance established

Meaning:
Milestones are not task fragments.
They are product-legible steps in the evolution of the harness.

---

## 4. Milestone boundary function
At a milestone boundary, the system should do four things conceptually.

### A. Freeze
Freeze the current design meaning of the new layer.

### B. Review
Review what was learned, what remains uncertain, and what changed in product understanding.

### C. Decide
Decide what belongs in:
- accepted product law
- backlog
- user decision queue

### D. Publish
Write the result into canonical product history.

This means a milestone is a governance event, not just a documentation event.

---

## 5. Required milestone review surfaces
Every milestone should review at least these surfaces.

### 1. Product surface
Question:
What changed in the product’s design identity?

### 2. Governance surface
Question:
What changed in what the system may decide autonomously?

### 3. Learning surface
Question:
What new lessons were formalized, and what stayed provisional?

### 4. Contract surface
Question:
Did anything change in what the user should expect from the product?

### 5. History surface
Question:
Is the Git/GitHub history now a faithful representation of the new product state?

These five surfaces make milestone review product-centered rather than implementation-centered.

---

## 6. Canonical milestone decision set
At each milestone boundary, the product should be able to classify new material into four buckets.

### Bucket A — accepted now
This becomes official product law.

### Bucket B — backlog
This is learned but not yet promoted.

### Bucket C — deferred for stronger evidence
This may matter later, but the product has not earned a judgment yet.

### Bucket D — user/product decision required
This cannot be silently absorbed into the product.

This four-bucket model prevents milestone reviews from becoming binary approve/reject exercises.

---

## 7. Relationship to backlog and promotion
Milestone governance is the place where promotion policy becomes operational.

Meaning:
- backlog can accumulate between milestones
- evidence can strengthen continuously
- but promotion into official product rule should normally be decided at milestone boundaries

This creates a healthy separation:
- **continuous learning**
- **staged formalization**

That separation is essential for product stability.

---

## 8. Relationship to Git history
For oh-my-hermes, Git history is not just engineering history.
It is part of the product governance surface.

Therefore each milestone commit should represent:
- a coherent design step
- a clear governance step
- a legible product-history boundary

Design rule:
**A milestone commit should explain what product law now exists that did not exist before.**

That is the standard for meaningful canonical history.

---

## 9. Milestone package
A proper milestone should conceptually include:

1. **design artifact(s)**
   - what new layer was defined
2. **governance judgment**
   - what was accepted vs deferred
3. **history update**
   - commit + push to canonical remote
4. **next-design edge**
   - what the new frontier now is

This makes milestones directional.
A good milestone does not only close a topic.
It establishes the next design question.

---

## 10. Good milestone shape
A good milestone should be:

### Coherent
One design theme, not random accumulation.

### Legible
A decision-maker can understand why it mattered.

### Governed
It states what is now official and what is still provisional.

### Forward-linked
It identifies the next unresolved design layer.

If one of these is missing, the milestone is weak.

---

## 11. Bad milestone anti-patterns
The model should reject these anti-patterns.

### Anti-pattern 1 — activity dump
Many changes, no clear product decision.

### Anti-pattern 2 — hidden governance
The product changed, but the milestone never states what judgment was made.

### Anti-pattern 3 — silent contract change
A milestone silently changes what the user should expect.

### Anti-pattern 4 — backlog erasure
Open uncertainty disappears instead of being explicitly carried forward.

### Anti-pattern 5 — implementation-led history
History reflects file churn, not product evolution.

These anti-patterns destroy the value of milestone discipline.

---

## 12. Milestone cadence rule
Milestones should happen on **meaning boundaries**, not arbitrary time intervals.

Recommended trigger:
A milestone is due when a new design layer becomes coherent enough to be treated as product law or product-governance structure.

Not when:
- a lot of typing happened
- a day passed
- the working tree feels large

This preserves milestone quality.

---

## 13. Milestone hierarchy
Not all milestones are equal.
Use three levels.

### Level 1 — Local refinement milestone
A narrower internal design refinement.

### Level 2 — Policy milestone
A new governance or operating-policy layer.

### Level 3 — Contract milestone
A change that affects user-facing product identity or guarantees.

Why this matters:
The higher the milestone level, the stronger the review and explanation burden should be.

---

## 14. Current recommendation for oh-my-hermes
At the current stage of this product, milestone governance should prioritize:

1. preserving a clean design sequence
2. separating accepted rules from active uncertainty
3. making GitHub history map to product learning stages
4. preventing silent drift while autonomy grows

This is more important right now than raw execution speed.
Because the product being built is the harness itself.

---

## 15. Recommended milestone review questions
At each milestone, the governing questions should be:

1. What new product layer became coherent?
2. What did we decide is now official?
3. What remains backlog rather than policy?
4. Did anything approach product-contract territory?
5. Is the GitHub history now an honest representation of that state?
6. What is the next design layer that should be addressed?

This gives the milestone review a stable operating frame.

---

## 16. Recommended next design layer
After milestone governance, the next natural design layer is:

# Product Constitution Model

Question:
What are the few top-level constitutional rules that no autonomous learning loop may silently violate?

Why this is next:
Milestone governance explains how product evolution becomes history.
A constitution explains the permanent upper bound on what that evolution is allowed to change.

---

## 17. Recommended conclusion
oh-my-hermes should treat milestones as:

**the place where autonomous learning becomes governed product history.**

That is the right model because this product is not only trying to execute well.
It is trying to evolve without losing its identity.
