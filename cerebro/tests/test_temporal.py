from cerebro.semantica import UnidadeSemantica, RelacaoSemantica
from cerebro.temporal import (
    IntervaloTemporal,
    intervalo_da_relacao,
    intervalo_da_unidade,
    unidades_validas_em,
    relacoes_validas_em,
)


def unidade(id_: str, inicio: str, fim: str | None):
    return UnidadeSemantica(
        id=id_,
        source_id="DOC-1",
        kind="FATO",
        content=id_,
        provenance={"origin": "fonte"},
        metadata={
            "temporal": {
                "valid_from": inicio,
                "valid_until": fim,
                "recorded_at": "2026-01-10T00:00:00+00:00",
            }
        },
    )


def test_intervalo_rejeita_ordem_invalida():
    try:
        IntervaloTemporal("2026-02-01T00:00:00+00:00", "2026-01-01T00:00:00+00:00")
    except ValueError:
        return
    raise AssertionError("intervalo inválido não foi rejeitado")


def test_unidades_filtradas_por_tempo_de_validade():
    itens = [
        unidade("U1", "2026-01-01T00:00:00+00:00", "2026-03-01T00:00:00+00:00"),
        unidade("U2", "2026-04-01T00:00:00+00:00", None),
    ]
    validas = unidades_validas_em(itens, "2026-02-01T00:00:00+00:00")
    assert [u.id for u in validas] == ["U1"]


def test_tempo_da_relacao_e_preservado():
    relacao = RelacaoSemantica(
        "U1",
        "CONTRADIZ",
        "U2",
        provenance={
            "temporal": {
                "valid_from": "2026-05-01T00:00:00+00:00",
                "valid_until": None,
                "recorded_at": "2026-05-02T00:00:00+00:00",
            }
        },
    )
    intervalo = intervalo_da_relacao(relacao)
    assert intervalo.valid_from == "2026-05-01T00:00:00+00:00"
    assert intervalo.recorded_at == "2026-05-02T00:00:00+00:00"
    assert len(relacoes_validas_em([relacao], "2026-06-01T00:00:00+00:00")) == 1


def test_tempo_da_unidade_separa_validade_de_registro():
    item = unidade("U1", "2026-01-01T00:00:00+00:00", None)
    intervalo = intervalo_da_unidade(item)
    assert intervalo.valid_from == "2026-01-01T00:00:00+00:00"
    assert intervalo.recorded_at == "2026-01-10T00:00:00+00:00"
