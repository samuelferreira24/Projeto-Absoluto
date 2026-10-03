from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

def related(conn, target, source, relation_type, limit):
    clauses, params = ["r.target LIKE ?"], [f"%{target}%"]
    if source:
        clauses.append("d.source_id=?"); params.append(source)
    if relation_type:
        clauses.append("r.relation_type=?"); params.append(relation_type)
    params.append(limit)
    return conn.execute(
        f"""SELECT d.source_id, d.path, r.relation_type, r.target
            FROM relations r JOIN documents d ON d.id=r.source_document_id
            WHERE {' AND '.join(clauses)}
            ORDER BY d.source_id, d.path, r.target LIMIT ?""", params).fetchall()

def main():
    parser = argparse.ArgumentParser(description="Navigate relation edges in the index.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--source")
    parser.add_argument("--type", dest="relation_type")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("target")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be >= 1")
    conn = sqlite3.connect(args.db)
    try:
        rows = related(conn, args.target, args.source, args.relation_type, args.limit)
    finally:
        conn.close()
    for source, path, relation_type, target in rows:
        print(f"[{source}] {path} --{relation_type}--> {target}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
