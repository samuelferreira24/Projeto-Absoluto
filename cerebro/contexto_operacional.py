"""Contexto operacional compartilhado entre chats, agentes e sessões."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "0.1"


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class AcaoContexto:
    id: str
    acao: str
    motivo: str
    resultado: str
    executor: str | None = None
    ferramenta: str | None = None
    evidencias: list[str] = field(default_factory=list)
    ocorreu_em: str = field(default_factory=agora)


@dataclass(frozen=True)
class DecisaoContexto:
    id: str
    decisao: str
    motivo: str
    alternativas: list[str] = field(default_factory=list)
    evidencia: list[str] = field(default_factory=list)
    tomada_em: str = field(default_factory=agora)


@dataclass
class ContextoOperacional:
    """Contrato portátil que qualquer chat compatível pode consumir."""

    project_id: str = "PROJETO-ABSOLUTO"
    contexto_id: str = "CONTEXTO-OPERACIONAL-0001"
    objetivo: str | None = None
    objetivo_maior: str | None = None
    estado_atual: str = "EM_CONSTRUCAO"
    o_que_esta_sendo_feito: list[str] = field(default_factory=list)
    como_esta_sendo_feito: list[str] = field(default_factory=list)
    por_que_esta_sendo_feito: list[str] = field(default_factory=list)
    plano_atual: list[str] = field(default_factory=list)
    proximo_passo: str | None = None
    bloqueios: list[str] = field(default_factory=list)
    riscos: list[str] = field(default_factory=list)
    restricoes: list[str] = field(default_factory=list)
    decisoes: list[DecisaoContexto] = field(default_factory=list)
    acoes_recentes: list[AcaoContexto] = field(default_factory=list)
    tarefas_pendentes: list[str] = field(default_factory=list)
    evidencias_relevantes: list[str] = field(default_factory=list)
    aprendizados_relevantes: list[str] = field(default_factory=list)
    mudancas_desde_ultima_sessao: list[str] = field(default_factory=list)
    agentes_ativos: list[str] = field(default_factory=list)
    ferramentas_disponiveis: list[str] = field(default_factory=list)
    origem: str = "cerebro"
    atualizado_em: str = field(default_factory=agora)
    metadata: dict[str, Any] = field(default_factory=dict)

    def atualizar(self, **changes: Any) -> "ContextoOperacional":
        permitidos = set(self.__dataclass_fields__) - {"project_id", "contexto_id"}
        desconhecidos = set(changes) - permitidos
        if desconhecidos:
            raise ValueError(f"Campos desconhecidos: {sorted(desconhecidos)}")
        for chave, valor in changes.items():
            setattr(self, chave, valor)
        self.atualizado_em = agora()
        return self

    def to_dict(self) -> dict[str, Any]:
        dados = asdict(self)
        dados["schema_version"] = SCHEMA_VERSION
        return dados

    def salvar(self, path: str | Path) -> None:
        destino = Path(path)
        destino.parent.mkdir(parents=True, exist_ok=True)
        self.atualizado_em = agora()
        destino.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    @classmethod
    def carregar(cls, path: str | Path) -> "ContextoOperacional":
        dados = json.loads(Path(path).read_text(encoding="utf-8"))
        dados.pop("schema_version", None)
        dados["decisoes"] = [DecisaoContexto(**item) for item in dados.get("decisoes", [])]
        dados["acoes_recentes"] = [AcaoContexto(**item) for item in dados.get("acoes_recentes", [])]
        return cls(**dados)


def validar_contexto(dados: dict[str, Any]) -> list[str]:
    erros: list[str] = []
    obrigatorios = {"schema_version", "project_id", "contexto_id", "estado_atual", "objetivo", "o_que_esta_sendo_feito", "como_esta_sendo_feito", "proximo_passo", "atualizado_em"}
    erros.extend(f"campo obrigatório ausente: {campo}" for campo in sorted(obrigatorios - dados.keys()))
    if dados.get("schema_version") != SCHEMA_VERSION:
        erros.append("schema_version incompatível")
    for campo in ("o_que_esta_sendo_feito", "como_esta_sendo_feito", "plano_atual", "bloqueios", "riscos", "restricoes", "tarefas_pendentes"):
        if campo in dados and not isinstance(dados[campo], list):
            erros.append(f"{campo} deve ser lista")
    return erros


def construir_contexto(cerebro: Any, *, objetivo: str | None = None, proximo_passo: str | None = None, contexto_da_sessao: dict[str, Any] | None = None) -> ContextoOperacional:
    estado = cerebro.estado.to_dict()
    tarefas = list(cerebro.grafo_tarefas.tarefas.values())
    pendentes = [t.id for t in tarefas if t.estado.value != "CONCLUIDA"]
    prontas = [t.id for t in tarefas if t.estado.value == "PRONTA"]
    plano = [t.id for t in cerebro.agendador.planejar().tarefas] if hasattr(cerebro, "agendador") else []
    sessao = dict(contexto_da_sessao or {})

    return ContextoOperacional(
        project_id=estado.get("project_id", "PROJETO-ABSOLUTO"),
        objetivo=objetivo or estado.get("next_priority"),
        objetivo_maior=sessao.get("objetivo_maior"),
        estado_atual=estado.get("status", "EM_CONSTRUCAO"),
        o_que_esta_sendo_feito=list(estado.get("in_construction", [])) + prontas,
        como_esta_sendo_feito=list(sessao.get("como_esta_sendo_feito", [])) + plano,
        por_que_esta_sendo_feito=list(sessao.get("por_que_esta_sendo_feito", [])),
        plano_atual=plano,
        proximo_passo=proximo_passo or (plano[0] if plano else estado.get("next_priority")),
        bloqueios=list(estado.get("open_problems", [])),
        riscos=list(estado.get("risks", [])),
        restricoes=list(sessao.get("restricoes", [])),
        tarefas_pendentes=pendentes,
        evidencias_relevantes=list(sessao.get("evidencias_relevantes", [])),
        aprendizados_relevantes=[\n            getattr(r, "title", getattr(r, "titulo", ""))\n            for r in cerebro.registros()\n            if getattr(r, "kind", getattr(r, "tipo", "")) in {"APRENDIZADO", "ENTENDIMENTO", "DESCOBERTA"}\n        ][-20:],
        mudancas_desde_ultima_sessao=list(sessao.get("mudancas_desde_ultima_sessao", [])),
        agentes_ativos=list(sessao.get("agentes_ativos", [])),
        ferramentas_disponiveis=list(sessao.get("ferramentas_disponiveis", [])),
        metadata=sessao,
    )


def salvar_contexto(cerebro: Any, path: str | Path = "cerebro/data/contexto_operacional.json", **kwargs: Any) -> dict[str, Any]:
    contexto = construir_contexto(cerebro, **kwargs)
    contexto.salvar(path)
    return contexto.to_dict()


def gerar_prompt_contexto(contexto: dict[str, Any]) -> str:
    return "\n".join([
        "# CONTEXTO OPERACIONAL — PROJETO ABSOLUTO",
        "Leia este contexto antes de decidir ou executar qualquer ação.",
        "",
        "## O que está sendo feito",
        json.dumps(contexto.get("o_que_esta_sendo_feito", []), ensure_ascii=False, indent=2),
        "",
        "## Como está sendo feito",
        json.dumps(contexto.get("como_esta_sendo_feito", []), ensure_ascii=False, indent=2),
        "",
        "## Por que está sendo feito",
        json.dumps(contexto.get("por_que_esta_sendo_feito", []), ensure_ascii=False, indent=2),
        "",
        "## Objetivo atual",
        str(contexto.get("objetivo")),
        "",
        "## Plano e próximo passo",
        json.dumps({"plano": contexto.get("plano_atual", []), "proximo_passo": contexto.get("proximo_passo")}, ensure_ascii=False, indent=2),
        "",
        "## Decisões, ações e mudanças recentes",
        json.dumps({"decisoes": contexto.get("decisoes", []), "acoes_recentes": contexto.get("acoes_recentes", []), "mudancas": contexto.get("mudancas_desde_ultima_sessao", [])}, ensure_ascii=False, indent=2),
        "",
        "## Bloqueios, riscos e restrições",
        json.dumps({"bloqueios": contexto.get("bloqueios", []), "riscos": contexto.get("riscos", []), "restricoes": contexto.get("restricoes", [])}, ensure_ascii=False, indent=2),
        "",
        "## Regra de continuidade",
        "Antes de agir, confirme o objetivo e o estado. Ao agir, registre o que fez, como fez, por que fez, resultado, evidência e próximo passo. Não apague trabalho anterior silenciosamente. Se encontrar contradição, preserve-a e marque para resolução.",
    ])


def salvar_prompt_contexto(cerebro: Any, path: str | Path = "cerebro/data/CONTEXTO_PARA_QUALQUER_CHAT.md", **kwargs: Any) -> str:
    prompt = gerar_prompt_contexto(salvar_contexto(cerebro, path=Path(path).with_suffix(".json"), **kwargs))
    destino = Path(path)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(prompt + "\n", encoding="utf-8")
    return prompt
