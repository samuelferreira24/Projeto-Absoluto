from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata
from datetime import datetime
from typing import Iterable

from .nucleo import Registro
from .temporal import intervalo_da_unidade


@dataclass(frozen=True)
class ResultadoBusca:
    registro: Registro
    score: float
    motivos: tuple[str, ...]


def _normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in texto if not unicodedata.combining(c))


def _tokens(texto: str) -> list[str]:
    return [t for t in re.findall(r"[\wÀ-ÿ]+", _normalizar(texto)) if len(t) > 1]


def _instante_valido(instante: str | None) -> datetime | None:
    if instante is None:
        return None
    try:
        return datetime.fromisoformat(instante.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"instante ISO-8601 inválido: {instante}") from exc


def buscar_hibrido(
    registros: Iterable[Registro],
    consulta: str,
    limite: int = 10,
    *,
    instante: str | None = None,
    incluir_superados: bool = False,
) -> list[ResultadoBusca]:
    """Busca textual simples, agora consciente de validade temporal e supersessão."""
    query = set(_tokens(consulta))
    if not query:
        return []

    ponto = _instante_valido(instante)
    resultados: list[ResultadoBusca] = []
    for registro in registros:
        if registro.state == "SUPERADO" and not incluir_superados:
            continue
        if ponto is not None:
            intervalo = intervalo_da_unidade(registro)
            if not intervalo.valido_em(ponto.isoformat()):
                continue

        campos = {
            "titulo": _tokens(registro.title),
            "conteudo": _tokens(registro.content),
            "tipo": _tokens(registro.kind),
        }
        score = 0.0
        motivos: list[str] = []
        for nome, tokens, peso in (
            ("titulo", campos["titulo"], 4.0),
            ("conteudo", campos["conteudo"], 1.0),
            ("tipo", campos["tipo"], 1.5),
        ):
            inter = query.intersection(tokens)
            if inter:
                score += peso * len(inter) / max(1, len(query))
                motivos.append(f"{nome}:{','.join(sorted(inter))}")

        if score:
            if ponto is not None:
                motivos.append("temporal:valido")
            if registro.source:
                motivos.append("proveniencia:fonte")
                score += 0.05
            resultados.append(ResultadoBusca(registro, score, tuple(motivos)))

    resultados.sort(key=lambda r: (-r.score, r.registro.id))
    return resultados[:limite]


def expandir_relacoes(
    registros: Iterable[Registro],
    ids_iniciais: Iterable[str],
    profundidade: int = 1,
    *,
    instante: str | None = None,
    incluir_superados: bool = False,
) -> list[Registro]:
    por_id = {r.id: r for r in registros}
    visitados = set(ids_iniciais)
    fronteira = set(ids_iniciais)
    ponto = _instante_valido(instante)

    def elegivel(registro: Registro) -> bool:
        if registro.state == "SUPERADO" and not incluir_superados:
            return False
        if ponto is None:
            return True
        return intervalo_da_unidade(registro).valido_em(ponto.isoformat())

    for _ in range(max(0, profundidade)):
        proxima: set[str] = set()
        for registro_id in fronteira:
            registro = por_id.get(registro_id)
            if not registro or not elegivel(registro):
                continue
            for relacao in registro.relations:
                alvo = relacao.get("target")
                if alvo in por_id and alvo not in visitados and elegivel(por_id[alvo]):
                    proxima.add(alvo)
            for outro in por_id.values():
                if any(r.get("target") == registro_id for r in outro.relations) and outro.id not in visitados and elegivel(outro):
                    proxima.add(outro.id)
        visitados.update(proxima)
        fronteira = proxima
    return [por_id[i] for i in visitados if i in por_id and elegivel(por_id[i])]
