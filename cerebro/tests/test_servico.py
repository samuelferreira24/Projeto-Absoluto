import tempfile
import unittest
from pathlib import Path

from cerebro.rede_evolutiva import ArestaRede, NoRede
from cerebro.servico import Cerebro


class TestServico(unittest.TestCase):
    def test_fachada_executa_fluxo_basico(self):
        with tempfile.TemporaryDirectory() as tmp:
            arquivo = Path(tmp) / "fonte.txt"
            arquivo.write_text("Memória temporal do projeto", encoding="utf-8")
            cerebro = Cerebro(Path(tmp) / "data")
            registro = cerebro.ingerir(arquivo)
            self.assertEqual(registro.kind, "DOCUMENTO")
            resultados = cerebro.buscar("memória temporal")
            self.assertEqual(resultados[0].registro.id, registro.id)
            diagnostico = cerebro.diagnostico()
            self.assertEqual(diagnostico["registros"], 1)
            self.assertEqual(diagnostico["fontes"], 1)

    def test_rede_persiste_e_recarrega_sem_ordem_fixa(self):
        with tempfile.TemporaryDirectory() as tmp:
            dados = Path(tmp) / "data"
            cerebro = Cerebro(dados)
            cerebro.adicionar_nos_rede([
                NoRede("pesquisa", "PESQUISA", "Pesquisa", potencial_multiplicador=2),
                NoRede("construcao", "COMPONENTE", "Construção", potencial_multiplicador=3),
            ])
            cerebro.conectar_rede(ArestaRede("pesquisa", "IMPULSIONA", "construcao", peso=2))
            cerebro.salvar_estado()

            recarregado = Cerebro(dados)
            self.assertEqual(set(recarregado.rede.nos), {"pesquisa", "construcao"})
            self.assertEqual(recarregado.relacionados_rede("construcao"), ["pesquisa"])
            self.assertEqual(recarregado.impulso_total("construcao"), 7)
            self.assertEqual(recarregado.validar_rede(), [])


if __name__ == "__main__":
    unittest.main()
