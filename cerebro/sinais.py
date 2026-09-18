from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any


TIPOS_SINAL = {
    "HUMANO",
    "CHAT",
    "INTERFACE",
    "ARQUIVO",
    "WEB",
    "API",
    "APP",
    "CODIGO",
    "GITHUB",
    "CODEX",
    "TERMINAL",
    "AGENTE",
    "OUTRO",
}


@dataclass(frozen=True)
class Sinal:
    """Envelope universal de entrada/saída do Cérebro.

    Um sinal não é sinônimo de internet. Internet pode ser o meio de transporte
    de vários sinais, mas o Cérebro deve aceitar também sinais locais, humanos,
    de interfaces, arquivos, processos, outros agentes e fontes futuras.
    """

    id: str
    tipo: str
    origem: str
    payload: Any
    ocorrido_em: str
    canal: str | None = None
    destino: str | None = None
    contexto: dict[str, Any] = field(default_factory=dict)
    proveniencia: dict[str, Any] = field(default_factory=dict)
    confianca: str = "DESCONHECIDA"
    bruto: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id or not self.tipo or not self.origem:
            raise ValueError("id, tipo e origem são obrigatórios")
        if self.tipo not in TIPOS_SINAL:
            raise ValueError(f"tipo de sinal inválido: {self.tipo}")
        if not self.ocorrido_em:
            raise ValueError("ocorrido_em é obrigatório")

    @staticmethod
    def novo(
        tipo: str,
        origem: str,
        payload: Any,
        *,
        ocorrido_em: str | None = None,
        canal: str | None = None,
        destino: str | None = None,
        contexto: dict[str, Any] | None = None,
        proveniencia: dict[str, Any] | None = None,
        confianca: str = "DESCONHECIDA",
        bruto: Any = None,
        metadata: dict[str, Any] | None = None,
    ) -> "Sinal":
        ocorrido = ocorrido_em or datetime.now(timezone.utc).isoformat()
        identidade = repr((tipo, origem, ocorrido, payload, canal, destino))
        sinal_id = sha256(identidade.encode("utf-8")).hexdigest()
        return Sinal(
            id=sinal_id,
            tipo=tipo,
            origem=origem,
            payload=payload,
            ocorrido_em=ocorrido,
            canal=canal,
            destino=destino,
            contexto=contexto or {},
            proveniencia=proveniencia or {},
            confianca=confianca,
            bruto=payload if bruto is None else bruto,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class RegistroSinais:
    """Registro simples e substituível para sinais recebidos pelo Cérebro."""

    def __init__(self) -> None:
        self._sinais: dict[str, Sinal] = {}

    def registrar(self, sinal: Sinal) -> bool:
        if sinal.id in self._sinais:
            return False
        self._sinais[sinal.id] = sinal
        return True

    def registrar_varios(self, sinais: list[Sinal]) -> int:
        return sum(self.registrar(sinal) for sinal in sinais)

    def listar(self, *, tipo: str | None = None, origem: str | None = None) -> list[Sinal]:
        sinais = list(self._sinais.values())
        if tipo is not None:
            sinais = [s for s in sinais if s.tipo == tipo]
        if origem is not None:
            sinais = [s for s in sinais if s.origem == origem]
        return sorted(sinais, key=lambda s: s.ocorrido_em)

    def limpar(self) -> None:
        self._sinais.clear()
