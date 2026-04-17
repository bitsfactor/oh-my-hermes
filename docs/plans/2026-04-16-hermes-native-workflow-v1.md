# Hermes-Native Workflow v1 for XAPI Image Backend

> Purpose: replace OMX-bound workflow runtime assumptions with a Hermes-native three-stage workflow that preserves the good semantics of `$deep-interview -> $ralplan -> $ralph` while making Hermes the long-term autonomous supervisor.

## 1. Executive conclusion
### Recommended answer
**Keep the 3-stage workflow shape, but reimplement it as Hermes-native control layers.**

### Final mapping
- **OMX `$deep-interview`** -> **Hermes Intake**
- **OMX `$ralplan`** -> **Hermes Plan**
- **OMX `$ralph`** -> **Hermes Execute**

### Why
This preserves the proven cognitive structure while removing dependency on:
- `.omx/` runtime contracts
- OMX-specific state files
- OMX-specific MCP/state machinery
- OMX TUI/team lifecycle assumptions

---

## 2. Design goal
### Question
What exactly are we trying to preserve, and what exactly are we trying to remove?

### Recommended answer
**Preserve workflow semantics; remove runtime coupling.**

### Preserve
1. requirement clarification before execution
2. planning before implementation
3. persistent execution until verified completion
4. explicit stop/go gates
5. evidence-based completion

### Remove
1. `.omx/*` directory assumptions
2. `omx_state` MCP dependency
3. `omx team / cancel / hud / resume / explore` runtime dependence
4. in-skill assumptions about OMX launchers
5. tight coupling between prompt skill and OMX state machine

---

## 3. Hermes-native workflow overview
### Recommended workflow
The Hermes-native stack should be:

1. **Hermes Intake**
   - turn vague user intent into a bounded spec
2. **Hermes Plan**
   - turn the bounded spec into an implementation plan + execution graph
3. **Hermes Execute**
   - run the plan task-by-task until verification passes end-to-end

### Key principle
Each stage produces an explicit artifact that becomes the input for the next stage.

---

## 4. Stage 1 — Hermes Intake
### Equivalent of
OMX `$deep-interview`

### Purpose
Convert a vague objective into an execution-ready specification.

### Intake gate: ask once, only for delivery-critical choices
Hermes should default to **one-shot autonomy**.

Before planning/execution, Hermes may ask **at most one up-front clarification turn**, and only if the unresolved choice would materially change the final delivered artifact.

Examples of delivery-critical choices:
- default production model family when multiple materially different outputs are possible
- access target: local-only vs LAN vs public Internet
- delivery surface: code only vs running service vs public endpoint

Non-critical execution details must be resolved autonomously during execution and must **not** cause mid-run user interruption.

If Hermes can infer a reasonable default from the user goal, it should do so and record the assumption in the intake artifact.

### Exposure target must be explicit
“Externally accessible” is not precise enough for final acceptance.
The intake/plan artifacts must classify exposure as one of:
- loopback only
- LAN reachable
- public Internet reachable
- public Internet reachable with domain/TLS

Hermes must not treat LAN verification as completion for a public Internet delivery goal.

### Recommended output artifact
```text
docs/plans/YYYY-MM-DD-intake-spec-v1.md
```

### Required sections
- task statement
- desired outcome
- why this matters
- in-scope
- out-of-scope
- constraints
- decision boundaries
- assumptions
- testable success criteria
- open risks

### Important difference from OMX
Do **not** write to:
- `.omx/context/`
- `.omx/interviews/`
- `.omx/specs/`

Instead, keep the artifact in repo-visible planning docs.

---

## 5. Stage 2 — Hermes Plan
### Equivalent of
OMX `$ralplan`

### Delivery-critical decision freeze
Before the execute loop starts, Hermes must freeze any unresolved delivery-critical choices in the run state / intake artifact.

Required frozen fields:
- target delivery surface
- target exposure level: loopback / LAN / public Internet / public Internet + TLS
- default production model or model family
- final acceptance URL/endpoint expectations when network exposure is part of the goal

If one of these is still ambiguous and cannot be safely inferred, Hermes may ask one up-front question. After that, execution should proceed autonomously.

### Interrupt policy
During execution, Hermes should not interrupt the user for routine implementation choices, runtime failures, or recoverable integration issues.
Those must be handled inside the execution loop.

User interruption is allowed only for:
- missing credentials/resources that Hermes cannot obtain
- delivery-critical ambiguity not resolved during intake
- irreversible side effects outside the implied task scope

