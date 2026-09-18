from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .portas import Porta, RegistroPortas


Handler = Callable[..., Any]


@dataclass(frozen=True)
class ResultadoPorta:
    porta_id: str
    capacidade: str
    sucesso: bool
    resultado: Any = None
    erro: str | None = None


class AtivadorPortas:
    """Liga capacidades registradas a implementações executáveis em runtime.

    O registro continua descritivo e portátil; os handlers são injetados em
    runtime, evitando acoplamento permanente do Cérebro a um provedor.
    """

    def __init__(self, registro: RegistroPortas) -> None:
        self.registro = registro
        self._handlers: dict[tuple[str, str], Handler] = {}

    def ativar(self, porta_id: str, capacidade: str, handler: Handler) -> None:
        porta = self._obter_ativa(porta_id)
        if capacidade.casefold() not in {item.casefold() for item in porta.capacidades}:
            raise ValueError(
                f"capacidade '{capacidade}' não está registrada na porta '{porta_id}'"
            )
        self._handlers[(porta_id, capacidade.casefold())] = handler

    def desativar(self, porta_id: str, capacidade: str) -> None:
        self._handlers.pop((porta_id, capacidade.casefold()), None)

    def disponivel(self, capacidade: str, *, ambiente: str | None = None) -> bool:
        candidatos = self.registro.por_capacidade(capacidade)
        if ambiente is not None:
            candidatos = [
                porta for porta in candidatos
                if porta.ambiente.casefold() == ambiente.casefold()
            ]
        return any(
            (porta.id, capacidade.casefold()) in self._handlers
            for porta in candidatos
        )

    def executar(
        self,
        capacidade: str,
        *args: Any,
        ambiente: str | None = None,
        porta_id: str | None = None,
        **kwargs: Any,
    ) -> ResultadoPorta:
        porta = self._selecionar(
            capacidade,
            ambiente=ambiente,
            porta_id=porta_id,
        )
        chave = (porta.id, capacidade.casefold())
        handler = self._handlers.get(chave)
        if handler is None:
            raise RuntimeError(
                f"nenhuma implementação ativa para '{capacidade}' na porta '{porta.id}'"
            )

        try:
            resultado = handler(*args, **kwargs)
        except Exception as exc:
            return ResultadoPorta(
                porta_id=porta.id,
                capacidade=capacidade,
                sucesso=False,
                erro=f"{type(exc).__name__}: {exc}",
            )

        return ResultadoPorta(
            porta_id=porta.id,
            capacidade=capacidade,
            sucesso=True,
            resultado=resultado,
        )

    def _obter_ativa(self, porta_id: str) -> Porta:
        for porta in self.registro.listar(ativas=True):
            if porta.id == porta_id:
                return porta
        raise ValueError(f"porta ativa não encontrada: {porta_id}")

    def _selecionar(
        self,
        capacidade: str,
        *,
        ambiente: str | None,
        porta_id: str | None,
    ) -> Porta:
        if porta_id is not None:
            porta = self._obter_ativa(porta_id)
            if capacidade.casefold() not in {
                item.casefold() for item in porta.capacidades
            }:
                raise ValueError(
                    f"capacidade '{capacidade}' não pertence à porta '{porta_id}'"
                )
            return porta

        candidatos = self.registro.por_capacidade(capacidade)
        if ambiente is not None:
            candidatos = [
                porta for porta in candidatos
                if porta.ambiente.casefold() == ambiente.casefold()
            ]

        ativos = [
            porta for porta in candidatos
            if (porta.id, capacidade.casefold()) in self._handlers
        ]
        if not ativos:
            raise RuntimeError(
                f"nenhuma porta ativa e implementada para a capacidade '{capacidade}'"
            )

        return ativos[0]
