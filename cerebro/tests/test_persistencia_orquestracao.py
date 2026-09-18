from cerebro.grafo_tarefas import EstadoTarefa, NoTarefa
from cerebro.persistencia_orquestracao import carregar_orquestracao, salvar_orquestracao
from cerebro.sinergia import DetectorSinergia, ResultadoCombinacao


def test_persiste_e_recarrega_grafo_e_sinergias(tmp_path):
    grafo = __import__("cerebro.grafo_tarefas", fromlist=["GrafoTarefas"]).GrafoTarefas()
    grafo.adicionar(NoTarefa("a", "A", prioridade=3, estado=EstadoTarefa.CONCLUIDA))
    grafo.adicionar(NoTarefa("b", "B", depende_de=("a",), valor_estimado=5))
    detector = DetectorSinergia()
    detector.registrar(ResultadoCombinacao("ab", ("A", "B"), 12, 2, 3, 0.9, {"fase": "teste"}))

    caminho = tmp_path / "orquestracao.json"
    salvar_orquestracao(caminho, grafo, detector)
    recarregado, sinergia = carregar_orquestracao(caminho)

    assert recarregado.tarefas["a"].estado is EstadoTarefa.CONCLUIDA
    assert recarregado.tarefas["b"].depende_de == ("a",)
    assert len(sinergia.resultados) == 1
    assert sinergia.resultados[0].capacidades == ("A", "B")


def test_snapshot_nao_altera_fontes_em_memoria(tmp_path):
    grafo = __import__("cerebro.grafo_tarefas", fromlist=["GrafoTarefas"]).GrafoTarefas()
    grafo.adicionar(NoTarefa("a", "A"))
    detector = DetectorSinergia()
    caminho = tmp_path / "orquestracao.json"

    salvar_orquestracao(caminho, grafo, detector)

    assert grafo.tarefas["a"].estado is EstadoTarefa.PENDENTE
    assert detector.resultados == []
    assert not caminho.with_suffix(".json.tmp").exists()
