from cerebro.agendador import AgendadorAdaptativo
from cerebro.grafo_tarefas import GrafoTarefas, NoTarefa, EstadoTarefa


def test_agenda_prioriza_e_respeita_recurso_compartilhado():
    grafo = GrafoTarefas()
    grafo.adicionar_varias([
        NoTarefa("a", "alta", recursos=("cpu",), prioridade=10),
        NoTarefa("b", "baixa", recursos=("cpu",), prioridade=1),
        NoTarefa("c", "independente", recursos=("gpu",), prioridade=5),
    ])
    plano = AgendadorAdaptativo(grafo).planejar({"cpu", "gpu"})
    assert [t.id for t in plano.tarefas] == ["a", "c"]


def test_replanejamento_libera_dependencia_concluida():
    grafo = GrafoTarefas()
    grafo.adicionar(NoTarefa("a", "primeira", prioridade=2))
    grafo.adicionar(NoTarefa("b", "segunda", depende_de=("a",), prioridade=9))
    agendador = AgendadorAdaptativo(grafo)
    primeiro = agendador.planejar()
    agendador.executar_inicio(primeiro)
    agendador.registrar_resultado("a", True)
    segundo = agendador.replanejar()
    assert [t.id for t in segundo.tarefas] == ["b"]
    assert grafo.tarefas["a"].estado == EstadoTarefa.CONCLUIDA


def test_orcamento_impede_excesso():
    grafo = GrafoTarefas()
    grafo.adicionar(NoTarefa("a", "tarefa", prioridade=1))
    plano = AgendadorAdaptativo(grafo).planejar(orcamento=0.5)
    assert plano.tarefas == ()
