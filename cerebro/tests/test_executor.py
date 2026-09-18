from pathlib import Path

from cerebro.executor import ExecutorCerebro, PlanoCiclo
from cerebro.politica_execucao import Acao, NivelAutonomia, PoliticaExecucao
from cerebro.controle_agente import AutorizacaoAgente, ControleAgente, TelemetriaAgente
from cerebro.identidade import identidade_agente


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


def _executor_com_controle(tmp_path: Path) -> ExecutorCerebro:
    controle = ControleAgente(
        AutorizacaoAgente(
            identidade=identidade_agente(),
            ferramentas_permitidas=("pesquisa",),
            recursos_permitidos=("web",),
            nivel_maximo_autonomia=2,
            custo_maximo=5.0,
            cadeia_maxima=2,
        ),
        TelemetriaAgente(tmp_path / "telemetria.jsonl"),
    )
    return ExecutorCerebro(
        politica=PoliticaExecucao(NivelAutonomia.ACOES_REVERSIVEIS),
        controle=controle,
    )


def test_executor_aplica_controle_de_agente(tmp_path: Path):
    executor = _executor_com_controle(tmp_path)
    plano = PlanoCiclo(
        acao=Acao("pesquisa", NivelAutonomia.ACOES_REVERSIVEIS),
        ferramenta="pesquisa",
        recurso="web",
        custo_estimado=1.0,
    )
    resultado = executor.executar(plano, lambda _: {"ok": True})
    assert resultado["executado"] is True
    assert executor.controle.telemetria.resumo()["eventos"] == 2


def test_executor_bloqueia_ferramenta_fora_do_allowlist(tmp_path: Path):
    executor = _executor_com_controle(tmp_path)
    plano = PlanoCiclo(
        acao=Acao("shell", NivelAutonomia.ACOES_REVERSIVEIS),
        ferramenta="shell",
        recurso="web",
    )
    resultado = executor.executar(plano, lambda _: {"nao": "deve executar"})
    assert resultado["executado"] is False
    assert resultado["estado"] == "BLOQUEADO"
