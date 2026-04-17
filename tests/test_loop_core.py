from __future__ import annotations

import json
import subprocess
from pathlib import Path


def copy_script(repo_root: Path, script_name: str) -> None:
    source_script = Path(f"/root/projects/oh-my-hermes/scripts/{script_name}")
    target_script = repo_root / "scripts" / script_name
    target_script.parent.mkdir(parents=True, exist_ok=True)
    target_script.write_text(source_script.read_text(encoding="utf-8"), encoding="utf-8")


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

    assert "validated_json_count=3" in proc.stdout
    loop_state = json.loads((repo_root / ".hermes-flow" / "loop-core-state.json").read_text(encoding="utf-8"))
    assert loop_state["core_name"] == "回环核心"
    assert loop_state["current_mode"] == "governance-hardening"
    assert loop_state["observations"] == []
    assert loop_state["operator_state"]["state_id"] == "accepted-baseline"


def test_run_loop_core_cycle_internal_promotion_updates_operator_state(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    subprocess.run(
        ["python3", str(repo_root / "scripts" / "bootstrap_omh.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

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

    artifacts = json.loads((repo_root / ".hermes-flow" / "artifacts-index.json").read_text(encoding="utf-8"))
    assert artifacts["artifacts"]
    assert artifacts["artifacts"][0]["class"] == "loop_cycle_report"


def test_run_loop_core_cycle_control_plane_policy_requires_milestone_review(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    subprocess.run(
        ["python3", str(repo_root / "scripts" / "bootstrap_omh.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

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
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

    report = json.loads((repo_root / Path(proc.stdout.strip())).read_text(encoding="utf-8"))
    assert report["promotion"]["decision"] == "milestone_promotion_required"
    loop_state = json.loads((repo_root / ".hermes-flow" / "loop-core-state.json").read_text(encoding="utf-8"))
    assert loop_state["candidate_state"]["classification"] == "control_plane_policy"
    assert loop_state["operator_state"]["state_id"] == "accepted-baseline"


def test_run_loop_core_cycle_rejects_downgraded_explicit_promotion_for_control_plane_policy(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        copy_script(repo_root, script_name)

    subprocess.run(
        ["python3", str(repo_root / "scripts" / "bootstrap_omh.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

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

    subprocess.run(
        ["python3", str(repo_root / "scripts" / "bootstrap_omh.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

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

    subprocess.run(
        ["python3", str(repo_root / "scripts" / "bootstrap_omh.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

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

    subprocess.run(
        ["python3", str(repo_root / "scripts" / "bootstrap_omh.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

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

    subprocess.run(
        ["python3", str(repo_root / "scripts" / "bootstrap_omh.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

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

    subprocess.run(
        ["python3", str(repo_root / "scripts" / "bootstrap_omh.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

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

    subprocess.run(
        ["python3", str(repo_root / "scripts" / "bootstrap_omh.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

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

    subprocess.run(
        ["python3", str(repo_root / "scripts" / "bootstrap_omh.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )

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
