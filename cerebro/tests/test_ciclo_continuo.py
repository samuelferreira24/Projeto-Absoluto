from cerebro.ciclo_continuo import CicloContinuo
from cerebro.orquestrador import Missao, Orquestrador


def test_ciclo_escolhe_maior_sinal_sem_fila_fixa(tmp_path):
    o = Orquestrador(tmp_path / "orquestrador.json")
    o.registrar_missao(Missao("M-1", "continuar construção"))
    ciclo = CicloContinuo(o)

    resultado = ciclo.rodar(
        "M-1",
        lambda _: [("pesquisa", 1.0), ("outro", 2.0)],
        lambda _, caminho: {"caminho": caminho},
    )

    assert resultado["executado"] is True
    assert resultado["resultado"] == {"caminho": "outro"}
    assert any(r.etapa == "DECISAO" for r in o.historico)


def test_ciclo_nao_inventa_caminho(tmp_path):
    o = Orquestrador(tmp_path / "orquestrador.json")
    o.registrar_missao(Missao("M-1", "aguardar"))
    ciclo = CicloContinuo(o)

    resultado = ciclo.rodar("M-1", lambda _: [], lambda *_: {"erro": "não deveria executar"})

    assert resultado["executado"] is False
    assert "nenhum caminho" in resultado["motivo"]
