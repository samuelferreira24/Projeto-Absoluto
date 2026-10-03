from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path

def safe_match_query(query: str) -> str:
    tokens = re.findall(r"[\wÀ-ÿ]+", query, flags=re.UNICODE)
    return " OR ".join(f'"{token.replace(chr(34), chr(34) + chr(34))}"' for token in tokens) or query

def _search_raw(conn, query, source, path_prefix, extension, limit):
    clauses, params = ["documents_fts MATCH ?"], [query]
    if source:
        clauses.append("d.source_id=?"); params.append(source)
    if path_prefix:
        clauses.append("d.path LIKE ?"); params.append(path_prefix.rstrip("/") + "%")
    if extension:
        ext = extension if extension.startswith(".") else "." + extension
        clauses.append("d.extension=?"); params.append(ext.lower())
    params.append(limit)
    return conn.execute(
        f"""SELECT d.id, d.source_id, d.path, d.title, d.root,
                   snippet(documents_fts, 2, '[', ']', '…', 32),
                   bm25(documents_fts), d.latest_commit, d.latest_commit_date
            FROM documents_fts JOIN documents d ON d.id=documents_fts.rowid
            WHERE {' AND '.join(clauses)}
            ORDER BY bm25(documents_fts), d.path LIMIT ?""", params).fetchall()

def search(conn, query, source, limit, path_prefix=None, extension=None):
    query = query.strip()
    if not query or limit < 1:
        return []
    try:
        return _search_raw(conn, query, source, path_prefix, extension, limit)
    except sqlite3.OperationalError:
        return _search_raw(conn, safe_match_query(query), source, path_prefix, extension, limit)

def search_symbols(conn, query, source, limit, kind=None):
    clauses = ["(s.name LIKE ? OR s.kind LIKE ?)"]
    params = [f"%{query}%", f"%{query}%"]
    if source:
        clauses.append("d.source_id=?"); params.append(source)
    if kind:
        clauses.append("s.kind=?"); params.append(kind)
    params.append(limit)
    return conn.execute(
        f"""SELECT s.kind, s.name, d.source_id, d.path, s.line
            FROM symbols s JOIN documents d ON d.id=s.document_id
            WHERE {' AND '.join(clauses)}
            ORDER BY s.name, d.path, s.line LIMIT ?""", params).fetchall()

def main():
    parser = argparse.ArgumentParser(description="Search the unified navigation index.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--source")
    parser.add_argument("--path-prefix")
    parser.add_argument("--extension")
    parser.add_argument("--kind")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--symbols", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("query", nargs="+")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be >= 1")
    query = " ".join(args.query)
    conn = sqlite3.connect(args.db)
    try:
        if args.symbols:
            rows = search_symbols(conn, query, args.source, args.limit, args.kind)
            results = [{"kind": r[0], "name": r[1], "source": r[2], "path": r[3], "line": r[4]} for r in rows]
        else:
            rows = search(conn, query, args.source, args.limit, args.path_prefix, args.extension)
            results = [{"id": r[0], "source": r[1], "path": r[2], "title": r[3], "root": r[4],
                        "snippet": r[5], "rank": r[6], "latest_commit": r[7], "latest_commit_date": r[8]} for r in rows]
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
