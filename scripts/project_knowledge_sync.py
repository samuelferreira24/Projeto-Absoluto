#!/usr/bin/env python3
"""Synchronize observable Projeto Absoluto knowledge and map projections."""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from abs_core.project_knowledge import KnowledgeStore, RepositoryScanner
from abs_core.project_knowledge_runtime import RuntimeKnowledgeCollector
from abs_core.runtime import build_runtime


def synchronize(root: Path, output: Path, include_runtime: bool = True) -> dict[str, str]:
    knowledge = RepositoryScanner(root).scan()
    if include_runtime:
        with tempfile.TemporaryDirectory(prefix="pa-knowledge-") as tmp:
            runtime = build_runtime(str(Path(tmp) / "abs.db"))
            knowledge = RuntimeKnowledgeCollector().collect(runtime, knowledge)
    return KnowledgeStore(output).write(knowledge)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-runtime", action="store_true")
    args = parser.parse_args()
    result = synchronize(
        Path(".").resolve(),
        Path("continuidade/07_conhecimento").resolve(),
        include_runtime=not args.no_runtime,
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
