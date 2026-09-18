from __future__ import annotations

import json
from pathlib import Path

from cerebro.conhecimento import BaseConhecimento
from cerebro.servico import Cerebro


def test_conhecimento_preserva_proveniencia_temporal_e_idempotencia(tmp_path: Path) -> None:
    base = BaseConhecimento(tmp_path / "conhecimento")
    item = base.criar(
        "FATO",
        "API atual",
        "A API é suportada.",
        source_ids=("DOC-1",),
        evidence_ids=("EVID-1",),
        provenance={"origem": "documento", "arquivo": "fonte.md"},
        confidence="ALTA",
        temporal={"valid_from": "2026-09-01T00:00:00+00:00", "recorded_at": "2026-09-18T00:00:00+00:00"},
    )
    again = base.criar(
        "FATO",
        "API atual",
        "A API é suportada.",
        source_ids=("DOC-1",),
        evidence_ids=("EVID-1",),
        provenance={"origem": "documento", "arquivo": "fonte.md"},
        confidence="ALTA",
        temporal={"valid_from": "2026-09-01T00:00:00+00:00", "recorded_at": "2026-09-18T00:00:00+00:00"},
    )

    assert again.id == item.id
    assert len(base.listar()) == 1
    assert base.buscar("API suportada", instante="2026-09-18T00:00:00+00:00")[0].conhecimento.id == item.id
    assert (tmp_path / "conhecimento" / "historico_conhecimento" / f"{item.id}.jsonl").exists()


def test_conhecimento_atualiza_sem_apagar_historico(tmp_path: Path) -> None:
    base = BaseConhecimento(tmp_path / "conhecimento")
    item = base.criar(
        "HIPOTESE", "Teste", "Versão 1",
        provenance={"origem": "experimento"},
    )
    atualizado = base.atualizar(item.id, content="Versão 2", confidence="MEDIA")

    assert atualizado.version == 2
    assert base.obter(item.id).content == "Versão 2"
    linhas = (tmp_path / "conhecimento" / "conhecimento.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(linhas) == 2
    historico = (tmp_path / "conhecimento" / "historico_conhecimento" / f"{item.id}.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(historico) == 2


def test_conhecimento_conflitante_e_relacionado_sem_apagar_fonte(tmp_path: Path) -> None:
    base = BaseConhecimento(tmp_path / "conhecimento")
    a = base.criar("FATO", "Regra", "A regra vale.", source_ids=("DOC-A",), provenance={"origem": "A"})
    b = base.criar("FATO", "Regra alternativa", "A regra não vale.", source_ids=("DOC-B",), provenance={"origem": "B"})
    base.relacionar(b.id, "CONTRADIZ", a.id, provenance={"motivo": "fontes conflitantes"})

    atual = base.obter(b.id)
    assert any(r["type"] == "CONTRADIZ" and r["target"] == a.id for r in atual.relations)
    assert base.obter(a.id).state == "NOVO"


def test_servico_expoe_conhecimento_e_importa_aprendizados(tmp_path: Path) -> None:
    cerebro = Cerebro(tmp_path / "data")
    item = cerebro.registrar_conhecimento(
        "DESCOBERTA",
        "Integração",
        "Conhecimento passa a participar do Cérebro.",
        fontes=("DOC-1",),
        proveniencia={"origem": "teste"},
        confianca="MEDIA",
    )
    resultado = cerebro.buscar_conhecimento("Cérebro Integração")
    assert resultado[0].conhecimento.id == item.id

    memoria = tmp_path / "memoria"
    memoria.mkdir()
    (memoria / "aprendizados.jsonl").write_text(
        json.dumps({
            "tipo": "APRENDIZADO",
            "titulo": "Aprendizado integrado",
            "conteudo": "O aprendizado pode ser recuperado como conhecimento.",
            "origem": "teste",
            "evidencias": ["DOC-1"],
            "confianca": "alta",
        }, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    importados = cerebro.importar_aprendizados_para_conhecimento(memoria)
    assert len(importados) == 1
    assert cerebro.buscar_conhecimento("aprendizado recuperado")
    assert cerebro.diagnostico()["conhecimento"]["itens"] == 2
