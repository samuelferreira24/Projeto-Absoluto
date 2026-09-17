from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
from typing import Any


TIPOS = {
    "APRENDIZADO",
    "DESCOBERTA",
    "ENTENDIMENTO",
    "MUDANCA_DE_ENTENDIMENTO",
    "CORRECAO",
    "ERRO",
    "DECISAO",
    "PROGRESSO",
    "EVENTO_DE_CONSTRUCAO",
}


@dataclass(frozen=True)
class Aprendizado:
    tipo: str
    titulo: str
    conteudo: str
    origem: str
    criado_em: str
    evidencias: tuple[str, ...] = ()
    contexto: tuple[str, ...] = ()
    relacoes: tuple[dict[str, Any], ...] = ()
    confianca: str = "nao_determinada"
    supersede: str | None = None
    id: str = field(default="")

    def __post_init__(self) -> None:
        if self.tipo not in TIPOS:
            raise ValueError(f"tipo de aprendizado inválido: {self.tipo}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _id(tipo: str, titulo: str, conteudo: str, origem: str) -> str:
    bruto = "|".join((tipo, titulo, conteudo, origem)).encode("utf-8")
    return hashlib.sha256(bruto).hexdigest()


def novo_aprendizado(
    tipo: str,
    titulo: str,
    conteudo: str,
    origem: str,
    *,
    evidencias: tuple[str, ...] = (),
    contexto: tuple[str, ...] = (),
    relacoes: tuple[dict[str, Any], ...] = (),
    confianca: str = "nao_determinada",
    supersede: str | None = None,
) -> Aprendizado:
    criado_em = datetime.now(timezone.utc).isoformat()
    return Aprendizado(
        tipo=tipo,
        titulo=titulo,
        conteudo=conteudo,
        origem=origem,
        criado_em=criado_em,
        evidencias=evidencias,
        contexto=contexto,
        relacoes=relacoes,
        confianca=confianca,
        supersede=supersede,
        id=_id(tipo, titulo, conteudo, origem),
    )


def registrar_aprendizado(aprendizado: Aprendizado, arquivo: str | Path) -> bool:
    """Registra sem duplicar: o ID determinístico torna a operação idempotente."""
    path = Path(arquivo)
    path.parent.mkdir(parents=True, exist_ok=True)
    existente: set[str] = set()
    if path.exists():
        for linha in path.read_text(encoding="utf-8").splitlines():
            if not linha.strip():
                continue
            try:
                existente.add(json.loads(linha).get("id", ""))
            except json.JSONDecodeError:
                continue
    if aprendizado.id in existente:
        return False
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(aprendizado.to_dict(), ensure_ascii=False) + "\n")
    return True


def registrar_evento_construcao(
    titulo: str,
    conteudo: str,
    origem: str,
    *,
    evidencias: tuple[str, ...] = (),
    contexto: tuple[str, ...] = (),
    relacoes: tuple[dict[str, Any], ...] = (),
) -> Aprendizado:
    return novo_aprendizado(
        "EVENTO_DE_CONSTRUCAO",
        titulo,
        conteudo,
        origem,
        evidencias=evidencias,
        contexto=contexto,
        relacoes=relacoes,
    )
