from __future__ import annotations
import hashlib, json, os, sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"
DEFAULT_ROOT = Path(os.getenv("ABS_CONTINUITY_DIR", str(Path.home() / ".abs" / "continuity"))).expanduser()

def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def atomic_write(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)

class OperationalContinuity:
    """Checkpoint verificável e recuperação mínima do estado operacional do ABS."""
    def __init__(self, db_path: str | Path, root: str | Path = DEFAULT_ROOT) -> None:
        self.db_path = Path(db_path).expanduser().resolve()
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.snapshot_path = self.root / "abs.db.snapshot"
        self.manifest_path = self.root / "manifest.json"

    def checkpoint(self) -> dict[str, Any]:
        if not self.db_path.exists():
            raise FileNotFoundError(self.db_path)
        tmp = self.snapshot_path.with_suffix(".tmp")
        src = sqlite3.connect(str(self.db_path)); dst = sqlite3.connect(str(tmp))
        try:
            src.backup(dst); dst.commit()
        finally:
            dst.close(); src.close()
        tmp.replace(self.snapshot_path)
        manifest = {"schema_version": SCHEMA_VERSION, "created_at": now(),
                    "database": str(self.db_path), "snapshot": str(self.snapshot_path),
                    "sha256": sha256(self.snapshot_path)}
        atomic_write(self.manifest_path, manifest)
        return manifest

    def verify(self) -> dict[str, Any]:
        if not self.snapshot_path.exists() or not self.manifest_path.exists():
            return {"valid": False, "reason": "checkpoint_missing"}
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        actual = sha256(self.snapshot_path)
        return {"valid": manifest.get("schema_version") == SCHEMA_VERSION and actual == manifest.get("sha256"),
                "expected_sha256": manifest.get("sha256"), "actual_sha256": actual,
                "created_at": manifest.get("created_at")}
