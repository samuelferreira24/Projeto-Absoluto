from __future__ import annotations

import argparse
import hashlib
import sqlite3
from pathlib import Path


def verify_source(conn: sqlite3.Connection, source: str | None = None):
    clauses = ["1=1"]
    params = []
    if source:
        clauses.append("source_id=?")
        params.append(source)
    rows = conn.execute(f"SELECT id, source_id, root, path, content_sha256 FROM documents WHERE {' AND '.join(clauses)} ORDER BY source_id, path", params).fetchall()
    result = []
    for doc_id, source_id, root, path, expected in rows:
        file_path = Path(root) / path
        status = "ok"
        actual = None
        try:
            if not file_path.is_file() or file_path.is_symlink():
                status = "missing"
            else:
                actual = hashlib.sha256(file_path.read_bytes()).hexdigest()
                if actual != expected:
                    status = "hash_mismatch"
        except OSError as exc:
            status = f"unreadable:{type(exc).__name__}"
        result.append({"id": doc_id, "source": source_id, "path": path, "status": status, "expected_sha256": expected, "actual_sha256": actual})
    return result


def verify_fts(conn: sqlite3.Connection) -> None:
    conn.execute("INSERT INTO documents_fts(documents_fts) VALUES ('integrity-check')")


def rebuild_fts(conn: sqlite3.Connection) -> None:
    conn.execute("INSERT INTO documents_fts(documents_fts) VALUES ('rebuild')")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify indexed source provenance and FTS integrity.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--source")
    parser.add_argument("--rebuild", action="store_true", help="rebuild the derived FTS index before verification")
    args = parser.parse_args()
    conn = sqlite3.connect(args.db)
    try:
        if args.rebuild:
            rebuild_fts(conn)
        verify_fts(conn)
        rows = verify_source(conn, args.source)
    finally:
        conn.close()
    bad = [r for r in rows if r["status"] != "ok"]
    for row in rows:
        print(f"[{row['status']}] {row['source']}:{row['path']}")
    print(f"verified={len(rows)} invalid={len(bad)}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
