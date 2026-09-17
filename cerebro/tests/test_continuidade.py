from pathlib import Path

import pytest

from cerebro.continuidade import ErroContinuidade, gerar_prompt_retoma, salvar_snapshot, validar_manifesto, validar_ou_erro


ROOT = Path(__file__).resolve().parents[2]


def manifesto_valido() -> dict:
    return {
        "schema_version": "0.1",
        "project": {"id": "PROJETO-ABSOLUTO", "name": "Projeto Absoluto"},
        "construction": {"current_branch": "base-cerebro-v0.1", "current_stage": "fundacao"},
        "continuity": {"required_file": "docs/continuidade.md"},
        "required_validation": ["tests"],
        "rules": ["preservar histórico"],
        "integration_boundary": {"strategy": "adaptadores por contrato"},
    }


def escrever_manifesto(tmp_path: Path, data: dict) -> Path:
    import json
    root = tmp_path / "repo"
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "continuidade.md").write_text("ok", encoding="utf-8")
    path = root / "manifest.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_manifesto_valido(tmp_path: Path):
    path = escrever_manifesto(tmp_path, manifesto_valido())
    assert validar_manifesto(path, path.parent) == []
    validar_ou_erro(path, path.parent)


def test_detecta_referencia_ausente(tmp_path: Path):
    data = manifesto_valido()
    data["continuity"]["required_file"] = "docs/inexistente.md"
    path = escrever_manifesto(tmp_path, data)
    erros = validar_manifesto(path, path.parent)
    assert any("inexistente" in erro for erro in erros)


def test_detecta_campo_essencial_ausente(tmp_path: Path):
    data = manifesto_valido()
    del data["integration_boundary"]
    path = escrever_manifesto(tmp_path, data)
    with pytest.raises(ErroContinuidade):
        validar_ou_erro(path, path.parent)


def test_manifesto_operacional_real_do_projeto():
    path = ROOT / "cerebro" / "especificacao" / "MANIFESTO_EXECUCAO_V0_1.json"
    assert validar_manifesto(path, ROOT) == []


class _Estado:
    def to_dict(self):
        return {"project_id": "PROJETO-ABSOLUTO", "next_priority": "continuar"}


class _Runtime:
    class E:
        def to_dict(self):
            return {"estado": "PARADO", "ciclos": 1}
    estado = E()


class _Tarefa:
    def __init__(self):
        self.id = "T1"
        self.objetivo = "continuar"
        self.depende_de = ()
        self.recursos = ()
        self.capacidades = ()
        self.estado = type("E", (), {"value": "PENDENTE"})()
        self.prioridade = 1.0


class _Rede:
    nos = {}
    arestas = {}


class _Orq:
    missoes = {}


class _Registro:
    def __init__(self, kind, title):
        self.kind = kind
        self.title = title

    def to_dict(self):
        return {"kind": self.kind, "title": self.title}


class _Cerebro:
    estado = _Estado()
    runtime = _Runtime()
    rede = _Rede()
    orquestrador = _Orq()
    grafo_tarefas = type("G", (), {"tarefas": {"T1": _Tarefa()}})()

    def registros(self):
        return [_Registro("APRENDIZADO", "Aprendizado persistente")]


def test_snapshot_preserva_estado_tarefas_e_aprendizado(tmp_path: Path):
    destino = tmp_path / "continuidade.json"
    snapshot = salvar_snapshot(
        _Cerebro(),
        destino,
        objetivo_atual="preservar contexto",
        proximo_passo="implementar recuperação",
        contexto_da_sessao={"origem": "chat"},
    )
    import json
    dados = json.loads(destino.read_text(encoding="utf-8"))
    assert dados["schema_version"] == "0.2"
    assert dados["objetivo_atual"] == "preservar contexto"
    assert dados["proximo_passo"] == "implementar recuperação"
    assert dados["tarefas"][0]["estado"] == "PENDENTE"
    assert dados["aprendizados"][0]["title"] == "Aprendizado persistente"
    assert dados["contexto_da_sessao"]["origem"] == "chat"
    assert snapshot["project_id"] == "PROJETO-ABSOLUTO"


def test_prompt_de_retoma_e_portatil():
    prompt = gerar_prompt_retoma({
        "project_id": "PROJETO-ABSOLUTO",
        "snapshot_at": "2026-09-17T00:00:00+00:00",
        "objetivo_atual": "preservar contexto",
        "proximo_passo": "recuperar",
        "estado_sistema": {"status": "EM_CONSTRUCAO"},
        "tarefas": [],
        "aprendizados": [{"kind": "APRENDIZADO", "title": "teste"}],
        "contexto_da_sessao": {"motivo": "continuidade"},
    })
    assert prompt.startswith("# RETOMADA DO PROJETO ABSOLUTO")
    assert "preservar contexto" in prompt
    assert "Não recomece do zero" in prompt
