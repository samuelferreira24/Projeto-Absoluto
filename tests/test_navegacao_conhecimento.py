from __future__ import annotations

from pathlib import Path

from tools.navegacao.coverage import source_coverage
from tools.navegacao.index import connect, index_source
from tools.navegacao.investigate import investigate
from tools.navegacao.navigator import Navigator


def _repo(root: Path) -> None:
    (root / "pkg").mkdir()
    (root / "pkg" / "engine.py").write_text(
        "class NavigatorEngine:\n"
        "    def verify_source(self):\n"
        "        return True\n", encoding="utf-8")
    (root / "README.md").write_text(
        "# Knowledge navigation\nThe verifier checks indexed provenance.\n", encoding="utf-8")
    (root / "binary.bin").write_bytes(b"\x00\x01\x02")


def test_ai_investigation_is_standalone_and_provenance_aware(tmp_path):
    repo = tmp_path / "repo"; repo.mkdir()
    _repo(repo); db = tmp_path / "nav.sqlite"
    with connect(db) as conn:
        changed, removed = index_source(conn, "repo", repo); conn.commit()
        assert changed == 2 and removed == 0
        bundle = investigate(conn, "como verificar a proveniencia?", source="repo")
        assert bundle["mode"] == "evidence_retrieval"
        assert bundle["evidence"]
        assert all(item["sha256"] for item in bundle["evidence"])
        coverage = source_coverage(conn, "repo")
        assert coverage["index"]["indexed_documents"] == 2
        assert coverage["filesystem"]["ignored_files"] == 1
    nav = Navigator(db)
    assert nav.navigate("NavigatorEngine", source="repo")["symbols"]


def test_legacy_navigator_api_remains_usable(tmp_path):
    repo = tmp_path / "repo"; repo.mkdir()
    _repo(repo); db = tmp_path / "nav.sqlite"
    with connect(db) as conn:
        index_source(conn, "repo", repo); conn.commit()
    nav = Navigator(db)
    assert nav.search("provenance", source="repo")
    assert nav.symbols("NavigatorEngine", source="repo")
    assert nav.inspect("repo", "pkg/engine.py") is not None
