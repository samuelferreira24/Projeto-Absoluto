import importlib.util
import random
from pathlib import Path

p=Path(__file__).parents[1]/"06_prototipo_executavel"/"prototipo.py"
spec=importlib.util.spec_from_file_location("proto06",p)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def execute(C,ctx,outcomes):
    return C().run(m.Mission("benchmark",dict(ctx)),m.ScriptedExecutor(list(outcomes)))

def test_1000_deterministic_missions():
    rng=random.Random(20260927)
    for _ in range(1000):
        ctx={
          "defined_steps":rng.choice([False,True]),
          "open_ended":rng.choice([False,True]),
          "high_uncertainty":rng.choice([False,True]),
          "parallelizable":rng.choice([False,True]),
          "independent_parts":rng.randint(1,4),
        }
        outcomes=["success"]
        a=execute(m.CandidateA,ctx,outcomes)
        b=execute(m.CandidateB,ctx,outcomes)
        assert a==b
        assert a[1]=="COMPLETE"

def test_repeatability():
    ctx={"defined_steps":True,"open_ended":True,"parallelizable":True,"independent_parts":3}
    assert execute(m.CandidateA,ctx,["success"])==execute(m.CandidateA,ctx,["success"])
    assert execute(m.CandidateB,ctx,["success"])==execute(m.CandidateB,ctx,["success"])
