from __future__ import annotations

import json
import subprocess
from pathlib import Path


def test_bootstrap_omh_creates_loop_core_state(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    source_script = Path("/root/projects/oh-my-hermes/scripts/bootstrap_omh.py")
    target_script = repo_root / "scripts" / "bootstrap_omh.py"
    target_script.parent.mkdir(parents=True, exist_ok=True)
    target_script.write_text(source_script.read_text(encoding="utf-8"), encoding="utf-8")

    proc = subprocess.run(
        ["python3", str(target_script)],
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


def test_run_loop_core_cycle_records_observation_candidate_and_report(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()

    for script_name in ["bootstrap_omh.py", "run_loop_core_cycle.py"]:
        source_script = Path(f"/root/projects/oh-my-hermes/scripts/{script_name}")
        target_script = repo_root / "scripts" / script_name
        target_script.parent.mkdir(parents=True, exist_ok=True)
        target_script.write_text(source_script.read_text(encoding="utf-8"), encoding="utf-8")

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
    assert loop_state["promotions"][0]["decision"] == "record_only"

    report = json.loads((repo_root / report_path).read_text(encoding="utf-8"))
    assert report["cycle_id"] == "loop-cycle-001"
    assert report["candidate"]["status"] == "candidate_detected"

    artifacts = json.loads((repo_root / ".hermes-flow" / "artifacts-index.json").read_text(encoding="utf-8"))
    assert artifacts["artifacts"]
    assert artifacts["artifacts"][0]["class"] == "loop_cycle_report"
