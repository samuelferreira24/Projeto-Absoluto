import os

from abs_core.local import LocalABS


def test_local_abs_echo():
    os.environ["ABS_CODEX_COMMAND"] = "codex"
    abs_system = LocalABS()
    result = abs_system.task({
        "objective": "ABS_LOCAL_TEST",
        "capability_id": "echo",
        "approved": False,
    })
    assert result["state"] == "completed"
    assert result["result"]["type"] == "echo"
