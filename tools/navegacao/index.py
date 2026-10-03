from __future__ import annotations

import argparse
import hashlib
import sqlite3
from pathlib import Path


DEFAULT_EXCLUDES = {
    ".git", "__pycache__", ".venv", "node_modules", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".tox", ".idea", ".vscode",
}

TEXT_EXTENSIONS = {
    ".md", ".markdown", ".txt", ".json", ".jsonl", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".py", ".js", ".ts", ".tsx", ".jsx",
    ".sh", ".bash", ".zsh", ".html", ".css", ".scss", ".sql",
    ".xml", ".csv", ".gitignore", ".gitattributes",
}


def is_text_file(path: Path) -> bool:
    if path.name in {".gitignore", ".gitattributes"}:
        return True
    return path.suffix.lower() in TEXT_EXTENSIONS


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def connect(db: Path) -> sqlite3.Connection:
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            source_id TEXT NOT NULL,
            root TEXT NOT NULL,
            path TEXT NOT NULL,
            title TEXT NOT NULL,
            extension TEXT NOT NULL,
            content_sha256 TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            content TEXT NOT NULL,
            UNIQUE(source_id, path)
        );

        CREATE INDEX IF NOT EXISTS idx_documents_source_path
            ON documents(source_id, path);

        CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
            title,
            path,
            content,
            source_id UNINDEXED,
            content='documents',
            content_rowid='id'
        );
    """)
    return conn


def upsert_document(conn: sqlite3.Connection, source_id: str, root: Path, path: Path) -> bool:
    data = path.read_bytes()
    if b"\x00" in data[:8192]:
        return False
    try:
        content = data.decode("utf-8")
    except UnicodeDecodeError:
        return False

    rel = path.relative_to(root).as_posix()
    sha = digest(data)
    old = conn.execute(
        "SELECT id, content_sha256 FROM documents WHERE source_id=? AND path=?",
        (source_id, rel),
    ).fetchone()
    if old and old[1] == sha:
        return False

    title = path.name
    ext = path.suffix.lower() or path.name
    if old:
        doc_id = old[0]
        conn.execute(
            """UPDATE documents SET root=?, title=?, extension=?,
               content_sha256=?, size_bytes=?, content=?
               WHERE id=?""",
            (str(root), title, ext, sha, len(data), content, doc_id),
        )
        conn.execute("DELETE FROM documents_fts WHERE rowid=?", (doc_id,))
    else:
        cur = conn.execute(
            """INSERT INTO documents
               (source_id, root, path, title, extension, content_sha256, size_bytes, content)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (source_id, str(root), rel, title, ext, sha, len(data), content),
        )
        doc_id = cur.lastrowid

    conn.execute(
        "INSERT INTO documents_fts(rowid, title, path, content, source_id) VALUES (?, ?, ?, ?, ?)",
        (doc_id, title, rel, content, source_id),
    )
    return True


def index_source(conn: sqlite3.Connection, source_id: str, root: Path) -> tuple[int, int]:
    changed = 0
    seen: set[str] = set()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in DEFAULT_EXCLUDES for part in path.relative_to(root).parts):
            continue
        if not is_text_file(path):
            continue
        rel = path.relative_to(root).as_posix()
        seen.add(rel)
        try:
            changed += int(upsert_document(conn, source_id, root, path))
        except (OSError, UnicodeError):
            continue

    rows = conn.execute(
        "SELECT id, path FROM documents WHERE source_id=?", (source_id,)
    ).fetchall()
    removed = 0
    for doc_id, rel in rows:
        if rel not in seen:
            conn.execute("DELETE FROM documents_fts WHERE rowid=?", (doc_id,))
            conn.execute("DELETE FROM documents WHERE id=?", (doc_id,))
            removed += 1
    return changed, removed


def main() -> int:
    parser = argparse.ArgumentParser(description="Index multiple repositories for navigation.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument(
        "--repo", action="append", required=True,
        metavar="SOURCE_ID=PATH",
        help="Repository source, e.g. projeto-absoluto=/workspace/Projeto-Absoluto",
    )
    args = parser.parse_args()

    conn = connect(args.db)
    totals = [0, 0]
    try:
        for spec in args.repo:
            if "=" not in spec:
                parser.error("--repo must be SOURCE_ID=PATH")
            source_id, raw_root = spec.split("=", 1)
            root = Path(raw_root).expanduser().resolve()
            if not root.is_dir():
                parser.error(f"repository does not exist: {root}")
            changed, removed = index_source(conn, source_id, root)
            totals[0] += changed
            totals[1] += removed
        conn.commit()
    finally:
        conn.close()

    print(f"indexed_changed={totals[0]} removed={totals[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
