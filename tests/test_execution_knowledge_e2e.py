from pathlib import Path

from abs_core.adapters import EchoCapability
from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
from abs_core.orchestrator import Orchestrator
from abs_core.project_knowledge_runtime import ExecutionKnowledgeRecorder
from abs_core.store import WorkStore


def _runtime(tmp_path: Path, adapter):
    (tmp_path / "abs_core").mkdir()
    (tmp_path / "abs_core" / "orchestrator.py").write_text("x", encoding="utf-8")
    output = tmp_path / "knowledge"
    recorder = ExecutionKnowledgeRecorder(tmp_path, output)
    store = WorkStore(tmp_path / "abs.db")
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("echo", "Echo", "test", adapter))
    return Orchestrator(registry, store, knowledge_runtime=recorder), recorder, output


def test_orchestrator_execution_promotes_path_to_operational(tmp_path):
    orchestrator, _, output = _runtime(tmp_path, EchoCapability())
    work = orchestrator.create("prove automatic execution evidence")
    result = orchestrator.run(work.id, "echo")

    import json

    data = json.loads((output / "project_knowledge.json").read_text(encoding="utf-8"))
    path = next(item for item in data["paths"] if item["id"] == "PATH-ABS-ORCHESTRATOR")
    assert result.state.value == "completed"
    assert path["state"] == "operational"
    assert any(
        item["kind"] == "execution" and item["status"] == "operational"
        for item in data["evidence"]
    )
    assert any(event["type"] == "execution_observed" for event in data["events"])


def test_orchestrator_failed_execution_promotes_path_to_degraded(tmp_path):
    class Failing:
        def execute(self, objective, context):
            raise RuntimeError("forced failure")

    orchestrator, _, output = _runtime(tmp_path, Failing())
    work = orchestrator.create("prove failure evidence")
    result = orchestrator.run(work.id, "echo")

    import json

    data = json.loads((output / "project_knowledge.json").read_text(encoding="utf-8"))
    path = next(item for item in data["paths"] if item["id"] == "PATH-ABS-ORCHESTRATOR")
    assert result.state.value == "failed"
    assert path["state"] == "degraded"
    assert any(
        item["kind"] == "execution" and item["status"] == "failure"
        for item in data["evidence"]
    )
