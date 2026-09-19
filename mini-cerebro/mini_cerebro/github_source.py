from __future__ import annotations
import subprocess,tempfile
from pathlib import Path
from .core import MiniCerebro

def acquire_repository(repo_url: str, destination: str | None = None) -> Path:
    """Acquire a Git repository without modifying the source repository."""
    target = Path(destination) if destination else Path(tempfile.mkdtemp(prefix="mini-cerebro-"))
    target = target.resolve()
    if target.exists() and any(target.iterdir()):
        raise ValueError(f"destination is not empty: {target}")
    subprocess.run(["git","clone","--no-hardlinks",repo_url,str(target)],
                   check=True, capture_output=True, text=True)
    return target

def ingest_github_repo(db_path: str, repo_url: str, destination: str | None = None):
    """Acquire repository, then let the Mini-Cérebro ingest it read-only."""
    root=acquire_repository(repo_url,destination)
    brain=MiniCerebro(db_path)
    result=brain.ingest_dir(root)
    result["acquired_path"]=str(root)
    return result

def ingest_existing_zip(db_path: str, zip_path: str):
    brain=MiniCerebro(db_path)
    return brain.ingest_zip(Path(zip_path))
