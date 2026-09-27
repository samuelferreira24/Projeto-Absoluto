import importlib.util
from pathlib import Path
import copy

p=Path(__file__).parents[1]/"06_prototipo_executavel"/"prototipo.py"
spec=importlib.util.spec_from_file_location("proto06", p)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def run(C, ctx, outcomes):
    return C().run(m.Mission("x", copy.deepcopy(ctx)), m.ScriptedExecutor(list(outcomes)))

def test_same_mission_matrix():
    cases=[
      ({"defined_steps":True},["failure","success"]),
      ({"defined_steps":True},["state_changed","success"]),
      ({"high_uncertainty":True},["verification_failure","success"]),
      ({"parallelizable":True,"independent_parts":3},["failure","success"]),
      ({"required_capability_missing":True},["success"]),
      ({"authorization_required":True,"grant_authorization":True},["success"]),
    ]
    for ctx,outcomes in cases:
        a=run(m.CandidateA,ctx,outcomes); b=run(m.CandidateB,ctx,outcomes)
        assert a[1]==b[1]=="COMPLETE"
        assert a[0] == b[0]

def test_compound_failure_and_recovery():
    for C in (m.CandidateA,m.CandidateB):
        trace,status=run(C,{"defined_steps":True},["failure","failure","success"])
        assert status=="COMPLETE"
        assert trace.count("RECOVERY")==2
