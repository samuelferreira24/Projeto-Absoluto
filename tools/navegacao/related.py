from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def related(conn: sqlite3.Connection, target: str, source: str | None, limit: int):
    if source:
        return conn.execute(
            """SELECT d.source_id, d.path, r.relation_type, r.target
               FROM relations r JOIN documents d ON d.id=r.source_document_id
               WHERE r.target LIKE ? AND d.source_id=?
               ORDER BY d.path LIMIT ?""",
            (f"%{target}%", source, limit),
        ).fetchall()
    return conn.execute(
        """SELECT d.source_id, d.path, r.relation_type, r.target
           FROM relations r JOIN documents d ON d.id=r.source_document_id
           WHERE r.target LIKE ?
           ORDER BY d.source_id, d.path LIMIT ?""",
        (f"%{target}%", limit),
    ).fetchall()


def main() -> int:
    parser = argparse.ArgumentParser(description="Navigate relation edges in the index.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--source")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("target")
    args = parser.parse_args()
    conn = sqlite3.connect(args.db)
    try:
        rows = related(conn, args.target, args.source, args.limit)
    finally:
        conn.close()
    for source, path, relation_type, target in rows:
        print(f"[{source}] {path} --{relation_type}--> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
