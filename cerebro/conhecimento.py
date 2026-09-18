from __future__ import annotations

"""Camada persistente de conhecimento do Cérebro.

A camada não substitui o acervo bruto nem a memória legada. Ela cria uma
representação canônica, versionada e relacionada do conhecimento que pode ser
recuperada pelo Cérebro e compartilhada por diferentes agentes.
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
import hashlib
import json
import re
import unicodedata


TIPOS_CONHECIMENTO = {
    "FATO", "HIPOTESE", "INTERPRETACAO", "EVIDENCIA", "CONHECIMENTO",
    "DECISAO", "EXPERIENCIA", "APRENDIZADO", "DESCOBERTA", "ENTENDIMENTO",
    "ERRO", "RESULTADO", "PROCEDIMENTO", "PRINCIPIO", "QUESTAO_ABERTA",
}
ESTADOS = {"NOVO", "EM_ANALISE", "EM_TESTE", "VALIDADO", "REFUTADO", "SUPERADO", "ARQUIVADO"}
CONFIANCAS = {"ALTA", "MEDIA", "BAIXA", "DESCONHECIDA"}
RELACOES = {
    "DERIVA_DE", "SUSTENTA", "CONTRADIZ", "CORRIGE", "SUBSTITUI",
    "APRENDE_DE", "GERA", "DEPENDE_DE", "RELACIONA_SE_COM",
}


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto.casefold())
    return "".join(c for c in texto if not unicodedata.combining(c))


def _tokens(texto: str) -> set[str]:
    return {x for x in re.findall(r"[\\wÀ-ÿ]+", _normalizar(texto)) if len(x) > 1}


def _deterministic_id(kind: str, title: str, content: str, sources: Iterable[str]) -> str:
    material = json.dumps(
        [kind.upper(), title, content, sorted(set(sources))],
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return "KN-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]


@dataclass
class Conhecimento:
    id: str
    kind: str
    title: str
    content: str
    source_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    provenance: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    confidence: str = "DESCONHECIDA"
    state: str = "NOVO"
    temporal: dict[str, str | None] = field(default_factory=dict)
    supersedes: tuple[str, ...] = ()
    relations: tuple[dict[str, str], ...] = ()
    version: int = 1
    created_at: str = field(default_factory=agora)
    updated_at: str = field(default_factory=agora)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.kind = self.kind.upper()
        self.confidence = self.confidence.upper()
        self.state = self.state.upper()
        if self.kind not in TIPOS_CONHECIMENTO:
            raise ValueError(f"tipo de conhecimento inválido: {self.kind}")
        if self.confidence not in CONFIANCAS:
            raise ValueError(f"confiança inválida: {self.confidence}")
        if self.state not in ESTADOS:
            raise ValueError(f"estado inválido: {self.state}")
        if not self.id or not self.title or not self.content:
            raise ValueError("id, title e content são obrigatórios")
        if not self.source_ids and not self.provenance:
            raise ValueError("conhecimento precisa de fonte ou proveniência")
        if self.version < 1:
            raise ValueError("version deve ser >= 1")
        for key in ("valid_from", "valid_until", "recorded_at"):
            if key in self.temporal and self.temporal[key] is not None:
                datetime.fromisoformat(str(self.temporal[key]).replace("Z", "+00:00"))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ResultadoConhecimento:
    conhecimento: Conhecimento
    score: float
    motivos: tuple[str, ...]


class BaseConhecimento:
    """Armazenamento append-only do conhecimento atual + histórico por item."""

    SCHEMA_VERSION = "0.1"

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / "conhecimento.jsonl"
        self.history = self.root / "historico_conhecimento"
        self.history.mkdir(parents=True, exist_ok=True)

    def _iter_raw(self) -> Iterable[dict[str, Any]]:
        if not self.path.exists():
            return ()
        def gen():
            for line in self.path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    value = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(value, dict):
                    yield value
        return gen()

    def _current(self) -> dict[str, Conhecimento]:
        atual: dict[str, Conhecimento] = {}
        for raw in self._iter_raw():
            try:
                item = Conhecimento(**raw)
            except (TypeError, ValueError):
                continue
            anterior = atual.get(item.id)
            if anterior is None or item.version >= anterior.version:
                atual[item.id] = item
        return atual

    def listar(self) -> list[Conhecimento]:
        return list(self._current().values())

    def obter(self, conhecimento_id: str) -> Conhecimento | None:
        return self._current().get(conhecimento_id)

    def adicionar(self, item: Conhecimento) -> Conhecimento:
        existente = self.obter(item.id)
        if existente is not None:
            if existente.to_dict() == item.to_dict():
                return existente
            item.version = existente.version + 1
            item.created_at = existente.created_at
            item.updated_at = agora()
        self._append(item)
        return item

    def criar(
        self,
        kind: str,
        title: str,
        content: str,
        *,
        source_ids: Iterable[str] = (),
        evidence_ids: Iterable[str] = (),
        provenance: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
        confidence: str = "DESCONHECIDA",
        state: str = "NOVO",
        temporal: dict[str, str | None] | None = None,
        supersedes: Iterable[str] = (),
        relations: Iterable[dict[str, str]] = (),
        metadata: dict[str, Any] | None = None,
    ) -> Conhecimento:
        sources = tuple(dict.fromkeys(str(x) for x in source_ids))
        item_id = _deterministic_id(kind, title, content, sources)
        return self.adicionar(Conhecimento(
            id=item_id,
            kind=kind,
            title=title,
            content=content,
            source_ids=sources,
            evidence_ids=tuple(dict.fromkeys(str(x) for x in evidence_ids)),
            provenance=dict(provenance or {}),
            context=dict(context or {}),
            confidence=confidence,
            state=state,
            temporal=dict(temporal or {}),
            supersedes=tuple(dict.fromkeys(str(x) for x in supersedes)),
            relations=tuple(dict(x) for x in relations),
            metadata=dict(metadata or {}),
        ))

    def atualizar(
        self,
        conhecimento_id: str,
        *,
        content: str | None = None,
        confidence: str | None = None,
        state: str | None = None,
        temporal: dict[str, str | None] | None = None,
        provenance: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
        relations: Iterable[dict[str, str]] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Conhecimento:
        atual = self.obter(conhecimento_id)
        if atual is None:
            raise KeyError(conhecimento_id)
        dados = atual.to_dict()
        if content is not None:
            dados["content"] = content
        if confidence is not None:
            dados["confidence"] = confidence
        if state is not None:
            dados["state"] = state
        if temporal is not None:
            dados["temporal"] = dict(temporal)
        if provenance is not None:
            dados["provenance"] = dict(provenance)
        if context is not None:
            dados["context"] = dict(context)
        if relations is not None:
            dados["relations"] = tuple(dict(x) for x in relations)
        if metadata is not None:
            dados["metadata"] = dict(metadata)
        dados["version"] = atual.version + 1
        dados["created_at"] = atual.created_at
        dados["updated_at"] = agora()
        novo = Conhecimento(**dados)
        self._append(novo)
        return novo

    def relacionar(self, source_id: str, relation: str, target_id: str, *, provenance: dict[str, Any] | None = None) -> Conhecimento:
        if self.obter(source_id) is None or self.obter(target_id) is None:
            raise KeyError("relação referencia conhecimento inexistente")
        relation = relation.upper()
        if relation not in RELACOES:
            raise ValueError(f"relação inválida: {relation}")
        atual = self.obter(source_id)
        assert atual is not None
        relacoes = list(atual.relations)
        relacao = {"type": relation, "target": target_id}
        if relacao not in relacoes:
            relacoes.append(relacao)
        if provenance:
            relacoes[-1] = {**relacoes[-1], "provenance": json.dumps(provenance, ensure_ascii=False, sort_keys=True)}
        return self.atualizar(source_id, relations=relacoes)

    def superseder(self, previous_id: str, *, kind: str, title: str, content: str, **kwargs: Any) -> Conhecimento:
        novo = self.criar(kind, title, content, supersedes=(previous_id,), **kwargs)
        self.relacionar(novo.id, "SUBSTITUI", previous_id)
        self.atualizar(previous_id, state="SUPERADO")
        return self.obter(novo.id) or novo

    def buscar(
        self,
        consulta: str,
        limite: int = 10,
        *,
        instante: str | None = None,
        incluir_superados: bool = False,
        tipos: set[str] | None = None,
    ) -> list[ResultadoConhecimento]:
        query = _tokens(consulta)
        if not query:
            return []
        ponto = datetime.fromisoformat(instante.replace("Z", "+00:00")) if instante else None
        resultados: list[ResultadoConhecimento] = []
        for item in self.listar():
            if tipos and item.kind not in tipos:
                continue
            if item.state == "SUPERADO" and not incluir_superados:
                continue
            if ponto and not self._valido_em(item, ponto):
                continue
            titulo = _tokens(item.title)
            conteudo = _tokens(item.content)
            contexto = _tokens(json.dumps(item.context, ensure_ascii=False))
            score = 4.0 * len(query & titulo) / max(1, len(query))
            score += 1.0 * len(query & conteudo) / max(1, len(query))
            score += 0.5 * len(query & contexto) / max(1, len(query))
            motivos = []
            if query & titulo:
                motivos.append("titulo")
            if query & conteudo:
                motivos.append("conteudo")
            if item.source_ids or item.provenance:
                score += 0.1
                motivos.append("proveniencia")
            if ponto:
                motivos.append("temporal:valido")
            if score:
                resultados.append(ResultadoConhecimento(item, score, tuple(motivos)))
        resultados.sort(key=lambda x: (-x.score, x.conhecimento.id))
        return resultados[:limite]

    @staticmethod
    def _valido_em(item: Conhecimento, ponto: datetime) -> bool:
        inicio = item.temporal.get("valid_from")
        fim = item.temporal.get("valid_until")
        if inicio and ponto < datetime.fromisoformat(str(inicio).replace("Z", "+00:00")):
            return False
        if fim and ponto > datetime.fromisoformat(str(fim).replace("Z", "+00:00")):
            return False
        return True

    def relacionados(self, ids: Iterable[str], profundidade: int = 1, *, incluir_superados: bool = False) -> list[Conhecimento]:
        por_id = self._current()
        visitados = set(ids)
        fronteira = set(ids)
        for _ in range(max(0, profundidade)):
            proxima: set[str] = set()
            for item_id in fronteira:
                item = por_id.get(item_id)
                if not item:
                    continue
                for rel in item.relations:
                    alvo = rel.get("target")
                    if alvo in por_id and alvo not in visitados:
                        if incluir_superados or por_id[alvo].state != "SUPERADO":
                            proxima.add(alvo)
                for outro in por_id.values():
                    if any(rel.get("target") == item_id for rel in outro.relations) and outro.id not in visitados:
                        if incluir_superados or outro.state != "SUPERADO":
                            proxima.add(outro.id)
            visitados.update(proxima)
            fronteira = proxima
        return [por_id[i] for i in visitados if i in por_id]

    def importar_aprendizados(self, registros: Iterable[dict[str, Any]]) -> list[Conhecimento]:
        importados = []
        for aprendizado in registros:
            tipo = str(aprendizado.get("tipo", "APRENDIZADO")).upper()
            kind = tipo if tipo in TIPOS_CONHECIMENTO else "APRENDIZADO"
            importados.append(self.criar(
                kind,
                str(aprendizado.get("titulo", "Aprendizado sem título")),
                str(aprendizado.get("conteudo", "")),
                source_ids=(),
                evidence_ids=aprendizado.get("evidencias", ()) or (),
                provenance={
                    "tipo": "aprendizado",
                    "origem": aprendizado.get("origem", "memoria"),
                    "aprendizado_id": aprendizado.get("id"),
                },
                context={"contexto": aprendizado.get("contexto", ())},
                confidence=str(aprendizado.get("confianca", "DESCONHECIDA")).upper(),
                supersedes=((aprendizado["supersede"],) if aprendizado.get("supersede") else ()),
                metadata={"memoria_origem": "aprendizados.jsonl"},
            ))
        return importados

    def diagnostico(self) -> dict[str, Any]:
        itens = self.listar()
        return {
            "schema_version": self.SCHEMA_VERSION,
            "itens": len(itens),
            "tipos": {k: sum(1 for x in itens if x.kind == k) for k in sorted({x.kind for x in itens})},
            "superados": sum(1 for x in itens if x.state == "SUPERADO"),
            "com_proveniencia": sum(1 for x in itens if x.source_ids or x.provenance),
            "confianca_desconhecida": sum(1 for x in itens if x.confidence == "DESCONHECIDA"),
        }

    def _append(self, item: Conhecimento) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as arquivo:
            arquivo.write(json.dumps(item.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
        historico = self.history / f"{item.id}.jsonl"
        with historico.open("a", encoding="utf-8") as arquivo:
            arquivo.write(json.dumps({
                "at": agora(),
                "version": item.version,
                "record": item.to_dict(),
            }, ensure_ascii=False, sort_keys=True) + "\n")
