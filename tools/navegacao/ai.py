from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from .investigate import investigate


def main() -> int:
    parser = argparse.ArgumentParser(description="AI-facing interface for Verifiable Knowledge Navigation.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--source")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--inspect-limit", type=int, default=5)
    parser.add_argument("question", nargs="*")
    args = parser.parse_args()
    question = " ".join(args.question).strip()
    if not question:
        payload = json.load(sys.stdin)
        question = str(payload.get("question", "")).strip()
        args.source = payload.get("source", args.source)
        args.limit = int(payload.get("limit", args.limit))
        args.inspect_limit = int(payload.get("inspect_limit", args.inspect_limit))
    if not question:
        parser.error("question is required (argument or JSON stdin)")
    with sqlite3.connect(args.db) as conn:
        result = investigate(conn, question, source=args.source,
                             limit=args.limit, inspect_limit=args.inspect_limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
