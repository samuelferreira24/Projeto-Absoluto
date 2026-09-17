import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_status_capacidades_do_quadro_mestre():
    path = ROOT / "cerebro" / "especificacao" / "STATUS_CAPACIDADES_V0_1.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["project_id"] == "PA-PROJETO-ABSOLUTO"
    assert len(data["capabilities"]) >= 30
    ids = [item["id"] for item in data["capabilities"]]
    assert len(ids) == len(set(ids))
    assert data["current_focus"]
    assert data["next_gate"]
