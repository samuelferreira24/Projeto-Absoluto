from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
import json

TIPOS_SEMANTICOS = {"FATO", "HIPOTESE", "INTERPRETACAO", "DECISAO", "PERGUNTA", "OUTRO"}
CONFIANCAS = {"ALTA", "MEDIA", "BAIXA", "DESCONHECIDA"}
ESTADOS = {"NOVO", "EM_ANALISE", "EM_TESTE", "VALIDADO", "REFUTADO", "SUPERADO", "ARQUIVADO"}


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
        self.confidence = self.confidence.upper()
        self.state = self.state.upper()
        if self.confidence not in CONFIANCAS:
            raise ValueError(f"Confiança inválida: {self.confidence}")
        if self.state not in ESTADOS:
            raise ValueError(f"Estado inválido: {self.state}")
        if not self.source_id or not self.relation or not self.target_id:
            raise ValueError("source_id, relation e target_id são obrigatórios")
