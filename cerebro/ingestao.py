from __future__ import annotations

from dataclasses import dataclass, asdict
from email import policy
from email.parser import BytesParser
from pathlib import Path
from typing import Any
import csv
import hashlib
import html
import json
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET

from .nucleo import RepositorioJSONL, Registro, agora, hash_arquivo, novo_registro


@dataclass
class DocumentoEstruturado:
    nome: str
    formato: str
    tamanho: int
    sha256: str
    origem: str
    extraido_em: str
    texto: str
    estrutura: list[dict[str, Any]]
    metadados: dict[str, Any]
    erros: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _limpar(texto: str) -> str:
    texto = html.unescape(texto).replace("\r\n", "\n").replace("\r", "\n")
    return re.sub(r"[ \t]+", " ", texto).strip()


def _docx(path: Path) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    partes: list[str] = []
    estrutura: list[dict[str, Any]] = []
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
        for p in root.findall(".//w:body/w:p", ns):
            texto = _limpar("".join(t.text or "" for t in p.findall(".//w:t", ns)))
            if texto:
                estilo = p.find("w:pPr/w:pStyle", ns)
                nivel = estilo.get(f"{{{ns['w']}}}val") if estilo is not None else None
                partes.append(texto)
                estrutura.append({"tipo": "paragrafo", "texto": texto, "estilo": nivel})
        tabelas = root.findall(".//w:tbl", ns)
        for i, tabela in enumerate(tabelas, 1):
            linhas = []
            for tr in tabela.findall("w:tr", ns):
                linhas.append([_limpar("".join(t.text or "" for t in tc.findall(".//w:t", ns))) for tc in tr.findall("w:tc", ns)])
            estrutura.append({"tipo": "tabela", "indice": i, "linhas": linhas})
    return "\n".join(partes), estrutura, {"parser": "stdlib-docx-xml"}


def _html_mht(path: Path) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    raw = path.read_bytes()
    msg = BytesParser(policy=policy.default).parsebytes(raw)
    partes: list[str] = []
    estrutura: list[dict[str, Any]] = []
    for part in msg.walk():
        if part.get_content_type() in ("text/plain", "text/html"):
            try:
                texto = part.get_content()
            except Exception:
                continue
            if part.get_content_type() == "text/html":
                texto = re.sub(r"<[^>]+>", " ", texto)
            texto = _limpar(texto)
            if texto:
                partes.append(texto)
                estrutura.append({"tipo": part.get_content_type(), "texto": texto})
    return "\n".join(partes), estrutura, {"parser": "email-mime"}


def _json(path: Path) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    texto = json.dumps(data, ensure_ascii=False, indent=2)
    return texto, [{"tipo": "json", "valor": data}], {"parser": "json-stdlib"}


def _csv(path: Path) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    texto = "\n".join(" | ".join(row) for row in rows)
    return texto, [{"tipo": "linha", "indice": i + 1, "valores": row} for i, row in enumerate(rows)], {"parser": "csv-stdlib"}


def extrair(path: str | Path) -> DocumentoEstruturado:
    path = Path(path)
    ext = path.suffix.lower()
    erros: list[str] = []
    try:
        if ext == ".docx":
            texto, estrutura, meta = _docx(path)
            formato = "docx"
        elif ext in {".mht", ".mhtml", ".html", ".htm"}:
            texto, estrutura, meta = _html_mht(path)
            formato = ext.lstrip(".")
        elif ext == ".json":
            texto, estrutura, meta = _json(path)
            formato = "json"
        elif ext == ".csv":
            texto, estrutura, meta = _csv(path)
            formato = "csv"
        elif ext in {".txt", ".md"}:
            texto = path.read_text(encoding="utf-8")
            estrutura = [{"tipo": "texto", "texto": texto}]
            meta = {"parser": "utf8-stdlib"}
            formato = ext.lstrip(".")
        elif ext == ".pdf":
            try:
                from pypdf import PdfReader
                reader = PdfReader(str(path))
                paginas = [p.extract_text() or "" for p in reader.pages]
                texto = "\n\n".join(_limpar(p) for p in paginas)
                estrutura = [{"tipo": "pagina", "indice": i + 1, "texto": p} for i, p in enumerate(paginas)]
                meta = {"parser": "pypdf", "paginas": len(paginas)}
            except ImportError:
                raise RuntimeError("PDF requer a dependência opcional pypdf")
            formato = "pdf"
        else:
            raise ValueError(f"Formato não suportado na V0.1: {ext or '<sem extensão>'}")
    except Exception as exc:
        erros.append(str(exc))
        texto, estrutura, meta = "", [], {"parser": None}
        formato = ext.lstrip(".") or "desconhecido"
    return DocumentoEstruturado(path.name, formato, path.stat().st_size, hash_arquivo(path), str(path), agora(), texto, estrutura, meta, erros)


def registrar_fonte(repo: RepositorioJSONL, documento: DocumentoEstruturado) -> Registro:
    origem = Path(documento.origem)
    fonte_destino: str | None = None
    if origem.exists() and origem.is_file():
        fontes_dir = repo.root / "fontes"
        fontes_dir.mkdir(parents=True, exist_ok=True)
        destino = fontes_dir / f"{documento.sha256}{origem.suffix.lower()}"
        if not destino.exists():
            shutil.copy2(origem, destino)
        fonte_destino = str(destino)

    registro = novo_registro(
        repo, "DOCUMENTO", documento.nome, documento.texto,
        source=documento.origem,
        provenance={
            "tipo": "ingestao",
            "obtido_em": documento.extraido_em,
            "sha256": documento.sha256,
            "formato": documento.formato,
            "extrator": documento.metadados.get("parser"),
            "erros": documento.erros,
            "fonte_original_preservada": fonte_destino is not None,
            "copia_original": fonte_destino,
        },
        metadata={"tamanho": documento.tamanho, "estrutura": documento.estrutura, **documento.metadados},
    )
    repo.salvar(registro)
    return registro
