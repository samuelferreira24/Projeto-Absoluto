"""Identidade portável do Projeto Absoluto.

IDs pertencem ao projeto, não à conta, IA, plataforma ou fornecedor que
esteja operando o sistema. O módulo fornece identificadores determinísticos
ou únicos para projeto, agente, sessão e recurso.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass


_PADRAO = re.compile(r"^[A-Z][A-Z0-9_-]{2,63}$")


@dataclass(frozen=True)
class Identidade:
    """Identidade estável de uma entidade operacional."""

    id: str
    tipo: str
    versao: int = 1

    def __post_init__(self) -> None:
        if not self.id or not isinstance(self.id, str):
            raise ValueError("id deve ser uma string não vazia")
        if not self.tipo or not isinstance(self.tipo, str):
            raise ValueError("tipo deve ser uma string não vazia")
        if self.versao < 1:
            raise ValueError("versao deve ser >= 1")

    def to_dict(self) -> dict:
        return {"id": self.id, "tipo": self.tipo, "versao": self.versao}


def novo_id(prefixo: str, *, tamanho: int = 12) -> str:
    """Cria um ID portável no formato PREFIXO-HEX."""
    prefixo = prefixo.strip().upper().replace(" ", "-")
    if not _PADRAO.fullmatch(prefixo):
        raise ValueError("prefixo inválido")
    if tamanho < 4 or tamanho > 32:
        raise ValueError("tamanho deve estar entre 4 e 32")
    return f"{prefixo}-{uuid.uuid4().hex[:tamanho]}"


def identidade_projeto() -> Identidade:
    return Identidade("PA-PROJETO-ABSOLUTO", "PROJETO")


def identidade_agente() -> Identidade:
    return Identidade(novo_id("PA-AGENTE"), "AGENTE")


def identidade_sessao() -> Identidade:
    return Identidade(novo_id("PA-SESSAO"), "SESSAO")


def identidade_recurso(tipo: str) -> Identidade:
    tipo = tipo.strip().upper()
    return Identidade(novo_id(f"PA-{tipo}"), tipo)
