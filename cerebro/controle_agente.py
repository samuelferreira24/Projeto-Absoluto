from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any
import hashlib
import json
from datetime import datetime, timezone

from .identidade import Identidade, identidade_agente
from .eventos import Evento
from .eventos_ledger import LedgerEventos


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class AutorizacaoAgente:
    """Política mínima, portátil e explícita para um agente operacional."""

    identidade: Identidade
    ferramentas_permitidas: tuple[str, ...] = ()
    recursos_permitidos: tuple[str, ...] = ()
    nivel_maximo_autonomia: int = 2
    custo_maximo: float = 0.0
    retries_maximos: int = 0
    cadeia_maxima: int = 1
    requer_aprovacao: bool = False
    ativo: bool = True

    def __post_init__(self) -> None:
        if self.nivel_maximo_autonomia < 0:
            raise ValueError("nivel_maximo_autonomia não pode ser negativo")
        if self.custo_maximo < 0 or self.retries_maximos < 0 or self.cadeia_maxima < 1:
            raise ValueError("limites de execução inválidos")

    def autorizar(self, *, ferramenta: str, recurso: str | None = None,
                  nivel: int = 0, custo_estimado: float = 0.0,
                  cadeia: int = 1, aprovacao: bool = False) -> tuple[bool, str]:
        if not self.ativo:
            return False, "agente inativo"
        if nivel > self.nivel_maximo_autonomia:
            return False, "nível de autonomia excede o limite"
        if self.requer_aprovacao and not aprovacao:
            return False, "aprovação necessária"
        if ferramenta not in self.ferramentas_permitidas:
            return False, f"ferramenta não permitida: {ferramenta}"
        if recurso is not None and self.recursos_permitidos and recurso not in self.recursos_permitidos:
            return False, f"recurso não permitido: {recurso}"
        if custo_estimado < 0 or custo_estimado > self.custo_maximo:
            return False, "custo excede o limite do agente"
        if cadeia < 1 or cadeia > self.cadeia_maxima:
            return False, "cadeia de execução excede o limite"
        return True, "OK"


@dataclass(frozen=True)
class EventoTelemetria:
    tipo: str
    agente_id: str
    operacao: str
    estado: str
    timestamp: str = field(default_factory=agora)
    correlation_id: str | None = None
    parent_id: str | None = None
    ferramenta: str | None = None
    recurso: str | None = None
    duracao_ms: float | None = None
    custo: float | None = None
    detalhes: dict[str, Any] = field(default_factory=dict)

    @property
    def evento_id(self) -> str:
        base = {
            "tipo": self.tipo, "agente_id": self.agente_id,
            "operacao": self.operacao, "estado": self.estado,
            "timestamp": self.timestamp, "correlation_id": self.correlation_id,
            "parent_id": self.parent_id, "ferramenta": self.ferramenta,
            "recurso": self.recurso,
        }
        return "TEL-" + hashlib.sha256(
            json.dumps(base, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()[:24]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["evento_id"] = self.evento_id
        return data


class TelemetriaAgente:
    """Persistência append-only de observabilidade operacional."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def registrar(self, evento: EventoTelemetria) -> None:
        with self.path.open("a", encoding="utf-8") as arquivo:
            arquivo.write(json.dumps(evento.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")

    def listar(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return [json.loads(linha) for linha in self.path.read_text(encoding="utf-8").splitlines() if linha.strip()]

    def resumo(self) -> dict[str, Any]:
        eventos = self.listar()
        return {
            "eventos": len(eventos),
            "por_tipo": {tipo: sum(1 for e in eventos if e.get("tipo") == tipo)
                         for tipo in sorted({str(e.get("tipo")) for e in eventos})},
            "falhas": sum(1 for e in eventos if e.get("estado") == "FALHOU"),
            "bloqueios": sum(1 for e in eventos if e.get("estado") == "BLOQUEADO"),
        }


@dataclass
class ControleAgente:
    """Plano de controle entre intenção do agente e execução."""

    autorizacao: AutorizacaoAgente
    telemetria: TelemetriaAgente
    ledger: LedgerEventos | None = None

    def verificar(self, *, operacao: str, ferramenta: str, recurso: str | None = None,
                  nivel: int = 0, custo_estimado: float = 0.0, cadeia: int = 1,
                  aprovacao: bool = False, correlation_id: str | None = None,
                  parent_id: str | None = None) -> tuple[bool, str]:
        permitido, motivo = self.autorizacao.autorizar(
            ferramenta=ferramenta, recurso=recurso, nivel=nivel,
            custo_estimado=custo_estimado, cadeia=cadeia, aprovacao=aprovacao,
        )
        estado = "AUTORIZADO" if permitido else "BLOQUEADO"
        self.telemetria.registrar(EventoTelemetria(
            tipo="agent.authorization", agente_id=self.autorizacao.identidade.id,
            operacao=operacao, estado=estado, correlation_id=correlation_id,
            parent_id=parent_id, ferramenta=ferramenta, recurso=recurso,
            detalhes={"motivo": motivo, "nivel": nivel},
        ))
        if self.ledger is not None:
            self.ledger.append(Evento(
                origem=self.autorizacao.identidade.id, destino=ferramenta,
                tipo="AUTORIZACAO_AGENT",
                payload={"operacao": operacao, "estado": estado, "motivo": motivo},
                correlation_id=correlation_id, causation_id=parent_id,
            ))
        return permitido, motivo

    def registrar_resultado(self, *, operacao: str, estado: str,
                            ferramenta: str | None = None, recurso: str | None = None,
                            duracao_ms: float | None = None, custo: float | None = None,
                            correlation_id: str | None = None, parent_id: str | None = None,
                            detalhes: dict[str, Any] | None = None) -> None:
        self.telemetria.registrar(EventoTelemetria(
            tipo="agent.execution", agente_id=self.autorizacao.identidade.id,
            operacao=operacao, estado=estado, correlation_id=correlation_id,
            parent_id=parent_id, ferramenta=ferramenta, recurso=recurso,
            duracao_ms=duracao_ms, custo=custo, detalhes=dict(detalhes or {}),
        ))
