import tempfile
import unittest
from pathlib import Path

from cerebro.agendador import PerfilExecutor
from cerebro.grafo_tarefas import NoTarefa
from cerebro.servico import Cerebro


class TestSchedulerIntegrado(unittest.TestCase):
    def test_servico_expoe_scheduler_recursos_e_executor(self):
        with tempfile.TemporaryDirectory() as tmp:
            cerebro = Cerebro(Path(tmp) / "data")
            cerebro.adicionar_tarefa(
                NoTarefa(
                    "pesquisa",
                    "Pesquisar",
                    capacidades=("pesquisa",),
                    valor_estimado=10,
                    tempo_estimado=2,
                    combustivel_estimado=1,
                )
            )
            cerebro.registrar_executor(
                PerfilExecutor("agente-pesquisa", capacidades=("pesquisa",), modelos=("modelo-x",))
            )
            cerebro.definir_combustivel(5)
            plano = cerebro.planejar_tarefas(limite=1)
            self.assertEqual([t.id for t in plano.tarefas], ["pesquisa"])
            self.assertEqual(cerebro.diagnostico()["executores"], 1)
            self.assertEqual(cerebro.diagnostico()["combustivel_restante"], 5)

    def test_servico_replaneja_e_cancela(self):
        with tempfile.TemporaryDirectory() as tmp:
            cerebro = Cerebro(Path(tmp) / "data")
            cerebro.adicionar_tarefa(NoTarefa("a", "A", valor_estimado=2))
            cerebro.adicionar_tarefa(NoTarefa("b", "B", depende_de=("a",), valor_estimado=3))
            plano = cerebro.planejar_tarefas()
            cerebro.iniciar_plano(plano)
            cerebro.concluir_tarefa("a", True)
            proximo = cerebro.replanejar_tarefas(motivo="resultado recebido")
            self.assertEqual([t.id for t in proximo.tarefas], ["b"])
            canceladas = cerebro.cancelar_tarefa("b", motivo="objetivo mudou")
            self.assertEqual(canceladas, ["b"])


if __name__ == "__main__":
    unittest.main()
