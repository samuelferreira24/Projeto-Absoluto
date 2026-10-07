from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from .coverage import all_coverage, source_coverage
from .inspect import inspect_document
from .investigate import investigate
from .related import related
from .search import search, search_symbols
from .verify import verify_fts, verify_source


def dispatch(conn: sqlite3.Connection, request: dict) -> dict:
    action = str(request.get("action", "investigate"))
    source = request.get("source")
    limit = int(request.get("limit", 20))
    if limit < 1:
        raise ValueError("limit must be >= 1")

    if action == "search":
        rows = search(conn, str(request.get("query", "")), source, limit,
                      request.get("path_prefix"), request.get("extension"))
        return {"action": action, "results": [
            {"id": r[0], "source": r[1], "path": r[2], "title": r[3],
             "snippet": r[5], "rank": r[6], "latest_commit": r[7],
             "latest_commit_date": r[8]} for r in rows]}

    if action == "symbols":
        rows = search_symbols(conn, str(request.get("query", "")), source, limit, request.get("kind"))
        return {"action": action, "results": [
            {"kind": r[0], "name": r[1], "source": r[2], "path": r[3], "line": r[4]} for r in rows]}

    if action == "inspect":
        result = inspect_document(conn, str(source), str(request["path"]))
        return {"action": action, "result": result}

    if action == "related":
        rows = related(conn, str(request.get("query", "")), source, request.get("relation_type"), limit)
        return {"action": action, "results": [
            {"source": r[0], "path": r[1], "type": r[2], "target": r[3]} for r in rows]}

    if action == "investigate":
        return investigate(conn, str(request.get("question", request.get("query", ""))),
                           source=source, limit=limit,
                           inspect_limit=int(request.get("inspect_limit", 5)))

    if action == "coverage":
        return {"action": action, "result": source_coverage(conn, source) if source else all_coverage(conn)}

    if action == "verify":
        verify_fts(conn)
        rows = verify_source(conn, source)
        return {"action": action, "checked": len(rows),
                "invalid": [r for r in rows if r["status"] != "ok"]}

    raise ValueError(f"unknown action: {action}")


def main() -> int:
    parser = argparse.ArgumentParser(description="JSON-lines agent protocol for Verifiable Knowledge Navigation.")
    parser.add_argument("--db", required=True, type=Path)
    args = parser.parse_args()

    with sqlite3.connect(args.db) as conn:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                request = json.loads(line)
                if not isinstance(request, dict):
                    raise ValueError("request must be a JSON object")
                result = dispatch(conn, request)
                print(json.dumps({"ok": True, **result}, ensure_ascii=False), flush=True)
            except Exception as exc:
                print(json.dumps({"ok": False, "error": type(exc).__name__,
                                  "message": str(exc)}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
