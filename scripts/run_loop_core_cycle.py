#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any

LOOP_CORE_STATE_PATH = ".hermes-flow/loop-core-state.json"
ARTIFACTS_INDEX_PATH = ".hermes-flow/artifacts-index.json"
DEFAULT_REPORT_PATH = "artifacts/reports/latest-loop-cycle.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError("Could not find repo root from current working directory")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def append_artifact(repo_root: Path, artifact_class: str, artifact_path: str, produced_by: str) -> None:
    index_path = repo_root / ARTIFACTS_INDEX_PATH
    artifacts = load_json(index_path)
    artifacts.setdefault("artifacts", []).append(
        OrderedDict(
            {
                "artifact_id": f"artifact-{utc_now().replace(':', '').replace('-', '')}",
                "class": artifact_class,
                "path": artifact_path,
                "produced_by": produced_by,
                "created_at": utc_now(),
            }
        )
    )
    artifacts["updated_at"] = utc_now()
    dump_json(index_path, artifacts)


def next_cycle_id(loop_state: dict[str, Any]) -> str:
    prior = loop_state.get("last_cycle_id")
    if not prior:
        return "loop-cycle-001"
    prefix, number = prior.rsplit("-", 1)
    return f"{prefix}-{int(number) + 1:03d}"


def build_candidate(summary: str, classification: str, target_file: str = "", auto_apply: bool = False) -> OrderedDict:
    return OrderedDict(
        {
            "candidate_id": f"candidate-{utc_now().replace(':', '').replace('-', '')}",
            "summary": summary,
            "classification": classification,
            "target_file": target_file,
            "auto_apply": auto_apply,
            "status": "candidate_detected",
            "created_at": utc_now(),
        }
    )


def run_cycle(repo_root: Path, observation: str, candidate_summary: str, classification: str, mode: str, report_path: str) -> Path:
    loop_state_path = repo_root / LOOP_CORE_STATE_PATH
    loop_state = load_json(loop_state_path)
    cycle_id = next_cycle_id(loop_state)
    timestamp = utc_now()

    observation_record = OrderedDict(
        {
            "cycle_id": cycle_id,
            "observation": observation,
            "captured_at": timestamp,
        }
    )
    candidate_record = build_candidate(candidate_summary, classification)
    promotion_record = OrderedDict(
        {
            "cycle_id": cycle_id,
            "decision": "record_only",
            "reason": "Loop-core bootstrap keeps promotion conservative until stronger governance exists.",
            "decided_at": timestamp,
            "candidate_id": candidate_record["candidate_id"],
        }
    )

    loop_state.setdefault("observations", []).append(observation_record)
    loop_state.setdefault("candidates", []).append(candidate_record)
    loop_state.setdefault("promotions", []).append(promotion_record)
    loop_state["last_cycle_id"] = cycle_id
    loop_state["candidate_state"] = candidate_record["candidate_id"]
    loop_state["current_mode"] = mode
    loop_state["updated_at"] = timestamp
    dump_json(loop_state_path, loop_state)

    report = OrderedDict(
        {
            "cycle_id": cycle_id,
            "mode": mode,
            "observation": observation_record,
            "candidate": candidate_record,
            "promotion": promotion_record,
            "operator_state": loop_state.get("operator_state", "accepted_baseline"),
            "generated_at": timestamp,
        }
    )
    final_report_path = repo_root / report_path
    dump_json(final_report_path, report)
    append_artifact(repo_root, "loop_cycle_report", str(final_report_path), "omh-loop-core-runner-v1")
    return final_report_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one conservative 回环核心 cycle for omh.")
    parser.add_argument("--observation", required=True, help="Observed runtime or design signal.")
    parser.add_argument("--candidate-summary", required=True, help="Proposed improvement summary.")
    parser.add_argument("--classification", default="internal_operating_rule", help="Candidate classification.")
    parser.add_argument("--mode", default="governance-hardening", help="Loop operating mode.")
    parser.add_argument("--report-path", default=DEFAULT_REPORT_PATH, help="Relative path for cycle report JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = find_repo_root(Path.cwd())
    report_path = run_cycle(
        repo_root,
        observation=args.observation,
        candidate_summary=args.candidate_summary,
        classification=args.classification,
        mode=args.mode,
        report_path=args.report_path,
    )
    print(str(report_path))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
