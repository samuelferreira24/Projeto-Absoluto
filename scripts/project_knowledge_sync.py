#!/usr/bin/env python3
"""Synchronize observable Projeto Absoluto knowledge and map projections."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from abs_core.project_knowledge import synchronize


def run_tests(root: Path) -> tuple[str, str]:
    """Run the repository suite and convert the result into explicit evidence."""
    proc = subprocess.run(
        ["python", "-m", "pytest", "-q", "tests"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    output = (proc.stdout + "\n" + proc.stderr).strip()
    detail = output.splitlines()[-1] if output else f"pytest exit={proc.returncode}"
    return ("tested" if proc.returncode == 0 else "failure"), detail


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default="continuidade/07_conhecimento")
    parser.add_argument("--no-tests", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    status = None
    detail = ""
    if not args.no_tests:
        status, detail = run_tests(root)

    result = synchronize(root, Path(args.output).resolve(), status, detail)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if status in (None, "tested") else 1


if __name__ == "__main__":
    raise SystemExit(main())
