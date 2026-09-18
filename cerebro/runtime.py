from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Iterator
import fcntl
import json
import os
import socket
import threading
import uuid

from .ciclo_continuo import CicloContinuo
from .orquestrador import Orquestrador


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _parse_iso(valor: str | None) -> datetime | None:
    if not valor:
        return None
    return datetime.fromisoformat(valor.replace("Z", "+00:00"))


@dataclass
class EstadoRuntime:
    estado: str = "PARADO"
    ultimo_ciclo: str | None = None
    ciclos: int = 0
    motivo_parada: str | None = None
    runtime_id: str | None = None
    lease_id: str | None = None
    lease_expira_em: str | None = None
    heartbeat_em: str | None = None


class RuntimeContinuo:
    """Runtime recuperável com claim atômico, lease e heartbeat.

    O lock interprocessos serializa claim/renew/release do lease local. A
    expiração permite recuperar um worker abandonado. Efeitos externos
    continuam exigindo idempotência.
    """

    def __init__(
        self,
        orquestrador: Orquestrador,
        path: str | Path = "cerebro/data/runtime.json",
        lease_path: str | Path | None = None,
        lease_segundos: int = 300,
    ) -> None:
        if lease_segundos <= 0:
            raise ValueError("lease_segundos deve ser positivo")
        self.orquestrador = orquestrador
        self.path = Path(path)
        self.lease_path = Path(lease_path) if lease_path else self.path.with_suffix(".lease")
        self.lock_path = self.lease_path.with_suffix(self.lease_path.suffix + ".lock")
        self.lease_segundos = lease_segundos
        self._heartbeat_intervalo = max(1.0, min(30.0, lease_segundos / 3))
        self.estado = EstadoRuntime(runtime_id=f"{socket.gethostname()}-{uuid.uuid4().hex[:12]}")
        self._carregar()

    @contextmanager
    def _lock_lease(self) -> Iterator[None]:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        with self.lock_path.open("a+") as arquivo:
            fcntl.flock(arquivo.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(arquivo.fileno(), fcntl.LOCK_UN)

    def _carregar(self) -> None:
        if not self.path.exists():
            return
        self.estado = EstadoRuntime(**json.loads(self.path.read_text(encoding="utf-8")))
        if self.estado.estado == "EXECUTANDO":
            expiracao = _parse_iso(self.estado.lease_expira_em)
            if expiracao is None or expiracao <= datetime.now(timezone.utc):
                self.estado.estado = "RECUPERADO"
                self.estado.motivo_parada = "lease do runtime anterior expirou"
                self.estado.lease_id = None
                self.estado.lease_expira_em = None
                self.estado.heartbeat_em = None
                self._salvar()

    def _salvar(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporario = self.path.with_name(f".{self.path.name}.{os.getpid()}.tmp")
        temporario.write_text(
            json.dumps(self.estado.__dict__, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(temporario, self.path)

    def _lease_expirado(self) -> bool:
        if not self.lease_path.exists():
            return True
        try:
            dados = json.loads(self.lease_path.read_text(encoding="utf-8"))
            expiracao = _parse_iso(dados.get("expira_em"))
            return expiracao is None or expiracao <= datetime.now(timezone.utc)
        except (OSError, json.JSONDecodeError):
            return True

    def _nova_expiracao(self) -> str:
        return (datetime.now(timezone.utc) + timedelta(seconds=self.lease_segundos)).replace(microsecond=0).isoformat()

    def adquirir_lease(self, lease_id: str, expira_em: str | None = None) -> None:
        self.lease_path.parent.mkdir(parents=True, exist_ok=True)
        expiracao = _parse_iso(expira_em) or _parse_iso(self._nova_expiracao())
        assert expiracao is not None
        with self._lock_lease():
            if self.lease_path.exists():
                if not self._lease_expirado():
                    raise RuntimeError("runtime já possui lease ativo")
                try:
                    self.lease_path.unlink()
                except FileNotFoundError:
                    pass
            dados = {
                "lease_id": lease_id,
                "runtime_id": self.estado.runtime_id,
                "expira_em": expiracao.isoformat(),
                "criado_em": agora(),
            }
            flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
            fd = os.open(self.lease_path, flags)
            try:
                os.write(fd, json.dumps(dados, ensure_ascii=False).encode("utf-8"))
            finally:
                os.close(fd)
        self.estado.lease_id = lease_id
        self.estado.lease_expira_em = expiracao.isoformat()
        self.estado.heartbeat_em = agora()
        self._salvar()

    def renovar_lease(self, lease_id: str, expira_em: str | None = None) -> None:
        with self._lock_lease():
            if self.estado.lease_id != lease_id:
                raise RuntimeError("lease inválido")
            if not self.lease_path.exists():
                raise RuntimeError("lease não existe mais")
            dados = json.loads(self.lease_path.read_text(encoding="utf-8"))
            if dados.get("lease_id") != lease_id:
                raise RuntimeError("lease não pertence a este runtime")
            expiracao_atual = _parse_iso(dados.get("expira_em"))
            if expiracao_atual is not None and expiracao_atual <= datetime.now(timezone.utc):
                raise RuntimeError("lease expirado")
            expiracao = _parse_iso(expira_em) or _parse_iso(self._nova_expiracao())
            assert expiracao is not None
            heartbeat = agora()
            dados["expira_em"] = expiracao.isoformat()
            dados["heartbeat_em"] = heartbeat
            temporario = self.lease_path.with_name(f".{self.lease_path.name}.{os.getpid()}.tmp")
            temporario.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
            os.replace(temporario, self.lease_path)
        self.estado.lease_expira_em = expiracao.isoformat()
        self.estado.heartbeat_em = heartbeat
        self._salvar()

    def liberar_lease(self, lease_id: str) -> None:
        with self._lock_lease():
            if self.estado.lease_id != lease_id:
                raise RuntimeError("lease inválido")
            try:
                dados = json.loads(self.lease_path.read_text(encoding="utf-8"))
                if dados.get("lease_id") == lease_id:
                    self.lease_path.unlink()
            except FileNotFoundError:
                pass
        self.estado.lease_id = None
        self.estado.lease_expira_em = None
        self.estado.heartbeat_em = None
        self._salvar()

    def _iniciar_heartbeat(self, lease_id: str) -> tuple[threading.Event, threading.Thread]:
        parar = threading.Event()

        def loop() -> None:
            while not parar.wait(self._heartbeat_intervalo):
                try:
                    self.renovar_lease(lease_id)
                except RuntimeError:
                    parar.set()
                    return

        thread = threading.Thread(target=loop, name=f"heartbeat-{lease_id[:12]}", daemon=True)
        thread.start()
        return parar, thread

    def executar_ciclo(
        self,
        missao_id: str,
        candidatos: Callable,
        executor: Callable,
        lease_id: str | None = None,
        lease_expira_em: str | None = None,
    ) -> dict[str, Any]:
        identificador = lease_id or f"{self.estado.runtime_id}-{uuid.uuid4().hex[:12]}"
        self.adquirir_lease(identificador, lease_expira_em)
        heartbeat_stop, heartbeat_thread = self._iniciar_heartbeat(identificador)
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
            heartbeat_stop.set()
            heartbeat_thread.join(timeout=1.0)
            if self.estado.lease_id == identificador:
                self.liberar_lease(identificador)

    def parar(self, motivo: str = "parada solicitada") -> None:
        if self.estado.lease_id:
            try:
                self.liberar_lease(self.estado.lease_id)
            except RuntimeError:
                self.estado.lease_id = None
                self.estado.lease_expira_em = None
                self.estado.heartbeat_em = None
        self.estado.estado = "PARADO"
        self.estado.motivo_parada = motivo
        self._salvar()
