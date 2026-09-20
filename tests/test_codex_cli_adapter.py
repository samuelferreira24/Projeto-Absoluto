import json
import sys

from abs_core.codex_adapter import CodexCapability


def _fake_codex(tmp_path):
    script = tmp_path / "fake_codex.py"
    script.write_text(
        """
import json
import sys

args = sys.argv[1:]
if "resume" in args:
    thread_id = args[args.index("resume") + 1]
else:
    thread_id = "thread-created"
print(json.dumps({"type": "thread.started", "thread_id": thread_id}))
print(json.dumps({
    "type": "item.completed",
    "item": {"type": "agent_message", "text": "CODEX_CLI_OK"}
}))
""",
        encoding="utf-8",
    )
    return script


def test_codex_cli_adapter_creates_and_resumes_session(tmp_path):
    fake = _fake_codex(tmp_path)
    adapter = CodexCapability(command=sys.executable)

    first = adapter.execute("first", {"value": 1, "_codex_cwd": str(tmp_path)})
    assert first["thread_id"] == "thread-created"
    assert first["final_response"] == "CODEX_CLI_OK"

    second = adapter.execute(
        "second",
        {"_codex_thread_id": first["thread_id"], "_codex_cwd": str(tmp_path)},
    )
    assert second["thread_id"] == "thread-created"
    assert second["final_response"] == "CODEX_CLI_OK"
    assert fake.exists()


def test_codex_cli_adapter_uses_explicit_sandbox_settings(monkeypatch):
    monkeypatch.setenv("ABS_CODEX_SANDBOX", "workspace-write")
    monkeypatch.setenv("ABS_CODEX_APPROVAL", "never")
    adapter = CodexCapability(command="codex")
    assert adapter.sandbox == "workspace-write"
    assert adapter.approval == "never"