### Recommended output artifact
```text
docs/plans/YYYY-MM-DD-implementation-plan-v1.md
```

### Required sections
- phase list
- task list
- file paths likely touched
- input/output per phase
- verification commands
- acceptance criteria per phase
- failure recovery rules
- executor guidance for each task

### Important difference from OMX
Hermes Plan should not assume handoff to `$ralph` or `$team`.
It should hand off to **Hermes Execute**.

---

## 6. Stage 3 — Hermes Execute
### Equivalent of
OMX `$ralph`

### Purpose
Execute the approved plan until it is truly done, with verification and recovery loops.

### Final acceptance rule
Hermes Execute must validate the **actual requested delivery level**, not the nearest partial success.

Examples:
- If the goal is public Internet access, LAN-only verification is insufficient.
- If the goal is a production-default model, a temporary fallback model is insufficient unless explicitly frozen during intake.
- If the goal is final handoff, internal smoke success alone is insufficient without the requested user-facing surface.

### Recommended responsibilities
- load current run state
- choose next task
- dispatch acpx/Codex with bounded context
- run verification independently
- classify failures
- retry or diagnose
- manage background processes
- persist state for resume
- stop only when final acceptance is green at the requested delivery level

### Verification cadence carried from execution design
Hermes Execute must enforce both:
- **per-code-change review**: minimum 3 real review/fix rounds before a code-writing task can close
- **per-phase review**: minimum 5 real review rounds before a phase can close

If any current review still reports a blocking bug, execution continues and the task/phase stays open.

### Important difference from OMX
This is not a prompt-only persistence loop. It is a **supervisor-controlled runtime loop**.

---

## 7. New state model
### Question
What replaces `.omx/`?

### Recommended answer
**Use repo-local Hermes-owned workflow state.**

### Recommended state root
```text
.hermes-flow/
```

### Recommended files
```text
.hermes-flow/
  run-state.json
  intake-state.json
  task-graph.json
  verification-state.json
  incidents.json
  process-state.json
  artifacts-index.json
```

### State meanings
#### `run-state.json`
- current workflow stage
- active phase
- active task id
- overall status
- last updated timestamp

#### `intake-state.json`
- source user goal
- intake artifact path
- ambiguity notes
- frozen scope/non-goals

#### `task-graph.json`
- all tasks
- dependency edges
- status per task
- retry counts
- executor assignment metadata

#### `verification-state.json`
- task-level verification results
- integration verification results
- final acceptance results

#### `incidents.json`
- repeated failures
- diagnosis records
- blocked conditions
- escalation triggers

#### `process-state.json`
- running API server pid/session
- running ComfyUI pid/session
- port bindings
- readiness status

#### `artifacts-index.json`
- generated images
- smoke-test outputs
- log snapshots
- failure captures

---

## 8. New artifact layout
### Recommended directories
```text
docs/plans/
  YYYY-MM-DD-product-spec-v1.md
  YYYY-MM-DD-technical-design-v1.md
  YYYY-MM-DD-autonomous-execution-design-v1.md
  YYYY-MM-DD-intake-spec-v1.md
  YYYY-MM-DD-implementation-plan-v1.md

.hermes-flow/
  *.json

artifacts/
  smoke/
  verification/
  failures/
  generated/
```

### Why
This keeps planning, state, and outputs separate and observable.

---

## 9. Hermes Intake design rules
### Recommended rules
1. ask only the highest-leverage unresolved question
2. do not ask for facts that tools can discover
3. stop intake only when scope/non-goals/decision boundaries are explicit enough
4. freeze the result into a document before planning
5. if ambiguity remains but a default exists, record the default instead of stalling

### Success condition
The output spec is precise enough that Hermes Plan can proceed without asking foundational questions again.

---

## 10. Hermes Plan design rules
### Recommended rules
1. every phase must have a concrete deliverable
2. every task must have a verification method
3. every task must have bounded scope
4. file paths should be explicit whenever possible
5. default to serial execution unless non-overlap is clear
6. define real acceptance criteria, not vague prose

### Success condition
Hermes Execute can run the plan mechanically without inventing missing structure.

---

## 11. Hermes Execute design rules
### Recommended rules
1. execute one write-conflicting task at a time
2. always verify independently after executor claims success
3. capture command output for failures
4. use bounded retries
5. switch to diagnosis mode on repeated failure
6. persist state after every meaningful transition
7. manage background services as supervised processes
8. require final end-to-end proof before declaring done

