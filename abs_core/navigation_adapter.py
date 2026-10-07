from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from tools.navegacao.coverage import all_coverage
from tools.navegacao.index import connect, index_source
from tools.navegacao.investigate import investigate
from tools.navegacao.navigator import KnowledgeNavigator
from tools.navegacao.verify import verify_fts, verify_source


class KnowledgeNavigationCapability:
    """Native ABS adapter over the independent Verifiable Knowledge Navigation layer."""
    id = "knowledge-navigation"
    name = "Navegação de Conhecimento Verificável"
    kind = "knowledge"

    def __init__(self, *, db_path=None, sources=None):
        self.db_path = Path(db_path or os.getenv("ABS_NAVIGATION_DB_PATH", ".abs-navigation/index.sqlite"))
        self.sources = sources or self._default_sources()
        self._initialized = False

    def _default_sources(self):
        root = Path(__file__).resolve().parents[1]
        sources = {"projeto-absoluto": root}
        sibling = root.parent / "Sistema"
        if sibling.is_dir():
            sources["sistema"] = sibling
        raw = os.getenv("ABS_NAVIGATION_SOURCES", "").strip()
        if raw:
            for spec in raw.split(","):
                if "=" not in spec:
                    continue
                source, path = spec.split("=", 1)
                path = Path(path).expanduser()
                if source.strip() and path.is_dir():
                    sources[source.strip()] = path.resolve()
        return sources

    def _ensure_index(self):
        if self._initialized:
            return
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with connect(self.db_path) as conn:
            for source, root in self.sources.items():
                index_source(conn, source, Path(root))
            conn.commit()
        self._initialized = True

    def execute(self, objective: str, context: dict[str, Any]):
        self._ensure_index()
        action = str(context.get("action") or "investigate").strip().lower()
        source = context.get("source")
        limit = int(context.get("limit", 8))

        with connect(self.db_path) as conn:
            if action == "search":
                from tools.navegacao.search import search
                rows = search(conn, str(context.get("query") or objective), source, limit)
                result = {"action": action, "results": [
                    {"source": r[1], "path": r[2], "title": r[3], "snippet": r[5],
                     "latest_commit": r[7], "latest_commit_date": r[8]} for r in rows]}
            elif action == "symbols":
                from tools.navegacao.search import search_symbols
                rows = search_symbols(conn, str(context.get("query") or objective), source, limit)
                result = {"action": action, "results": [
                    {"kind": r[0], "name": r[1], "source": r[2], "path": r[3], "line": r[4]}
                    for r in rows]}
            elif action == "inspect":
                nav = KnowledgeNavigator(self.db_path)
                result = {"action": action, "result": nav.inspect(str(source), str(context["path"]))}
            elif action == "coverage":
                result = {"action": action, "result": all_coverage(conn)}
            elif action == "verify":
                verify_fts(conn)
                rows = verify_source(conn, source)
                result = {"action": action, "checked": len(rows),
                          "invalid": [row for row in rows if row["status"] != "ok"]}
            else:
                result = investigate(conn, str(context.get("question") or objective),
                                     source=source, limit=limit,
                                     inspect_limit=int(context.get("inspect_limit", 5)))
        return {"type": "knowledge_navigation", "capability": self.id,
                "objective": objective, "source_filter": source, "result": result}
