from cerebro.grafo_tarefas import EstadoTarefa, GrafoTarefas, NoTarefa


def test_dependencias_liberam_tarefa():
    grafo = GrafoTarefas()
    grafo.adicionar(NoTarefa(id="a", objetivo="pesquisar"))
    grafo.adicionar(NoTarefa(id="b", objetivo="sintetizar", depende_de=("a",)))
    assert [t.id for t in grafo.prontas()] == ["a"]
    grafo.marcar("a", EstadoTarefa.CONCLUIDA)
    assert [t.id for t in grafo.prontas()] == ["b"]


def test_recursos_impedem_paralelismo():
    grafo = GrafoTarefas()
    grafo.adicionar(NoTarefa(id="a", objetivo="x", recursos=("gpu",)))
    grafo.adicionar(NoTarefa(id="b", objetivo="y", recursos=("gpu",)))
    lote = grafo.lotes_paralelos({"gpu"})
    assert len(lote) == 1
    assert len(lote[0]) == 1


def test_detecta_dependencia_inexistente_e_ciclo():
    grafo = GrafoTarefas()
    grafo.adicionar(NoTarefa(id="a", objetivo="x", depende_de=("ausente",)))
    assert "a: dependência inexistente: ausente" in grafo.validar()

    ciclo = GrafoTarefas()
    ciclo.adicionar(NoTarefa(id="a", objetivo="x", depende_de=("b",)))
    ciclo.adicionar(NoTarefa(id="b", objetivo="y", depende_de=("a",)))
    assert "grafo contém ciclo de dependências" in ciclo.validar()
