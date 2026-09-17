import tempfile
import unittest
from pathlib import Path

from cerebro.nucleo import RepositorioJSONL, Registro, novo_registro


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


if __name__ == "__main__":
    unittest.main()
