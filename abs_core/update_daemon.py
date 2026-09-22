from __future__ import annotations

import argparse
import fcntl
import os
import subprocess
import time
from pathlib import Path

from . import update_manager as um

INTERVAL = int(os.getenv("ABS_UPDATE_INTERVAL", "60"))
SERVICE = os.getenv("ABS_UPDATE_DAEMON_SERVICE", "abs-updater")
LOCK_PATH = Path(os.getenv("ABS_UPDATE_LOCK", str(Path.home() / ".abs" / "update-daemon.lock"))).expanduser()
LOG_PATH = Path(os.getenv("ABS_UPDATE_LOG", str(Path.home() / ".abs" / "update-daemon.log"))).expanduser()


def _log(message: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S%z')} {message}\n")


def _lock():
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    handle = LOCK_PATH.open("w", encoding="utf-8")
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close()
        return None
    return handle


def run_once() -> dict:
    _log("check started")
    result = um.check()
    _log(
        "check completed: "
        f"current={result['current_commit']} "
        f"target={result['target_commit']} "
        f"update_available={result['update_available']}"
    )
    if not result["update_available"]:
        return {"checked": True, "updated": False, **result}
    _log(f"update candidate detected: {result['current_commit']} -> {result['target_commit']}")
    try:
        applied = um.apply()
        _log(f"update result: {applied}")
        try:
            subprocess.run(["sv", "restart", SERVICE], cwd=um.REPO_DIR, check=True, timeout=30)
        except Exception as exc:
            _log(f"updater self-restart failed: {exc}")
        return {"checked": True, **applied}
    except Exception as exc:
        _log(f"update rejected/failed: {exc}")
        return {
            "checked": True,
            "updated": False,
            "error": str(exc),
            **result,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="ABS independent update daemon")
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    lock = _lock()
    if lock is None:
        _log("another updater instance is already running")
        return 0

    try:
        if args.once:
            print(run_once())
            return 0

        _log(f"daemon started; interval={INTERVAL}s")
        while True:
            try:
                run_once()
            except Exception as exc:
                _log(f"check failed: {exc}")
            time.sleep(INTERVAL)
    finally:
        fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
        lock.close()


if __name__ == "__main__":
    raise SystemExit(main())
