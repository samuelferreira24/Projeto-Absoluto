from cerebro.eventos import Evento
from cerebro.identidade import identidade_agente, identidade_projeto, identidade_recurso, identidade_sessao, novo_id


def test_identidade_do_projeto_e_estavel():
    assert identidade_projeto().id == "PA-PROJETO-ABSOLUTO"
    assert identidade_projeto().tipo == "PROJETO"


def test_identidades_operacionais_sao_portaveis_e_unicas():
    ids = {
        identidade_agente().id,
        identidade_agente().id,
        identidade_sessao().id,
        identidade_recurso("FERRAMENTA").id,
    }
    assert len(ids) == 4
    assert all(item.startswith("PA-") for item in ids)


def test_novo_id_rejeita_prefixo_invalido():
    try:
        novo_id("a")
    except ValueError:
        pass
    else:
        raise AssertionError("prefixo inválido deveria ser rejeitado")


def test_evento_tem_correlacao_causacao_e_idempotencia():
    evento = Evento(
        origem="PA-AGENTE-1",
        destino="PA-CEREBRO",
        tipo="REGISTRAR_RESULTADO",
        payload={"resultado": "ok"},
        correlation_id="PA-CORRELACAO-1",
        causation_id="PA-EVENTO-ANTERIOR",
    )
    data = evento.to_dict()
    assert data["event_id"].startswith("PA-EVENTO-")
    assert data["correlation_id"] == "PA-CORRELACAO-1"
    assert data["causation_id"] == "PA-EVENTO-ANTERIOR"
    assert data["idempotency_key"] == evento.calcular_idempotencia()


def test_evento_rejeita_status_invalido():
    try:
        Evento(origem="A", tipo="B", status="INVALIDO")
    except ValueError:
        pass
    else:
        raise AssertionError("status inválido deveria ser rejeitado")
