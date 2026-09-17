from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json
import os
import uuid


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class PedidoDespertar:
    id: str
    missao_id: str
    origem: str
    estado: str = "PENDENTE"
    correlation_id: str | None = None
    criado_em: str = ""
    processado_em: str | None = None
    detalhes: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if not self.criado_em:
            self.criado_em = agora()
        if self.estado not in {"PENDENTE", "PROCESSANDO", "CONCLUIDO", "FALHOU"}:
            raise ValueError(f"estado de despertar inválido: {self.estado}")


class Despertador:
    """Controla pedidos de despertar independentes da interface do usuário.

    O despertador não escolhe a estratégia nem executa uma IA. Ele cria uma
    fronteira durável entre um evento externo e o runtime do Projeto.
    """

    def __init__(self, path: str | Path = "cerebro/data/despertar.json") -> None:
        self.path = Path(path)
        self.pedidos: list[PedidoDespertar] = []
        self._carregar()

    def _carregar(self) -> None:
        if self.path.exists():
            dados = json.loads(self.path.read_text(encoding="utf-8"))
            self.pedidos = [PedidoDespertar(**item) for item in dados.get("pedidos", [])]

    def _salvar(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporario = self.path.with_name(f".{self.path.name}.{os.getpid()}.tmp")
        temporario.write_text(
            json.dumps({"schema_version": "0.1", "pedidos": [asdict(p) for p in self.pedidos]}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(temporario, self.path)

    def solicitar(self, missao_id: str, origem: str, correlation_id: str | None = None, detalhes: dict[str, Any] | None = None) -> PedidoDespertar:
        pedido = PedidoDespertar(
            id=f"WAKE-{uuid.uuid4().hex}",
            missao_id=missao_id,
            origem=origem,
            correlation_id=correlation_id,
            detalhes=detalhes or {},
        )
        self.pedidos.append(pedido)
        self._salvar()
        return pedido

    def pendentes(self, missao_id: str | None = None) -> list[PedidoDespertar]:
        return [p for p in self.pedidos if p.estado == "PENDENTE" and (missao_id is None or p.missao_id == missao_id)]

    def iniciar(self, pedido_id: str) -> PedidoDespertar:
        pedido = next(p for p in self.pedidos if p.id == pedido_id)
        if pedido.estado != "PENDENTE":
            raise RuntimeError(f"pedido não está pendente: {pedido.estado}")
        pedido.estado = "PROCESSANDO"
        self._salvar()
        return pedido

    def concluir(self, pedido_id: str) -> PedidoDespertar:
        pedido = next(p for p in self.pedidos if p.id == pedido_id)
        pedido.estado = "CONCLUIDO"
        pedido.processado_em = agora()
        self._salvar()
        return pedido

    def falhar(self, pedido_id: str, erro: str) -> PedidoDespertar:
        pedido = next(p for p in self.pedidos if p.id == pedido_id)
        pedido.estado = "FALHOU"
        pedido.processado_em = agora()
        pedido.detalhes = {**(pedido.detalhes or {}), "erro": erro}
        self._salvar()
        return pedido
