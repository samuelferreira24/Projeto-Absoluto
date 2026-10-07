from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from .coverage import all_coverage
from .index import connect, index_source
from .investigate import investigate
from .verify import verify_fts, verify_source


QUERIES = [
    ("file", "navigator.py"),
    ("concept", "proveniência"),
    ("structure", "Navigator"),
    ("implementation", "index"),
    ("verification", "hash"),
    ("cross_repo", "Sistema"),
]


def validate(db: Path, repositories: dict[str, Path]) -> dict:
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
        investigations = []
        for kind, query in QUERIES:
            bundle = investigate(conn, query, limit=6, inspect_limit=3)
            investigations.append({
                "kind": kind,
                "query": query,
                "documents": len(bundle["documents"]),
                "symbols": len(bundle["symbols"]),
                "relations": len(bundle["relations"]),
                "evidence": len(bundle["evidence"]),
            })
        return {
            "status": "PASS" if not bad else "FAIL",
            "repositories": {k: str(v) for k, v in repositories.items()},
            "indexing": totals,
            "coverage": coverage,
            "provenance": {"checked": len(provenance), "invalid": len(bad)},
            "query_matrix": investigations,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate navigation against real repositories.")
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
    result = validate(args.db, repos)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    print(text)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text + "\n", encoding="utf-8")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
