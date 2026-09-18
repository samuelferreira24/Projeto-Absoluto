from cerebro.agendador import AgendadorAdaptativo, PerfilExecutor
from cerebro.grafo_tarefas import EstadoTarefa, GrafoTarefas, NoTarefa


def test_combustivel_bloqueia_tarefa_excedente():
    g = GrafoTarefas()
    g.adicionar(NoTarefa("a", "A", valor_estimado=10, combustivel_estimado=8))
    s = AgendadorAdaptativo(g)
    s.definir_combustivel(5)
    plano = s.planejar()
    assert plano.tarefas == ()
    assert "a: combustível" in plano.restricoes_bloqueantes


def test_executor_e_modelo_sao_selecionados_dinamicamente():
    g = GrafoTarefas()
    g.adicionar(NoTarefa("a", "A", capacidades=("pesquisa",), valor_estimado=10))
    s = AgendadorAdaptativo(g)
    s.registrar_executor(PerfilExecutor("lento", capacidades=("pesquisa",), fator_tempo=2.0, custo_multiplicador=1.0))
    s.registrar_executor(PerfilExecutor("rapido", capacidades=("pesquisa",), fator_tempo=0.5, custo_multiplicador=1.0))
    executor = s.selecionar_executor(g.tarefas["a"])
    assert executor is not None
    assert executor.id == "rapido"


def test_paralelo_ou_sequencial_e_decidido_pelo_contexto():
    g = GrafoTarefas()
    g.adicionar_varias([
        NoTarefa("a", "A", recursos=("cpu",), valor_estimado=5, tempo_estimado=10),
        NoTarefa("b", "B", recursos=("gpu",), valor_estimado=5, tempo_estimado=4),
    ])
    s = AgendadorAdaptativo(g)
    paralelo = s.planejar({"cpu", "gpu"})
    assert paralelo.modo_execucao == "PARALELO"
    assert paralelo.tempo_estimado == 10

    g2 = GrafoTarefas()
    g2.adicionar(NoTarefa("a", "A", valor_estimado=5, tempo_estimado=2))
    g2.adicionar(NoTarefa("b", "B", depende_de=("a",), valor_estimado=5, tempo_estimado=3))
    s2 = AgendadorAdaptativo(g2)
    s2.executar_inicio(s2.planejar())
    s2.registrar_resultado("a", True)
    sequencial = s2.planejar()
    assert sequencial.modo_execucao == "SEQUENCIAL"


def test_cancelamento_preserva_dependentes_no_historico():
    g = GrafoTarefas()
    g.adicionar(NoTarefa("a", "A"))
    g.adicionar(NoTarefa("b", "B", depende_de=("a",)))
    s = AgendadorAdaptativo(g)
    canceladas = s.cancelar_tarefa("a", motivo="nova evidência", cancelar_dependentes=True)
    assert canceladas == ["a", "b"]
    assert g.tarefas["a"].estado == EstadoTarefa.CANCELADA
    assert g.tarefas["b"].estado == EstadoTarefa.CANCELADA
    assert any(e["evento"] == "CANCELAMENTO" for e in s.historico)


def test_replanejamento_usa_experiencia_e_registra_motivo():
    g = GrafoTarefas()
    g.adicionar_varias([
        NoTarefa("a", "A", valor_estimado=10, tempo_estimado=10),
        NoTarefa("b", "B", valor_estimado=9, tempo_estimado=2),
    ])
    s = AgendadorAdaptativo(g)
    primeiro = s.planejar(limite=1)
    s.executar_inicio(primeiro)
    s.registrar_resultado("a", True, tempo_real=50, observacao="mais lento que previsto")
    segundo = s.replanejar(motivo="nova medição de latência", mudancas={"tempo": "50"})
    assert segundo.tarefas[0].id == "b"
    assert any(e["evento"] == "REPLANEJAMENTO" and e["motivo"] == "nova medição de latência" for e in s.historico)


def test_padroes_bem_sucedidos_sao_reutilizaveis():
    g = GrafoTarefas()
    g.adicionar(NoTarefa("a", "A"))
    s = AgendadorAdaptativo(g)
    s.registrar_resultado("a", True)
    s.grafo.marcar("a", EstadoTarefa.PENDENTE)
    s.registrar_resultado("a", True)
    assert s.padroes_orquestracao_reutilizaveis(2) == [{"tarefa": "a", "ocorrencias": 2}]
