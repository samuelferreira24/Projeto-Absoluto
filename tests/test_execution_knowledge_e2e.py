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


def test_v1_acceptance_crosses_navigation_intelligence_verification_and_memory(tmp_path):
    from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
    from abs_core.conversational_tools import ConversationalToolRuntime
    from abs_core.data_layer import ABSDataLayer
    from abs_core.intelligence import CognitiveRuntime, IntelligenceRegistry, IntelligenceResource
    from abs_core.navigation_adapter import KnowledgeNavigationCapability
    from abs_core.orchestrator import Orchestrator
    from abs_core.verification import ResultVerifier

    source = tmp_path / "source"
    source.mkdir()
    (source / "architecture.md").write_text(
        "# Architecture\nThe verification boundary is explicit.\n",
        encoding="utf-8",
    )
    db_path = tmp_path / "abs.db"
    registry = CapabilityRegistry()
    navigation = KnowledgeNavigationCapability(
        db_path=tmp_path / "nav.sqlite",
        sources={"projeto-absoluto": source},
    )
    registry.register(CapabilityRecord(
        "knowledge-navigation", navigation.name, navigation.kind, navigation,
    ))
    registry.register(CapabilityRecord("fake-chat", "Fake Chat", "test", EchoCapability()))

    intelligence = IntelligenceRegistry()
    intelligence.register(IntelligenceResource(
        id="intelligence:fake-chat",
        capability_id="fake-chat",
        name="Fake Chat",
        source="local",
        local=True,
        capabilities=("conversation", "reasoning"),
        status="available",
    ))
    data_layer = ABSDataLayer(db_path)
    orchestrator = Orchestrator(
        registry,
        WorkStore(db_path),
        data_layer=data_layer,
        verifier=ResultVerifier(),
    )
    cognitive = CognitiveRuntime(
        registry,
        intelligence,
        orchestrator,
        store_path=str(db_path),
        data_layer=data_layer,
    )
    cognitive.tool_runtime = ConversationalToolRuntime(
        planner=None,
        dispatcher=None,
        capabilities=registry,
        orchestrator=orchestrator,
    )

    result = cognitive.turn("Onde está implementada a verificação no projeto?", approved=True)

    assert result["work_state"] == "completed"
    assert result["result"]["verification"]["accepted"] is True
    assert result["result"]["final_response"]
    assert result["result"]["type"] == "echo"
    assert result["provenance"]
    assert data_layer.search(kind="work_result", limit=10)
    assert data_layer.search(kind="conversation", query=result["session_id"], limit=10)
