from cerebro.politica_execucao import Acao, NivelAutonomia, PoliticaExecucao


def test_politica_permite_acoes_ate_o_limite():
    politica = PoliticaExecucao(NivelAutonomia.ACOES_REVERSIVEIS)
    assert politica.autorizada(Acao("pesquisar", NivelAutonomia.PESQUISAR))
    assert politica.autorizada(Acao("registrar_resultado", NivelAutonomia.ACOES_REVERSIVEIS))


def test_politica_bloqueia_alem_do_limite():
    politica = PoliticaExecucao(NivelAutonomia.PESQUISAR)
    assert not politica.autorizada(Acao("criar_branch", NivelAutonomia.DELEGAR))


def test_autorizacao_explicita_nao_e_concedida_pela_politica():
    politica = PoliticaExecucao(NivelAutonomia.ALTERAR_SISTEMAS_AUTORIZADOS)
    assert not politica.autorizada(Acao("acao_sensivel", NivelAutonomia.ALTERAR_SISTEMAS_AUTORIZADOS, exige_autorizacao=True))


def test_aprovacao_vinculada_e_consumida():
    acao = Acao("acao_sensivel", NivelAutonomia.ALTERAR_SISTEMAS_AUTORIZADOS, exige_autorizacao=True)
    politica = PoliticaExecucao(NivelAutonomia.ALTERAR_SISTEMAS_AUTORIZADOS)
    token = politica.emitir_aprovacao(acao, ferramenta="git", recurso="repo-x", custo_maximo=2.0)
    assert politica.autorizada(acao, ferramenta="git", recurso="repo-x", custo_estimado=1.0, aprovacao_id=token)
    politica.consumir_aprovacao(token)
    assert not politica.autorizada(acao, ferramenta="git", recurso="repo-x", custo_estimado=1.0, aprovacao_id=token)

def test_aprovacao_nao_pode_ser_reutilizada_para_outra_ferramenta():
    acao = Acao("acao_sensivel", NivelAutonomia.ALTERAR_SISTEMAS_AUTORIZADOS, exige_autorizacao=True)
    politica = PoliticaExecucao(NivelAutonomia.ALTERAR_SISTEMAS_AUTORIZADOS)
    token = politica.emitir_aprovacao(acao, ferramenta="git", recurso="repo-x")
    assert not politica.autorizada(acao, ferramenta="shell", recurso="repo-x", aprovacao_id=token)


def test_escopo_de_execucao_compara_caminho_resolvido(tmp_path):
    import sys
    from cerebro.politica_execucao import EscopoExecucao

    escopo = EscopoExecucao(executaveis_permitidos=(sys.executable,))
    permitido, motivo = escopo.validar_comando((sys.executable, "-V"))
    assert permitido is True
    assert motivo == "OK"

    outro = tmp_path / "mesmo_nome"
    outro.write_text("", encoding="utf-8")
    permitido, _ = escopo.validar_comando((str(outro),))
    assert permitido is False
