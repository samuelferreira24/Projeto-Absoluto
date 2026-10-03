from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Conflict:
    kind: str
    field: str
    values: tuple[Any,...]
    sources: tuple[str,...]
    severity: str = "warning"

class ConflictDetector:
    """Detects explicit disagreements; it does not decide which source is correct."""
    def detect(self, claims:list[dict[str,Any]])->list[Conflict]:
        grouped:dict[str,list[dict[str,Any]]]={}
        for claim in claims:
            field=str(claim.get("field","")).strip()
            if field: grouped.setdefault(field,[]).append(claim)
        found=[]
        for field,items in grouped.items():
            values=[]
            sources=[]
            for item in items:
                value=item.get("value")
                if value not in values: values.append(value)
                sources.append(str(item.get("source","unknown")))
            if len(values)>1:
                found.append(Conflict("value_disagreement",field,tuple(values),tuple(sources)))
        return found
