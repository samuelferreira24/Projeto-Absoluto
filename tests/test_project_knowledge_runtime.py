from types import SimpleNamespace
from abs_core.project_knowledge import ProjectKnowledge
from abs_core.project_knowledge_runtime import RuntimeKnowledgeCollector


def test_runtime_snapshot_discovers_connections_devices_and_capabilities():
    cap = SimpleNamespace(id="echo", name="Echo", kind="test")
    conn = SimpleNamespace(id="internet-http", name="Internet", status="available",
                           capabilities=["web"], public=lambda: {
                               "id": "internet-http", "name": "Internet",
                               "status": "available", "capabilities": ["web"]})
    device = SimpleNamespace(id="local-1", name="Local", status="online",
                             capabilities=[], public=lambda: {
                                 "id": "local-1", "name": "Local",
                                 "status": "online", "capabilities": []})
    runtime = SimpleNamespace(
        registry=SimpleNamespace(list=lambda: [cap]),
        connections=SimpleNamespace(list=lambda: [conn]),
        resources=SimpleNamespace(list=lambda: [device]),
        tool_knowledge=SimpleNamespace(list=lambda: []),
    )
    k = RuntimeKnowledgeCollector().collect(runtime, ProjectKnowledge())
    assert any(x["id"] == "runtime:capability:echo" for x in k.capabilities)
    assert any(x["id"] == "runtime:connection:internet-http" for x in k.resources)
    assert any(x["id"] == "runtime:device:local-1" for x in k.nodes)
    assert any(x.kind == "runtime_snapshot" for x in k.evidence)
