import tempfile
import unittest
from pathlib import Path

from cerebro.servico import Cerebro


class TestMemoriaProcesso(unittest.TestCase):
    def test_guarda_entendimento_descoberta_e_progresso(self):
        with tempfile.TemporaryDirectory() as tmp:
            cerebro = Cerebro(Path(tmp) / "data")

            entendimento = cerebro.registrar_entendimento(
                "Planejamento não linear",
                "O planejamento é uma rede de caminhos que se impulsionam mutuamente.",
                contexto={"origem": "construcao"},
            )
            descoberta = cerebro.registrar_descoberta(
                "Lacuna de memória do processo",
                "O Cérebro precisava registrar também os entendimentos e o próprio progresso.",
                relacoes=[{"type": "deriva_de", "target": entendimento.id}],
            )
            progresso = cerebro.registrar_progresso(
                "Memória do processo habilitada",
                "A captura direta passou a aceitar entendimento, descoberta e progresso.",
                relacoes=[{"type": "responde_a", "target": descoberta.id}],
            )

            recarregado = Cerebro(Path(tmp) / "data")
            ids = {r.id for r in recarregado.registros()}
            self.assertEqual(ids, {entendimento.id, descoberta.id, progresso.id})
            self.assertEqual(recarregado.buscar("planejamento não linear")[0].registro.id, entendimento.id)
            self.assertEqual(descoberta.relations[0]["target"], entendimento.id)
            self.assertEqual(progresso.relations[0]["target"], descoberta.id)

    def test_captura_preserva_contexto_proveniencia_e_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            cerebro = Cerebro(Path(tmp) / "data")
            registro = cerebro.registrar_memoria(
                "CONHECIMENTO",
                "Teste de memória",
                "conteúdo",
                fonte="sessao:teste",
                contexto={"fase": "construcao"},
                proveniencia={"agente": "teste", "evidencia": "unitario"},
                metadata={"correlation_id": "CORR-1"},
            )

            carregado = Cerebro(Path(tmp) / "data").registros()[0]
            self.assertEqual(carregado.source, "sessao:teste")
            self.assertEqual(carregado.provenance["agente"], "teste")
            self.assertEqual(carregado.metadata["contexto"]["fase"], "construcao")
            self.assertEqual(carregado.metadata["correlation_id"], "CORR-1")


if __name__ == "__main__":
    unittest.main()
