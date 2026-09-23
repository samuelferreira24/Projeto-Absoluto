import json

from abs_core.codex_adapter import CodexCapability


class Completed:
    returncode = 0
    stderr = ""
    stdout = (
        '{"type":"thread.started","thread_id":"thread-created"}\n'
        '{"type":"item.completed","item":{"type":"agent_message","text":"CODEX_CLI_OK"}}\n'
    )


def test_codex_cli_adapter_creates_and_resumes_session(monkeypatch, tmp_path):
    calls = []

    monkeypatch.setattr("abs_core.codex_adapter.shutil.which", lambda command: "/usr/bin/codex")

    def fake_run(args, **kwargs):
        calls.append((args, kwargs))
        return Completed()

    monkeypatch.setattr("abs_core.codex_adapter.subprocess.run", fake_run)

    adapter = CodexCapability(command="codex")
    first = adapter.execute("first", {"value": 1, "_codex_cwd": str(tmp_path)})
    assert first["thread_id"] == "thread-created"
    assert first["final_response"] == "CODEX_CLI_OK"
    assert calls[0][0][:5] == [
        "/usr/bin/codex", "exec", "--json", "--sandbox", "workspace-write"
    ]

    second = adapter.execute(
        "second",
        {"_codex_thread_id": first["thread_id"], "_codex_cwd": str(tmp_path)},
    )
    assert second["thread_id"] == "thread-created"
    assert second["final_response"] == "CODEX_CLI_OK"
    assert calls[1][0][:6] == [
        "/usr/bin/codex", "exec", "resume", "thread-created", "--json", "--sandbox"
    ]


def test_codex_cli_adapter_uses_explicit_sandbox_settings(monkeypatch):
    monkeypatch.setenv("ABS_CODEX_SANDBOX", "workspace-write")
    monkeypatch.setenv("ABS_CODEX_APPROVAL", "never")
    adapter = CodexCapability(command="codex")
    assert adapter.sandbox == "workspace-write"
    assert adapter.approval == "never"


def test_codex_cli_adapter_supports_explicit_bypass(monkeypatch):
    adapter = CodexCapability(command="codex", bypass_sandbox=True)
    monkeypatch.setattr("abs_core.codex_adapter.shutil.which", lambda command: "/usr/bin/codex")

    def fake_run(args, **kwargs):
        assert "--dangerously-bypass-approvals-and-sandbox" in args
        assert "--sandbox" not in args
        return Completed()

    monkeypatch.setattr("abs_core.codex_adapter.subprocess.run", fake_run)
    result = adapter.execute("controlled", {})
    assert result["final_response"] == "CODEX_CLI_OK"
