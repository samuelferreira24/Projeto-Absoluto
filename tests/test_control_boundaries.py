from abs_core.agent_registry import AgentRecord, AgentRegistry
from abs_core.conflicts import ConflictDetector
from abs_core.idempotency import IdempotencyLedger

def test_agent_registry_requires_identity_policy_and_responsibility():
    registry=AgentRegistry()
    agent=registry.register(AgentRecord("a1","Planner","planning","human-approved",["model:x"],["tool:y"]))
    assert agent.id=="a1"
    assert registry.get("a1").policy=="human-approved"

def test_conflict_detector_reports_disagreement_without_resolving_it():
    found=ConflictDetector().detect([
        {"field":"status","value":"ready","source":"a"},
        {"field":"status","value":"blocked","source":"b"},
    ])
    assert len(found)==1
    assert found[0].field=="status"
    assert set(found[0].values)=={"ready","blocked"}

def test_idempotency_reserves_only_once():
    ledger=IdempotencyLedger()
    first=ledger.reserve("k1")
    second=ledger.reserve("k1")
    assert first==second
    assert ledger.complete("k1",{"ok":True}).status=="completed"
