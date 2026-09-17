from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
import json

ESTADOS_EXPERIENCIA = {"REGISTRADA", "ANALISADA", "APRENDIDA", "SUPERADA"}
ESTADOS_LICAO = {"IDENTIFICADA", "VALIDANDO", "VALIDADA", "REFUTADA", "SUPERADA"}
ESTADOS_SABEDORIA = {"PROPOSTA", "VALIDANDO", "VALIDADA", "LIMITADA", "SUPERADA"}


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class Experiencia:
    """Registro estruturado de uma experiência que pode gerar aprendizado."""

    id: str
    objetivo: str
    contexto: dict[str, Any] = field(default_factory=dict)
    acao: str = ""
    resultado: str = ""
    evidencias: list[str] = field(default_factory=list)
    decisoes: list[str] = field(default_factory=list)
    erros: list[str] = field(default_factory=list)
    estado: str = "REGISTRADA"
    registrada_em: str = field(default_factory=agora)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.estado = self.estado.upper()
        if self.estado not in ESTADOS_EXPERIENCIA:
            raise ValueError(f"Estado de experiência inválido: {self.estado}")
        if not self.id or not self.objetivo:
            raise ValueError("id e objetivo são obrigatórios")
        if not isinstance(self.contexto, dict) or not isinstance(self.evidencias, list):
            raise ValueError("contexto deve ser objeto e evidencias deve ser lista")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


@dataclass
class LicaoAprendida:
    """Lição transferível derivada de uma ou mais experiências."""

    id: str
    principio: str
    recomendacao: str
    baseada_em: list[str] = field(default_factory=list)
    contexto_aplicabilidade: dict[str, Any] = field(default_factory=dict)
    contraexemplos: list[str] = field(default_factory=list)
    evidencias: list[str] = field(default_factory=list)
    estado: str = "IDENTIFICADA"
    confianca: str = "DESCONHECIDA"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.estado = self.estado.upper()
        self.confianca = self.confianca.upper()
        if self.estado not in ESTADOS_LICAO:
            raise ValueError(f"Estado de lição inválido: {self.estado}")
        if not self.id or not self.principio or not self.recomendacao:
            raise ValueError("id, principio e recomendacao são obrigatórios")
        if not self.baseada_em:
            raise ValueError("uma lição precisa apontar para pelo menos uma experiência")
        if not isinstance(self.contexto_aplicabilidade, dict):
            raise ValueError("contexto_aplicabilidade deve ser objeto")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SabedoriaAplicada:
    """Regra contextual para orientar decisões sem transformar hipótese em verdade."""

    id: str
    principio: str
    quando_aplicar: list[str]
    quando_evitar: list[str] = field(default_factory=list)
    como_adaptar: list[str] = field(default_factory=list)
    baseada_em: list[str] = field(default_factory=list)
    evidencias: list[str] = field(default_factory=list)
    resultados_observados: list[str] = field(default_factory=list)
    consequencias_conhecidas: list[str] = field(default_factory=list)
    limites: list[str] = field(default_factory=list)
    estado: str = "PROPOSTA"
    confianca: str = "DESCONHECIDA"
    revisada_em: str = field(default_factory=agora)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.estado = self.estado.upper()
        self.confianca = self.confianca.upper()
        if self.estado not in ESTADOS_SABEDORIA:
            raise ValueError(f"Estado de sabedoria inválido: {self.estado}")
        if not self.id or not self.principio:
            raise ValueError("id e principio são obrigatórios")
        if not self.quando_aplicar:
            raise ValueError("sabedoria aplicada precisa definir quando_aplicar")
        if not self.baseada_em:
            raise ValueError("sabedoria aplicada precisa apontar para sua base")
        if not self.evidencias and self.estado == "VALIDADA":
            raise ValueError("sabedoria validada precisa de evidências")

    def pode_ser_aplicada(self, contexto: dict[str, Any]) -> bool:
        """Avalia apenas os critérios positivos declarados; não substitui julgamento."""
        if self.estado not in {"VALIDADA", "LIMITADA"}:
            return False
        if not self.contexto_compativel(contexto):
            return False
        return True

    def contexto_compativel(self, contexto: dict[str, Any]) -> bool:
        requisitos = self.metadata.get("requisitos_contextuais", {})
        if not isinstance(requisitos, dict):
            return False
        return all(contexto.get(chave) == valor for chave, valor in requisitos.items())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validar_experiencias(experiencias: list[Experiencia]) -> list[str]:
    erros: list[str] = []
    ids = [e.id for e in experiencias]
    if len(ids) != len(set(ids)):
        erros.append("IDs de experiências duplicados")
    for experiencia in experiencias:
        if experiencia.estado in {"APRENDIDA", "SUPERADA"} and not experiencia.resultado:
            erros.append(f"{experiencia.id}: estado exige resultado registrado")
    return erros


def validar_licoes(licoes: list[LicaoAprendida], experiencias: list[Experiencia]) -> list[str]:
    erros: list[str] = []
    ids = [l.id for l in licoes]
    if len(ids) != len(set(ids)):
        erros.append("IDs de lições duplicados")
    experiencia_ids = {e.id for e in experiencias}
    for licao in licoes:
        if not any(ref in experiencia_ids for ref in licao.baseada_em):
            erros.append(f"{licao.id}: nenhuma experiência de origem presente")
        if licao.estado == "VALIDADA" and not licao.evidencias:
            erros.append(f"{licao.id}: lição validada sem evidências")
    return erros


def validar_sabedoria(sabedorias: list[SabedoriaAplicada], licoes: list[LicaoAprendida]) -> list[str]:
    erros: list[str] = []
    ids = [s.id for s in sabedorias]
    if len(ids) != len(set(ids)):
        erros.append("IDs de sabedorias duplicados")
    base_ids = {l.id for l in licoes}
    for sabedoria in sabedorias:
        if not any(ref in base_ids for ref in sabedoria.baseada_em):
            erros.append(f"{sabedoria.id}: nenhuma lição de origem presente")
        if sabedoria.estado == "VALIDADA" and not sabedoria.evidencias:
            erros.append(f"{sabedoria.id}: sabedoria validada sem evidências")
        if sabedoria.estado == "VALIDADA" and not sabedoria.limites:
            erros.append(f"{sabedoria.id}: sabedoria validada sem limites explícitos")
    return erros
