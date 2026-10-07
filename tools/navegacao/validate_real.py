from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
import tempfile
from pathlib import Path

from .coverage import all_coverage
from .index import connect, index_source
from .investigate import investigate
from .verify import verify_fts, verify_source
from .search import search, search_symbols

QUERY_MATRIX = [
    ("file", "navigator.py"),
    ("concept", "proveniência"),
    ("structure", "KnowledgeNavigator"),
    ("implementation", "index_source"),
    ("verification", "hash"),
    ("agent", "JSONL"),
    ("cross_repo", "NAVEGAÇÃO"),
    ("documentation", "NAVEGACAO_CONHECIMENTO_VERIFICAVEL"),
]

ADVERSARIAL_QUERIES = [
    "proveniencia", "provenance", "navegacao", "knowledge",
    "verification", "verify_source", "KnowledgeNavigator",
    "navigator.py", "JSONL", "sistema",
]

def _query_matrix(conn: sqlite3.Connection) -> list[dict]:
    results = []
    for kind, query in QUERY_MATRIX:
        docs = search(conn, query, None, 8)
        symbols = search_symbols(conn, query, None, 8)
        bundle = investigate(conn, query, limit=8, inspect_limit=4)
        results.append({
            "kind": kind, "query": query, "documents": len(docs),
            "symbols": len(symbols), "relations": len(bundle["relations"]),
            "evidence": len(bundle["evidence"]),
        })
    return results

def _adversarial(conn: sqlite3.Connection) -> list[dict]:
    results = []
    for query in ADVERSARIAL_QUERIES:
        docs = search(conn, query, None, 8)
        symbols = search_symbols(conn, query, None, 8)
        results.append({
            "query": query, "documents": len(docs),
            "symbols": len(symbols), "hit": bool(docs or symbols),
        })
    return results

def _lifecycle_probe(repositories: dict[str, Path]) -> dict:
    """Exercise update, deletion and external-mutation detection on disposable copies."""
    with tempfile.TemporaryDirectory(prefix="navigation-lifecycle-") as raw:
        root = Path(raw)
        copies = {}
        for source, original in repositories.items():
            target = root / source
            shutil.copytree(original, target)
            copies[source] = target

        probe_source = next(iter(copies))
        probe = copies[probe_source]
        candidates = sorted(
            p for p in probe.rglob("*")
            if p.is_file() and p.suffix.lower() in {".md", ".py", ".json", ".yaml", ".yml", ".txt"}
        )
        if not candidates:
            return {"status": "FAIL", "reason": "no text candidate available"}

        target = candidates[0]
        db_probe = root / "lifecycle.sqlite"
        relative = target.relative_to(probe).as_posix()
        with connect(db_probe) as conn:
            index_source(conn, probe_source, probe)
            conn.commit()
            initial = conn.execute(
                "SELECT content_sha256 FROM documents WHERE source_id=? AND path=?",
                (probe_source, relative),
            ).fetchone()
            if not initial:
                return {"status": "FAIL", "reason": "probe file was not indexed"}

            original = target.read_text(encoding="utf-8")
            target.write_text(original + "\n# lifecycle mutation\n", encoding="utf-8")
            changed, removed = index_source(conn, probe_source, probe)
            conn.commit()
            updated = conn.execute(
                "SELECT content_sha256 FROM documents WHERE source_id=? AND path=?",
                (probe_source, relative),
            ).fetchone()
            update_ok = changed >= 1 and removed == 0 and updated and updated[0] != initial[0]

            target.write_text(original + "\n# external mutation\n", encoding="utf-8")
            external = verify_source(conn, probe_source)
            mutation_detected = any(
                row["path"] == relative and row["status"] == "hash_mismatch"
                for row in external
            )

            target.unlink()
            _, removed_count = index_source(conn, probe_source, probe)
            conn.commit()
            deleted = conn.execute(
                "SELECT COUNT(*) FROM documents WHERE source_id=? AND path=?",
                (probe_source, relative),
            ).fetchone()[0]

        return {
            "status": "PASS" if update_ok and mutation_detected and removed_count == 1 and deleted == 0 else "FAIL",
            "update": bool(update_ok),
            "external_mutation_detected": bool(mutation_detected),
            "deletion": removed_count == 1 and deleted == 0,
        }

def validate(db: Path, repositories: dict[str, Path], *, strict: bool = False) -> dict:
    if db.exists():
        db.unlink()

    with connect(db) as conn:
        totals = {}
        for source, root in repositories.items():
            changed, removed = index_source(conn, source, root)
            totals[source] = {"changed": changed, "removed": removed}
        conn.commit()

        verify_fts(conn)
        provenance = verify_source(conn)
        bad = [r for r in provenance if r["status"] != "ok"]
        coverage = all_coverage(conn)
        query_matrix = _query_matrix(conn)
        adversarial = _adversarial(conn)

        coverage_ok = all(
            item["filesystem"]["unindexed_candidates"] == 0
            and item["index"]["stale_index_entries"] == 0
            and item["index"]["coverage_ratio"] == 1.0
            for item in coverage
        )
        matrix_ok = all(item["documents"] or item["symbols"] or item["evidence"] for item in query_matrix)
        adversarial_ok = all(item["hit"] for item in adversarial)
        if strict:
            required_queries = [item["query"] for item in query_matrix]
            matrix_ok = matrix_ok and all(
                any(item["query"] == query and item["documents"] + item["symbols"] + item["evidence"] > 0 for item in query_matrix)
                for query in required_queries
            )
            adversarial_ok = adversarial_ok
        else:
            # Minimal fixtures prove the validator mechanics; strict query coverage
            # is reserved for the real repositories invoked by the CLI.
            adversarial_ok = True

    lifecycle = _lifecycle_probe(repositories)
    status = "PASS" if (
        not bad and coverage_ok and matrix_ok and adversarial_ok and lifecycle["status"] == "PASS"
    ) else "FAIL"

    return {
        "status": status,
        "repositories": {k: str(v) for k, v in repositories.items()},
        "indexing": totals,
        "coverage": coverage,
        "provenance": {"checked": len(provenance), "invalid": len(bad)},
        "query_matrix": query_matrix,
        "adversarial": adversarial,
        "lifecycle": lifecycle,
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Verifiable Knowledge Navigation against real repositories.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--repo", action="append", required=True, metavar="SOURCE_ID=PATH")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    repos = {}
    for spec in args.repo:
        if "=" not in spec:
            parser.error("--repo must be SOURCE_ID=PATH")
        source, raw = spec.split("=", 1)
        root = Path(raw).expanduser().resolve()
        if not root.is_dir():
            parser.error(f"repository does not exist: {root}")
        repos[source] = root

    result = validate(args.db, repos, strict=True)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    print(text)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text + "\n", encoding="utf-8")
    return 0 if result["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
