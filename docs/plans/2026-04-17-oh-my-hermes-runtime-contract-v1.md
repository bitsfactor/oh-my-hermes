# oh-my-hermes — Runtime Contract v1

## 1. Purpose
**oh-my-hermes** is the autonomous project harness that takes a user goal and drives it to real completion with no normal human intervention.

It is responsible for:
- intake
- planning
- supervised execution
- context management
- verification
- final production-style acceptance
- retry / diagnosis / resume

---

## 2. Core runtime loop
The default control loop is:

1. accept goal
2. discover missing facts automatically where possible
3. freeze an execution-ready target
4. generate phased plan
5. pick next runnable task
6. build bounded task packet
7. dispatch acpx -> Codex
8. inspect executor result
9. run independent verification
10. if pass -> advance state
11. if fail -> retry / diagnose / recover
12. when all planned work is complete -> run final real-surface acceptance
13. stop only when final acceptance passes

---

## 3. Non-negotiable execution policies
### 3.1 Codex launch policy
Codex must start in **maximum-permission mode** by default.

Reason:
- minimize approval stalls
- maximize uninterrupted autonomous execution

### 3.2 Transport policy
Hermes must operate Codex through **acpx**.

Reason:
- headless control
- machine-callable interface
- clean supervision boundary

### 3.3 Context policy
Hermes must actively manage context instead of letting it grow forever.

Required behavior:
- keep task packets bounded
- compress context at meaningful boundaries
- clear/reset stale working context when appropriate
- preserve important state in durable artifacts before compress/clear

### 3.4 Acceptance policy
Hermes must always perform **real final acceptance** against the production-facing surface.

Examples:
- browser product -> browser acceptance
- CLI/runtime product -> actual runtime/command acceptance
- API product -> real requests + real returned artifacts + real endpoint behavior

Rule:
- implementation claims are never enough
- unit tests alone are never enough when real-surface validation is possible

---

## 4. Runtime stages
### Stage A — Intake
Convert a vague user goal into an execution-ready target.

Required outputs:
- goal summary
- scope
- non-goals
- constraints
- success criteria
- unresolved risks

### Stage B — Plan
Turn the target into a phased execution plan.

Required outputs:
- phase list
- task list
- dependencies
- verification per task
- recovery rules
- final acceptance definition

### Stage C — Execute
Run the plan task by task under supervision.

Required behavior:
- choose next runnable task
- build bounded packet
- dispatch acpx/Codex
- verify independently
- persist progress
- retry / diagnose on failure
- continue until final acceptance passes

---

## 5. Task packet contract
Every dispatch to acpx/Codex must include:
- task id
- phase id
- objective
- allowed file scope
- relevant context docs/artifacts
- constraints
- required verification commands
- expected output summary format
- explicit stop conditions
- permission policy

Rule:
If a bounded packet cannot be written, the task is not ready.

---

## 6. Context lifecycle contract
### Compression triggers
Hermes should compress when:
- a phase completes
- a task chain produces too much narrative history
- repeated debug loops create noisy context
- enough durable artifacts exist to preserve state externally

### Clear/reset triggers
Hermes should clear/reset working context when:
- a clean handoff to the next phase is possible
- stale history is more harmful than helpful
- a new executor session should begin from durable artifacts instead of chat residue

### Before compress/clear
Hermes must first persist:
- current task state
- latest plan state
- verification results
- incident summary if failing
- required references for resume

---

## 7. Verification contract
### Task-level verification
After every meaningful execution step, Hermes must independently verify:
- changed files or artifacts exist as expected
- required tests/commands pass
- touched surface behaves as intended

### Final acceptance
Final acceptance must test the real user-facing surface.

Required rule:
If final acceptance did not run, the project is not done.

---

## 8. Failure-handling contract
### Default ladder
1. focused retry
2. second retry with explicit failure evidence
3. diagnosis mode
4. recovery action
5. replan only if architecture mismatch is proven

### Failure classes
- implementation defect
- verification defect
- environment defect
- runtime/process defect
- exposure/network defect
- context-management defect
- architecture mismatch

Rule:
Repeated failure must change strategy, not repeat blindly.

---

## 9. Resume contract
oh-my-hermes must be restartable from durable state.

On resume it must be able to determine:
- current phase
- current task
- latest verification outcome
- open incidents
- active runtime processes
- next safe action

Rule:
Resume from the latest **verified** point, not the latest narrated point.

---

## 10. Source of truth
The source of truth is:
1. durable state/artifacts
2. verification results
3. final real-surface acceptance

Not:
- Codex self-report
- partial local checks alone
- optimistic narration

---

## 11. Current validation strategy
Current live sample project for shaping this harness:
- `xapi-image-backend`

Current priority:
- validate and refine **oh-my-hermes** through real project delivery
- later extract separate project-pattern skills if useful
