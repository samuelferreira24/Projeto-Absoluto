from pathlib import Path

from cerebro.orquestrador import Missao, Orquestrador


def test_missao_persiste_e_recarrega(tmp_path: Path) -> None:
    path = tmp_path / "orquestrador.json"
    o = Orquestrador(path)
    o.registrar_missao(Missao("M-1", "Construir capacidade"))

    recarregado = Orquestrador(path)
    assert recarregado.missoes["M-1"].objetivo == "Construir capacidade"
    assert recarregado.historico[0].estado == "CRIADA"


def test_ciclo_continua_por_missao_sem_fila_fixa(tmp_path: Path) -> None:
    o = Orquestrador(tmp_path / "orquestrador.json")
    o.registrar_missao(Missao("M-1", "Explorar caminhos"))

    resultado = o.executar_um_ciclo("M-1", lambda missao: {"proximo_caminho": "descoberto", "objetivo": missao.objetivo})

    assert resultado["executado"] is True
    assert resultado["resultado"]["proximo_caminho"] == "descoberto"
    assert o.missoes["M-1"].estado == "ATIVA"
    assert [r.estado for r in o.historico[-2:]] == ["INICIADO", "CONCLUIDO"]


def test_missao_inativa_nao_executa(tmp_path: Path) -> None:
    o = Orquestrador(tmp_path / "orquestrador.json")
    o.registrar_missao(Missao("M-1", "Aguardar", estado="PAUSADA"))

    resultado = o.executar_um_ciclo("M-1", lambda _: {"deve": "não executar"})

    assert resultado["executado"] is False