### Success condition
The workflow can survive interruption, resume later, and still converge.

---

## 12. acpx/Codex integration contract
### Question
How should Hermes talk to the coding executor?

### Recommended answer
**Hermes should send task-bounded execution packets to acpx/Codex.**

### Required packet fields
- task id
- objective
- allowed file scope
- constraints
- required tests/commands
- expected deliverable summary
- stop conditions

### Why
This prevents executor drift and keeps Hermes in control.

---

## 13. Verification contract
### Question
What is the source of truth for progress?

### Recommended answer
**Verification state, not executor narration.**

### Required verification layers
1. static sanity
2. task-level tests
3. integration checks
4. live API checks
5. artifact validation
6. final acceptance checklist

### Rule
If verification did not pass, progress is not real.

---

## 14. Failure-handling contract
### Recommended answer
**Hermes owns failure classification and recovery policy.**

### Required flow
1. capture failure evidence
2. classify failure type
3. choose smallest repair action
4. retry within cap
5. enter diagnosis mode if repeating
6. replan only when architecture mismatch is proven

### Why
This is the main thing a true supervisor adds beyond a coding agent loop.

---

## 15. Process supervision contract
### Recommended answer
**All long-lived runtime components must be explicitly supervised by Hermes.**

### Covered components
- FastAPI app
- ComfyUI backend
- optional public tunnel/proxy

### Required checks
- alive
- port open
- readiness endpoint good
- logs not obviously broken

### Rule
Process existence is necessary but not sufficient; readiness must also pass.

---

## 16. Recovery and resume contract
### Recommended answer
**Every stage must be restartable from files, not dependent on chat memory.**

### Required behavior
On restart, Hermes should be able to:
- read `run-state.json`
- determine current stage
- determine current incomplete task
- inspect recent incidents
- inspect running processes
- continue from the last verified point

### Why
This is essential for 24/7 autonomy.

---

## 17. What to reuse conceptually from OMX
### Reuse
#### from `deep-interview`
- ambiguity reduction mindset
- explicit non-goals
- decision-boundary capture
- intent-first clarification

#### from `ralplan`
- plan-before-execute discipline
- structured planning
- explicit tradeoff handling
- execution handoff artifact

#### from `ralph`
- persistence until verified completion
- no fake done
- retry/fix loop
- evidence-based closure

### Do not reuse directly
- OMX path layout
- OMX state commands
- OMX launch/runtime assumptions
- OMX-specific cleanup semantics

---

## 18. Proposed Hermes-native command semantics
### Recommended future naming
If you later formalize these as commands/skills, use names that express function rather than OMX heritage.

### Recommended names
- **`/intake`** = requirements clarification
- **`/plan`** = planning and task graph generation
- **`/execute`** = autonomous delivery loop

### Optional aliases
If you want continuity with OMX-era mental models, aliases are fine:
- `/intake` alias: `/deep-interview`
- `/plan` alias: `/ralplan`
- `/execute` alias: `/ralph`

### Recommended policy
Keep aliases only as a migration bridge; make Hermes-native names the canonical ones.

---

## 19. Final recommended long-term architecture
### Recommended answer
The long-term system should be:

- **Hermes Intake** for clarification
- **Hermes Plan** for decomposition and execution design
- **Hermes Execute** for persistent supervisor-driven implementation
- **acpx/Codex** for bounded coding work
- **repo-local Hermes flow state** for durability
- **verification gates** for truth

This gives you the same high-level workflow shape as OMX, but with the control plane owned by Hermes.

---

## 20. Direct answer to the original question
### Question
Do we still need to use OMX’s `deep-interview`, `ralplan`, and `ralph` skills?

### Recommended answer
**No as a long-term dependency. Yes only as a temporary reference or migration scaffold.**

### Best practice
- borrow the workflow pattern
- do not depend on OMX runtime assumptions
- rebuild the workflow as Hermes-native artifacts + state + verification loops

---

## 21. What should happen next
Now that the workflow design is pinned, the next concrete document should be:

**`docs/plans/2026-04-16-implementation-plan-v1.md`**

But it should be written specifically for:
- Hermes Intake artifacts
- Hermes Plan outputs
- Hermes Execute runtime semantics
- `.hermes-flow/` state ownership
- acpx/Codex task packets
- explicit verification and recovery gates
