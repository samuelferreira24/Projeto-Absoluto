from __future__ import annotations
"""ABS V3 adaptive control plane: cost, capacity and intelligence admission."""
import os, resource as _resource, threading, time
from dataclasses import dataclass
from enum import Enum
from typing import Any
from .v2 import ABSV2Orchestrator

class CostClass(str, Enum):
    FREE_LOCAL="free_local"; FREE_EXTERNAL="free_external"; SUBSCRIPTION="subscription"; PAID_API="paid_api"
class CostPolicy(str, Enum):
    FREE_ONLY="free_only"; FREE_FIRST="free_first"; PAID_ALLOWED="paid_allowed"
class CapacityState(str, Enum):
    HEALTHY="healthy"; PRESSURE="pressure"; CRITICAL="critical"

@dataclass(frozen=True)
class CapacitySnapshot:
    cpu_count:int; load_ratio:float; rss_bytes:int; available_bytes:int|None; state:CapacityState; timestamp:float
@dataclass(frozen=True)
class CostBudget:
    max_spend:float=0.0; spent:float=0.0; currency:str="USD"
    @property
    def remaining(self): return max(0.0,self.max_spend-self.spent)
@dataclass(frozen=True)
class IntelligenceCandidate:
    id:str; cost_class:CostClass; capabilities:tuple[str,...]=(); estimated_cost:float=0.0
    healthy:bool=True; latency_ms:float=0.0; local:bool=False
@dataclass(frozen=True)
class V3Decision:
    allowed:bool; candidate_id:str|None; cost_class:CostClass|None; reason:str
    capacity:CapacitySnapshot; policy:CostPolicy

class CapacityGovernor:
    def __init__(self,pressure_ratio=.80,critical_ratio=.95):
        self.pressure_ratio=pressure_ratio; self.critical_ratio=critical_ratio; self._lock=threading.RLock()
    def snapshot(self):
        cpu=max(1,os.cpu_count() or 1)
        try: load=os.getloadavg()[0]/cpu
        except (AttributeError,OSError): load=0.0
        rss=int(_resource.getrusage(_resource.RUSAGE_SELF).ru_maxrss)*(1024 if os.name=="linux" else 1)
        avail=None
        try:
            mem={}
            with open("/proc/meminfo",encoding="utf-8") as f:
                for line in f:
                    k,v=line.split(":",1)
                    if k in {"MemAvailable","MemTotal"}: mem[k]=int(v.strip().split()[0])*1024
            total=mem.get("MemTotal"); avail=mem.get("MemAvailable")
            if total and avail is not None: load=max(load,1-avail/total)
        except (OSError,ValueError): pass
        state=CapacityState.CRITICAL if load>=self.critical_ratio else CapacityState.PRESSURE if load>=self.pressure_ratio else CapacityState.HEALTHY
        return CapacitySnapshot(cpu,round(load,4),rss,avail,state,time.time())
    def admission(self,priority="normal"):
        snap=self.snapshot()
        if snap.state is CapacityState.CRITICAL and priority not in {"critical","recovery"}: raise RuntimeError("v3_capacity_critical")
        return snap

class CostPolicyEngine:
    def __init__(self,default_policy=CostPolicy.FREE_FIRST): self.default_policy=default_policy
    def policy(self,context):
        raw=str(context.get("cost_policy") or os.getenv("ABS_COST_POLICY") or self.default_policy.value).lower()
        try: return CostPolicy(raw)
        except ValueError: raise ValueError("invalid_cost_policy")
    def admissible(self,candidate,policy,budget):
        if not candidate.healthy: return False
        if candidate.cost_class is CostClass.PAID_API: return policy is CostPolicy.PAID_ALLOWED and candidate.estimated_cost<=budget.remaining
        if candidate.cost_class is CostClass.SUBSCRIPTION: return policy in {CostPolicy.FREE_FIRST,CostPolicy.PAID_ALLOWED}
        return True

