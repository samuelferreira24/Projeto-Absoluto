from __future__ import annotations
from dataclasses import asdict,dataclass,field
from threading import RLock
from typing import Any

@dataclass
class AgentRecord:
    id:str
    name:str
    responsibility:str
    policy:str
    model_refs:list[str]=field(default_factory=list)
    tool_refs:list[str]=field(default_factory=list)
    status:str="registered"
    metadata:dict[str,Any]=field(default_factory=dict)

class AgentRegistry:
    """Identity registry only: registering an agent grants no authority or execution rights."""
    def __init__(self)->None:
        self._lock=RLock(); self._items:dict[str,AgentRecord]={}

    def register(self,agent:AgentRecord)->AgentRecord:
        if not agent.id: raise ValueError("agent_id_required")
        if not agent.responsibility: raise ValueError("agent_responsibility_required")
        if not agent.policy: raise ValueError("agent_policy_required")
        with self._lock:
            if agent.id in self._items: raise ValueError(f"Agent already registered: {agent.id}")
            self._items[agent.id]=agent
            return AgentRecord(**asdict(agent))

    def get(self,agent_id:str)->AgentRecord:
        with self._lock: return AgentRecord(**asdict(self._items[agent_id]))

    def list(self)->list[AgentRecord]:
        with self._lock: return [AgentRecord(**asdict(x)) for x in self._items.values()]
