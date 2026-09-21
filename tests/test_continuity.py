import sqlite3
from pathlib import Path
from abs_core.continuity import OperationalContinuity

def test_checkpoint_and_verify(tmp_path: Path):
    db = tmp_path / "abs.db"
    conn = sqlite3.connect(db); conn.execute("CREATE TABLE t (id INTEGER)"); conn.execute("INSERT INTO t VALUES (1)"); conn.commit(); conn.close()
    c = OperationalContinuity(db, tmp_path / "continuity")
    assert c.checkpoint()["sha256"]
    assert c.verify()["valid"] is True

def test_verify_detects_corruption(tmp_path: Path):
    db = tmp_path / "abs.db"
    conn = sqlite3.connect(db); conn.execute("CREATE TABLE t (id INTEGER)"); conn.commit(); conn.close()
    c = OperationalContinuity(db, tmp_path / "continuity"); c.checkpoint()
    c.snapshot_path.write_bytes(c.snapshot_path.read_bytes() + b"x")
    assert c.verify()["valid"] is False
