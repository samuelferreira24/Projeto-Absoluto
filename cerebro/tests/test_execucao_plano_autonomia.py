from cerebro.agendador import AgendadorAdaptativo
from cerebro.controle_execucao import ControleExecucao
from cerebro.execucao_plano import ExecutorPlano
from cerebro.executor import ExecutorCerebro
from cerebro.grafo_tarefas import GrafoTarefas, NoTarefa, EstadoTarefa
from cerebro.politica_execucao import NivelAutonomia, PoliticaExecucao


def test_tarefa_sensivel_respeita_nivel_de_autonomia(tmp_path):
    grafo = GrafoTarefas()
    grafo.adicionar(NoTarefa("sensivel", "alterar sistema", valor_estimado=10, nivel_autonomia=int(NivelAutonomia.ALTERAR_SISTEMAS_AUTORIZADOS), ferramenta="git", reversivel=False))
    scheduler = AgendadorAdaptativo(grafo)
    plano = scheduler.planejar()
    executor = ExecutorPlano(scheduler, ControleExecucao(tmp_path / "controle.json"), ExecutorCerebro(politica=PoliticaExecucao(NivelAutonomia.ACOES_REVERSIVEIS)))

    resultado = executor.executar(plano, {"sensivel": lambda _: {"ok": True}})

    assert resultado[0].executado is False
    assert resultado[0].estado in {"BLOQUEADO", "FALHOU"}
    assert grafo.tarefas["sensivel"].estado == EstadoTarefa.FALHOU


def test_tarefa_que_exige_aprovacao_recebe_token_explicitamente(tmp_path):
    grafo = GrafoTarefas()
    grafo.adicionar(NoTarefa("sensivel", "alterar sistema", valor_estimado=10, nivel_autonomia=int(NivelAutonomia.ALTERAR_SISTEMAS_AUTORIZADOS), ferramenta="git", reversivel=False, exige_aprovacao=True))
    scheduler = AgendadorAdaptativo(grafo)
    plano = scheduler.planejar()
    politica = PoliticaExecucao(NivelAutonomia.ALTERAR_SISTEMAS_AUTORIZADOS)
    acao = __import__("cerebro.politica_execucao", fromlist=["Acao"]).Acao("executar_tarefa:sensivel", NivelAutonomia.ALTERAR_SISTEMAS_AUTORIZADOS, reversivel=False, exige_autorizacao=True)
    token = politica.emitir_aprovacao(acao, ferramenta="git", recurso=None, custo_maximo=20)
    executor = ExecutorPlano(scheduler, ControleExecucao(tmp_path / "controle.json"), ExecutorCerebro(politica=politica))

    resultado = executor.executar(plano, {"sensivel": lambda _: {"ok": True}}, aprovacoes={"sensivel": token})

    assert resultado[0].executado is True
    assert grafo.tarefas["sensivel"].estado == EstadoTarefa.CONCLUIDA
