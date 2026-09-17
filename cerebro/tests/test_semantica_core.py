import unittest
import tempfile

from cerebro.auditoria import auditar_semantica
from cerebro.recuperacao import buscar_hibrido, expandir_relacoes
from cerebro.semantica import RelacaoSemantica, UnidadeSemantica
from cerebro.nucleo import novo_registro, RepositorioJSONL


class TestSemanticaCore(unittest.TestCase):
    def test_unidade_derivada_exige_proveniencia_e_origem(self):
        unidade = UnidadeSemantica(
            id="S-1", source_id="DOC-1", kind="INTERPRETACAO", content="Síntese derivada",
            derived_from=["F-1"], provenance={"processo": "manual"}, metadata={"origin": "inferencia"},
        )
        resultado = auditar_semantica([unidade])
        self.assertTrue(resultado.ok)

    def test_relacao_inexistente_e_detectada(self):
        unidade = UnidadeSemantica(id="F-1", source_id="DOC-1", kind="FATO", content="Conteúdo", provenance={"origem": "fonte"})
        relacao = RelacaoSemantica(source_id="F-1", relation="SUSTENTA", target_id="X-99", provenance={"processo": "manual"})
        resultado = auditar_semantica([unidade], [relacao])
        self.assertFalse(resultado.ok)
        self.assertTrue(any("destino inexistente" in erro for erro in resultado.erros))

    def test_busca_hibrida_prioriza_titulo(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = RepositorioJSONL(tmp)
            a = novo_registro(repo, "PESQUISA", "Memória temporal", "conteúdo geral")
            b = novo_registro(repo, "IDEIA", "Outra", "memória temporal no conteúdo")
            repo.salvar(a); repo.salvar(b)
            resultados = buscar_hibrido(repo._iter_registros(), "memória temporal")
            self.assertEqual(resultados[0].registro.id, a.id)

    def test_expansao_por_relacoes(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = RepositorioJSONL(tmp)
            a = novo_registro(repo, "IDEIA", "A")
            b = novo_registro(repo, "IDEIA", "B")
            a.add_relation("deriva_de", b.id)
            repo.salvar(a); repo.salvar(b)
            encontrados = expandir_relacoes(list(repo._iter_registros()), [a.id], profundidade=1)
            self.assertEqual({r.id for r in encontrados}, {a.id, b.id})


if __name__ == "__main__":
    unittest.main()
