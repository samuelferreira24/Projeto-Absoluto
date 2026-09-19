import tempfile,zipfile
from pathlib import Path
from mini_cerebro.core import MiniCerebro

def test_ingest_and_search():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); (root/"a.md").write_text("# Memória\nmemória independente da interface",encoding="utf-8")
        m=MiniCerebro(root/"db.sqlite3"); r=m.ingest_dir(root)
        assert r["documents"]==2
        assert m.search("memória")
def test_zip():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); f=root/"a.txt"; f.write_text("observação técnica",encoding="utf-8")
        z=root/"a.zip"
        with zipfile.ZipFile(z,"w") as zz: zz.write(f,"a.txt")
        m=MiniCerebro(root/"db.sqlite3"); r=m.ingest_zip(z)
        assert r["documents"]==1
        assert m.search("observação")
