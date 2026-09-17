from cerebro.semantica import UnidadeSemantica, RelacaoSemantica


def test_unidade_semantica_preserva_proveniencia_e_estado():
    unidade = UnidadeSemantica(
        id="SEM-2026-0001",
        source_id="DOC-2026-0001",
        kind="hipotese",
        content="Exemplo de hipótese",
        confidence="baixa",
        provenance={"method": "manual", "location": "p3"},
        derived_from=["DOC-2026-0001"],
        state="em_teste",
    )
    dados = unidade.to_dict()
    assert dados["kind"] == "HIPOTESE"
    assert dados["confidence"] == "BAIXA"
    assert dados["state"] == "EM_TESTE"
    assert dados["provenance"]["location"] == "p3"
    assert dados["derived_from"] == ["DOC-2026-0001"]


def test_unidade_rejeita_classificacao_desconhecida():
    try:
        UnidadeSemantica("SEM-2026-0002", "DOC-2026-0001", "CERTEZA", "x")
    except ValueError as erro:
        assert "Tipo semântico inválido" in str(erro)
    else:
        raise AssertionError("classificação inválida foi aceita")


def test_relacao_preserva_confianca_e_proveniencia():
    relacao = RelacaoSemantica(
        source_id="SEM-2026-0001",
        relation="DERIVA_DE",
        target_id="DOC-2026-0001",
        provenance={"method": "manual"},
        confidence="media",
        state="novo",
    )
    assert relacao.confidence == "MEDIA"
    assert relacao.provenance["method"] == "manual"
    assert relacao.state == "NOVO"
