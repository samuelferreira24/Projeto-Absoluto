from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Transport:
    id:str; type:str; reach:str; connected:bool=True; cost:float=0.0; energy:float=0.0; bandwidth:float|None=None; latency:float|None=None; internet_required:bool=False; bidirectional:bool=True; metadata:dict[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        if not self.id or not self.type or not self.reach: raise ValueError("id, type and reach are required")
        if self.cost<0 or self.energy<0: raise ValueError("cost and energy cannot be negative")

def viable(transports:list[Transport], *, require_internet=False, require_bidirectional=False):
    return [t for t in transports if t.connected and (not require_internet or t.internet_required) and (not require_bidirectional or t.bidirectional)]

def select(transports:list[Transport], **kwargs):
    candidates=viable(transports,**kwargs)
    return min(candidates,key=lambda t:(t.cost+t.energy,t.latency if t.latency is not None else 999999,-(t.bandwidth or 0))) if candidates else None
