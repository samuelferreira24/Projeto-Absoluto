from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Any
import json

from .ciclo_continuo import CicloContinuo
from .orquestrador import Orquestrador


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class EstadoRuntime:
    estado: str = "PARADO"
    ultimo_ciclo: str | None = None
    ciclos: int = 0
    motivo_parada: str | None = None
    lease_id: str | None = None
    lease_expira_em: str | None = None


class RuntimeContinuo:
    """Laço persistente com lease para evitar dois runtimes simultâneos."""

    def __init__(self, orquestrador: Orquestrador, path: str | Path = "cerebro/data/runtime.json") -> None:
        self.orquestrador = orquestrador
        self.path = Path(path)
        self.estado = EstadoRuntime()
        self._carregar()

    def _carregar(self) -> None:
        if self.path.exists():
            self.estado = EstadoRuntime(**json.loads(self.path.read_text(encoding="utf-8")))
            if self.estado.estado == "EXECUTANDO":
                self.estado.estado = "RECUPERADO"
                self.estado.motivo_parada = "runtime anterior foi interrompido"
                self.estado.lease_id = None
                self.estado.lease_expira_em = None
                self._salvar()

    def _salvar(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.estado.__dict__, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def adquirir_lease(self, lease_id: str, expira_em: str) -> None:
        if self.estado.lease_id is not None and self.estado.estado == "EXECUTANDO":
            raise RuntimeError("runtime já possui lease ativo")
        self.estado.lease_id = lease_id
        self.estado.lease_expira_em = expira_em
        self._salvar()

    def liberar_lease(self, lease_id: str) -> None:
        if self.estado.lease_id != lease_id:
            raise RuntimeError("lease inválido")
        self.estado.lease_id = None
        self.estado.lease_expira_em = None
        self._salvar()

    def executar_ciclo(self, missao_id: str, candidatos: Callable, executor: Callable, lease_id: str | None = None, lease_expira_em: str | None = None) -> dict[str, Any]:
        if lease_id is not None:
            self.adquirir_lease(lease_id, lease_expira_em or agora())
        self.estado.estado = "EXECUTANDO"
        self.estado.motivo_parada = None
        self._salvar()
        try:
            resultado = CicloContinuo(self.orquestrador).rodar(missao_id, candidatos, executor)
            self.estado.ciclos += 1
            self.estado.ultimo_ciclo = agora()
            self.estado.estado = "AGUARDANDO_PROXIMO_CICLO"
            self._salvar()
            return resultado
        except Exception as exc:
            self.estado.estado = "ERRO_RECUPERAVEL"
            self.estado.motivo_parada = str(exc)
            self._salvar()
            raise
        finally:
            if lease_id is not None and self.estado.lease_id == lease_id:
                self.estado.lease_id = None
                self.estado.lease_expira_em = None
                self._salvar()

    def parar(self, motivo: str = "parada solicitada") -> None:
        self.estado.estado = "PARADO"
        self.estado.motivo_parada = motivo
        self.estado.lease_id = None
        self.estado.lease_expira_em = None
        self._salvar()
