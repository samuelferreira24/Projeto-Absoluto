from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from collections import Counter
from email import policy
from email.parser import BytesParser
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET


EXTENSOES_TEXTO = {".txt", ".md", ".json", ".csv", ".html", ".htm", ".mht", ".mhtml"}
EXTENSOES_DOC = {".docx"}
EXTENSOES_PDF = {".pdf"}
PALAVRAS_CHAVE = {
    "capacidade": r"\b(?:capacidade|capaz|pode|deve ser capaz|habilidade)\b",
    "requisito": r"\b(?:requisito|necessário|necessidade|obrigat[oó]rio)\b",
    "arquitetura": r"\b(?:arquitetura|estrutura|componente|m[oó]dulo|sistema)\b",
    "memoria": r"\b(?:mem[oó]ria|c[eé]rebro|hist[oó]rico|contexto)\b",
    "automacao": r"\b(?:automa[cç][aã]o|autom[aá]tico|automaticamente|24/?7)\b",
    "aprendizado": r"\b(?:aprendizado|aprendizagem|li[cç][aã]o|sabedoria|experi[eê]ncia)\b",
    "integracao": r"\b(?:integra[cç][aã]o|API|MCP|conector|plataforma|interface)\b",
    "planejamento": r"\b(?:planejamento|plano|objetivo|estrat[eé]gia|evolu[cç][aã]o)\b",
}


@dataclass(frozen=True)
class DocumentoAnalisado:
    path: str
    formato: str
    tamanho: int
    sha256: str
    caracteres: int
    palavras: int
    secoes: int
    sinais: dict[str, int]
    erros: tuple[str, ...] = ()


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for bloco in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloco)
    return h.hexdigest()


def extrair_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragrafos = []
    for p in root.findall(".//w:p", ns):
        texto = "".join(t.text or "" for t in p.findall(".//w:t", ns)).strip()
        if texto:
            paragrafos.append(texto)
    return "\n".join(paragrafos)


def extrair_mht(path: Path) -> str:
    with path.open("rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)
    partes = []
    for part in msg.walk():
        if part.get_content_type() in {"text/plain", "text/html"}:
            try:
                partes.append(part.get_content())
            except Exception:
                continue
    return "\n".join(partes)


def extrair_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("pypdf não instalado") from exc
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extrair_texto(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".docx":
        return extrair_docx(path)
    if ext in {".mht", ".mhtml"}:
        return extrair_mht(path)
    if ext == ".pdf":
        return extrair_pdf(path)
    if ext in {".txt", ".md", ".json", ".csv", ".html", ".htm"}:
        return path.read_text(encoding="utf-8", errors="replace")
    raise ValueError(f"formato não suportado: {ext}")


def _secoes(texto: str) -> int:
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    return sum(bool(re.match(r"^(?:#{1,6}\s+|\d+(?:\.\d+)*[.)]?\s+|[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][^.!?]{2,80}:$)", l)) for l in linhas)


def analisar_arquivo(path: Path, raiz: Path | None = None) -> DocumentoAnalisado:
    erros: list[str] = []
    try:
        texto = extrair_texto(path)
    except Exception as exc:
        texto = ""
        erros.append(f"extração: {exc}")
    sinais = {nome: len(re.findall(padrao, texto, flags=re.IGNORECASE)) for nome, padrao in PALAVRAS_CHAVE.items()}
    relativo = str(path.relative_to(raiz)) if raiz else str(path)
    return DocumentoAnalisado(
        path=relativo,
        formato=path.suffix.lower() or "sem_extensão",
        tamanho=path.stat().st_size,
        sha256=_sha256(path),
        caracteres=len(texto),
        palavras=len(re.findall(r"\b\w+\b", texto, flags=re.UNICODE)),
        secoes=_secoes(texto),
        sinais=sinais,
        erros=tuple(erros),
    )


def analisar_diretorio(root: str | Path) -> dict:
    raiz = Path(root)
    documentos: list[DocumentoAnalisado] = []
    for path in sorted(raiz.rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        if path.suffix.lower() not in EXTENSOES_TEXTO | EXTENSOES_DOC | EXTENSOES_PDF:
            continue
        documentos.append(analisar_arquivo(path, raiz))

    formatos = Counter(d.formato for d in documentos)
    sinais = Counter()
    for d in documentos:
        sinais.update(d.sinais)
    erros = [asdict(d) for d in documentos if d.erros]
    return {
        "schema_version": "0.1",
        "raiz": str(raiz),
        "quantidade_documentos": len(documentos),
        "formatos": dict(formatos),
        "total_caracteres": sum(d.caracteres for d in documentos),
        "total_palavras": sum(d.palavras for d in documentos),
        "sinais_globais": dict(sinais),
        "documentos": [asdict(d) for d in documentos],
        "erros_extracao": erros,
    }


def salvar_relatorio(root: str | Path, destino: str | Path) -> dict:
    resultado = analisar_diretorio(root)
    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)
    destino_path.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return resultado
