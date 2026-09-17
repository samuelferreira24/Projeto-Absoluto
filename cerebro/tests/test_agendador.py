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


def test_valor_risco_e_custo_alteram_priorizacao():
    grafo = GrafoTarefas()
    grafo.adicionar_varias([
        NoTarefa("segura", "baixo valor", valor_estimado=5, custo_estimado=1, risco=0.0),
        NoTarefa("arriscada", "alto valor", valor_estimado=20, custo_estimado=1, risco=0.9),
    ])
    plano = AgendadorAdaptativo(grafo).planejar(limite=1)
    assert [t.id for t in plano.tarefas] == ["segura"]


def test_prazo_menor_aumenta_urgencia():
    grafo = GrafoTarefas()
    grafo.adicionar_varias([
        NoTarefa("normal", "normal", valor_estimado=10, custo_estimado=1, prazo=10),
        NoTarefa("urgente", "urgente", valor_estimado=10, custo_estimado=1, prazo=2),
    ])
    plano = AgendadorAdaptativo(grafo).planejar(limite=1)
    assert [t.id for t in plano.tarefas] == ["urgente"]


def test_retry_preserva_falha_e_reabre_tarefa():
    grafo = GrafoTarefas()
    grafo.adicionar(NoTarefa("a", "tarefa", prioridade=2))
    agendador = AgendadorAdaptativo(grafo)
    plano = agendador.planejar()
    agendador.executar_inicio(plano)
    agendador.registrar_resultado("a", False, observacao="falha transitória")
    agendador.retentar_tarefa("a", motivo="recurso recuperado")
    assert grafo.tarefas["a"].estado == EstadoTarefa.PENDENTE
    assert any(e["evento"] == "RESULTADO" and e["sucesso"] is False for e in agendador.historico)
    assert any(e["evento"] == "RETRY" for e in agendador.historico)


def test_historico_preserva_decisao_e_replanejamento():
    grafo = GrafoTarefas()
    grafo.adicionar(NoTarefa("a", "tarefa", valor_estimado=3))
    agendador = AgendadorAdaptativo(grafo)
    agendador.replanejar()
    assert any(e["evento"] == "REPLANEJAMENTO" for e in agendador.historico)


def test_experiencia_altera_planejamento_futuro():
    grafo = GrafoTarefas()
    grafo.adicionar_varias([
        NoTarefa("a", "tarefa a", valor_estimado=10, custo_estimado=1, tempo_estimado=10),
        NoTarefa("b", "tarefa b", valor_estimado=10, custo_estimado=1, tempo_estimado=2),
    ])
    agendador = AgendadorAdaptativo(grafo)
    primeiro = agendador.planejar(limite=1)
    assert primeiro.tarefas[0].id == "a"
    agendador.executar_inicio(primeiro)
    agendador.registrar_resultado("a", True, tempo_real=50)
    grafo.marcar("a", EstadoTarefa.CONCLUIDA)
    segundo = agendador.replanejar(limite=1)
    assert segundo.tarefas[0].id == "b"
    assert agendador.perfil_tarefa("a")["fator_tempo"] > 1.0


def test_experiencia_de_falha_reduz_prioridade_da_tarefa():
    grafo = GrafoTarefas()
    grafo.adicionar_varias([
        NoTarefa("a", "tarefa a", valor_estimado=10, custo_estimado=1),
        NoTarefa("b", "tarefa b", valor_estimado=9, custo_estimado=1),
    ])
    agendador = AgendadorAdaptativo(grafo)
    primeiro = agendador.planejar(limite=1)
    assert primeiro.tarefas[0].id == "a"
    agendador.executar_inicio(primeiro)
    agendador.registrar_resultado("a", False)
    agendador.retentar_tarefa("a", motivo="nova estratégia")
    segundo = agendador.replanejar(limite=1)
    assert segundo.tarefas[0].id == "b"


def test_resultado_preserva_metricas_no_historico():
    grafo = GrafoTarefas()
    grafo.adicionar(NoTarefa("a", "tarefa", prioridade=2))
    agendador = AgendadorAdaptativo(grafo)
    agendador.registrar_resultado("a", True, custo_real=3.5, tempo_real=4.0, qualidade=0.8)
    evento = [e for e in agendador.historico if e["evento"] == "RESULTADO"][-1]
    assert evento["custo_real"] == 3.5
    assert evento["tempo_real"] == 4.0
    assert evento["qualidade"] == 0.8


def test_tempo_do_plano_reflete_paralelismo():
    grafo = GrafoTarefas()
    grafo.adicionar_varias([
        NoTarefa("a", "tarefa a", recursos=("cpu",), prioridade=2, tempo_estimado=10),
        NoTarefa("b", "tarefa b", recursos=("gpu",), prioridade=2, tempo_estimado=4),
    ])
    plano = AgendadorAdaptativo(grafo).planejar({"cpu", "gpu"})
    assert [t.id for t in plano.tarefas] == ["a", "b"]
    assert plano.tempo_estimado == 10.0


def test_grafo_invalido_bloqueia_planejamento():
    grafo = GrafoTarefas()
    grafo.adicionar(NoTarefa("a", "tarefa", depende_de=("ausente",)))
    plano = AgendadorAdaptativo(grafo).planejar()
    assert plano.tarefas == ()
    assert "grafo inválido" in plano.motivo
