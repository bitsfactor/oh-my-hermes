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
VERIFICATION_STATE_PATH = ".hermes-flow/verification-state.json"
RUN_STATE_PATH = ".hermes-flow/run-state.json"
DEFAULT_REPORT_PATH = "artifacts/reports/latest-loop-cycle.json"
DEFAULT_EVIDENCE_REPORT_PATH = "artifacts/reports/latest-execution-evidence.json"
PROMOTION_LADDER = {
    "record_only",
    "internal_promotion",
    "milestone_promotion_required",
    "user_decision_required",
}
ALLOWED_CLASSIFICATIONS = {
    "internal_operating_rule",
    "control_plane_policy",
    "product_contract_rule",
}
MINIMUM_DECISION_RANK = {
    "record_only": 0,
    "internal_promotion": 1,
    "milestone_promotion_required": 2,
    "user_decision_required": 3,
}
CLASSIFICATION_MINIMUM_DECISION = {
    "internal_operating_rule": "internal_promotion",
    "control_plane_policy": "milestone_promotion_required",
    "product_contract_rule": "user_decision_required",
}


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


def normalize_loop_state(loop_state: dict[str, Any]) -> dict[str, Any]:
    if isinstance(loop_state.get("operator_state"), str):
        loop_state["operator_state"] = OrderedDict(
            {
                "state_id": loop_state["operator_state"],
                "status": "accepted",
                "summary": "Migrated accepted baseline",
                "updated_at": loop_state.get("updated_at"),
            }
        )
    loop_state.setdefault("accepted_state_history", [])
    loop_state.setdefault("observations", [])
    loop_state.setdefault("candidates", [])
    loop_state.setdefault("promotions", [])
    return loop_state


def classify_promotion(classification: str, requested_decision: str | None) -> tuple[str, str]:
    if classification not in ALLOWED_CLASSIFICATIONS:
        raise ValueError(f"Unsupported classification: {classification}")
    minimum_decision = CLASSIFICATION_MINIMUM_DECISION[classification]
    if requested_decision:
        if requested_decision not in PROMOTION_LADDER:
            raise ValueError(f"Unsupported promotion decision: {requested_decision}")
        if MINIMUM_DECISION_RANK[requested_decision] < MINIMUM_DECISION_RANK[minimum_decision]:
            raise ValueError(
                f"Requested promotion decision {requested_decision} violates minimum governance boundary {minimum_decision} for {classification}"
            )
        return requested_decision, "Explicit decision requested by operator."

    if classification == "product_contract_rule":
        return "user_decision_required", "Contract-level candidates must not silently promote."
    if classification == "control_plane_policy":
        return "milestone_promotion_required", "Control-plane policy changes require milestone review."
    return "internal_promotion", "Internal operating rule is eligible for autonomous internal promotion."


def validate_cycle_request(repo_root: Path, classification: str, requested_decision: str | None, report_path: str, evidence_path: str | None = None, evidence_report_path: str | None = None) -> None:
    repo_root_resolved = repo_root.resolve()
    classify_promotion(classification, requested_decision)
    candidate_paths = [(repo_root / report_path).resolve()]
    if evidence_path is not None:
        candidate_paths.append((repo_root / evidence_path).resolve())
    if evidence_report_path is not None:
        candidate_paths.append((repo_root / evidence_report_path).resolve())
    for candidate_path in candidate_paths:
        if not candidate_path.is_relative_to(repo_root_resolved):
            raise ValueError(f"Path escapes repo root: {candidate_path}")


