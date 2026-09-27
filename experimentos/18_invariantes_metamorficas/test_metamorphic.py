import importlib.util
from pathlib import Path

p=Path(__file__).parents[1]/"06_prototipo_executavel"/"prototipo.py"
spec=importlib.util.spec_from_file_location("proto06",p)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def choose(C,ctx):
    return C().choose(m.Mission("x",dict(ctx)))

def test_irrelevant_resource_does_not_change_mode():
    base={"defined_steps":True}
    altered=dict(base,resource="vps",resource_status="available")
    for C in (m.CandidateA,m.CandidateB):
        assert choose(C,base)==choose(C,altered)

def test_context_change_must_change_strategy_when_requirement_changes():
    before={"defined_steps":True}
    after={"open_ended":True}
    for C in (m.CandidateA,m.CandidateB):
        assert choose(C,before)=="WORKFLOW"
        assert choose(C,after)=="AGENT"

def test_failure_is_monotonic_toward_recovery():
    for C in (m.CandidateA,m.CandidateB):
        mission=m.Mission("x",{"defined_steps":True})
        trace,status=C().run(mission,m.ScriptedExecutor(["failure","success"]))
        assert trace[:2]==["WORKFLOW","RECOVERY"]
        assert status=="COMPLETE"
