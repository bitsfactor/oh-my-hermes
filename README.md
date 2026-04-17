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
- `scripts/run_loop_core_cycle.py` runs one conservative recursive loop cycle
- `tests/test_loop_core.py` verifies bootstrap + one loop-cycle report end to end

This is not the full product yet.
It is the first repo-owned executable proof that omh can begin to operate on omh through a governed recursive loop.
