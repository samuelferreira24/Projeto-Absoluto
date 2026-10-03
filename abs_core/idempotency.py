from __future__ import annotations
from dataclasses import dataclass
from threading import RLock
from typing import Any

@dataclass(frozen=True)
class IdempotencyRecord:
    key: str
    status: str
    result: Any = None

class IdempotencyLedger:
    """In-memory V1 deduplication boundary; persistence can be supplied by a durable store later."""
    def __init__(self) -> None:
        self._lock=RLock()
        self._items: dict[str,IdempotencyRecord]={}

    def get(self,key:str)->IdempotencyRecord|None:
        with self._lock: return self._items.get(key)

    def reserve(self,key:str)->IdempotencyRecord:
        if not key: raise ValueError("idempotency_key_required")
        with self._lock:
            existing=self._items.get(key)
            if existing is not None: return existing
            item=IdempotencyRecord(key,"reserved")
            self._items[key]=item
            return item

    def complete(self,key:str,result:Any=None)->IdempotencyRecord:
        with self._lock:
            if key not in self._items: raise KeyError(key)
            item=IdempotencyRecord(key,"completed",result)
            self._items[key]=item
            return item

    def fail(self,key:str,result:Any=None)->IdempotencyRecord:
        with self._lock:
            if key not in self._items: raise KeyError(key)
            item=IdempotencyRecord(key,"failed",result)
            self._items[key]=item
            return item
