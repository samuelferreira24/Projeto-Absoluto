from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.navegacao.index import connect, index_source
from tools.navegacao.search import search, search_symbols


class NavigationV1Tests(unittest.TestCase):
    def test_searches_two_repositories_without_mixing_source_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projeto = root / "Projeto-Absoluto"
            sistema = root / "Sistema"
            projeto.mkdir()
            sistema.mkdir()
            (projeto / "memoria.md").write_text("# Memória temporal\nestado atual e proveniência", encoding="utf-8")
            (sistema / "memoria.md").write_text("# Memória histórica\narquitetura anterior", encoding="utf-8")

            conn = connect(root / "index.sqlite")
            try:
                index_source(conn, "projeto-absoluto", projeto)
                index_source(conn, "sistema", sistema)
                conn.commit()
                results = search(conn, "memória", None, 20)
                self.assertEqual({row[1] for row in results}, {"projeto-absoluto", "sistema"})
                self.assertEqual(search(conn, "proveniência", "projeto-absoluto", 20)[0][1], "projeto-absoluto")
                self.assertEqual(search(conn, "arquitetura", "sistema", 20)[0][1], "sistema")
            finally:
                conn.close()

    def test_incremental_index_removes_deleted_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            repo.mkdir()
            target = repo / "a.md"
            target.write_text("conteúdo antigo", encoding="utf-8")
            conn = connect(root / "index.sqlite")
            try:
                self.assertEqual(index_source(conn, "repo", repo), (1, 0))
                conn.commit()
                target.unlink()
                self.assertEqual(index_source(conn, "repo", repo), (0, 1))
                conn.commit()
                self.assertEqual(search(conn, "antigo", None, 20), [])
            finally:
                conn.close()

    def test_python_symbols_and_imports_are_indexed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            repo.mkdir()
            (repo / "app.py").write_text(
                "import json\n\nclass Navigator:\n    def search(self):\n        return json.loads('{}')\n",
                encoding="utf-8",
            )
            conn = connect(root / "index.sqlite")
            try:
                index_source(conn, "repo", repo)
                conn.commit()
                rows = search_symbols(conn, "Navigator", None, 20)
                self.assertEqual(rows[0][0:2], ("class", "Navigator"))
                self.assertEqual(search_symbols(conn, "search", None, 20)[0][1], "search")
                rel = conn.execute("SELECT target FROM relations").fetchall()
                self.assertIn(("json",), rel)
            finally:
                conn.close()


if __name__ == "__main__":
    unittest.main()
