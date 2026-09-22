import json
import pytest
import abs_core.update_manager as um

def test_status_reads_commit(monkeypatch, tmp_path):
    state = tmp_path / "state.json"
    monkeypatch.setattr(um, "STATE_PATH", state)
    monkeypatch.setattr(um, "_git", lambda *args: "abc123")
    result = um.status()
    assert result["current_commit"] == "abc123"
    assert result["last_known_good"] is None

def test_apply_refuses_dirty_tree(monkeypatch):
    monkeypatch.setattr(um, "_git", lambda *args: " M file" if args == ("status", "--porcelain") else "abc")
    with pytest.raises(um.UpdateError, match="non-runtime changes"):
        um.apply()

def test_state_round_trip(monkeypatch, tmp_path):
    state = tmp_path / "state.json"
    monkeypatch.setattr(um, "STATE_PATH", state)
    um._save_state({"last_known_good": "abc"})
    assert json.loads(state.read_text())["last_known_good"] == "abc"


def test_candidate_validation_passes(monkeypatch):
    class Result:
        returncode = 0
        stdout = "5 passed"
        stderr = ""
    monkeypatch.setattr(um.subprocess, "run", lambda *args, **kwargs: Result())
    monkeypatch.setattr(um, "RUN_TESTS", True)
    result = um._validate_target()
    assert result["validation"] == "passed"


def test_candidate_validation_rejects(monkeypatch):
    class Result:
        returncode = 1
        stdout = "1 failed"
        stderr = ""
    monkeypatch.setattr(um.subprocess, "run", lambda *args, **kwargs: Result())
    monkeypatch.setattr(um, "RUN_TESTS", True)
    with pytest.raises(um.UpdateError, match="candidate validation failed"):
        um._validate_target()
