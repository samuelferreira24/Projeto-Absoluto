"""Contrato mínimo e executável para a camada de ingestão do Cérebro V0.1.

A implementação é agnóstica ao formato. Adaptadores futuros devem produzir
uma representação intermediária compatível com este contrato sem substituir
a fonte original.
"""

from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from typing import Any


SUPPORTED_FORMATS = {
    ".docx": "DOCX",
    ".pdf": "PDF",
    ".mht": "MHT",
    ".mhtml": "MHT",
    ".html": "HTML",
    ".htm": "HTML",
    ".txt": "TXT",
    ".md": "MARKDOWN",
    ".json": "JSON",
    ".csv": "CSV",
}


@dataclass(frozen=True)
class SourceIdentity:
    """Identity and integrity metadata for an input source."""

    name: str
    format: str
    size_bytes: int
    sha256: str


@dataclass
class IntermediateDocument:
    """Format-neutral representation produced by an ingestion adapter."""

    source: SourceIdentity
    text: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    structure: list[dict[str, Any]] = field(default_factory=list)
    provenance: list[dict[str, Any]] = field(default_factory=list)


def identify_format(path: str | Path) -> str:
    """Return the normalized format name for a supported file extension."""
    suffix = Path(path).suffix.lower()
    try:
        return SUPPORTED_FORMATS[suffix]
    except KeyError as exc:
        raise ValueError(f"Formato não suportado: {suffix or '<sem extensão>'}") from exc


def fingerprint_source(path: str | Path) -> SourceIdentity:
    """Calculate stable source metadata without modifying the source file."""
    source_path = Path(path)
    digest = sha256()
    with source_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return SourceIdentity(
        name=source_path.name,
        format=identify_format(source_path),
        size_bytes=source_path.stat().st_size,
        sha256=digest.hexdigest(),
    )
