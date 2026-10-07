from __future__ import annotations

from pathlib import Path
import sqlite3

from .index import DEFAULT_EXCLUDES, MAX_FILE_SIZE_BYTES, is_text_file


def source_coverage(conn: sqlite3.Connection, source: str) -> dict:
    """Return measurable coverage of one indexed source."""
    row = conn.execute("SELECT root FROM documents WHERE source_id=? LIMIT 1", (source,)).fetchone()
    if not row:
        return {"source": source, "root": None, "filesystem": {}, "index": {}}
    root = Path(row[0])
    discovered = text_candidates = ignored = 0
    ignored_reasons = {"excluded_directory": 0, "non_text": 0, "oversized": 0, "unreadable": 0}
    seen: set[str] = set()
    if root.is_dir():
        for path in root.rglob("*"):
            if not path.is_file() or path.is_symlink():
                continue
            discovered += 1
            rel_parts = path.relative_to(root).parts
            if any(part in DEFAULT_EXCLUDES for part in rel_parts):
                ignored += 1; ignored_reasons["excluded_directory"] += 1; continue
            if not is_text_file(path):
                ignored += 1; ignored_reasons["non_text"] += 1; continue
            try:
                if path.stat().st_size > MAX_FILE_SIZE_BYTES:
                    ignored += 1; ignored_reasons["oversized"] += 1; continue
                text_candidates += 1
                seen.add(path.relative_to(root).as_posix())
            except OSError:
                ignored += 1; ignored_reasons["unreadable"] += 1
    indexed_paths = {r[0] for r in conn.execute("SELECT path FROM documents WHERE source_id=?", (source,)).fetchall()}
    stale = sorted(indexed_paths - seen)
    missing = sorted(seen - indexed_paths)
    ratio = (len(indexed_paths) / text_candidates) if text_candidates else 1.0
    return {
        "source": source, "root": str(root),
        "filesystem": {
            "discovered_files": discovered, "text_candidates": text_candidates,
            "ignored_files": ignored, "ignored_reasons": ignored_reasons,
            "unindexed_candidates": len(missing), "unindexed_paths": missing[:100],
        },
        "index": {
            "indexed_documents": len(indexed_paths), "stale_index_entries": len(stale),
            "stale_paths": stale[:100], "coverage_ratio": round(ratio, 6),
            "symbols": conn.execute("SELECT COUNT(*) FROM symbols s JOIN documents d ON d.id=s.document_id WHERE d.source_id=?", (source,)).fetchone()[0],
            "relations": conn.execute("SELECT COUNT(*) FROM relations r JOIN documents d ON d.id=r.source_document_id WHERE d.source_id=?", (source,)).fetchone()[0],
        },
    }


def all_coverage(conn: sqlite3.Connection) -> list[dict]:
    sources = [r[0] for r in conn.execute("SELECT DISTINCT source_id FROM documents ORDER BY source_id").fetchall()]
    return [source_coverage(conn, source) for source in sources]
