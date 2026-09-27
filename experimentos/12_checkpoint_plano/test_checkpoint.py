import json
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class MissionState:
    objective: str
    context: dict
    plan: list
    step: int
    status: str

def test_checkpoint_resume_and_replan():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"mission.json"
        s=MissionState("x", {"defined_steps": True}, ["WORKFLOW"], 1, "RUNNING")
        p.write_text(json.dumps(asdict(s)))
        loaded=MissionState(**json.loads(p.read_text()))
        assert loaded.plan == ["WORKFLOW"]
        loaded.context["open_ended"]=True
        loaded.plan=["WORKFLOW","AGENT"]
        loaded.step += 1
        p.write_text(json.dumps(asdict(loaded)))
        resumed=MissionState(**json.loads(p.read_text()))
        assert resumed.plan == ["WORKFLOW","AGENT"]
        assert resumed.step == 2
        assert resumed.status == "RUNNING"
