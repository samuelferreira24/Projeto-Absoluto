from pathlib import Path

from cerebro.ciclo_continuo import CicloContinuo
from cerebro.orquestrador import Missao, Orquestrador


def test_continuous_cycle_returns_observation_and_re_evaluates(tmp_path: Path):
    path = tmp_path / "orquestrador.json"
    o = Orquestrador(path)
    missao = Missao("M-1", "avaliar caminho")
    o.registrar_missao(missao)
    ciclo = CicloContinuo(o)

    def candidatos(_):
        return [("A", 0.4), ("B", 0.8)]

    resultado = ciclo.rodar("M-1", candidatos, lambda m, caminho: {
        "state": "completed",
        "caminho_executado": caminho,
    })
    assert resultado["caminho"] == "B"
    assert resultado["observacao"]["estado"] == "completed"

    reavaliado = ciclo.reavaliar(
        "M-1",
        lambda m: [("A", 0.9), ("B", 0.2)],
        observacao=resultado["observacao"],
    )
    assert reavaliado["proximo"] == "A"
    assert reavaliado["opcoes"][0]["pontuacao"] == 0.9


def test_pending_cycle_recovers_same_idempotency_identity(tmp_path: Path):
    path = tmp_path / "orquestrador.json"
    o = Orquestrador(path)
    o.registrar_missao(Missao("M-2", "recuperar ciclo"))

    ciclo_id = "CICLO-RECOVERY"
    key = "M-2:CICLO-RECOVERY"
    o._registrar("M-2", "CICLO", "INICIADO", {"objetivo": "recuperar ciclo"}, ciclo_id, key)
    o.salvar()

    recovered = Orquestrador(path)
    seen = {}

    result = recovered.executar_um_ciclo(
        "M-2",
        lambda m: seen.update(m.contexto["_execucao"]) or {"state": "completed"},
    )

    assert result["ciclo_id"] == ciclo_id
    assert result["idempotency_key"] == key
    assert seen["ciclo_id"] == ciclo_id
    assert seen["idempotency_key"] == key
