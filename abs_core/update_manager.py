from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path
from urllib.request import urlopen

REPO_DIR = Path(os.getenv("ABS_REPO_DIR", Path.cwd())).resolve()
STATE_PATH = Path(os.getenv("ABS_UPDATE_STATE", str(Path.home() / ".abs" / "update-state.json"))).expanduser()
REMOTE = os.getenv("ABS_UPDATE_REMOTE", "origin")
REF = os.getenv("ABS_UPDATE_REF", "main")
HEALTH_URL = os.getenv("ABS_UPDATE_HEALTH_URL", "http://127.0.0.1:8787/health")
SERVICE = os.getenv("ABS_UPDATE_SERVICE", "abs")
HEALTH_TIMEOUT = int(os.getenv("ABS_UPDATE_HEALTH_TIMEOUT", "30"))
RUNTIME_IGNORED_PATHS = ("abs.db", "abs.db-", "__pycache__/", ".pytest_cache/")


class UpdateError(RuntimeError):
    pass


def _git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=REPO_DIR, text=True, capture_output=True, timeout=60)
    if p.returncode:
        raise UpdateError(p.stderr.strip() or "git command failed")
    return p.stdout.strip()


def _run(*args: str) -> None:
    p = subprocess.run(list(args), cwd=REPO_DIR, text=True, capture_output=True, timeout=60)
    if p.returncode:
        raise UpdateError(p.stderr.strip() or "command failed")


def _load_state() -> dict:
    if not STATE_PATH.exists():
        return {}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def _save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(STATE_PATH)


def _health() -> dict:
    with urlopen(HEALTH_URL, timeout=5) as r:
        return json.loads(r.read().decode("utf-8"))


def _wait_health() -> dict:
    deadline = time.time() + HEALTH_TIMEOUT
    last = None
    while time.time() < deadline:
        try:
            last = _health()
            if last.get("status") == "alive":
                return last
        except Exception:
            pass
        time.sleep(1)
    raise UpdateError(f"ABS health check failed: {last!r}")


def status() -> dict:
    return {
        "current_commit": _git("rev-parse", "HEAD"),
        "configured_ref": REF,
        "remote": REMOTE,
        "last_update": _load_state().get("last_update"),
        "last_known_good": _load_state().get("last_known_good"),
        "rollback_commit": _load_state().get("rollback_commit"),
    }


def check() -> dict:
    before = _git("rev-parse", "HEAD")
    _git("fetch", "--tags", REMOTE, REF)
    target = _git("rev-parse", "FETCH_HEAD")
    return {"current_commit": before, "target_commit": target, "update_available": before != target, "ref": REF}


def _runtime_only_change(path: str) -> bool:
    normalized = path.removeprefix("./")
    return (
        normalized == "abs.db"
        or normalized.startswith("abs.db-")
        or normalized.startswith("__pycache__/")
        or "/__pycache__/" in normalized
        or normalized == ".pytest_cache"
        or normalized.startswith(".pytest_cache/")
        or "/.pytest_cache/" in normalized
    )


def _blocking_worktree_changes() -> list[str]:
    porcelain = _git("status", "--porcelain")
    if not porcelain:
        return []
    blocking: list[str] = []
    for line in porcelain.splitlines():
        path = line[3:].strip()
        # For rename/copy records, inspect the destination path.
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if not _runtime_only_change(path):
            blocking.append(line)
    return blocking


def _require_clean_worktree(action: str) -> None:
    blocking = _blocking_worktree_changes()
    if blocking:
        raise UpdateError(
            f"Refusing {action}: working tree has non-runtime changes: " + "; ".join(blocking)
        )


def _restart() -> None:
    _run("sv", "restart", SERVICE)


def apply() -> dict:
    before = _git("rev-parse", "HEAD")
    _require_clean_worktree("update")
    target_info = check()
    target = target_info["target_commit"]
    if before == target:
        return {"updated": False, **target_info}

    state = _load_state()
    state.update({"rollback_commit": before, "target_commit": target, "started_at": time.time()})
    _save_state(state)

    try:
        _git("reset", "--hard", target)
        _restart()
        health = _wait_health()
    except Exception as exc:
        try:
            _git("reset", "--hard", before)
            _restart()
            _wait_health()
        except Exception as rollback_exc:
            raise UpdateError(f"Update failed; rollback also failed: {rollback_exc}") from exc
        raise UpdateError(f"Update failed; rollback completed: {exc}") from exc

    state.update({"last_known_good": target, "last_update": time.time(), "health": health})
    _save_state(state)
    return {"updated": True, "previous_commit": before, "current_commit": target, "health": health}


def rollback() -> dict:
    state = _load_state()
    target = state.get("rollback_commit") or state.get("last_known_good")
    if not target:
        raise UpdateError("No rollback commit recorded")
    before = _git("rev-parse", "HEAD")
    _require_clean_worktree("rollback")
    _git("reset", "--hard", target)
    _restart()
    health = _wait_health()
    state.update({"last_known_good": target, "rollback_commit": before, "last_rollback": time.time(), "health": health})
    _save_state(state)
    return {"rolled_back": True, "previous_commit": before, "current_commit": target, "health": health}


def main() -> int:
    parser = argparse.ArgumentParser(description="ABS external update manager")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("status", "check", "apply", "rollback"):
        sub.add_parser(name)
    args = parser.parse_args()
    result = globals()[args.command]()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
