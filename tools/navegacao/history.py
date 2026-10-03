from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def history(root: Path, query: str, pathspec: str | None, limit: int):
    cmd = ["git", "-C", str(root), "log", "--all", "--date=iso-strict",
           f"--max-count={limit}", "--format=%H%x09%cI%x09%an%x09%s"]
    if query:
        cmd += ["-S", query]
    if pathspec:
        cmd += ["--", pathspec]
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return []
    return [line.split("\t", 3) for line in out.splitlines() if line]


def main() -> int:
    parser = argparse.ArgumentParser(description="Search Git history for a repository.")
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--path")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("query")
    args = parser.parse_args()
    for sha, date, author, subject in history(args.repo.resolve(), args.query, args.path, args.limit):
        print(f"{sha[:12]}  {date}  {author}  {subject}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
