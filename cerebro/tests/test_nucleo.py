import tempfile
import unittest
from pathlib import Path

from cerebro.nucleo import RepositorioJSONL, novo_registro


class TestNucleo(unittest.TestCase):
    def test_registro_e_relacao(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = RepositorioJSONL(tmp)
            r = novo_registro(repo, "IDEIA", "Teste", "conteúdo")
            r.add_relation("deriva_de", "PESQUISA-2026-0001")
            repo.salvar(r)
            encontrados = repo.buscar("conteúdo")
            self.assertEqual(len(encontrados), 1)
            self.assertEqual(encontrados[0].id, r.id)
            self.assertEqual(encontrados[0].relations[0]["type"], "deriva_de")

    def test_id_incremental(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = RepositorioJSONL(tmp)
            repo.salvar(novo_registro(repo, "IDEIA", "Um"))
            repo.salvar(novo_registro(repo, "IDEIA", "Dois"))
            self.assertEqual(repo.proximo_numero("IDEIA"), 3)

    def test_atualizacao_incrementa_versao_e_preserva_historico(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = RepositorioJSONL(tmp)
            r = novo_registro(repo, "IDEIA", "Original", "v1")
            repo.salvar(r)

            r.title = "Atualizada"
            r.content = "v2"
            repo.atualizar(r)

            encontrados = repo.buscar("v2")
            self.assertEqual(len(encontrados), 1)
            self.assertEqual(encontrados[0].version, 2)
            self.assertEqual(encontrados[0].title, "Atualizada")

            historico = (Path(tmp) / "historico" / f"{r.id}.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(historico), 2)
            self.assertIn('"version": 1', historico[0])
            self.assertIn('"version": 2', historico[1])

    def test_salvar_recusa_id_duplicado(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = RepositorioJSONL(tmp)
            r = novo_registro(repo, "IDEIA", "Uma")
            repo.salvar(r)
            with self.assertRaises(ValueError):
                repo.salvar(r)


if __name__ == "__main__":
    unittest.main()
