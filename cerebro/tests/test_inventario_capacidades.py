from cerebro.inventario_capacidades import inventariar, resumo


def test_inventario_distingue_capacidade_implementada_de_exposicao():
    itens = inventariar()
    assert itens
    assert any(i["implementada"] and i["exposta_pelo_cerebro"] for i in itens)
    assert any(i["implementada"] and not i["exposta_pelo_cerebro"] for i in itens)


def test_resumo_tem_numeros_consistentes():
    r = resumo()
    assert r["total_capacidades"] == r["implementadas"]
    assert r["expostas_pelo_cerebro"] <= r["implementadas"]
    assert r["usadas_internamente"] <= r["implementadas"]
    assert r["implementadas_parcialmente"] >= 0
