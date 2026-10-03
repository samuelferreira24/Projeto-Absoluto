from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def safe_match_query(query: str) -> str:\n    """Converte linguagem livre em uma consulta FTS segura quando necessário."""\n    try:\n        tokens = re.findall(r"[\\wÀ-ÿ]+", query, flags=re.UNICODE)\n        return " OR ".join(f'"{token.replace(chr(34), chr(34)+chr(34))}"' for token in tokens) or query\n    except Exception:\n        return query\n\n\ndef search(conn: sqlite3.Connection, query: str, source: str | None, limit: int):
    if source:
        rows = conn.execute(
            """SELECT d.id, d.source_id, d.path, d.title, d.root,
                      snippet(documents_fts, 2, '[', ']', '…', 32),
                      bm25(documents_fts), d.latest_commit, d.latest_commit_date
               FROM documents_fts JOIN documents d ON d.id=documents_fts.rowid
               WHERE documents_fts MATCH ? AND d.source_id=?
               ORDER BY bm25(documents_fts) LIMIT ?""",
            (query, source, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            """SELECT d.id, d.source_id, d.path, d.title, d.root,
                      snippet(documents_fts, 2, '[', ']', '…', 32),
                      bm25(documents_fts), d.latest_commit, d.latest_commit_date
               FROM documents_fts JOIN documents d ON d.id=documents_fts.rowid
               WHERE documents_fts MATCH ?
               ORDER BY bm25(documents_fts) LIMIT ?""",
            (query, limit),
        ).fetchall()
    return rows


def search_symbols(conn: sqlite3.Connection, query: str, source: str | None, limit: int):
    if source:
        return conn.execute(
            """SELECT s.kind, s.name, d.source_id, d.path, s.line
               FROM symbols s JOIN documents d ON d.id=s.document_id
               WHERE (s.name LIKE ? OR s.kind LIKE ?) AND d.source_id=?
               ORDER BY s.name LIMIT ?""",
            (f"%{query}%", f"%{query}%", source, limit),
        ).fetchall()
    return conn.execute(
        """SELECT s.kind, s.name, d.source_id, d.path, s.line
           FROM symbols s JOIN documents d ON d.id=s.document_id
           WHERE (s.name LIKE ? OR s.kind LIKE ?)
           ORDER BY s.name LIMIT ?""",
        (f"%{query}%", f"%{query}%", limit),
    ).fetchall()


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the unified navigation index.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--source")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--symbols", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("query", nargs="+")
    args = parser.parse_args()
    query = " ".join(args.query)
    conn = sqlite3.connect(args.db)
    try:
        if args.symbols:
            rows = search_symbols(conn, query, args.source, args.limit)
            results = [
                {"kind": r[0], "name": r[1], "source": r[2], "path": r[3], "line": r[4]}
                for r in rows
            ]
        else:
            rows = search(conn, query, args.source, args.limit)
            results = [
                {"id": r[0], "source": r[1], "path": r[2], "title": r[3],
                 "root": r[4], "snippet": r[5], "rank": r[6],
                 "latest_commit": r[7], "latest_commit_date": r[8]}
                for r in rows
            ]
    finally:
        conn.close()
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for item in results:
            if args.symbols:
                print(f"[{item['source']}] {item['kind']} {item['name']} @ {item['path']}:{item['line']}")
            else:
                print(f"[{item['source']}] {item['path']}")
                print(f"  {item['snippet']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
