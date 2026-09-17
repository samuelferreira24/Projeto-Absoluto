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
