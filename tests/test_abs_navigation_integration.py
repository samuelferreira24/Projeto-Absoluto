from pathlib import Path

from abs_core.navigation_adapter import KnowledgeNavigationCapability


def _fixture(root: Path) -> None:
    (root / "pkg").mkdir()
    (root / "pkg" / "engine.py").write_text(
        "class Engine:\n    def verify_source(self):\n        return True\n", encoding="utf-8")
    (root / "README.md").write_text(
        "# Navigation\nProvenance is verified with a hash.\n", encoding="utf-8")


def test_abs_consumes_navigation_without_navigation_importing_abs(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    _fixture(source)
    capability = KnowledgeNavigationCapability(
        db_path=tmp_path / "nav.sqlite", sources={"fixture": source})
    result = capability.execute(
        "como a proveniência é verificada?",
        {"action": "investigate", "source": "fixture", "limit": 8})
    assert result["type"] == "knowledge_navigation"
    bundle = result["result"]
    assert bundle["mode"] == "evidence_retrieval"
    assert bundle["evidence"]
    assert all(item["source"] == "fixture" and item["sha256"] for item in bundle["evidence"])


def test_abs_navigation_capability_supports_verification_and_coverage(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    _fixture(source)
    capability = KnowledgeNavigationCapability(
        db_path=tmp_path / "nav.sqlite", sources={"fixture": source})
    coverage = capability.execute("coverage", {"action": "coverage"})
    assert coverage["result"]["result"][0]["index"]["coverage_ratio"] == 1.0
    verification = capability.execute(
        "verify", {"action": "verify", "source": "fixture"})
    assert verification["result"]["invalid"] == []

def test_conversational_runtime_selects_navigation_and_records_work(tmp_path):
    from abs_core.capabilities import CapabilityRecord, CapabilityRegistry
    from abs_core.conversational_tools import ConversationalToolRuntime
    from abs_core.orchestrator import Orchestrator
    from abs_core.store import WorkStore
    from abs_core.verification import ResultVerifier

    source = tmp_path / "source"
    source.mkdir()
    _fixture(source)
    navigation = KnowledgeNavigationCapability(
        db_path=tmp_path / "nav.sqlite", sources={"projeto-absoluto": source})
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord(
        "knowledge-navigation", navigation.name, navigation.kind, navigation))
    orchestrator = Orchestrator(
        registry, WorkStore(tmp_path / "abs.db"), verifier=ResultVerifier())
    runtime = ConversationalToolRuntime(
        planner=None, dispatcher=None, capabilities=registry, orchestrator=orchestrator)

    intent = runtime.detect("Onde está implementada a proveniência no projeto?")
    assert intent["tool_id"] == "knowledge-navigation"
    result = runtime.execute("Onde está implementada a proveniência no projeto?")
    assert result["type"] == "tool_result"
    assert result["tool"] == "knowledge-navigation"
    assert result["work_id"]
    assert result["provenance"]
    assert result["result"]["type"] == "knowledge_navigation"
