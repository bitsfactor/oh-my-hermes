# oh-my-hermes

oh-my-hermes is the standalone product repository for the Hermes-native autonomous harness.

## Product role
This repository is the product root for:
- harness design
- governance design
- self-evolution design
- milestone history for the harness itself
- the first executable seed of the 回环核心

It is intentionally separate from any sample project used to validate it.

## Separation of concerns
- `oh-my-hermes` = the harness product
- sample projects such as `xapi-image-backend` = validation/dogfood projects driven by the harness

## Current design sequence
See `docs/plans/` for the current product design stack.

## Executable loop-core seed
The repo now contains the first concrete executable slice of the 回环核心:
- `scripts/bootstrap_omh.py` initializes omh's own loop-core control surface
- `scripts/run_loop_core_cycle.py` runs one governed recursive loop cycle
- `tests/test_loop_core.py` verifies bootstrap, promotion behavior, evidence-ingest behavior, and repo-state ingestion end to end

Current executable abilities:
- explicit accepted operator state vs candidate state
- promotion ladder with internal promotion / milestone review / user-decision boundaries
- evidence auto-ingest from execution-result JSON into the loop cycle
- repo-state ingest from `.hermes-flow/run-state.json` and `.hermes-flow/verification-state.json` into recursive candidate generation

This is still not the full product.
It is now a repo-owned executable proof that omh can begin to derive its own recursive improvements from real workflow-state evidence, not only hand-authored observations.
