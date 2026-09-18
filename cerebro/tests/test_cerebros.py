from cerebro.cerebros import CerebroRemoto, RegistroCerebros


def test_registra_e_recupera_nucleos(tmp_path):
    registro = RegistroCerebros(tmp_path / "cerebros.json")
    registro.registrar(
        CerebroRemoto(
            id="c1",
            nome="Cérebro local",
            ambiente="computador",
            capacidades=("orquestracao", "memoria"),
        )
    )
    registro.registrar(
        CerebroRemoto(
            id="c2",
            nome="Cérebro remoto",
            ambiente="servidor",
            capacidades=("pesquisa", "execucao"),
        )
    )

    assert [c.id for c in registro.listar()] == ["c1", "c2"]
    assert [c.id for c in registro.por_capacidade("pesquisa")] == ["c2"]
    assert [c.id for c in registro.por_ambiente("computador")] == ["c1"]


def test_nao_impoe_um_unico_cerebro(tmp_path):
    registro = RegistroCerebros(tmp_path / "cerebros.json")
    for i in range(3):
        registro.registrar(
            CerebroRemoto(
                id=f"c{i}",
                nome=f"Cérebro {i}",
                ambiente="ambiente",
            )
        )

    assert len(registro.listar()) == 3
