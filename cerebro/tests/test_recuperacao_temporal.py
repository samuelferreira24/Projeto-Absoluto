from cerebro.nucleo import Registro
from cerebro.recuperacao import buscar_hibrido, expandir_relacoes


def registro(id_, titulo, *, state="NOVO", valid_from=None, valid_until=None, source="fonte"):
    metadata = {}
    if valid_from is not None or valid_until is not None:
        metadata["temporal"] = {
            "valid_from": valid_from,
            "valid_until": valid_until,
            "recorded_at": "2026-09-17T00:00:00+00:00",
        }
    return Registro(
        id=id_,
        kind="CONHECIMENTO",
        title=titulo,
        created_at="2026-01-01T00:00:00+00:00",
        updated_at="2026-09-17T00:00:00+00:00",
        content=titulo,
        state=state,
        source=source,
        metadata=metadata,
    )


def test_busca_exclui_fato_fora_da_validade():
    atual = registro(
        "k1",
        "API atual",
        valid_from="2026-09-01T00:00:00+00:00",
    )
    futuro = registro(
        "k2",
        "API futura",
        valid_from="2026-10-01T00:00:00+00:00",
    )

    resultado = buscar_hibrido(
        [atual, futuro],
        "API",
        instante="2026-09-17T00:00:00+00:00",
    )

    assert [x.registro.id for x in resultado] == ["k1"]


def test_busca_exclui_superado_por_padrao():
    superado = registro("k1", "API antiga", state="SUPERADO")
    atual = registro("k2", "API atual")

    resultado = buscar_hibrido([superado, atual], "API")

    assert [x.registro.id for x in resultado] == ["k2"]


def test_busca_pode_recuperar_superado_explicitamente():
    superado = registro("k1", "API antiga", state="SUPERADO")

    resultado = buscar_hibrido([superado], "API", incluir_superados=True)

    assert [x.registro.id for x in resultado] == ["k1"]


def test_expansao_de_relacoes_respeita_tempo():
    origem = registro("k1", "origem", valid_from="2026-01-01T00:00:00+00:00")
    alvo = registro("k2", "alvo", valid_from="2026-10-01T00:00:00+00:00")
    origem.relations = [{"type": "HABILITA", "target": "k2"}]

    resultado = expandir_relacoes(
        [origem, alvo],
        ["k1"],
        instante="2026-09-17T00:00:00+00:00",
    )

    assert [x.id for x in resultado] == ["k1"]
