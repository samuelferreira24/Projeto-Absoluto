from cerebro.executor import ExecutorCerebro, PlanoCiclo
from cerebro.politica_execucao import Acao, NivelAutonomia, PoliticaExecucao


def test_executor_bloqueia_acao_fora_da_politica():
    executor = ExecutorCerebro(politica=PoliticaExecucao(NivelAutonomia.PESQUISAR))
    plano = PlanoCiclo(Acao("alterar", NivelAutonomia.ALTERAR_SISTEMAS_AUTORIZADOS))

    resultado = executor.executar(plano, lambda _: {"nao": "deve ocorrer"})

    assert resultado["executado"] is False
    assert resultado["estado"] == "BLOQUEADO"


def test_executor_executa_acao_autorizada():
    executor = ExecutorCerebro(politica=PoliticaExecucao(NivelAutonomia.ACOES_REVERSIVEIS))
    plano = PlanoCiclo(Acao("pesquisar", NivelAutonomia.PESQUISAR))

    resultado = executor.executar(plano, lambda p: {"acao": p.acao.nome})

    assert resultado == {"executado": True, "estado": "CONCLUIDO", "resultado": {"acao": "pesquisar"}}


def test_executor_pode_receber_fonte_contextual_sem_importar_servico():
    class Fonte:
        def candidatos_rede(self, contexto=None):
            return [("CAMINHO-A", 1.0)]

    executor = ExecutorCerebro(cerebro=Fonte())

    assert executor.selecionar({"urgencia": 1.0}) == [("CAMINHO-A", 1.0)]
