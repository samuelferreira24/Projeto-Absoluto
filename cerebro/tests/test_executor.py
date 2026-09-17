from cerebro.executor import ExecutorCerebro, PlanoCiclo
from cerebro.politica_execucao import Acao, NivelAutonomia, PoliticaExecucao


def test_executor_bloqueia_acao_fora_da_politica(tmp_path):
    executor = ExecutorCerebro(politica=PoliticaExecucao(NivelAutonomia.PESQUISAR))
    plano = PlanoCiclo(Acao("alterar", NivelAutonomia.ALTERAR_SISTEMAS_AUTORIZADOS))

    resultado = executor.executar(plano, lambda _: {"nao": "deve ocorrer"})

    assert resultado["executado"] is False
    assert resultado["estado"] == "BLOQUEADO"


def test_executor_executa_acao_autorizada(tmp_path):
    executor = ExecutorCerebro(politica=PoliticaExecucao(NivelAutonomia.ACOES_REVERSIVEIS))
    plano = PlanoCiclo(Acao("pesquisar", NivelAutonomia.PESQUISAR))

    resultado = executor.executar(plano, lambda p: {"acao": p.acao.nome})

    assert resultado == {"executado": True, "estado": "CONCLUIDO", "resultado": {"acao": "pesquisar"}}
