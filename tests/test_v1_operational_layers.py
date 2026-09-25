from __future__ import annotations

from abs_core.data_layer import ABSDataLayer
from abs_core.runtime import build_runtime
from abs_core.verification import ResultVerifier


def test_v1_data_layer_and_verification():
    data = ABSDataLayer(":memory:")
    item = data.put("decision", {"ok": True}, key="v1")
    assert item
    assert data.search(kind="decision", query="v1")
    result = ResultVerifier().verify({"type": "echo", "final_response": "ok"})
    assert result.accepted is True


def test_v1_runtime_has_data_layer_and_verifier():
    runtime = build_runtime(":memory:")
    assert runtime.data_layer is not None
    work = runtime.orchestrator.create("preflight")
    work = runtime.orchestrator.run(work.id, "echo", approved=True)
    assert work.state.value == "completed"
    assert work.result["verification"]["accepted"] is True
    assert runtime.data_layer.search(kind="work_result", query=work.id, limit=1)
