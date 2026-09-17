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

    def salvar(self, registro: Registro) -> None:
        path = self._path(registro)
        with path.open("a", encoding="utf-8") as f:
            f.write(registro.to_json().replace("\n", " ") + "\n")
        historico = self.root / "historico" / f"{registro.id}.jsonl"
        with historico.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"at": agora(), "version": registro.version, "record": registro.to_dict()}, ensure_ascii=False) + "\n")

    def buscar(self, texto: str) -> list[Registro]:
        termo = texto.casefold()
        encontrados: list[Registro] = []
        for path in (self.root / "registros").glob("*.jsonl"):
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                data = json.loads(line)
                if termo in json.dumps(data, ensure_ascii=False).casefold():
                    encontrados.append(Registro(**data))
        return encontrados

    def proximo_numero(self, tipo: str, ano: int | None = None) -> int:
        ano = ano or datetime.now(timezone.utc).year
        prefix = f"{tipo.upper()}-{ano}-"
        maior = 0
        for path in (self.root / "registros").glob("*.jsonl"):
            for line in path.read_text(encoding="utf-8").splitlines():
                try:
                    rid = json.loads(line).get("id", "")
                    if rid.startswith(prefix):
                        maior = max(maior, int(rid.rsplit("-", 1)[1]))
                except (ValueError, json.JSONDecodeError):
                    continue
        return maior + 1


def novo_registro(repo: RepositorioJSONL, tipo: str, titulo: str, conteudo: str = "", **kwargs: Any) -> Registro:
    rid = novo_id(tipo, repo.proximo_numero(tipo))
    now = agora()
    return Registro(id=rid, kind=tipo, title=titulo, created_at=now, updated_at=now, content=conteudo, **kwargs)


def slug(texto: str) -> str:
    texto = re.sub(r"[^\w\s-]", "", texto, flags=re.UNICODE).strip().lower()
    return re.sub(r"[-\s]+", "-", texto)[:100] or uuid.uuid4().hex[:8]
