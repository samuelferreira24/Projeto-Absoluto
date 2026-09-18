from cerebro.agendador import AgendadorAdaptativo
from cerebro.controle_execucao import ControleExecucao
from cerebro.executor import ExecutorCerebro
from cerebro.execucao_plano import ExecutorPlano
from cerebro.grafo_tarefas import EstadoTarefa, GrafoTarefas, NoTarefa


def _setup(tmp_path):
    grafo = GrafoTarefas()
    grafo.adicionar(NoTarefa("a", "A", valor_estimado=10, capacidades=("pesquisa",)))
    scheduler = AgendadorAdaptativo(grafo)
    controle = ControleExecucao(tmp_path / "controle.json")
    return grafo, scheduler, controle


def test_executor_plano_executa_e_persiste_resultado(tmp_path):
    grafo, scheduler, controle = _setup(tmp_path)
    plano = scheduler.planejar()
    executor = ExecutorPlano(scheduler, controle, ExecutorCerebro())
    resultado = executor.executar(plano, {"a": lambda tarefa: {"ok": True, "id": tarefa.id}})

    assert resultado[0].executado is True
    assert resultado[0].estado == "CONCLUIDA"
    assert grafo.tarefas["a"].estado == EstadoTarefa.CONCLUIDA
    assert controle.claims["a"].estado == "CONCLUIDA"


def test_executor_plano_bloqueia_sem_handler(tmp_path):
    grafo, scheduler, controle = _setup(tmp_path)
    plano = scheduler.planejar()
    executor = ExecutorPlano(scheduler, controle, ExecutorCerebro())
    resultado = executor.executar(plano, {})

    assert resultado[0].executado is False
    assert resultado[0].estado == "FALHOU"
    assert grafo.tarefas["a"].estado == EstadoTarefa.FALHOU


def test_executor_plano_nao_duplica_claim_ativo(tmp_path):
    grafo, scheduler, controle = _setup(tmp_path)
    plano = scheduler.planejar()
    controle.claim("a")
    executor = ExecutorPlano(scheduler, controle, ExecutorCerebro())
    resultado = executor.executar(plano, {"a": lambda _: {"ok": True}})

    assert resultado[0].estado == "BLOQUEADO"


def test_servico_iniciar_plano_nao_cria_claim_duplicado(tmp_path):
    from cerebro.servico import Cerebro

    cerebro = Cerebro(tmp_path / "data")
    cerebro.adicionar_tarefa(NoTarefa("a", "A", valor_estimado=10))
    plano = cerebro.planejar_tarefas()
    cerebro.iniciar_plano(plano)

    assert "a" not in cerebro.controle_execucao.claims
    resultado = cerebro.executar_plano(plano, {"a": lambda tarefa: {"ok": True}})

    assert resultado[0]["estado"] == "CONCLUIDA"
    assert cerebro.controle_execucao.claims["a"].estado == "CONCLUIDA"
