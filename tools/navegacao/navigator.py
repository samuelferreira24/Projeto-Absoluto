from __future__ import annotations

import sqlite3
from pathlib import Path

from .coverage import all_coverage, source_coverage
from .inspect import inspect_document
from .investigate import investigate
from .related import related
from .search import search, search_symbols


class KnowledgeNavigator:
    """Stable facade for Verifiable Knowledge Navigation.

    Independent from ABS runtime: can be used directly by an AI or operator.
    Navigator remains as a compatibility alias.
    """

    def __init__(self, db: Path | str):
        self.db = Path(db)

    def _connect(self):
        return sqlite3.connect(self.db)

    def search(self, query: str, *, source: str | None = None, limit: int = 20,
               path_prefix: str | None = None, extension: str | None = None):
        with self._connect() as conn:
            rows = search(conn, query, source, limit, path_prefix, extension)
        return [{"id": r[0], "source": r[1], "path": r[2], "title": r[3], "root": r[4],
                 "snippet": r[5], "rank": r[6], "latest_commit": r[7], "latest_commit_date": r[8]} for r in rows]

    def symbols(self, query: str, *, source: str | None = None, limit: int = 20, kind: str | None = None):
        with self._connect() as conn:
            rows = search_symbols(conn, query, source, limit, kind)
        return [{"kind": r[0], "name": r[1], "source": r[2], "path": r[3], "line": r[4]} for r in rows]

    def inspect(self, source: str, path: str):
        with self._connect() as conn:
            return inspect_document(conn, source, path)

    def related(self, target: str, *, source: str | None = None, relation_type: str | None = None, limit: int = 50):
        with self._connect() as conn:
            rows = related(conn, target, source, relation_type, limit)
        return [{"source": r[0], "path": r[1], "type": r[2], "target": r[3]} for r in rows]

    def investigate(self, question: str, *, source: str | None = None, limit: int = 8, inspect_limit: int = 5):
        with self._connect() as conn:
            return investigate(conn, question, source=source, limit=limit, inspect_limit=inspect_limit)

    def coverage(self, source: str | None = None):
        with self._connect() as conn:
            return source_coverage(conn, source) if source else all_coverage(conn)

    def navigate(self, query: str, *, source: str | None = None, limit: int = 20):
        """Compatibility bundle: search + symbols + first-hop relations."""
        results = self.search(query, source=source, limit=limit)
        symbols = self.symbols(query, source=source, limit=limit)
        relations = self.related(query, source=source, limit=limit)
        return {"query": query, "results": results, "symbols": symbols, "relations": relations}


Navigator = KnowledgeNavigator
