from __future__ import annotations

import json

from tools.navegacao.agent import dispatch
from tools.navegacao.index import connect, index_source


def test_agent_protocol_dispatches_without_abs_runtime(tmp_path):
    repo = tmp_path / "repo"; repo.mkdir()
    (repo / "engine.py").write_text(
        "class Engine:\n    pass\n# provenance\n", encoding="utf-8")
    db = tmp_path / "nav.sqlite"
    with connect(db) as conn:
        index_source(conn, "repo", repo); conn.commit()
        result = dispatch(conn, {"action": "search", "query": "provenance", "source": "repo"})
        assert result["results"]
        result = dispatch(conn, {"action": "symbols", "query": "Engine", "source": "repo"})
        assert result["results"]
        result = dispatch(conn, {"action": "coverage", "source": "repo"})
        assert result["result"]["index"]["indexed_documents"] == 1