class IntelligenceSelector:
    def rank(self,candidates,policy,budget,required=None):
        required=required or set(); engine=CostPolicyEngine()
        eligible=[c for c in candidates if required.issubset(set(c.capabilities)) and engine.admissible(c,policy,budget)]
        order={CostClass.FREE_LOCAL:0,CostClass.FREE_EXTERNAL:1,CostClass.SUBSCRIPTION:2,CostClass.PAID_API:3}
        return sorted(eligible,key=lambda c:(order[c.cost_class],0 if c.local else 1,c.estimated_cost,c.latency_ms,c.id))

class ABSV3Orchestrator(ABSV2Orchestrator):
    version="v3"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs); self.capacity=CapacityGovernor(); self.cost_policy=CostPolicyEngine(); self.intelligence_selector=IntelligenceSelector()
    def status(self):
        s=self.capacity.snapshot()
        return {"version":"v3","capacity":{"state":s.state.value,"load_ratio":s.load_ratio,"cpu_count":s.cpu_count,"rss_bytes":s.rss_bytes,"available_bytes":s.available_bytes},"cost_policy_default":self.cost_policy.default_policy.value}
    def _candidate(self,cap):
        meta=getattr(cap,"metadata",{}) or {}; kind=str(getattr(cap,"kind","")).lower(); raw=str(meta.get("cost_class") or "").lower()
        if not raw: raw=CostClass.FREE_LOCAL.value if kind=="local_ai" or "local" in kind else CostClass.PAID_API.value if "api" in kind or kind=="external_ai" else CostClass.FREE_EXTERNAL.value
        try: cc=CostClass(raw)
        except ValueError: cc=CostClass.FREE_EXTERNAL
        return IntelligenceCandidate(cap.id,cc,tuple(meta.get("capabilities") or ()),float(meta.get("estimated_cost",0) or 0),True,float(meta.get("latency_ms",0) or 0),cc is CostClass.FREE_LOCAL)
    def _gate(self,work,context):
        policy=self.cost_policy.policy(context); budget=CostBudget(float(context.get("max_spend",os.getenv("ABS_MAX_SPEND","0")) or 0),float(context.get("spent",0) or 0))
        snap=self.capacity.admission(str(context.get("priority") or "normal")); required=set(context.get("required_capabilities") or ())
        caps=self.registry.list()
        ai_caps=[c for c in caps if str(getattr(c,"kind","")).lower() in {"local_ai","external_ai"} or "ai" in str(getattr(c,"kind","")).lower()]
        # Explicit non-AI capabilities (echo, github, http, etc.) remain V2-compatible.
        explicit=str(context.get("capability_id") or "")
        if explicit:
            try:
                cap=self.registry.get(explicit)
                if cap not in ai_caps:
                    return V3Decision(True, explicit, CostClass.FREE_EXTERNAL, "explicit_non_ai_capability", snap, policy)
            except KeyError:
                pass
        candidates=[self._candidate(c) for c in ai_caps]
        ranked=self.intelligence_selector.rank(candidates,policy,budget,required)
        preferred=str(context.get("intelligence_id") or context.get("capability_id") or "")
        if preferred: ranked=sorted(ranked,key=lambda c:(0 if c.id==preferred else 1,c.estimated_cost,c.latency_ms))
        if not ranked: return V3Decision(False,None,None,"no_admissible_intelligence",snap,policy)
        c=ranked[0]; return V3Decision(True,c.id,c.cost_class,"admitted",snap,policy)
    def run(self,work_id,capability_id=None,approved=False):
        work=self.store.load(work_id); context=dict(work.context)
        if capability_id: context["capability_id"]=capability_id
        decision=self._gate(work,context)
        if not decision.allowed:
            work.context["_v3"]={"status":"waiting_resource","reason":decision.reason,"cost_policy":decision.policy.value,"capacity":decision.capacity.state.value}; self.store.save(work); return work
        work.context["_v3"]={"status":"admitted","selected_intelligence":decision.candidate_id,"cost_class":decision.cost_class.value if decision.cost_class else None,"cost_policy":decision.policy.value,"capacity_state":decision.capacity.state.value}
        self.store.save(work)
        return super().run(work_id,decision.candidate_id,approved=approved)
