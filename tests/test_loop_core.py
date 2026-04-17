from __future__ import annotations

import json
import subprocess
from pathlib import Path


def copy_script(repo_root: Path, script_name: str) -> None:
    source_script = Path(f"/root/projects/oh-my-hermes/scripts/{script_name}")
    target_script = repo_root / "scripts" / script_name
    target_script.parent.mkdir(parents=True, exist_ok=True)
    target_script.write_text(source_script.read_text(encoding="utf-8"), encoding="utf-8")


def bootstrap_repo(repo_root: Path) -> None:
    subprocess.run(
        ["python3", str(repo_root / "scripts" / "bootstrap_omh.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )


def test_bootstrap_omh_creates_loop_core_state(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    copy_script(repo_root, "bootstrap_omh.py")

    proc = subprocess.run(
        ["python3", str(repo_root / "scripts" / "bootstrap_omh.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "validated_json_count=5" in proc.stdout
    loop_state = json.loads((repo_root / ".hermes-flow" / "loop-core-state.json").read_text(encoding="utf-8"))
    assert loop_state["core_name"] == "回环核心"
    assert loop_state["current_mode"] == "governance-hardening"
    assert loop_state["observations"] == []
    assert loop_state["operator_state"]["state_id"] == "accepted-baseline"

    run_state = json.loads((repo_root / ".hermes-flow" / "run-state.json").read_text(encoding="utf-8"))
    assert run_state["self_evolve"]["enabled"] is True
    assert run_state["self_evolve"]["auto_apply_control_plane"] is True
    assert "governance-hardening" in run_state["self_evolve"]["autonomous_modes"]

    verification_state = json.loads((repo_root / ".hermes-flow" / "verification-state.json").read_text(encoding="utf-8"))
    assert verification_state["task_review_state"] == {}
    assert verification_state["phase_review_state"] == {}

    milestone_queue = json.loads((repo_root / ".hermes-flow" / "milestone-queue.json").read_text(encoding="utf-8"))
    assert milestone_queue["pending"] == []
    assert milestone_queue["applied"] == []


def test_run_loop_core_cycle_internal_promotion_updates_operator_state(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--observation",
            "review loop stalled because promotion boundary was unclear",
            "--candidate-summary",
            "add explicit accepted-vs-candidate governance split",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    report_path = Path(proc.stdout.strip())
    assert report_path.name == "latest-loop-cycle.json"

    loop_state = json.loads((repo_root / ".hermes-flow" / "loop-core-state.json").read_text(encoding="utf-8"))
    assert loop_state["last_cycle_id"] == "loop-cycle-001"
    assert len(loop_state["observations"]) == 1
    assert len(loop_state["candidates"]) == 1
    assert len(loop_state["promotions"]) == 1
    assert loop_state["promotions"][0]["decision"] == "internal_promotion"
    assert loop_state["operator_state"]["state_id"].startswith("candidate-")
    assert loop_state["candidate_state"] is None
    assert len(loop_state["accepted_state_history"]) == 1

    report = json.loads((repo_root / report_path).read_text(encoding="utf-8"))
    assert report["cycle_id"] == "loop-cycle-001"
    assert report["candidate"]["status"] == "auto_applied"
    assert report["candidate"]["target_surface"]

    artifacts = json.loads((repo_root / ".hermes-flow" / "artifacts-index.json").read_text(encoding="utf-8"))
    assert artifacts["artifacts"]
    assert artifacts["artifacts"][0]["class"] == "loop_cycle_report"


def test_run_loop_core_cycle_control_plane_policy_requires_milestone_review_and_queues_candidate(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--observation",
            "control-plane thresholds changed under review pressure",
            "--candidate-summary",
            "tighten promotion thresholds for control-plane rules",
            "--classification",
            "control_plane_policy",
            "--mode",
            "delivery",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    report = json.loads((repo_root / Path(proc.stdout.strip())).read_text(encoding="utf-8"))
    assert report["promotion"]["decision"] == "milestone_promotion_required"
    assert report["milestone_queue_entry"]["status"] == "pending"
    assert report["auto_applied_milestone_entry"] is None
    assert ".hermes-flow/milestone-queue.json" in report["milestone_queue_entry"]["target_surface"]

    queue = json.loads((repo_root / ".hermes-flow" / "milestone-queue.json").read_text(encoding="utf-8"))
    assert len(queue["pending"]) == 1
    assert queue["pending"][0]["candidate_id"] == report["candidate"]["candidate_id"]


def test_run_loop_core_cycle_autonomously_applies_control_plane_candidate_in_governance_hardening(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--observation",
            "control-plane autonomy should not wait for manual confirmation",
            "--candidate-summary",
            "auto-apply milestone-reviewed control-plane improvement during self evolution",
            "--classification",
            "control_plane_policy",
            "--mode",
            "governance-hardening",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    report = json.loads((repo_root / Path(proc.stdout.strip())).read_text(encoding="utf-8"))
    assert report["promotion"]["decision"] == "milestone_promotion_required"
    assert report["milestone_queue_entry"]["status"] == "pending"
    assert report["auto_applied_milestone_entry"]["status"] == "applied"
    assert report["operator_state"]["state_id"] == report["candidate"]["candidate_id"]
    assert report["candidate_state"] is None

    queue = json.loads((repo_root / ".hermes-flow" / "milestone-queue.json").read_text(encoding="utf-8"))
    assert queue["pending"] == []
    assert queue["applied"][0]["queue_id"] == report["milestone_queue_entry"]["queue_id"]


def test_review_milestone_queue_entry_accepts_candidate_and_promotes_operator_state(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    cycle_proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--observation",
            "control-plane thresholds changed under review pressure",
            "--candidate-summary",
            "tighten promotion thresholds for control-plane rules",
            "--classification",
            "control_plane_policy",
            "--mode",
            "delivery",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    cycle_report = json.loads((repo_root / Path(cycle_proc.stdout.strip())).read_text(encoding="utf-8"))
    queue_id = cycle_report["milestone_queue_entry"]["queue_id"]

    review_proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--review-milestone-queue-id",
            queue_id,
            "--review-decision",
            "accepted",
            "--review-reason",
            "milestone review approved this control-plane improvement",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    reviewed = json.loads(review_proc.stdout)
    assert reviewed["queue_id"] == queue_id
    assert reviewed["status"] == "applied"
    assert reviewed["review_decision"] == "accepted"
    assert reviewed["milestone_decision_dossier"]["artifact_type"] == "milestone_decision_dossier"
    assert reviewed["milestone_decision_dossier"]["final_disposition"] == "applied"

    queue = json.loads((repo_root / ".hermes-flow" / "milestone-queue.json").read_text(encoding="utf-8"))
    assert queue["pending"] == []
    assert len(queue["applied"]) == 1
    assert queue["applied"][0]["review_decision"] == "accepted"
    assert queue["applied"][0]["milestone_decision_dossier"]["review_reason"] == "milestone review approved this control-plane improvement"

    loop_state = json.loads((repo_root / ".hermes-flow" / "loop-core-state.json").read_text(encoding="utf-8"))
    assert loop_state["operator_state"]["state_id"] == cycle_report["candidate"]["candidate_id"]
    assert loop_state["candidate_state"] is None


def test_review_milestone_queue_entry_rejects_candidate_and_clears_candidate_state(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    cycle_proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--observation",
            "control-plane thresholds changed under review pressure",
            "--candidate-summary",
            "tighten promotion thresholds for control-plane rules",
            "--classification",
            "control_plane_policy",
            "--mode",
            "delivery",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    cycle_report = json.loads((repo_root / Path(cycle_proc.stdout.strip())).read_text(encoding="utf-8"))
    queue_id = cycle_report["milestone_queue_entry"]["queue_id"]

    review_proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--review-milestone-queue-id",
            queue_id,
            "--review-decision",
            "rejected",
            "--review-reason",
            "milestone review rejected this candidate",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    reviewed = json.loads(review_proc.stdout)
    assert reviewed["status"] == "rejected"
    assert reviewed["review_decision"] == "rejected"
    assert reviewed["milestone_decision_dossier"]["final_disposition"] == "rejected"

    queue = json.loads((repo_root / ".hermes-flow" / "milestone-queue.json").read_text(encoding="utf-8"))
    assert queue["pending"] == []
    assert len(queue["rejected"]) == 1
    assert queue["rejected"][0]["milestone_decision_dossier"]["review_reason"] == "milestone review rejected this candidate"

    loop_state = json.loads((repo_root / ".hermes-flow" / "loop-core-state.json").read_text(encoding="utf-8"))
    assert loop_state["operator_state"]["state_id"] == "accepted-baseline"
    assert loop_state["candidate_state"] is None


def test_review_milestone_queue_entry_defers_candidate_and_records_decision_dossier(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    cycle_proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--observation",
            "control-plane thresholds changed under review pressure",
            "--candidate-summary",
            "tighten promotion thresholds for control-plane rules",
            "--classification",
            "control_plane_policy",
            "--mode",
            "delivery",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    cycle_report = json.loads((repo_root / Path(cycle_proc.stdout.strip())).read_text(encoding="utf-8"))
    queue_id = cycle_report["milestone_queue_entry"]["queue_id"]

    review_proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--review-milestone-queue-id",
            queue_id,
            "--review-decision",
            "deferred",
            "--review-reason",
            "wait for another milestone window",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    reviewed = json.loads(review_proc.stdout)
    assert reviewed["status"] == "deferred"
    assert reviewed["review_decision"] == "deferred"
    assert reviewed["milestone_decision_dossier"]["final_disposition"] == "deferred"

    queue = json.loads((repo_root / ".hermes-flow" / "milestone-queue.json").read_text(encoding="utf-8"))
    assert queue["pending"] == []
    assert len(queue["deferred"]) == 1
    assert queue["deferred"][0]["milestone_decision_dossier"]["review_reason"] == "wait for another milestone window"


def test_apply_milestone_queue_entry_promotes_candidate_to_operator_state(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    cycle_proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--observation",
            "control-plane thresholds changed under review pressure",
            "--candidate-summary",
            "tighten promotion thresholds for control-plane rules",
            "--classification",
            "control_plane_policy",
            "--mode",
            "delivery",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    cycle_report = json.loads((repo_root / Path(cycle_proc.stdout.strip())).read_text(encoding="utf-8"))
    queue_id = cycle_report["milestone_queue_entry"]["queue_id"]

    apply_proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--apply-milestone-queue-id",
            queue_id,
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    applied = json.loads(apply_proc.stdout)
    assert applied["queue_id"] == queue_id
    assert applied["status"] == "applied"

    queue = json.loads((repo_root / ".hermes-flow" / "milestone-queue.json").read_text(encoding="utf-8"))
    assert queue["pending"] == []
    assert len(queue["applied"]) == 1

    loop_state = json.loads((repo_root / ".hermes-flow" / "loop-core-state.json").read_text(encoding="utf-8"))
    assert loop_state["operator_state"]["state_id"] == cycle_report["candidate"]["candidate_id"]
    assert loop_state["candidate_state"] is None


def test_candidate_ids_are_cycle_stable_and_unique_across_milestone_runs(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    first_proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--observation",
            "first control-plane refinement",
            "--candidate-summary",
            "first milestone candidate",
            "--classification",
            "control_plane_policy",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    second_proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--observation",
            "second control-plane refinement",
            "--candidate-summary",
            "second milestone candidate",
            "--classification",
            "control_plane_policy",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    first_report_path = Path(first_proc.stdout.strip())
    second_report_path = Path(second_proc.stdout.strip())
    first_report = json.loads((repo_root / ".hermes-flow" / "loop-core-state.json").read_text(encoding="utf-8"))["candidates"][0]
    second_report = json.loads((repo_root / ".hermes-flow" / "loop-core-state.json").read_text(encoding="utf-8"))["candidates"][1]

    assert first_report["candidate_id"] == "candidate-loop-cycle-001"
    assert second_report["candidate_id"] == "candidate-loop-cycle-002"
    assert first_report["candidate_id"] != second_report["candidate_id"]
    assert first_report_path.name == "latest-loop-cycle.json"
    assert second_report_path.name == "latest-loop-cycle.json"


def test_apply_milestone_queue_entry_preserves_newer_candidate_state(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    first_proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--observation",
            "first milestone candidate",
            "--candidate-summary",
            "first control-plane refinement",
            "--classification",
            "control_plane_policy",
            "--mode",
            "delivery",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    first_report = json.loads((repo_root / Path(first_proc.stdout.strip())).read_text(encoding="utf-8"))
    first_queue_id = first_report["milestone_queue_entry"]["queue_id"]

    second_proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--observation",
            "second milestone candidate",
            "--candidate-summary",
            "second control-plane refinement",
            "--classification",
            "control_plane_policy",
            "--mode",
            "delivery",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    second_report = json.loads((repo_root / Path(second_proc.stdout.strip())).read_text(encoding="utf-8"))

    subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--apply-milestone-queue-id",
            first_queue_id,
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    loop_state = json.loads((repo_root / ".hermes-flow" / "loop-core-state.json").read_text(encoding="utf-8"))
    assert loop_state["operator_state"]["state_id"] == first_report["candidate"]["candidate_id"]
    assert loop_state["candidate_state"]["candidate_id"] == second_report["candidate"]["candidate_id"]


def test_review_milestone_queue_entry_requires_decision_and_reason(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--review-milestone-queue-id",
            "milestone-loop-cycle-001",
            "--review-decision",
            "accepted",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    assert "requires both --review-decision and --review-reason" in proc.stderr


def test_review_milestone_queue_entry_rejects_mixed_flags(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--review-milestone-queue-id",
            "milestone-loop-cycle-001",
            "--review-decision",
            "accepted",
            "--review-reason",
            "approve",
            "--observation",
            "should fail",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    assert "cannot be combined" in proc.stderr


def test_apply_milestone_queue_entry_rejects_mixed_flags(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--apply-milestone-queue-id",
            "milestone-loop-cycle-001",
            "--observation",
            "should fail",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    assert "cannot be combined" in proc.stderr


def test_run_loop_core_cycle_rejects_downgraded_explicit_promotion_for_control_plane_policy(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--observation",
            "control-plane change must not downgrade promotion boundary",
            "--candidate-summary",
            "reject unsafe control-plane override",
            "--classification",
            "control_plane_policy",
            "--mode",
            "delivery",
            "--promotion-decision",
            "internal_promotion",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    assert "violates minimum governance boundary" in proc.stderr


def test_run_loop_core_cycle_rejects_unknown_classification(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--observation",
            "unknown classification should fail closed",
            "--candidate-summary",
            "do not auto-promote unknown categories",
            "--classification",
            "mystery_rule",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    assert "Unsupported classification" in proc.stderr


def test_run_loop_core_cycle_rejects_report_path_outside_repo(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--observation",
            "report path should stay inside repo",
            "--candidate-summary",
            "reject out-of-repo report output",
            "--report-path",
            "../../outside-report.json",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    assert "Path escapes repo root" in proc.stderr


def test_run_loop_core_cycle_rejects_evidence_report_path_outside_repo(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    evidence_dir = repo_root / "artifacts" / "generated"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_path = evidence_dir / "execution-evidence.json"
    evidence_path.write_text(json.dumps({"signal": "ok"}), encoding="utf-8")

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--evidence-path",
            "artifacts/generated/execution-evidence.json",
            "--classification",
            "product_contract_rule",
            "--evidence-report-path",
            "../../outside-evidence-report.json",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    assert "Path escapes repo root" in proc.stderr


def test_run_loop_core_cycle_rejects_evidence_path_outside_repo(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    outside_root = tmp_path / "outside"
    outside_root.mkdir()
    outside_evidence = outside_root / "evidence.json"
    outside_evidence.write_text(json.dumps({"signal": "escape"}), encoding="utf-8")

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--evidence-path",
            str(outside_evidence),
            "--classification",
            "product_contract_rule",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    assert "Path escapes repo root" in proc.stderr


def test_invalid_evidence_driven_request_fails_closed_without_artifact_mutation(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    evidence_dir = repo_root / "artifacts" / "generated"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_path = evidence_dir / "execution-evidence.json"
    evidence_path.write_text(json.dumps({"signal": "escape contract"}), encoding="utf-8")

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--evidence-path",
            "artifacts/generated/execution-evidence.json",
            "--classification",
            "product_contract_rule",
            "--promotion-decision",
            "internal_promotion",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    assert "violates minimum governance boundary" in proc.stderr
    assert not (repo_root / "artifacts" / "reports" / "latest-execution-evidence.json").exists()

    artifacts = json.loads((repo_root / ".hermes-flow" / "artifacts-index.json").read_text(encoding="utf-8"))
    assert artifacts["artifacts"] == []


def test_run_loop_core_cycle_rejects_downgraded_explicit_promotion_for_contract_rule(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--observation",
            "contract change must not downgrade promotion boundary",
            "--candidate-summary",
            "reject unsafe operator override",
            "--classification",
            "product_contract_rule",
            "--promotion-decision",
            "internal_promotion",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    assert "violates minimum governance boundary" in proc.stderr


def test_run_loop_core_cycle_ingests_execution_evidence_and_requires_user_decision_for_contract_rules(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    evidence_dir = repo_root / "artifacts" / "generated"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_path = evidence_dir / "execution-evidence.json"
    evidence_path.write_text(
        json.dumps(
            {
                "task_id": "loop-task-1",
                "phase_id": "phase-governance",
                "review_clear": True,
                "verification_passed": True,
                "signal": "done semantics may need to change",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--evidence-path",
            "artifacts/generated/execution-evidence.json",
            "--classification",
            "product_contract_rule",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    report = json.loads((repo_root / Path(proc.stdout.strip())).read_text(encoding="utf-8"))
    assert report["promotion"]["decision"] == "user_decision_required"
    assert report["observation"]["evidence"]["payload"]["task_id"] == "loop-task-1"
    assert report["candidate"]["evidence"]["payload"]["signal"] == "done semantics may need to change"

    evidence_report = json.loads((repo_root / "artifacts" / "reports" / "latest-execution-evidence.json").read_text(encoding="utf-8"))
    assert evidence_report["payload"]["phase_id"] == "phase-governance"

    loop_state = json.loads((repo_root / ".hermes-flow" / "loop-core-state.json").read_text(encoding="utf-8"))
    assert loop_state["candidate_state"]["classification"] == "product_contract_rule"
    assert loop_state["operator_state"]["state_id"] == "accepted-baseline"


def test_run_loop_core_cycle_rejects_repo_state_with_explicit_classification_override(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--ingest-repo-state",
            "--classification",
            "internal_operating_rule",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    assert "cannot be combined" in proc.stderr


def test_run_loop_core_cycle_rejects_repo_state_with_manual_promotion_override(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--ingest-repo-state",
            "--promotion-decision",
            "internal_promotion",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    assert "cannot be combined" in proc.stderr


def test_run_loop_core_cycle_rejects_mixed_repo_state_and_evidence_inputs(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    evidence_dir = repo_root / "artifacts" / "generated"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_path = evidence_dir / "execution-evidence.json"
    evidence_path.write_text(json.dumps({"signal": "mixed"}), encoding="utf-8")

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--ingest-repo-state",
            "--evidence-path",
            "artifacts/generated/execution-evidence.json",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    assert "cannot be combined" in proc.stderr


def test_run_loop_core_cycle_uses_governance_history_learning_signal_when_recent_history_shows_friction(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    run_state = json.loads((repo_root / ".hermes-flow" / "run-state.json").read_text(encoding="utf-8"))
    run_state["workflow_stage"] = "observe"
    run_state["status"] = "ready"
    run_state["active_phase_id"] = None
    run_state["active_task_id"] = None
    run_state["self_evolve"]["auto_apply_control_plane"] = False
    (repo_root / ".hermes-flow" / "run-state.json").write_text(json.dumps(run_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    queue = json.loads((repo_root / ".hermes-flow" / "milestone-queue.json").read_text(encoding="utf-8"))
    queue["pending"] = []
    queue["applied"] = []
    queue["rejected"] = []
    queue["deferred"] = [
        {
            "queue_id": "milestone-loop-cycle-099",
            "cycle_id": "loop-cycle-099",
            "candidate_id": "candidate-loop-cycle-099",
            "summary": "older control-plane candidate",
            "classification": "control_plane_policy",
            "target_surface": ["docs/plans/"],
            "promotion_decision": "milestone_promotion_required",
            "status": "deferred",
            "queued_at": "2026-04-17T09:00:00Z",
            "review_decision": "deferred",
            "review_reason": "need more evidence",
            "reviewed_at": "2026-04-17T09:01:00Z",
            "milestone_decision_dossier": {
                "artifact_type": "milestone_decision_dossier",
                "queue_id": "milestone-loop-cycle-099",
                "candidate_id": "candidate-loop-cycle-099",
                "classification": "control_plane_policy",
                "summary": "older control-plane candidate",
                "target_surface": ["docs/plans/"],
                "promotion_decision": "milestone_promotion_required",
                "stop_artifact": {
                    "artifact_type": "milestone_stop_request",
                    "reason": "self_evolve_policy_disabled_auto_apply",
                },
                "review_decision": "deferred",
                "review_reason": "need more evidence",
                "final_disposition": "deferred",
                "reviewed_at": "2026-04-17T09:01:00Z",
            },
        }
    ]
    (repo_root / ".hermes-flow" / "milestone-queue.json").write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    verification_state = json.loads((repo_root / ".hermes-flow" / "verification-state.json").read_text(encoding="utf-8"))
    verification_state["task_review_state"] = {}
    verification_state["phase_review_state"] = {}
    verification_state["final_acceptance"] = []
    (repo_root / ".hermes-flow" / "verification-state.json").write_text(json.dumps(verification_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--ingest-repo-state",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    report = json.loads((repo_root / Path(proc.stdout.strip())).read_text(encoding="utf-8"))
    assert report["candidate"]["summary"].startswith("keep milestone stop boundaries legible")
    assert report["observation"]["evidence"]["governance_learning_signal"]["pattern"] == "governance_friction_present"
    assert report["observation"]["evidence"]["milestone_history_summary"]["deferred_count"] == 1


def test_run_loop_core_cycle_ingests_repo_state_and_stops_at_milestone_boundary_when_self_evolve_policy_disables_auto_apply(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    run_state = json.loads((repo_root / ".hermes-flow" / "run-state.json").read_text(encoding="utf-8"))
    run_state["workflow_stage"] = "execute"
    run_state["status"] = "blocked"
    run_state["active_phase_id"] = "phase-loop-core"
    run_state["active_task_id"] = "task-review"
    run_state["mode"] = "governance-hardening"
    run_state["self_evolve"]["auto_apply_control_plane"] = False
    (repo_root / ".hermes-flow" / "run-state.json").write_text(json.dumps(run_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    verification_state = json.loads((repo_root / ".hermes-flow" / "verification-state.json").read_text(encoding="utf-8"))
    verification_state["task_review_state"] = {
        "task-review": {
            "round_count": 4,
            "latest_blocking_bugs": ["promotion_boundary_unclear"],
            "latest_clear": False,
            "review_evidence": ["blocking bug remained after review"],
            "updated_at": "2026-04-17T07:30:00Z",
        }
    }
    verification_state["phase_review_state"] = {
        "phase-loop-core": {
            "round_count": 2,
            "latest_blocking_bugs": [],
            "latest_clear": True,
            "review_evidence": ["phase review partially clear"],
            "updated_at": "2026-04-17T07:30:00Z",
        }
    }
    (repo_root / ".hermes-flow" / "verification-state.json").write_text(json.dumps(verification_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--ingest-repo-state",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    report = json.loads((repo_root / Path(proc.stdout.strip())).read_text(encoding="utf-8"))
    assert report["candidate"]["classification"] == "control_plane_policy"
    assert report["promotion"]["decision"] == "milestone_promotion_required"
    assert report["auto_applied_milestone_entry"] is None
    assert report["candidate"]["summary"].endswith("stop at milestone boundary")
    assert report["milestone_stop_artifact"]["artifact_type"] == "milestone_stop_request"
    assert report["milestone_stop_artifact"]["reason"] == "self_evolve_policy_disabled_auto_apply"
    assert "operator explicitly applies the queued milestone candidate" in report["milestone_stop_artifact"]["continue_when"]

    queue = json.loads((repo_root / ".hermes-flow" / "milestone-queue.json").read_text(encoding="utf-8"))
    assert len(queue["pending"]) == 1
    assert queue["applied"] == []
    assert queue["pending"][0]["milestone_stop_artifact"]["reason"] == "self_evolve_policy_disabled_auto_apply"


def test_run_loop_core_cycle_ingests_repo_state_and_generates_control_plane_candidate(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    run_state = json.loads((repo_root / ".hermes-flow" / "run-state.json").read_text(encoding="utf-8"))
    run_state["workflow_stage"] = "execute"
    run_state["status"] = "blocked"
    run_state["active_phase_id"] = "phase-loop-core"
    run_state["active_task_id"] = "task-review"
    run_state["updated_at"] = "2026-04-17T07:30:00Z"
    (repo_root / ".hermes-flow" / "run-state.json").write_text(json.dumps(run_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    verification_state = json.loads((repo_root / ".hermes-flow" / "verification-state.json").read_text(encoding="utf-8"))
    verification_state["task_review_state"] = {
        "task-review": {
            "round_count": 4,
            "latest_blocking_bugs": ["promotion_boundary_unclear"],
            "latest_clear": False,
            "review_evidence": ["blocking bug remained after review"],
            "updated_at": "2026-04-17T07:30:00Z",
        }
    }
    verification_state["phase_review_state"] = {
        "phase-loop-core": {
            "round_count": 2,
            "latest_blocking_bugs": [],
            "latest_clear": True,
            "review_evidence": ["phase review partially clear"],
            "updated_at": "2026-04-17T07:30:00Z",
        }
    }
    verification_state["task_checks"] = [{"target": "task-review", "result": "pass"}]
    (repo_root / ".hermes-flow" / "verification-state.json").write_text(json.dumps(verification_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--ingest-repo-state",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    report = json.loads((repo_root / Path(proc.stdout.strip())).read_text(encoding="utf-8"))
    assert report["candidate"]["classification"] == "control_plane_policy"
    assert report["promotion"]["decision"] == "milestone_promotion_required"
    assert report["observation"]["evidence"]["run_state"]["status"] == "blocked"
    assert report["observation"]["evidence"]["task_review_summary"]["blocking_bug_count"] == 1
    assert report["milestone_queue_entry"]["status"] == "pending"
    assert report["auto_applied_milestone_entry"]["status"] == "applied"

    queue = json.loads((repo_root / ".hermes-flow" / "milestone-queue.json").read_text(encoding="utf-8"))
    assert queue["pending"] == []
    assert queue["applied"][0]["queue_id"] == report["milestone_queue_entry"]["queue_id"]


def test_run_loop_core_cycle_ingests_repo_state_with_ambiguous_acceptance_state_stays_control_plane(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    run_state = json.loads((repo_root / ".hermes-flow" / "run-state.json").read_text(encoding="utf-8"))
    run_state["workflow_stage"] = "final-acceptance"
    run_state["status"] = "running"
    (repo_root / ".hermes-flow" / "run-state.json").write_text(json.dumps(run_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    verification_state = json.loads((repo_root / ".hermes-flow" / "verification-state.json").read_text(encoding="utf-8"))
    verification_state["task_review_state"] = {
        "task-final": {
            "round_count": 3,
            "latest_blocking_bugs": [],
            "latest_clear": True,
            "review_evidence": ["clear"],
            "updated_at": "2026-04-17T07:35:00Z",
        }
    }
    verification_state["phase_review_state"] = {
        "phase-final": {
            "round_count": 5,
            "latest_blocking_bugs": [],
            "latest_clear": True,
            "review_evidence": ["clear"],
            "updated_at": "2026-04-17T07:35:00Z",
        }
    }
    verification_state["final_acceptance"] = [{"target": "surface", "result": "pending"}]
    (repo_root / ".hermes-flow" / "verification-state.json").write_text(json.dumps(verification_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--ingest-repo-state",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    report = json.loads((repo_root / Path(proc.stdout.strip())).read_text(encoding="utf-8"))
    assert report["candidate"]["classification"] == "control_plane_policy"
    assert report["promotion"]["decision"] == "milestone_promotion_required"


def test_run_loop_core_cycle_ingests_repo_state_without_acceptance_evidence_stays_control_plane(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    run_state = json.loads((repo_root / ".hermes-flow" / "run-state.json").read_text(encoding="utf-8"))
    run_state["workflow_stage"] = "final-acceptance"
    run_state["status"] = "running"
    (repo_root / ".hermes-flow" / "run-state.json").write_text(json.dumps(run_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    verification_state = json.loads((repo_root / ".hermes-flow" / "verification-state.json").read_text(encoding="utf-8"))
    verification_state["task_review_state"] = {
        "task-final": {
            "round_count": 3,
            "latest_blocking_bugs": [],
            "latest_clear": True,
            "review_evidence": ["clear"],
            "updated_at": "2026-04-17T07:35:00Z",
        }
    }
    verification_state["phase_review_state"] = {
        "phase-final": {
            "round_count": 5,
            "latest_blocking_bugs": [],
            "latest_clear": True,
            "review_evidence": ["clear"],
            "updated_at": "2026-04-17T07:35:00Z",
        }
    }
    verification_state["final_acceptance"] = []
    (repo_root / ".hermes-flow" / "verification-state.json").write_text(json.dumps(verification_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--ingest-repo-state",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    report = json.loads((repo_root / Path(proc.stdout.strip())).read_text(encoding="utf-8"))
    assert report["candidate"]["classification"] == "control_plane_policy"
    assert report["promotion"]["decision"] == "milestone_promotion_required"


def test_run_loop_core_cycle_ingests_repo_state_without_clear_reviews_stays_control_plane(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    run_state = json.loads((repo_root / ".hermes-flow" / "run-state.json").read_text(encoding="utf-8"))
    run_state["workflow_stage"] = "final-acceptance"
    run_state["status"] = "running"
    (repo_root / ".hermes-flow" / "run-state.json").write_text(json.dumps(run_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    verification_state = json.loads((repo_root / ".hermes-flow" / "verification-state.json").read_text(encoding="utf-8"))
    verification_state["task_review_state"] = {
        "task-final": {
            "round_count": 3,
            "latest_blocking_bugs": [],
            "latest_clear": False,
            "review_evidence": ["not clear yet"],
            "updated_at": "2026-04-17T07:35:00Z",
        }
    }
    verification_state["phase_review_state"] = {
        "phase-final": {
            "round_count": 5,
            "latest_blocking_bugs": [],
            "latest_clear": True,
            "review_evidence": ["clear"],
            "updated_at": "2026-04-17T07:35:00Z",
        }
    }
    verification_state["final_acceptance"] = [{"target": "surface", "result": "fail"}]
    (repo_root / ".hermes-flow" / "verification-state.json").write_text(json.dumps(verification_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--ingest-repo-state",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    report = json.loads((repo_root / Path(proc.stdout.strip())).read_text(encoding="utf-8"))
    assert report["candidate"]["classification"] == "control_plane_policy"
    assert report["promotion"]["decision"] == "milestone_promotion_required"


def test_run_loop_core_cycle_ingests_repo_state_and_auto_promotes_internal_rule_when_clear(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    bootstrap_repo(repo_root)

    run_state = json.loads((repo_root / ".hermes-flow" / "run-state.json").read_text(encoding="utf-8"))
    run_state["workflow_stage"] = "final-acceptance"
    run_state["status"] = "running"
    run_state["updated_at"] = "2026-04-17T07:35:00Z"
    (repo_root / ".hermes-flow" / "run-state.json").write_text(json.dumps(run_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    verification_state = json.loads((repo_root / ".hermes-flow" / "verification-state.json").read_text(encoding="utf-8"))
    verification_state["task_review_state"] = {
        "task-final": {
            "round_count": 3,
            "latest_blocking_bugs": [],
            "latest_clear": True,
            "review_evidence": ["clear"],
            "updated_at": "2026-04-17T07:35:00Z",
        }
    }
    verification_state["phase_review_state"] = {
        "phase-final": {
            "round_count": 5,
            "latest_blocking_bugs": [],
            "latest_clear": True,
            "review_evidence": ["clear"],
            "updated_at": "2026-04-17T07:35:00Z",
        }
    }
    verification_state["task_checks"] = [{"target": "task-final", "result": "pass"}]
    verification_state["phase_checks"] = [{"target": "phase-final", "result": "pass"}]
    verification_state["final_acceptance"] = [{"target": "surface", "result": "fail"}]
    (repo_root / ".hermes-flow" / "verification-state.json").write_text(json.dumps(verification_state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    proc = subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "run_loop_core_cycle.py"),
            "--ingest-repo-state",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    report = json.loads((repo_root / Path(proc.stdout.strip())).read_text(encoding="utf-8"))
    assert report["candidate"]["classification"] == "internal_operating_rule"
    assert report["promotion"]["decision"] == "internal_promotion"

    loop_state = json.loads((repo_root / ".hermes-flow" / "loop-core-state.json").read_text(encoding="utf-8"))
    assert loop_state["operator_state"]["state_id"].startswith("candidate-")
    assert loop_state["candidate_state"] is None