def build_candidate(summary: str, classification: str, target_file: str = "", auto_apply: bool = False, evidence: dict[str, Any] | None = None) -> OrderedDict:
    candidate = OrderedDict(
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
    if evidence is not None:
        candidate["evidence"] = evidence
    return candidate


def summarize_task_review_state(task_review_state: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_ids": sorted(task_review_state.keys()),
        "has_reviews": bool(task_review_state),
        "all_clear": bool(task_review_state) and all(bool(item.get("latest_clear", False)) for item in task_review_state.values()),
        "max_round_count": max((int(item.get("round_count", 0)) for item in task_review_state.values()), default=0),
        "blocking_bug_count": sum(len(item.get("latest_blocking_bugs", [])) for item in task_review_state.values()),
    }


def summarize_phase_review_state(phase_review_state: dict[str, Any]) -> dict[str, Any]:
    return {
        "phase_ids": sorted(phase_review_state.keys()),
        "has_reviews": bool(phase_review_state),
        "all_clear": bool(phase_review_state) and all(bool(item.get("latest_clear", False)) for item in phase_review_state.values()),
        "max_round_count": max((int(item.get("round_count", 0)) for item in phase_review_state.values()), default=0),
        "blocking_bug_count": sum(len(item.get("latest_blocking_bugs", [])) for item in phase_review_state.values()),
    }


def ingest_execution_evidence(repo_root: Path, evidence_path: str, report_path: str) -> tuple[OrderedDict, Path]:
    source_path = (repo_root / evidence_path).resolve()
    evidence = load_json(source_path)
    summary_bits: list[str] = []
    if evidence.get("task_id"):
        summary_bits.append(f"task={evidence['task_id']}")
    if evidence.get("phase_id"):
        summary_bits.append(f"phase={evidence['phase_id']}")
    if evidence.get("review_clear") is not None:
        summary_bits.append(f"review_clear={evidence['review_clear']}")
    if evidence.get("verification_passed") is not None:
        summary_bits.append(f"verification_passed={evidence['verification_passed']}")
    if evidence.get("signal"):
        summary_bits.append(f"signal={evidence['signal']}")

    ingested = OrderedDict(
        {
            "source_path": str(source_path),
            "summary": "; ".join(summary_bits) or "execution evidence ingested",
            "payload": evidence,
            "ingested_at": utc_now(),
        }
    )
    final_report_path = repo_root / report_path
    dump_json(final_report_path, ingested)
    append_artifact(repo_root, "execution_evidence_report", str(final_report_path), "omh-loop-core-runner-v1")
    return ingested, final_report_path


def build_loop_candidate_from_repo_state(repo_root: Path) -> tuple[OrderedDict, str, str, str]:
    run_state = load_json(repo_root / RUN_STATE_PATH)
    verification_state = load_json(repo_root / VERIFICATION_STATE_PATH)

    task_summary = summarize_task_review_state(verification_state.get("task_review_state", {}))
    phase_summary = summarize_phase_review_state(verification_state.get("phase_review_state", {}))
    verification_summary = OrderedDict(
        {
            "task_checks_passed": sum(1 for item in verification_state.get("task_checks", []) if item.get("result") == "pass"),
            "phase_checks_passed": sum(1 for item in verification_state.get("phase_checks", []) if item.get("result") == "pass"),
            "integration_checks_passed": sum(1 for item in verification_state.get("integration_checks", []) if item.get("result") == "pass"),
            "artifact_checks_passed": sum(1 for item in verification_state.get("artifact_checks", []) if item.get("result") == "pass"),
            "final_acceptance_passed": sum(1 for item in verification_state.get("final_acceptance", []) if item.get("result") == "pass"),
            "has_final_acceptance_evidence": bool(verification_state.get("final_acceptance", [])),
            "has_explicit_acceptance_gap": any(item.get("result") == "fail" for item in verification_state.get("final_acceptance", [])),
            "has_ambiguous_acceptance_state": any(item.get("result") not in {"pass", "fail"} for item in verification_state.get("final_acceptance", [])),
        }
    )
    evidence = OrderedDict(
        {
            "source": "repo_state",
            "run_state": OrderedDict(
                {
                    "workflow_stage": run_state.get("workflow_stage"),
                    "status": run_state.get("status"),
                    "active_phase_id": run_state.get("active_phase_id"),
                    "active_task_id": run_state.get("active_task_id"),
                    "mode": run_state.get("mode"),
                }
            ),
            "task_review_summary": task_summary,
            "phase_review_summary": phase_summary,
            "verification_summary": verification_summary,
            "captured_at": utc_now(),
        }
    )

    observation = (
        f"repo-state ingest: workflow_stage={run_state.get('workflow_stage')}; "
        f"status={run_state.get('status')}; task_blocking_bugs={task_summary['blocking_bug_count']}; "
        f"phase_blocking_bugs={phase_summary['blocking_bug_count']}"
    )

    if task_summary["blocking_bug_count"] or phase_summary["blocking_bug_count"]:
        candidate_summary = "tighten review and verification governance based on repo-state blockers"
        classification = "control_plane_policy"
    elif (
        task_summary["has_reviews"]
        and phase_summary["has_reviews"]
        and task_summary["all_clear"]
        and phase_summary["all_clear"]
        and verification_summary["has_final_acceptance_evidence"]
        and verification_summary["has_explicit_acceptance_gap"]
        and not verification_summary["has_ambiguous_acceptance_state"]
        and verification_summary["final_acceptance_passed"] == 0
    ):
        candidate_summary = "improve internal operating rule to close remaining acceptance gap"
        classification = "internal_operating_rule"
    else:
        candidate_summary = "record stable repo-state signal without changing contract semantics"
        classification = "control_plane_policy"

    return evidence, observation, candidate_summary, classification


def run_cycle(
    repo_root: Path,
    observation: str,
    candidate_summary: str,
    classification: str,
    mode: str,
    report_path: str,
    requested_decision: str | None = None,
    evidence: dict[str, Any] | None = None,
) -> Path:
    loop_state_path = repo_root / LOOP_CORE_STATE_PATH
    report_output_path = (repo_root / report_path).resolve()
    loop_state = normalize_loop_state(load_json(loop_state_path))
    cycle_id = next_cycle_id(loop_state)
    timestamp = utc_now()

    observation_record = OrderedDict(
        {
            "cycle_id": cycle_id,
            "observation": observation,
            "captured_at": timestamp,
        }
    )
    if evidence is not None:
        observation_record["evidence"] = evidence

    candidate_record = build_candidate(candidate_summary, classification, evidence=evidence)
    decision, reason = classify_promotion(classification, requested_decision)
    promotion_record = OrderedDict(
        {
            "cycle_id": cycle_id,
            "decision": decision,
            "reason": reason,
            "decided_at": timestamp,
            "candidate_id": candidate_record["candidate_id"],
        }
    )

    loop_state.setdefault("observations", []).append(observation_record)
    loop_state.setdefault("candidates", []).append(candidate_record)
    loop_state.setdefault("promotions", []).append(promotion_record)
    loop_state["last_cycle_id"] = cycle_id
    loop_state["candidate_state"] = OrderedDict(
        {
            "candidate_id": candidate_record["candidate_id"],
            "status": candidate_record["status"],
            "summary": candidate_record["summary"],
            "classification": candidate_record["classification"],
            "updated_at": timestamp,
        }
    )
    loop_state["current_mode"] = mode
    loop_state["updated_at"] = timestamp

    if decision == "internal_promotion":
        prior_operator = dict(loop_state.get("operator_state", {}))
        if prior_operator:
            loop_state.setdefault("accepted_state_history", []).append(prior_operator)
        loop_state["operator_state"] = OrderedDict(
            {
                "state_id": candidate_record["candidate_id"],
                "status": "accepted",
                "summary": candidate_record["summary"],
                "updated_at": timestamp,
            }
        )
        candidate_record["status"] = "auto_applied"
        loop_state["candidate_state"] = None

    dump_json(loop_state_path, loop_state)

    report = OrderedDict(
        {
            "cycle_id": cycle_id,
            "mode": mode,
            "observation": observation_record,
            "candidate": candidate_record,
            "promotion": promotion_record,
            "operator_state": loop_state.get("operator_state"),
            "candidate_state": loop_state.get("candidate_state"),
            "generated_at": timestamp,
        }
    )
    final_report_path = report_output_path
    dump_json(final_report_path, report)
    append_artifact(repo_root, "loop_cycle_report", str(final_report_path), "omh-loop-core-runner-v1")
    return final_report_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one governed 回环核心 cycle for omh.")
    parser.add_argument("--observation", help="Observed runtime or design signal.")
    parser.add_argument("--candidate-summary", help="Proposed improvement summary.")
    parser.add_argument("--classification", default=None, help="Candidate classification.")
    parser.add_argument("--mode", default="governance-hardening", help="Loop operating mode.")
    parser.add_argument("--report-path", default=DEFAULT_REPORT_PATH, help="Relative path for cycle report JSON.")
    parser.add_argument("--promotion-decision", choices=sorted(PROMOTION_LADDER), help="Force a promotion-ladder decision.")
    parser.add_argument("--evidence-path", help="Relative path to execution evidence JSON to ingest.")
    parser.add_argument("--evidence-report-path", default=DEFAULT_EVIDENCE_REPORT_PATH, help="Relative path for ingested evidence report JSON.")
    parser.add_argument("--ingest-repo-state", action="store_true", help="Derive observation/candidate/evidence from .hermes-flow repo state.")
    args = parser.parse_args()
    if args.ingest_repo_state:
        if args.evidence_path or args.observation or args.candidate_summary or args.promotion_decision or args.classification is not None:
            parser.error("--ingest-repo-state cannot be combined with --evidence-path, --observation, --candidate-summary, --promotion-decision, or an explicit --classification override.")
        return args
    if args.classification is None:
        args.classification = "internal_operating_rule"
    if args.evidence_path and not args.observation:
        args.observation = "execution evidence ingested"
    if args.evidence_path and not args.candidate_summary:
        args.candidate_summary = "derive loop-core improvement from ingested execution evidence"
    if not args.observation or not args.candidate_summary:
        parser.error("Either provide --observation and --candidate-summary, provide --evidence-path to auto-ingest evidence, or use --ingest-repo-state.")
    return args


def main() -> int:
    args = parse_args()
    repo_root = find_repo_root(Path.cwd())

    evidence = None
    observation = args.observation
    candidate_summary = args.candidate_summary
    classification = args.classification

    if args.ingest_repo_state:
        evidence, observation, candidate_summary, classification = build_loop_candidate_from_repo_state(repo_root)

    validate_cycle_request(
        repo_root,
        classification=classification,
        requested_decision=args.promotion_decision,
        report_path=args.report_path,
        evidence_path=args.evidence_path,
        evidence_report_path=args.evidence_report_path if args.evidence_path else None,
    )

    if args.evidence_path:
        evidence, _ = ingest_execution_evidence(repo_root, args.evidence_path, args.evidence_report_path)

    report_path = run_cycle(
        repo_root,
        observation=observation,
        candidate_summary=candidate_summary,
        classification=classification,
        mode=args.mode,
        report_path=args.report_path,
        requested_decision=args.promotion_decision,
        evidence=evidence,
    )
    print(str(report_path))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
