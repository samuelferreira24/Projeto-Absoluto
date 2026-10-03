from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def inspect_document(conn: sqlite3.Connection, source: str, path: str):
    row = conn.execute(
        """SELECT id, source_id, root, path, title, extension, size_bytes,
                  content_sha256, latest_commit, latest_commit_date, content
           FROM documents WHERE source_id=? AND path=?""",
        (source, path),
    ).fetchone()
    if not row:
        return None
    doc = {
        "id": row[0], "source": row[1], "root": row[2], "path": row[3],
        "title": row[4], "extension": row[5], "size_bytes": row[6],
        "content_sha256": row[7], "latest_commit": row[8],
        "latest_commit_date": row[9], "content": row[10],
    }
    doc["symbols"] = [
        {"kind": r[0], "name": r[1], "line": r[2]}
        for r in conn.execute(
            "SELECT kind, name, line FROM symbols WHERE document_id=? ORDER BY line",
            (row[0],),
        )
    ]
    doc["relations"] = [
        {"type": r[0], "target": r[1]}
        for r in conn.execute(
            "SELECT relation_type, target FROM relations WHERE source_document_id=? ORDER BY target",
            (row[0],),
        )
    ]
    return doc


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect one indexed object.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--source", required=True)
    parser.add_argument("--path", required=True)
    args = parser.parse_args()
    conn = sqlite3.connect(args.db)
    try:
        result = inspect_document(conn, args.source, args.path)
    finally:
        conn.close()
    if result is None:
        print("NOT_FOUND")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
