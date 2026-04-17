# oh-my-hermes — Skill 2 Definition v1

## Core definition
**oh-my-hermes** is the Hermes-native autonomous project harness.

Goal:
- user provides a project objective
- Hermes drives the full path from goal -> implementation -> real acceptance
- no human intervention is required during normal operation

This is not a normal prompt skill.
It is a harness/system design for autonomous delivery.

---

## Position relative to other work
### Skill 1
A separate future skill can cover:
- how to build a locally hosted but externally accessible API/service
- deployment/exposure patterns
- reusable API-project engineering patterns

### Skill 2 = oh-my-hermes
The current primary skill is:
- the autonomous execution harness itself

Current sample project for shaping this harness:
- `xapi-image-backend`

---

## Non-negotiable design rules
### 1. Codex permission policy
Codex must start in **maximum-permission mode** by default.

Reason:
- reduce approval friction
- maximize uninterrupted autonomy
- avoid false stalls caused by permission prompts

### 2. Executor transport policy
Hermes must operate Codex through **acpx**.

Reason:
- headless/machine-callable control surface
- better fit for supervised automation than interactive OMX runtime

### 3. Context lifecycle policy
Hermes must actively manage context.

Required behavior:
- design bounded task context
- compress context when the conversation/task state becomes too large
- clear/reset when appropriate instead of carrying unnecessary history forever
- preserve required state in durable artifacts rather than relying on raw chat context alone

Reason:
- prevent drift
- prevent context bloat
- improve restartability and long-horizon execution quality

### 4. Final acceptance policy
Hermes must always perform **real final acceptance** on the production-facing surface.

Rules:
- browser-facing deliverables -> verify with browser-based acceptance
- CLI/runtime deliverables -> verify by actual runtime/command effects
- API deliverables -> verify with real requests and real returned artifacts
- do not trust implementation claims alone
- do not trust only unit tests or one-sided local checks when final real-surface validation is possible

Reason:
- completion is defined by actual end-user-visible success
- not by executor narration
- not by partial internal checks

---

## Practical harness shape
### Stage A — intake
- turn vague goal into bounded target
- discover facts automatically where possible
- freeze scope/non-goals/success criteria

### Stage B — planning
- generate executable phased plan
- define task boundaries
- define verification per task
- define recovery rules

### Stage C — supervised execution
- dispatch bounded tasks to acpx/Codex
- monitor execution
- compress/clear context when appropriate
- verify independently
- retry or diagnose failures
- continue until real acceptance passes

---

## Source of truth
The source of truth for completion is:
1. durable project state/artifacts
2. verification results
3. final real-surface acceptance

Not:
- executor self-report
- partial local-only signs
- unverified narrative progress

---

## Current priority
Current priority is **not** to productize Skill 1 first.

Current priority is:
- use `xapi-image-backend` as the live sample project
- shape and validate **oh-my-hermes** as the autonomous harness
- later extract the API-building patterns into Skill 1 if useful
