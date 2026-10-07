from __future__ import annotations

import re
import sqlite3
import unicodedata

from .inspect import inspect_document
from .related import related
from .search import search, search_symbols

TERM_ALIASES = {
    "proveniencia": {"provenance"},
    "navegacao": {"navigation"},
    "conhecimento": {"knowledge"},
    "verificacao": {"verification", "verify"},
    "memoria": {"memory"},
    "sistema": {"system"},
    "busca": {"search"},
    "arquivo": {"file"},
}


def _terms(query: str) -> list[str]:
    normalized = unicodedata.normalize("NFKD", query)
    normalized = "".join(c for c in normalized if not unicodedata.combining(c))
    raw = re.findall(r"[A-Za-z0-9_À-ÿ]+", query)
    plain = re.findall(r"[A-Za-z0-9_]+", normalized)
    result: list[str] = []
    for term in [*raw, *plain]:
        term = term.strip().lower()
        if len(term) >= 3 and term not in result:
            result.append(term)
        for alias in TERM_ALIASES.get(term, set()):
            if alias not in result:
                result.append(alias)
    return result


def investigate(conn: sqlite3.Connection, question: str, *, source: str | None = None,
                limit: int = 8, inspect_limit: int = 5) -> dict:
    if limit < 1 or inspect_limit < 1:
        raise ValueError("limits must be >= 1")
    candidates = []
    seen_paths: set[tuple[str, str]] = set()
    queries = [question, *_terms(question)]
    for q in queries:
        for item in search(conn, q, source, limit):
            key = (item[1], item[2])
            if key in seen_paths:
                continue
            seen_paths.add(key)
            candidates.append({"type": "document", "source": item[1], "path": item[2],
                               "title": item[3], "snippet": item[5], "rank": item[6],
                               "latest_commit": item[7], "latest_commit_date": item[8]})
            if len(candidates) >= limit:
                break
        if len(candidates) >= limit:
            break
    symbols, seen_symbols = [], set()
    for term in _terms(question):
        for row in search_symbols(conn, term, source, limit):
            key = tuple(row)
            if key not in seen_symbols:
                seen_symbols.add(key)
                symbols.append({"kind": row[0], "name": row[1], "source": row[2],
                                "path": row[3], "line": row[4]})
            if len(symbols) >= limit:
                break
        if len(symbols) >= limit:
            break
    evidence = []
    for item in candidates[:inspect_limit]:
        doc = inspect_document(conn, item["source"], item["path"])
        if doc:
            evidence.append({"source": doc["source"], "path": doc["path"],
                             "sha256": doc["content_sha256"],
                             "latest_commit": doc["latest_commit"],
                             "latest_commit_date": doc["latest_commit_date"],
                             "symbols": doc["symbols"], "relations": doc["relations"],
                             "content": doc["content"]})
    relations, seen_relations = [], set()
    for term in _terms(question):
        for row in related(conn, term, source, None, limit):
            key = tuple(row)
            if key not in seen_relations:
                seen_relations.add(key)
                relations.append({"source": row[0], "path": row[1],
                                   "relation_type": row[2], "target": row[3]})
            if len(relations) >= limit:
                break
        if len(relations) >= limit:
            break
    return {
        "mode": "evidence_retrieval", "question": question, "source_filter": source,
        "query_terms": _terms(question), "documents": candidates,
        "symbols": symbols, "relations": relations, "evidence": evidence,
        "instructions": [
            "Treat this bundle as evidence, not as an answer.",
            "Prefer exact source/path/hash evidence over inference.",
            "If evidence is insufficient, perform another navigation step instead of inventing facts.",
        ],
    }
