from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def search(conn: sqlite3.Connection, query: str, source: str | None, limit: int):
    if source:
        sql = """
            SELECT d.id, d.source_id, d.path, d.title, d.root,
                   snippet(documents_fts, 2, '[', ']', '…', 24),
                   bm25(documents_fts)
            FROM documents_fts
            JOIN documents d ON d.id = documents_fts.rowid
            WHERE documents_fts MATCH ? AND d.source_id = ?
            ORDER BY bm25(documents_fts)
            LIMIT ?
        """
        args = (query, source, limit)
    else:
        sql = """
            SELECT d.id, d.source_id, d.path, d.title, d.root,
                   snippet(documents_fts, 2, '[', ']', '…', 24),
                   bm25(documents_fts)
            FROM documents_fts
            JOIN documents d ON d.id = documents_fts.rowid
            WHERE documents_fts MATCH ?
            ORDER BY bm25(documents_fts)
            LIMIT ?
        """
        args = (query, limit)
    return conn.execute(sql, args).fetchall()


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the unified navigation index.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--source")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("query", nargs="+")
    args = parser.parse_args()

    query = " ".join(args.query)
    conn = sqlite3.connect(args.db)
    try:
        rows = search(conn, query, args.source, args.limit)
    finally:
        conn.close()

    results = [
        {
            "id": r[0],
            "source": r[1],
            "path": r[2],
            "title": r[3],
            "root": r[4],
            "snippet": r[5],
            "rank": r[6],
        }
        for r in rows
    ]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"[{item['source']}] {item['path']}")
            print(f"  {item['snippet']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
