from __future__ import annotations

import json
from pathlib import Path

from cerebro.servico import Cerebro


def test_cerebro_consolida_aprendizado_acumulado_e_novo(tmp_path: Path) -> None:
    memoria = tmp_path / "memoria"
    memoria.mkdir()
    (memoria / "aprendizados_fundamentais_v0_1.json").write_text(
        json.dumps({
            "versao": "0.1",
            "aprendizados": [
                {"tipo": "ENTENDIMENTO", "titulo": "Antigo", "conteudo": "Aprendizado acumulado"}
            ],
        }, ensure_ascii=False),
        encoding="utf-8",
    )
    (memoria / "aprendizados.jsonl").write_text(
        json.dumps({"tipo": "APRENDIZADO", "titulo": "Novo", "conteudo": "Aprendizado atual"}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    cerebro = Cerebro(tmp_path / "data")
    resultado = cerebro.consolidar_aprendizados(memoria)

    assert resultado["quantidade"] == 2
    assert {item["titulo"] for item in resultado["aprendizados"]} == {"Antigo", "Novo"}
    assert (memoria / "aprendizados.jsonl").read_text(encoding="utf-8").count("Novo") == 1
    assert (memoria / "aprendizados_fundamentais_v0_1.json").read_text(encoding="utf-8").count("Antigo") == 1
    assert cerebro.diagnostico()["aprendizados_consolidados"] == 2
