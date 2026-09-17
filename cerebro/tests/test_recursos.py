from cerebro.recursos import EstoqueCapacidade, RecursoCapacidade


def test_recurso_consumo_e_reserva(tmp_path):
    recurso = RecursoCapacidade(
        id="PA-RECURSO-001",
        tipo="CREDITO_API",
        quantidade=100,
        unidade="unidades",
        origem="teste",
    )
    recurso.reservar().consumir(30, valor_gerado=75)
    assert recurso.disponivel == 70
    assert recurso.valor_gerado == 75
    assert recurso.estado == "RESERVADO"


def test_estoque_persiste_e_calcula_disponivel(tmp_path):
    estoque = EstoqueCapacidade(tmp_path / "estoque.jsonl")
    recurso = RecursoCapacidade(
        id="PA-RECURSO-002",
        tipo="GPU_HOURS",
        quantidade=10,
        unidade="hora",
        origem="teste",
    )
    estoque.adicionar(recurso)
    recurso.consumir(2)
    estoque.salvar(recurso)

    recuperado = estoque.obter("PA-RECURSO-002")
    assert recuperado is not None
    assert recuperado.disponivel == 8
    assert estoque.total_disponivel("GPU_HOURS", "hora") == 8


def test_idempotencia_de_recurso():
    a = EstoqueCapacidade.chave_idempotencia("aws", "credito-1", 100, "USD")
    b = EstoqueCapacidade.chave_idempotencia("aws", "credito-1", 100, "USD")
    assert a == b
