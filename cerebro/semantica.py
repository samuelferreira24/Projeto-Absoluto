from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
import json

TIPOS_SEMANTICOS = {"FATO", "HIPOTESE", "INTERPRETACAO", "DECISAO", "PERGUNTA", "OUTRO"}
CONFIANCAS = {"ALTA", "MEDIA", "BAIXA", "DESCONHECIDA"}
ESTADOS = {"NOVO", "EM_ANALISE", "EM_TESTE", "VALIDADO", "REFUTADO", "SUPERADO", "ARQUIVADO"}
RELACOES = {
    "DERIVA_DE", "SUSTENTA", "TESTA", "CONTRADIZ", "INFLUENCIA",
    "DEPENDE_DE", "SUBSTITUI", "PARTE_DE", "GERA", "CORRIGE",
    "APRENDE_DE", "RELACIONA_SE_COM",
}


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class UnidadeSemantica:
    id: str
    source_id: str
    kind: str
    content: str
    confidence: str = "DESCONHECIDA"
    provenance: dict[str, Any] = field(default_factory=dict)
    derived_from: list[str] = field(default_factory=list)
    state: str = "NOVO"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.kind = self.kind.upper()
        self.confidence = self.confidence.upper()
        self.state = self.state.upper()
        if self.kind not in TIPOS_SEMANTICOS:
            raise ValueError(f"Tipo semântico inválido: {self.kind}")
        if self.confidence not in CONFIANCAS:
            raise ValueError(f"Confiança inválida: {self.confidence}")
        if self.state not in ESTADOS:
            raise ValueError(f"Estado inválido: {self.state}")
        if not self.id or not self.source_id or not self.content:
            raise ValueError("id, source_id e content são obrigatórios")
        if not isinstance(self.provenance, dict):
            raise ValueError("provenance deve ser um objeto")
        if not isinstance(self.derived_from, list):
            raise ValueError("derived_from deve ser uma lista")

    @property
    def is_derived(self) -> bool:
        return bool(self.derived_from) or self.metadata.get("origin") == "inferencia"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


@dataclass
class RelacaoSemantica:
    source_id: str
    relation: str
    target_id: str
    provenance: dict[str, Any] = field(default_factory=dict)
    confidence: str = "DESCONHECIDA"
    state: str = "NOVO"

    def __post_init__(self) -> None:
        self.relation = self.relation.upper()
        self.confidence = self.confidence.upper()
        self.state = self.state.upper()
        if self.relation not in RELACOES:
            raise ValueError(f"Relação semântica inválida: {self.relation}")
        if self.confidence not in CONFIANCAS:
            raise ValueError(f"Confiança inválida: {self.confidence}")
        if self.state not in ESTADOS:
            raise ValueError(f"Estado inválido: {self.state}")
        if not self.source_id or not self.target_id:
            raise ValueError("source_id e target_id são obrigatórios")
        if not isinstance(self.provenance, dict):
            raise ValueError("provenance deve ser um objeto")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validar_unidade(unidade: UnidadeSemantica) -> list[str]:
    erros: list[str] = []
    if not unidade.provenance:
        erros.append("provenance ausente")
    if unidade.is_derived and not unidade.derived_from:
        erros.append("inferência sem derived_from")
    if unidade.is_derived and unidade.metadata.get("origin") == "fonte":
        erros.append("origin incompatível: unidade inferencial marcada como fonte")
    return erros


def validar_relacao(relacao: RelacaoSemantica) -> list[str]:
    erros: list[str] = []
    if not relacao.provenance:
        erros.append("provenance ausente")
    if relacao.source_id == relacao.target_id:
        erros.append("relação autorreferente não permitida por padrão")
    return erros


def validar_unidades(unidades: list[UnidadeSemantica], relacoes: list[RelacaoSemantica] | None = None) -> list[str]:
    """Valida o contrato semântico sem confundir referência externa com corrupção.

    `derived_from` pode apontar para uma fonte, documento ou registro que ainda não
    esteja no lote auditado. Já uma relação semântica explícita exige endpoints
    presentes no conjunto auditado, porque sua integridade estrutural depende deles.
    """
    erros: list[str] = []
    ids = [u.id for u in unidades]
    if len(ids) != len(set(ids)):
        erros.append("IDs de unidades duplicados")
    known = set(ids)
    for unidade in unidades:
        erros.extend(f"{unidade.id}: {erro}" for erro in validar_unidade(unidade))
    for relacao in relacoes or []:
        erros.extend(f"{relacao.source_id}->{relacao.target_id}: {erro}" for erro in validar_relacao(relacao))
        if relacao.source_id not in known:
            erros.append(f"relação com origem inexistente: {relacao.source_id}")
        if relacao.target_id not in known:
            erros.append(f"relação com destino inexistente: {relacao.target_id}")
    return erros
