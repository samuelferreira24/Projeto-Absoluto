from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import hashlib
import json
import re
import uuid

TIPOS = {
    "FONTE", "DOCUMENTO", "IDEIA", "PESQUISA", "CONHECIMENTO", "HIPOTESE",
    "EVIDENCIA", "DECISAO", "PLANEJAMENTO", "EXPERIMENTO", "PROBLEMA", "ERRO",
    "RESULTADO", "EXPERIENCIA", "APRENDIZADO", "QUESTAO_ABERTA", "METODO",
}
ESTADOS = {"NOVO", "EM_ANALISE", "EM_TESTE", "VALIDADO", "REFUTADO", "SUPERADO", "ARQUIVADO"}


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def hash_arquivo(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def novo_id(tipo: str, numero: int = 1, ano: int | None = None) -> str:
    ano = ano or datetime.now(timezone.utc).year
    tipo = tipo.upper().replace(" ", "_")
    return f"{tipo}-{ano}-{numero:04d}"


@dataclass
class Registro:
    id: str
    kind: str
    title: str
    created_at: str
    updated_at: str
    source: str | None = None
    content: str = ""
    state: str = "NOVO"
    relations: list[dict[str, str]] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)
    version: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.kind = self.kind.upper()
        if self.kind not in TIPOS:
            raise ValueError(f"Tipo inválido: {self.kind}")
        if self.state not in ESTADOS:
            raise ValueError(f"Estado inválido: {self.state}")
        if not self.id or not self.title:
            raise ValueError("id e title são obrigatórios")

    def add_relation(self, relation: str, target_id: str) -> None:
        self.relations.append({"type": relation, "target": target_id})
        self.updated_at = agora()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class RepositorioJSONL:
    """Armazenamento portátil e simples; cada registro ocupa uma linha JSON."""

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "registros").mkdir(exist_ok=True)
        (self.root / "fontes").mkdir(exist_ok=True)
        (self.root / "historico").mkdir(exist_ok=True)

    def _path(self, registro: Registro) -> Path:
        return self.root / "registros" / f"{registro.kind.lower()}.jsonl"

    def _ler_todos(self) -> list[Registro]:
        return list(self._iter_registros())

    def salvar(self, registro: Registro) -> None:
        existentes = {r.id: r for r in self._ler_todos()}
        if registro.id in existentes:
            raise ValueError(f"Registro já existe: {registro.id}. Use atualizar().")
        with self._path(registro).open("a", encoding="utf-8") as f:
            f.write(registro.to_json().replace("\n", " ") + "\n")
        self._registrar_historico(registro)

    def atualizar(self, registro: Registro) -> None:
        """Atualiza um registro sem apagar seu histórico; a versão é incrementada."""
        registros = self._ler_todos()
        encontrado = False
        for indice, atual in enumerate(registros):
            if atual.id == registro.id:
                if atual.kind != registro.kind:
                    raise ValueError("Não é permitido alterar o tipo de um registro existente")
                registro.created_at = atual.created_at
                registro.version = atual.version + 1
                registro.updated_at = agora()
                registros[indice] = registro
                encontrado = True
                break
        if not encontrado:
            raise KeyError(f"Registro não encontrado: {registro.id}")

        caminhos = {r.kind.lower(): self.root / "registros" / f"{r.kind.lower()}.jsonl" for r in registros}
        for path in set(caminhos.values()):
            itens = [r for r in registros if self._path(r) == path]
            with path.open("w", encoding="utf-8") as f:
                for item in itens:
                    f.write(item.to_json().replace("\n", " ") + "\n")
        self._registrar_historico(registro)

    def _registrar_historico(self, registro: Registro) -> None:
        historico = self.root / "historico" / f"{registro.id}.jsonl"
        with historico.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"at": agora(), "version": registro.version, "record": registro.to_dict()}, ensure_ascii=False) + "\n")

    def _iter_registros(self):
        for path in (self.root / "registros").glob("*.jsonl"):
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    yield Registro(**json.loads(line))
                except (json.JSONDecodeError, TypeError, ValueError):
                    continue

    def buscar(self, texto: str) -> list[Registro]:
        termo = texto.casefold()
        return [r for r in self._iter_registros() if termo in json.dumps(r.to_dict(), ensure_ascii=False).casefold()]

    def buscar_por_metadados(self, filtros: dict[str, Any]) -> list[Registro]:
        """Busca por igualdade em metadados, tipo, estado ou origem."""
        resultados = []
        for registro in self._iter_registros():
            corresponde = True
            for chave, esperado in filtros.items():
                atual = getattr(registro, chave) if chave in {"kind", "state", "source"} else registro.metadata.get(chave)
                if atual != esperado:
                    corresponde = False
                    break
            if corresponde:
                resultados.append(registro)
        return resultados

    def proximo_numero(self, tipo: str, ano: int | None = None) -> int:
        ano = ano or datetime.now(timezone.utc).year
        prefix = f"{tipo.upper()}-{ano}-"
        maior = 0
        for registro in self._iter_registros():
            if registro.id.startswith(prefix):
                try:
                    maior = max(maior, int(registro.id.rsplit("-", 1)[1]))
                except ValueError:
                    continue
        return maior + 1


def novo_registro(repo: RepositorioJSONL, tipo: str, titulo: str, conteudo: str = "", **kwargs: Any) -> Registro:
    rid = novo_id(tipo, repo.proximo_numero(tipo))
    now = agora()
    return Registro(id=rid, kind=tipo, title=titulo, created_at=now, updated_at=now, content=conteudo, **kwargs)


def slug(texto: str) -> str:
    texto = re.sub(r"[^\w\s-]", "", texto, flags=re.UNICODE).strip().lower()
    return re.sub(r"[-\s]+", "-", texto)[:100] or uuid.uuid4().hex[:8]
