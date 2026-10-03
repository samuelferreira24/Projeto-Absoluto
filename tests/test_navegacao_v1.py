from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.navegacao.index import connect, index_source
from tools.navegacao.search import search


class NavigationV1Tests(unittest.TestCase):
    def test_searches_two_repositories_without_mixing_source_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projeto = root / "Projeto-Absoluto"
            sistema = root / "Sistema"
            projeto.mkdir()
            sistema.mkdir()

            (projeto / "memoria.md").write_text(
                "# Memória temporal\nestado atual e proveniência", encoding="utf-8"
            )
            (sistema / "memoria.md").write_text(
                "# Memória histórica\narquitetura anterior", encoding="utf-8"
            )

            db = root / "index.sqlite"
            conn = connect(db)
            try:
                index_source(conn, "projeto-absoluto", projeto)
                index_source(conn, "sistema", sistema)
                conn.commit()

                results = search(conn, "memória", None, 20)
                sources = {row[1] for row in results}
                self.assertEqual(sources, {"projeto-absoluto", "sistema"})

                current = search(conn, "proveniência", "projeto-absoluto", 20)
                self.assertEqual(len(current), 1)
                self.assertEqual(current[0][1], "projeto-absoluto")

                historical = search(conn, "arquitetura", "sistema", 20)
                self.assertEqual(len(historical), 1)
                self.assertEqual(historical[0][1], "sistema")
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
                changed, removed = index_source(conn, "repo", repo)
                self.assertEqual((changed, removed), (1, 0))
                conn.commit()

                target.unlink()
                changed, removed = index_source(conn, "repo", repo)
                self.assertEqual((changed, removed), (0, 1))
                conn.commit()

                self.assertEqual(search(conn, "antigo", None, 20), [])
            finally:
                conn.close()


if __name__ == "__main__":
    unittest.main()
