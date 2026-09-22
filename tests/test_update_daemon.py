import abs_core.update_daemon as daemon


def test_run_once_logs_successful_no_update_check(monkeypatch, tmp_path):
    log_path = tmp_path / "update-daemon.log"
    monkeypatch.setattr(daemon, "LOG_PATH", log_path)
    monkeypatch.setattr(
        daemon.um,
        "check",
        lambda: {
            "current_commit": "abc123",
            "target_commit": "abc123",
            "update_available": False,
            "ref": "main",
        },
    )

    result = daemon.run_once()

    assert result["checked"] is True
    assert result["updated"] is False
    log = log_path.read_text()
    assert "check started" in log
    assert "check completed:" in log
    assert "update_available=False" in log
