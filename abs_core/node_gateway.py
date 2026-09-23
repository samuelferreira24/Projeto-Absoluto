from __future__ import annotations
from dataclasses import dataclass, field
from queue import Empty, Queue
from threading import Lock
from typing import Any
import time, uuid

@dataclass
class NodeWork:
    id:str
    capability:str
    payload:dict[str,Any]
    created_at:float=field(default_factory=time.time)

class NodeGateway:
    """Transport-neutral queue for work delegated to an independent ABS node."""
    def __init__(self,registry=None): self.registry=registry; self._queue=Queue(); self._results={}; self._lock=Lock()
    def enqueue(self,capability,payload=None,work_id=None):
        work=NodeWork(work_id or f"node-{uuid.uuid4().hex}",capability,payload or {})
        with self._lock: self._results.pop(work.id,None)
        self._queue.put(work); return work
    def next(self,timeout=0):
        try:return self._queue.get(timeout=max(0.0,timeout))
        except Empty:return None
    def complete(self,work_id,*,success,result=None,error=None):
        with self._lock:self._results[work_id]={"id":work_id,"success":success,"result":result,"error":error,"completed_at":time.time()}
    def result(self,work_id):
        with self._lock:return self._results.get(work_id)
