# oh-my-hermes — Bootstrap & Control-Plane Skeleton v1

## 1. Purpose
This document defines the **first concrete repository skeleton** needed to turn oh-my-hermes from runtime contract into an implementable control plane.

Goal:
- define the minimum durable files and directories
- define what must be created at bootstrap time
- define what the first runner/bootstrap script must do
- define the first executable loop boundary

This is the point where the harness stops being just a design and starts becoming repo-owned machinery.

---

## 2. Bootstrap objective
The first bootstrap must create a control plane that can:
1. initialize durable workflow state
2. represent a project goal and current stage
3. represent a phased task graph
4. write task packets for acpx/Codex
5. record verification outcomes
6. record incidents and process metadata
7. resume safely after interruption

If these are not materialized, oh-my-hermes is still only conceptual.

---

## 3. Required repository skeleton
### Recommended layout
```text
.hermes-flow/
  run-state.json
  intake-state.json
  task-graph.json
  verification-state.json
  incidents.json
  process-state.json
  artifacts-index.json
  locks/
    controller.lock
    process.lock
  packets/
  reports/
  checkpoints/
  snapshots/

artifacts/
  smoke/
  verification/
  failures/
  generated/
  browser/

scripts/
  bootstrap_oh_my_hermes.py
```

---

## 4. Minimum bootstrap deliverables
### 4.1 Durable state files
Bootstrap must create all top-level `.hermes-flow/*.json` files if missing.

### 4.2 Runtime directories
Bootstrap must create:
- `locks/`
- `packets/`
- `reports/`
- `checkpoints/`
- `snapshots/`

### 4.3 Artifact directories
Bootstrap must create:
- `artifacts/smoke/`
- `artifacts/verification/`
- `artifacts/failures/`
- `artifacts/generated/`
- `artifacts/browser/`

### 4.4 First script
Bootstrap must provide one first control script:
- `scripts/bootstrap_oh_my_hermes.py`

This script does **not** need to execute the whole harness yet.
It only needs to create and normalize the control-plane substrate.

---

## 5. Initial file contents
### 5.1 `run-state.json`
Minimum initial shape:
```json
{
  "workflow_id": null,
  "goal": null,
  "workflow_stage": "idle",
  "status": "idle",
  "active_phase_id": null,
  "active_task_id": null,
  "mode": null,
  "controller": null,
  "last_transition": null,
  "updated_at": null
}
```

### 5.2 `intake-state.json`
```json
{
  "goal_summary": null,
  "source_prompt": null,
  "scope": [],
  "non_goals": [],
  "constraints": [],
  "success_criteria": [],
  "open_risks": [],
  "frozen": false,
  "updated_at": null
}
```

### 5.3 `task-graph.json`
```json
{
  "plan_version": null,
  "phases": [],
  "updated_at": null
}
```

### 5.4 `verification-state.json`
```json
{
  "task_checks": [],
  "phase_checks": [],
  "integration_checks": [],
  "artifact_checks": [],
  "final_acceptance": [],
  "updated_at": null
}
```

### 5.5 `incidents.json`
```json
{
  "incidents": [],
  "updated_at": null
}
```

### 5.6 `process-state.json`
```json
{
  "processes": [],
  "updated_at": null
}
```

### 5.7 `artifacts-index.json`
```json
{
  "artifacts": [],
  "updated_at": null
}
```

---

## 6. Bootstrap script contract
### Required responsibilities
`bootstrap_oh_my_hermes.py` must:
1. detect repo root
2. create missing directories
3. create missing JSON files with default content
4. preserve existing files if already present
5. validate that all required files are readable JSON
6. print a compact summary of created vs existing items

### Required non-behavior
It must **not** yet:
- dispatch Codex
- modify project code outside bootstrap/control-plane setup
- invent a plan automatically
- run final acceptance

This is a substrate initializer, not the full harness runner.

---

## 7. First runner boundary
After bootstrap exists, the next runner can be narrowly defined as:

**`oh-my-hermes-runner-v1` responsibilities**
1. load goal + current durable state
2. ensure bootstrap substrate exists
3. choose next stage
4. write one bounded task packet
5. dispatch one supervised task through acpx/Codex
6. run one verification pass
7. persist new state

This defines the smallest real autonomous loop worth implementing.

---

## 8. Locking skeleton
### Required initial lock files
- `controller.lock`
- `process.lock`

### Initial policy
At bootstrap time these may be empty placeholders.

### Later policy
They will later hold:
- owner/session metadata
- timestamp
- stale-lock recovery hints

---

## 9. Context-management integration points
Bootstrap must prepare places for context lifecycle outputs.

### Why these directories exist now
- `snapshots/` -> compact durable summaries before compress/clear
- `reports/` -> executor/verification summaries used for resume
- `checkpoints/` -> explicit recovery points between phases or major transitions

This ensures context compression/clear will later be file-backed, not memory-only.

---

## 10. Acceptance integration points
The bootstrap skeleton must already reserve evidence locations for final acceptance.

### Required evidence buckets
- `artifacts/browser/` for browser validation captures
- `artifacts/smoke/` for smoke-run outputs
- `artifacts/verification/` for structured check results
- `artifacts/failures/` for failure evidence
- `artifacts/generated/` for returned/generated artifacts

Rule:
Real acceptance evidence must have durable storage from day one.

---

## 11. Validation of bootstrap itself
The bootstrap step is complete only if all of the following are true:
- all required directories exist
- all required JSON files exist
- all JSON files parse successfully
- rerunning bootstrap is idempotent
- bootstrap does not overwrite non-empty valid state accidentally
- bootstrap summary clearly reports created/existing items

---

## 12. Current next concrete implementation step
The next repo action after this document should be:

1. create `.hermes-flow/` skeleton
2. create `artifacts/` evidence directories
3. create `scripts/bootstrap_oh_my_hermes.py`
4. run the bootstrap script
5. verify the initialized substrate from the real filesystem

That is the first step where oh-my-hermes becomes partially real.
