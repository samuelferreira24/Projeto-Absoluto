from cerebro.sinais import RegistroSinais, Sinal


def test_sinal_nao_depende_de_internet():
    sinal = Sinal.novo(
        "HUMANO", "usuario", {"ordem": "continuar"},
        ocorrido_em="2026-09-18T17:00:00+00:00",
    )
    assert sinal.canal is None
    assert sinal.payload["ordem"] == "continuar"


def test_sinal_pode_representar_codex_e_github():
    codex = Sinal.novo("CODEX", "codex", "execução")
    github = Sinal.novo("GITHUB", "github", {"evento": "commit"})
    registro = RegistroSinais()
    assert registro.registrar(codex)
    assert registro.registrar(github)
    assert {s.tipo for s in registro.listar()} == {"CODEX", "GITHUB"}


def test_sinal_preserva_proveniencia_e_bruto():
    sinal = Sinal.novo(
        "API", "provedor-x", {"resultado": 1},
        proveniencia={"endpoint": "x", "metodo": "GET"},
        bruto={"resposta_original": "..."},
    )
    assert sinal.proveniencia["endpoint"] == "x"
    assert sinal.bruto == {"resposta_original": "..."}


def test_registro_de_sinais_e_idempotente():
    sinal = Sinal.novo("ARQUIVO", "arquivo-x", "conteudo", ocorrido_em="t")
    registro = RegistroSinais()
    assert registro.registrar(sinal)
    assert not registro.registrar(sinal)
    assert len(registro.listar()) == 1
