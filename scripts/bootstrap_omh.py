#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError("Could not find repo root from current working directory")


def dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def ensure_dir(path: Path, created: list[str], existing: list[str]) -> None:
    if path.exists():
        existing.append(str(path))
        return
    path.mkdir(parents=True, exist_ok=True)
    created.append(str(path))


def ensure_lock_file(path: Path, created: list[str], existing: list[str]) -> None:
    if path.exists():
        existing.append(str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")
    created.append(str(path))


def ensure_json_file(path: Path, default_data: dict[str, Any], created: list[str], existing: list[str], validated: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing.append(str(path))
        with path.open("r", encoding="utf-8") as handle:
            json.load(handle)
        validated.append(str(path))
        return

    data = dict(default_data)
    if "updated_at" in data and data["updated_at"] is None:
        data["updated_at"] = utc_now()
    dump_json(path, data)
    created.append(str(path))
    validated.append(str(path))


def main() -> int:
    repo_root = find_repo_root(Path.cwd())
    created: list[str] = []
    existing: list[str] = []
    validated: list[str] = []

    dirs = [
        repo_root / ".hermes-flow",
        repo_root / ".hermes-flow" / "locks",
        repo_root / ".hermes-flow" / "packets",
        repo_root / ".hermes-flow" / "reports",
        repo_root / ".hermes-flow" / "checkpoints",
        repo_root / ".hermes-flow" / "snapshots",
        repo_root / "artifacts",
        repo_root / "artifacts" / "verification",
        repo_root / "artifacts" / "generated",
        repo_root / "artifacts" / "reports",
        repo_root / "memory",
        repo_root / "memory" / "evolution",
        repo_root / "scripts",
        repo_root / "tests",
    ]
    for directory in dirs:
        ensure_dir(directory, created, existing)

    for lock_file in [
        repo_root / ".hermes-flow" / "locks" / "controller.lock",
        repo_root / ".hermes-flow" / "locks" / "process.lock",
    ]:
        ensure_lock_file(lock_file, created, existing)

    defaults = OrderedDict(
        {
            "run-state.json": OrderedDict(
                {
                    "workflow_id": None,
                    "goal": "Implement and harden the recursive 回环核心 for omh itself.",
                    "workflow_stage": "governance-hardening",
                    "status": "ready",
                    "active_phase_id": None,
                    "active_task_id": None,
                    "mode": "governance-hardening",
                    "controller": "omh",
                    "last_transition": None,
                    "updated_at": None,
                }
            ),
            "verification-state.json": OrderedDict(
                {
                    "task_checks": [],
                    "phase_checks": [],
                    "integration_checks": [],
                    "artifact_checks": [],
                    "final_acceptance": [],
                    "task_review_state": {},
                    "phase_review_state": {},
                    "updated_at": None,
                }
            ),
            "artifacts-index.json": OrderedDict(
                {
                    "artifacts": [],
                    "updated_at": None,
                }
            ),
            "loop-core-state.json": OrderedDict(
                {
                    "core_name": "回环核心",
                    "operator_state": OrderedDict(
                        {
                            "state_id": "accepted-baseline",
                            "status": "accepted",
                            "summary": "Current trusted omh baseline",
                            "updated_at": None,
                        }
                    ),
                    "candidate_state": None,
                    "accepted_state_history": [],
                    "last_cycle_id": None,
                    "current_mode": "governance-hardening",
                    "observations": [],
                    "candidates": [],
                    "promotions": [],
                    "updated_at": None,
                }
            ),
        }
    )

    for filename, default_data in defaults.items():
        ensure_json_file(repo_root / ".hermes-flow" / filename, default_data, created, existing, validated)

    print(f"repo_root={repo_root}")
    print(f"created_count={len(created)}")
    for item in created:
        print(f"CREATED {item}")
    print(f"existing_count={len(existing)}")
    for item in existing:
        print(f"EXISTING {item}")
    print(f"validated_json_count={len(validated)}")
    for item in validated:
        print(f"VALIDATED {item}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
