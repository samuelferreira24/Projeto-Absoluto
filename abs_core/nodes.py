from __future__ import annotations
from dataclasses import asdict, dataclass, field
from pathlib import Path
from threading import Lock
from typing import Any
import json, time

@dataclass
class ABSNode:
    id: str
    name: str
    environment: str = "unknown"
    capabilities: tuple[str, ...] = ()
    endpoint: str | None = None
    active: bool = True
    last_heartbeat: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)
    def heartbeat(self) -> None:
        self.last_heartbeat=time.time(); self.active=True
    def to_dict(self):
        d=asdict(self); d["capabilities"]=list(self.capabilities); return d

class NodeRegistry:
    """Portable identity/presence registry for independent ABS nodes."""
    def __init__(self,path: str|Path):
        self.path=Path(path); self._lock=Lock(); self._nodes={}; self._load()
    def _load(self):
        if not self.path.exists(): return
        try: data=json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError,json.JSONDecodeError): return
        for x in data if isinstance(data,list) else []:
            try:
                n=ABSNode(id=str(x["id"]),name=str(x.get("name",x["id"])),environment=str(x.get("environment","unknown")),capabilities=tuple(x.get("capabilities",[])),endpoint=x.get("endpoint"),active=bool(x.get("active",True)),last_heartbeat=float(x.get("last_heartbeat",time.time())),metadata=dict(x.get("metadata",{})))
                self._nodes[n.id]=n
            except (KeyError,TypeError,ValueError): pass
    def _save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True); tmp=self.path.with_suffix(self.path.suffix+".tmp"); tmp.write_text(json.dumps([n.to_dict() for n in self._nodes.values()],ensure_ascii=False,indent=2),encoding="utf-8"); tmp.replace(self.path)
    def register(self,node: ABSNode):
        with self._lock: self._nodes[node.id]=node; self._save()
        return node
    def heartbeat(self,node_id:str)->bool:
        with self._lock:
            n=self._nodes.get(node_id)
            if not n:return False
            n.heartbeat(); self._save(); return True
    def list(self,active:bool|None=None):
        with self._lock: nodes=list(self._nodes.values())
        return nodes if active is None else [n for n in nodes if n.active==active]
    def by_capability(self,capability:str): return [n for n in self.list(True) if capability in n.capabilities]
