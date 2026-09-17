from cerebro.reconstrucao_historica import classificar_texto


def test_identifica_relatorio_pos_construcao():
    texto = "Relatório de análise da construção do sistema. Foram encontrados erros e limitações no aplicativo."
    r = classificar_texto(texto, "relatorio.txt")
    assert r.papel_provavel == "relatorio_pos_construcao"
    assert r.confianca == "alta"


def test_identifica_construcao_com_claude():
    texto = "A construção do aplicativo foi feita com Claude e depois o sistema foi interrompido."
    r = classificar_texto(texto, "historico.txt")
    assert r.papel_provavel == "evidencia_construcao_com_claude"


def test_nao_trata_material_antigo_como_arquitetura_atual():
    texto = "O app antigo servirá apenas como material de estudo; não devemos reutilizar tudo sem análise."
    r = classificar_texto(texto, "estudo.txt")
    assert r.papel_provavel == "material_de_estudo_do_prototipo"
    assert r.reutilizacao == "somente_apos_contextualizacao"
