from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.navegacao.index import connect, index_source
from tools.navegacao.related import related
from tools.navegacao.navigator import Navigator
from tools.navegacao.verify import verify_fts, verify_source
from tools.navegacao.search import search, search_symbols


class NavigationV1Tests(unittest.TestCase):
    def test_searches_two_repositories_without_mixing_source_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projeto, sistema = root / "Projeto-Absoluto", root / "Sistema"
            projeto.mkdir(); sistema.mkdir()
            (projeto / "memoria.md").write_text("# Memória temporal\nestado atual e proveniência", encoding="utf-8")
            (sistema / "memoria.md").write_text("# Memória histórica\narquitetura anterior", encoding="utf-8")
            conn = connect(root / "index.sqlite")
            try:
                index_source(conn, "projeto-absoluto", projeto)
                index_source(conn, "sistema", sistema)
                conn.commit()
                self.assertEqual({r[1] for r in search(conn, "memória", None, 20)}, {"projeto-absoluto", "sistema"})
                self.assertEqual(search(conn, "proveniência", "projeto-absoluto", 20)[0][1], "projeto-absoluto")
                self.assertEqual(search(conn, "arquitetura", "sistema", 20)[0][1], "sistema")
            finally:
                conn.close()

    def test_search_filters(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); repo = root / "repo"
            (repo / "docs").mkdir(parents=True); (repo / "src").mkdir()
            (repo / "docs" / "a.md").write_text("governança sistema", encoding="utf-8")
            (repo / "src" / "a.py").write_text("governança sistema", encoding="utf-8")
            conn = connect(root / "index.sqlite")
            try:
                index_source(conn, "repo", repo); conn.commit()
                rows = search(conn, "governança", None, 20, "docs/", "md")
                self.assertEqual([r[2] for r in rows], ["docs/a.md"])
            finally:
                conn.close()

    def test_incremental_index_and_delete(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); repo = root / "repo"; repo.mkdir()
            target = repo / "a.md"; target.write_text("conteúdo antigo", encoding="utf-8")
            conn = connect(root / "index.sqlite")
            try:
                self.assertEqual(index_source(conn, "repo", repo), (1, 0)); conn.commit()
                self.assertEqual(index_source(conn, "repo", repo), (0, 0))
                target.unlink()
                self.assertEqual(index_source(conn, "repo", repo), (0, 1)); conn.commit()
                self.assertEqual(search(conn, "antigo", None, 20), [])
            finally:
                conn.close()

    def test_python_symbols_and_imports_are_indexed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); repo = root / "repo"; repo.mkdir()
            (repo / "app.py").write_text(
                "import json\n\nclass Navigator:\n    def search(self):\n        return json.loads('{}')\n", encoding="utf-8")
            conn = connect(root / "index.sqlite")
            try:
                index_source(conn, "repo", repo); conn.commit()
                self.assertEqual(search_symbols(conn, "Navigator", None, 20)[0][0:2], ("class", "Navigator"))
                self.assertEqual(search_symbols(conn, "search", None, 20)[0][1], "search")
                self.assertIn(("json",), conn.execute("SELECT target FROM relations").fetchall())
            finally:
                conn.close()

    def test_relation_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); repo = root / "repo"; repo.mkdir()
            (repo / "app.py").write_text("import json\nfrom pathlib import Path\n", encoding="utf-8")
            conn = connect(root / "index.sqlite")
            try:
                index_source(conn, "repo", repo); conn.commit()
                rows = related(conn, "json", None, "imports", 20)
                self.assertEqual(rows[0][2], "imports")
            finally:
                conn.close()

    def test_git_metadata_is_available_after_one_repository_scan(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"; repo.mkdir()
            subprocess.run(["git", "-C", str(repo), "init"], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
            (repo / "a.md").write_text("a", encoding="utf-8")
            (repo / "b.md").write_text("b", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-m", "initial"], check=True, capture_output=True)
            conn = connect(Path(tmp) / "index.sqlite")
            try:
                self.assertEqual(index_source(conn, "repo", repo), (2, 0))
                rows = conn.execute("SELECT latest_commit, latest_commit_date FROM documents").fetchall()
                self.assertTrue(all(row[0] and row[1] for row in rows))
            finally:
                conn.close()

    def test_navigator_facade_combines_first_hop_without_inventing_edges(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); repo = root / "repo"; repo.mkdir()
            (repo / "a.py").write_text("import json\nclass Navigator:\n    def search(self): return json.loads('{}')\n", encoding="utf-8")
            conn = connect(root / "index.sqlite")
            try:
                index_source(conn, "repo", repo); conn.commit()
            finally:
                conn.close()
            nav = Navigator(root / "index.sqlite")
            result = nav.navigate("Navigator", limit=10)
            self.assertTrue(result["results"])
            self.assertTrue(result["symbols"])
            self.assertIsInstance(result["relations"], list)

    def test_provenance_verification_detects_source_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); repo = root / "repo"; repo.mkdir()
            target = repo / "a.md"; target.write_text("original", encoding="utf-8")
            conn = connect(root / "index.sqlite")
            try:
                index_source(conn, "repo", repo); conn.commit()
                verify_fts(conn)
                self.assertEqual(verify_source(conn, "repo")[0]["status"], "ok")
                target.write_text("alterado fora do indexador", encoding="utf-8")
                self.assertEqual(verify_source(conn, "repo")[0]["status"], "hash_mismatch")
            finally:
                conn.close()

    def test_symlink_and_oversized_files_are_not_indexed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); repo = root / "repo"; repo.mkdir()
            (repo / "ok.md").write_text("ok", encoding="utf-8")
            large = repo / "large.md"
            large.write_bytes(b"x" * (5 * 1024 * 1024 + 1))
            try:
                (repo / "link.md").symlink_to(repo / "ok.md")
            except (OSError, NotImplementedError):
                pass
            conn = connect(root / "index.sqlite")
            try:
                index_source(conn, "repo", repo); conn.commit()
                paths = {r[0] for r in conn.execute("SELECT path FROM documents").fetchall()}
                self.assertIn("ok.md", paths)
                self.assertNotIn("large.md", paths)
                self.assertNotIn("link.md", paths)
            finally:
                conn.close()


if __name__ == "__main__":
    unittest.main()
