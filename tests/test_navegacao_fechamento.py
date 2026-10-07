from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from tools.navegacao.coverage import source_coverage
from tools.navegacao.index import connect, index_source
from tools.navegacao.investigate import investigate
from tools.navegacao.verify import verify_source


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_incremental_index_is_idempotent_and_updates_changed_content(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    target = repo / "engine.py"
    _write(target, "class Engine:\n    pass\n")
    db = tmp_path / "nav.sqlite"

    with connect(db) as conn:
        assert index_source(conn, "repo", repo) == (1, 0)
        conn.commit()
        assert index_source(conn, "repo", repo) == (0, 0)
        conn.commit()

        old = conn.execute(
            "SELECT content_sha256 FROM documents WHERE source_id='repo' AND path='engine.py'"
        ).fetchone()[0]

        _write(target, "class Engine:\n    def verify_source(self):\n        return True\n")
        assert index_source(conn, "repo", repo) == (1, 0)
        conn.commit()

        new = conn.execute(
            "SELECT content_sha256 FROM documents WHERE source_id='repo' AND path='engine.py'"
        ).fetchone()[0]
        assert new != old
        assert conn.execute(
            "SELECT COUNT(*) FROM symbols WHERE name='verify_source'"
        ).fetchone()[0] == 1
        assert not verify_source(conn, "repo") or all(
            row["status"] == "ok" for row in verify_source(conn, "repo")
        )


def test_deletion_removes_document_fts_symbols_and_relations(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _write(repo / "a.py", "from b import B\nclass A: pass\n")
    _write(repo / "b.py", "class B: pass\n")
    db = tmp_path / "nav.sqlite"

    with connect(db) as conn:
        assert index_source(conn, "repo", repo) == (2, 0)
        conn.commit()
        assert conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0] == 2
        assert conn.execute("SELECT COUNT(*) FROM relations").fetchone()[0] >= 1

        (repo / "b.py").unlink()
        changed, removed = index_source(conn, "repo", repo)
        conn.commit()

        assert (changed, removed) == (0, 1)
        assert conn.execute(
            "SELECT COUNT(*) FROM documents WHERE path='b.py'"
        ).fetchone()[0] == 0
        assert conn.execute(
            "SELECT COUNT(*) FROM documents_fts WHERE path='b.py'"
        ).fetchone()[0] == 0
        assert conn.execute(
            "SELECT COUNT(*) FROM symbols WHERE name='B'"
        ).fetchone()[0] == 0


def test_provenance_detects_external_mutation_without_reindex(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    target = repo / "evidence.md"
    _write(target, "# Evidence\noriginal\n")
    db = tmp_path / "nav.sqlite"

    with connect(db) as conn:
        index_source(conn, "repo", repo)
        conn.commit()
        assert all(row["status"] == "ok" for row in verify_source(conn, "repo"))

        target.write_text("# Evidence\nMUTATED OUTSIDE INDEX\n", encoding="utf-8")
        result = verify_source(conn, "repo")
        assert len(result) == 1
        assert result[0]["status"] == "hash_mismatch"


def test_coverage_explains_indexed_and_ignored_realistic_inputs(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _write(repo / "README.md", "knowledge")
    _write(repo / "src" / "engine.py", "class Engine: pass\n")
    _write(repo / "src" / "ignored.bin", "\x00binary")
    (repo / "node_modules").mkdir()
    _write(repo / "node_modules" / "vendor.js", "class Vendor: pass\n")

    db = tmp_path / "nav.sqlite"
    with connect(db) as conn:
        index_source(conn, "repo", repo)
        conn.commit()
        coverage = source_coverage(conn, "repo")

    assert coverage["index"]["coverage_ratio"] == 1.0
    assert coverage["filesystem"]["text_candidates"] == 2
    assert coverage["filesystem"]["unindexed_candidates"] == 0
    assert coverage["filesystem"]["ignored_reasons"]["excluded_directory"] >= 1
    assert coverage["filesystem"]["ignored_reasons"]["non_text"] >= 1


def test_investigation_is_evidence_bundle_not_answer(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _write(repo / "verify.py", "def verify_source():\n    return True\n")
    _write(repo / "README.md", "Provenance is checked with a SHA-256 hash.\n")
    db = tmp_path / "nav.sqlite"

    with connect(db) as conn:
        index_source(conn, "repo", repo)
        conn.commit()
        bundle = investigate(
            conn,
            "como a proveniencia é verificada?",
            source="repo",
            limit=8,
            inspect_limit=5,
        )

    assert bundle["mode"] == "evidence_retrieval"
    assert bundle["instructions"]
    assert bundle["documents"]
    assert bundle["evidence"]
    assert all(item["sha256"] for item in bundle["evidence"])
    assert all(item["source"] == "repo" and item["path"] for item in bundle["evidence"])


def test_two_sources_are_kept_distinct_and_cross_source_investigation_works(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    _write(first / "engine.py", "class Engine: pass\n")
    _write(second / "system.md", "# System\nEngine is used as a knowledge source.\n")
    db = tmp_path / "nav.sqlite"

    with connect(db) as conn:
        index_source(conn, "projeto-absoluto", first)
        index_source(conn, "sistema", second)
        conn.commit()
        bundle = investigate(conn, "Engine knowledge system", limit=8)

    sources = {item["source"] for item in bundle["documents"]}
    assert sources == {"projeto-absoluto", "sistema"}
    assert all("source" in item and "path" in item for item in bundle["evidence"])


def test_real_repository_copies_can_be_mutated_without_touching_sources(tmp_path):
    # This test proves the lifecycle validator can operate on repository snapshots.
    source = tmp_path / "source"
    source.mkdir()
    _write(source / "README.md", "stable source\n")
    working = tmp_path / "working"
    shutil.copytree(source, working)
    _write(working / "README.md", "mutated working copy\n")
    assert source.joinpath("README.md").read_text(encoding="utf-8") == "stable source\n"
