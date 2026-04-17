# oh-my-hermes — Evolution Evidence Model v1

## 1. Purpose
Define the design standard for **what evidence is sufficient** for oh-my-hermes to treat a runtime observation as a product-worthy evolution candidate.

This layer sits between:
- raw execution experience
- governance decision
- product change

Its purpose is to stop the system from evolving based on noise, isolated anecdotes, or accidental local conditions.

---

## 2. Core design question
The question is not:
- can the system patch itself?

The real question is:
- **when does observed execution evidence deserve to change the product?**

That is the difference between:
- a clever autonomous tool
and
- a stable self-improving product.

---

## 3. Design principle
A runtime observation should become a product evolution candidate only when it has enough evidence to be interpreted as one of the following:

1. **repeated structural friction**
2. **repeated recovery pattern**
3. **repeated governance gap**
4. **repeated verification blind spot**
5. **repeated operator-facing ambiguity**

Meaning:
The evidence model should favor **patterns** over anecdotes.

---

## 4. Five evidence dimensions
Every evolution candidate should be evaluated across five dimensions.

### A. Recurrence
Question:
Has this happened once, or is it recurring?

Interpretation:
- one-off event -> weak evidence
- repeated event across tasks/phases/projects -> strong evidence

Why it matters:
Product evolution should track durable patterns, not isolated accidents.

### B. Scope
Question:
What layer of the product does this affect?

Scopes:
- task-local behavior
- phase-level orchestration
- runner policy
- memory policy
- review policy
- acceptance policy
- user contract

Why it matters:
The broader the scope, the stronger the evidence bar should be.

### C. Causality
Question:
Do we understand why this happened?

Interpretation:
- symptom only -> weak
- mechanism understood -> strong

Why it matters:
Without causality, the system risks patching symptoms instead of improving the product.

### D. Risk
Question:
What is the downside if the inferred improvement is wrong?

Risk bands:
- low: internal clarity / documentation / bounded guardrails
- medium: workflow or policy refinements with operational impact
- high: changes affecting completion semantics, interruption policy, acceptance, or user contract

Why it matters:
Higher-risk changes require stronger evidence and tighter governance.

### E. Transferability
Question:
Is this insight specific to one repo/run, or is it reusable across future runs?

Interpretation:
- local-only quirk -> weak product candidate
- reusable harness lesson -> strong product candidate

Why it matters:
oh-my-hermes should evolve around reusable control intelligence, not sample-project accidents.

---

## 5. Canonical evidence grades
Recommended evidence grades:

### Grade 0 — Observation only
- single occurrence
- low understanding
- unclear transferability

Action:
- do not change product
- record only if useful

### Grade 1 — Plausible candidate
- useful observation
- bounded scope
- some understanding
- not yet clearly recurring

Action:
- record in backlog
- do not auto-apply by default

### Grade 2 — Strong candidate
- repeated or clearly structural
- mechanism understood
- low-to-medium risk
- likely transferable

Action:
- eligible for governed auto-upgrade if it stays within internal refinement boundaries

### Grade 3 — Contract-shaping evidence
- strong evidence
- broad scope
- touches product semantics, acceptance, or user interaction

Action:
- never silent auto-apply
- must go through user decision or explicit product-level design review

---

## 6. Candidate schema at the design level
A mature evolution candidate should conceptually contain:

- **source_context**
  - where the signal came from
- **pattern_type**
  - friction / recovery / governance gap / blind spot / ambiguity
- **recurrence_level**
  - isolated / repeated / systemic
- **affected_scope**
  - task / phase / runner / memory / review / acceptance / contract
- **causal_confidence**
  - weak / medium / strong
- **risk_level**
  - low / medium / high
- **transferability**
  - local / likely reusable / canonical
- **recommended_action**
  - record / auto-upgrade / ask user
- **relationship_to_existing_rules**
  - new refinement / clarification / replacement / supersession

This schema is important not because of its exact fields, but because it forces the system to justify product evolution in structured terms.

---

## 7. Design rule for repetition
The system should distinguish three repetition classes.

### Class A — Same issue repeated inside one task chain
Meaning:
Likely an execution or context-management weakness.

### Class B — Same issue repeated across multiple phases of one project
Meaning:
Likely a harness-policy weakness.

### Class C — Same issue repeated across different projects
Meaning:
Likely a true product-level evolution signal.

Interpretation:
The same symptom means different things depending on repetition horizon.

---

## 8. Evidence vs governance relationship
The evidence model should not replace governance.
It should feed governance.

Relationship:
- evidence answers: **how believable is this candidate?**
- governance answers: **what may the product do with it?**

So:
- weak evidence + low risk -> usually record only
- strong evidence + bounded internal scope -> can auto-upgrade
- strong evidence + contract impact -> must ask user

This keeps autonomy and product control separated cleanly.

---

## 9. Product learning loop
The intended learning loop becomes:

1. execution produces signal
2. signal is turned into candidate
3. candidate is enriched with evidence semantics
4. governance classifies allowed action
5. product artifact is changed or backlog is updated
6. later runs either reinforce or supersede that learning

This is better than a naive loop of:
- saw something
- patched something

Because it creates cumulative product intelligence instead of reactive mutation.

---

## 10. What should count as strong evidence first
Recommended first-class evidence sources:

1. **repeated recovery actions**
   - if the harness keeps fixing the same class of issue, the product probably lacks a rule

2. **repeated review findings**
   - if review repeatedly catches the same failure mode, the product likely needs a stronger guardrail

3. **repeated acceptance mismatches**
   - if execution often thinks it is done but final acceptance disagrees, the product likely needs a clearer completion rule

4. **repeated user clarification pressure**
   - if the system repeatedly reaches the same user-facing ambiguity, intake/plan design is incomplete

5. **repeated backlog clustering**
   - if backlog items cluster around the same theme, they may deserve promotion into product policy

These are better signals than isolated implementation trivia.

---

## 11. Anti-patterns
The evidence model should explicitly reject these anti-patterns.

### Anti-pattern 1 — One clever run becomes product law
A single successful improvisation is not enough evidence.

### Anti-pattern 2 — Local environment quirks become universal rules
Sample-project accidents must not become product-wide defaults.

### Anti-pattern 3 — Pain-driven overfitting
A frustrating bug can feel important without being broadly reusable.

### Anti-pattern 4 — Silent contract drift
Even strong evidence must not silently rewrite what the user believes the product guarantees.

---

## 12. Maturity target
The real maturity target is not “more self-patching.”
It is:

**evidence-backed product learning**

That means the system becomes trustworthy not because it changes often, but because it changes for reasons that are legible, structured, and governable.

---

## 13. Recommended next design consequence
Once this evidence model exists, the next design layer should be:

# Evolution Promotion Policy

Question:
When do repeated backlog patterns graduate into accepted product rules?

Why this is next:
The evidence model explains how to judge a candidate.
The promotion policy explains how accumulated evidence changes the product roadmap.

---

## 14. Recommended conclusion
oh-my-hermes should not evolve on raw experience.
It should evolve on **interpreted evidence**.

That is the design move that turns self-evolution from an automation trick into a real product discipline.
