from __future__ import annotations

import argparse
import ast
import hashlib
import re
import sqlite3
import subprocess
from pathlib import Path

DEFAULT_EXCLUDES = {".git", "__pycache__", ".venv", "node_modules", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".tox", ".idea", ".vscode"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024

TEXT_EXTENSIONS = {".md", ".markdown", ".txt", ".json", ".jsonl", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".bash",
    ".zsh", ".html", ".css", ".scss", ".sql", ".xml", ".csv", ".gitignore", ".gitattributes"}

def is_text_file(path: Path) -> bool:
    return path.name in {".gitignore", ".gitattributes"} or path.suffix.lower() in TEXT_EXTENSIONS

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def connect(db: Path) -> sqlite3.Connection:
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS navigation_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        INSERT OR IGNORE INTO navigation_meta(key, value) VALUES ('schema_version', '2');
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY, source_id TEXT NOT NULL, root TEXT NOT NULL,
            path TEXT NOT NULL, title TEXT NOT NULL, extension TEXT NOT NULL,
            content_sha256 TEXT NOT NULL, size_bytes INTEGER NOT NULL, content TEXT NOT NULL,
            latest_commit TEXT, latest_commit_date TEXT, UNIQUE(source_id, path)
        );
        CREATE INDEX IF NOT EXISTS idx_documents_source_path ON documents(source_id, path);
        CREATE TABLE IF NOT EXISTS symbols (
            id INTEGER PRIMARY KEY, document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
            kind TEXT NOT NULL, name TEXT NOT NULL, line INTEGER,
            UNIQUE(document_id, kind, name, line)
        );
        CREATE INDEX IF NOT EXISTS idx_symbols_name ON symbols(name);
        CREATE TABLE IF NOT EXISTS relations (
            id INTEGER PRIMARY KEY, source_document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
            relation_type TEXT NOT NULL, target TEXT NOT NULL,
            UNIQUE(source_document_id, relation_type, target)
        );
        CREATE INDEX IF NOT EXISTS idx_relations_target ON relations(target);
        CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
            title, path, content, source_id UNINDEXED, content='documents', content_rowid='id'
        );
    """)
    return conn

def git_metadata_map(root: Path) -> dict[str, tuple[str, str]]:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(root), "log", "--all", "--date=iso-strict",
             "--format=COMMIT%x09%H%x09%cI", "--name-only", "--diff-filter=ACMR"],
            text=True, stderr=subprocess.DEVNULL, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return {}
    result: dict[str, tuple[str, str]] = {}
    current: tuple[str, str] | None = None
    for line in out.splitlines():
        if line.startswith("COMMIT\t"):
            _, sha, date = line.split("\t", 2)
            current = (sha, date)
        elif current and line:
            result.setdefault(line.replace("\\", "/"), current)
    return result

def extract_symbols(content: str, suffix: str):
    found = []
    if suffix == ".py":
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    found.append(("function", node.name, node.lineno))
                elif isinstance(node, ast.ClassDef):
                    found.append(("class", node.name, node.lineno))
        except SyntaxError:
            pass
    elif suffix in {".js", ".ts", ".tsx", ".jsx"}:
        for kind, pattern in [
            ("function", r"\bfunction\s+([A-Za-z_$][\w$]*)"),
            ("class", r"\bclass\s+([A-Za-z_$][\w$]*)"),
            ("function", r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\(")]:
            for m in re.finditer(pattern, content):
                found.append((kind, m.group(1), content.count("\n", 0, m.start()) + 1))
    return found

def extract_relations(content: str, suffix: str):
    found = []
    if suffix == ".py":
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    found.extend(("imports", alias.name) for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    found.append(("imports", node.module))
        except SyntaxError:
            pass
    elif suffix in {".js", ".ts", ".tsx", ".jsx"}:
        for m in re.finditer(r"""(?:import\s+.*?\s+from\s+|require\(\s*|import\(\s*)['"]([^'"]+)['"]""", content):
            found.append(("imports", m.group(1)))
    return found

def refresh_structure(conn, doc_id, content, suffix):
    conn.execute("DELETE FROM symbols WHERE document_id=?", (doc_id,))
    conn.execute("DELETE FROM relations WHERE source_document_id=?", (doc_id,))
    for kind, name, line in extract_symbols(content, suffix):
        conn.execute("INSERT OR IGNORE INTO symbols(document_id, kind, name, line) VALUES (?, ?, ?, ?)",
                     (doc_id, kind, name, line))
    for relation_type, target in extract_relations(content, suffix):
        conn.execute("INSERT OR IGNORE INTO relations(source_document_id, relation_type, target) VALUES (?, ?, ?)",
                     (doc_id, relation_type, target))

def upsert_document(conn, source_id, root, path, git_meta):
    if path.is_symlink() or path.stat().st_size > MAX_FILE_SIZE_BYTES:
        return False
    data = path.read_bytes()
    if b"\x00" in data[:8192]:
        return False
    try:
        content = data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    rel = path.relative_to(root).as_posix()
    sha = digest(data)
    old = conn.execute("SELECT id, content_sha256 FROM documents WHERE source_id=? AND path=?",
                       (source_id, rel)).fetchone()
    if old and old[1] == sha:
        return False
    title, ext = path.name, (path.suffix.lower() or path.name)
    commit, commit_date = git_meta.get(rel, (None, None))
    if old:
        doc_id = old[0]
        conn.execute("""UPDATE documents SET root=?, title=?, extension=?, content_sha256=?,
                        size_bytes=?, content=?, latest_commit=?, latest_commit_date=? WHERE id=?""",
                     (str(root), title, ext, sha, len(data), content, commit, commit_date, doc_id))
        conn.execute("DELETE FROM documents_fts WHERE rowid=?", (doc_id,))
    else:
        doc_id = conn.execute("""INSERT INTO documents
            (source_id, root, path, title, extension, content_sha256, size_bytes, content, latest_commit, latest_commit_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (source_id, str(root), rel, title, ext, sha, len(data), content, commit, commit_date)).lastrowid
    conn.execute("INSERT INTO documents_fts(rowid, title, path, content, source_id) VALUES (?, ?, ?, ?, ?)",
                 (doc_id, title, rel, content, source_id))
    refresh_structure(conn, doc_id, content, ext)
    return True

def index_source(conn, source_id: str, root: Path):
    changed, seen = 0, set()
    git_meta = git_metadata_map(root)
    paths = sorted((p for p in root.rglob("*") if p.is_file() and not p.is_symlink()),
                   key=lambda p: p.relative_to(root).as_posix())
    for path in paths:
        rel_parts = path.relative_to(root).parts
        if any(part in DEFAULT_EXCLUDES for part in rel_parts) or not is_text_file(path):
            continue
        rel = path.relative_to(root).as_posix()
        try:
            if path.stat().st_size > MAX_FILE_SIZE_BYTES:
                continue
            seen.add(rel)
            changed += int(upsert_document(conn, source_id, root, path, git_meta))
        except (OSError, UnicodeError):
            continue
    removed = 0
    for doc_id, rel in conn.execute("SELECT id, path FROM documents WHERE source_id=?", (source_id,)).fetchall():
        if rel not in seen:
            conn.execute("DELETE FROM documents_fts WHERE rowid=?", (doc_id,))
            conn.execute("DELETE FROM documents WHERE id=?", (doc_id,))
            removed += 1
    return changed, removed

def main():
    parser = argparse.ArgumentParser(description="Index multiple repositories for navigation.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--repo", action="append", required=True, metavar="SOURCE_ID=PATH")
    args = parser.parse_args()
    conn = connect(args.db)
    totals = [0, 0]
    try:
        for spec in args.repo:
            if "=" not in spec:
                parser.error("--repo must be SOURCE_ID=PATH")
            source_id, raw_root = spec.split("=", 1)
            if not source_id.strip():
                parser.error("SOURCE_ID cannot be empty")
            root = Path(raw_root).expanduser().resolve()
            if not root.is_dir():
                parser.error(f"repository does not exist: {root}")
            changed, removed = index_source(conn, source_id.strip(), root)
            totals[0] += changed
            totals[1] += removed
        conn.commit()
    finally:
        conn.close()
    print(f"indexed_changed={totals[0]} removed={totals[1]}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
