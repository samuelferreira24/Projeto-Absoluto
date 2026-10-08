from __future__ import annotations
"""ABS V3 — integrated adaptive control plane.

The ABS owns authority, policy, admission, scheduling, verification and
recovery. Providers/executors are replaceable capabilities.
"""

import json, os, resource as _resource, threading, time, uuid, sqlite3, urllib.request, urllib.error
from collections import deque
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Callable

from .v2 import ABSV2Orchestrator

class CostClass(str, Enum):
    FREE_LOCAL="free_local"; FREE_EXTERNAL="free_external"; SUBSCRIPTION="subscription"; PAID_API="paid_api"
class CostPolicy(str, Enum):
    FREE_ONLY="free_only"; FREE_FIRST="free_first"; PAID_ALLOWED="paid_allowed"
class CapacityState(str, Enum):
    HEALTHY="healthy"; PRESSURE="pressure"; CRITICAL="critical"
class WorkDisposition(str, Enum):
    EXECUTE="execute"; WAIT="wait"; DEGRADE="degrade"; REPLAN="replan"; RECONCILE="reconcile"; DENY="deny"

@dataclass(frozen=True)
class CapacitySnapshot:
    cpu_count:int; load_ratio:float; rss_bytes:int; available_bytes:int|None
    total_bytes:int|None; state:CapacityState; concurrency:int; timestamp:float

@dataclass(frozen=True)
class CostBudget:
    max_spend:float=0.0; spent:float=0.0; currency:str="USD"
    @property
    def remaining(self): return max(0.0,self.max_spend-self.spent)

@dataclass
class IntelligenceCandidate:
    id:str; cost_class:CostClass; capabilities:tuple[str,...]=()
    estimated_cost:float=0.0; healthy:bool=True; latency_ms:float=0.0
    local:bool=False; quality:float=0.5; context_window:int=0

@dataclass(frozen=True)
class V3Decision:
    disposition:WorkDisposition; candidate_id:str|None; cost_class:CostClass|None
    reason:str; capacity:CapacitySnapshot; policy:CostPolicy

class V3StateStore:
    """Small durable control-plane store. PostgreSQL can replace it without changing contracts."""
    def __init__(self, path:str):
        self.path=path
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        self._lock=threading.RLock()
        self.db=sqlite3.connect(path,check_same_thread=False)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS v3_events(
          id TEXT PRIMARY KEY, work_id TEXT, kind TEXT, payload TEXT, ts REAL);
        CREATE TABLE IF NOT EXISTS v3_cost(
          id INTEGER PRIMARY KEY AUTOINCREMENT, work_id TEXT, candidate TEXT,
          cost_class TEXT, amount REAL, currency TEXT, ts REAL);
        CREATE TABLE IF NOT EXISTS v3_capacity(
          id INTEGER PRIMARY KEY AUTOINCREMENT, load REAL, available INTEGER,
          concurrency INTEGER, state TEXT, ts REAL);
        CREATE TABLE IF NOT EXISTS v3_learning(
          key TEXT PRIMARY KEY, attempts INTEGER, successes INTEGER,
          failures INTEGER, latency_sum REAL, updated REAL);
        """)
        self.db.commit()
    def event(self,work_id,kind,payload):
        with self._lock:
            self.db.execute("INSERT INTO v3_events VALUES(?,?,?,?,?)",
                            (str(uuid.uuid4()),work_id,kind,json.dumps(payload,default=str),time.time()))
            self.db.commit()
    def cost(self,work_id,candidate,cost_class,amount,currency="USD"):
        with self._lock:
            self.db.execute("INSERT INTO v3_cost(work_id,candidate,cost_class,amount,currency,ts) VALUES(?,?,?,?,?,?)",
                            (work_id,candidate,cost_class.value,amount,currency,time.time()))
            self.db.commit()
    def capacity(self,s):
        with self._lock:
            self.db.execute("INSERT INTO v3_capacity(load,available,concurrency,state,ts) VALUES(?,?,?,?,?)",
                            (s.load_ratio,s.available_bytes,s.concurrency,s.state.value,s.timestamp))
            self.db.commit()
    def learning(self,key):
        with self._lock:
            row=self.db.execute("SELECT attempts,successes,failures,latency_sum FROM v3_learning WHERE key=?",(key,)).fetchone()
            if not row: return {}
            a,ok,fail,total=row
            return {"attempts":a,"successes":ok,"failures":fail,"latency_avg":(total/a if a else 0.0)}

    def all_learning(self):
        with self._lock:
            rows=self.db.execute("SELECT key,attempts,successes,failures,latency_sum FROM v3_learning").fetchall()
            return {k:{"attempts":a,"successes":ok,"failures":fail,"latency_avg":(total/a if a else 0.0)} for k,a,ok,fail,total in rows}

    def learn(self,key,success,latency):
        with self._lock:
            row=self.db.execute("SELECT attempts,successes,failures,latency_sum FROM v3_learning WHERE key=?",(key,)).fetchone()
            a,ok,fail,total=row or (0,0,0,0.0)
            a+=1; ok+=int(success); fail+=int(not success); total+=latency
            self.db.execute("INSERT OR REPLACE INTO v3_learning VALUES(?,?,?,?,?,?)",
                            (key,a,ok,fail,total,time.time()))
            self.db.commit()

class CapacityGovernor:
    def __init__(self,pressure_ratio=.80,critical_ratio=.95,base_concurrency=2,max_concurrency=8):
        self.pressure_ratio=pressure_ratio; self.critical_ratio=critical_ratio
        self.base_concurrency=base_concurrency; self.max_concurrency=max_concurrency
        self._lock=threading.RLock()
    def snapshot(self,queue_depth=0):
        cpu=max(1,os.cpu_count() or 1)
        try: cpu_load=max(0.0,os.getloadavg()[0]/cpu)
        except (AttributeError,OSError): cpu_load=0.0
        rss=int(_resource.getrusage(_resource.RUSAGE_SELF).ru_maxrss)*(1024 if os.name=="linux" else 1)
        avail=total=None
        try:
            mem={}
            with open("/proc/meminfo",encoding="utf-8") as f:
                for line in f:
                    k,v=line.split(":",1)
                    if k in {"MemAvailable","MemTotal"}: mem[k]=int(v.strip().split()[0])*1024
            total=mem.get("MemTotal"); avail=mem.get("MemAvailable")
            mem_load=(1-avail/total) if total and avail is not None else 0
        except (OSError,ValueError): mem_load=0
        load=max(cpu_load,mem_load)
        state=CapacityState.CRITICAL if load>=self.critical_ratio else CapacityState.PRESSURE if load>=self.pressure_ratio else CapacityState.HEALTHY
        ratio=max(0.1,1.0-load)
        concurrency=max(1,min(self.max_concurrency,int(round(self.base_concurrency+ratio*(self.max_concurrency-self.base_concurrency)))))
        if state is CapacityState.CRITICAL: concurrency=1
        if queue_depth and state is CapacityState.HEALTHY: concurrency=min(self.max_concurrency,concurrency+1)
        return CapacitySnapshot(cpu,round(load,4),rss,avail,total,state,concurrency,time.time())
    def admission(self,priority="normal",queue_depth=0):
        s=self.snapshot(queue_depth)
        if s.state is CapacityState.CRITICAL and priority not in {"critical","recovery"}:
            return s,False
        return s,True

class CostPolicyEngine:
    def __init__(self,default_policy=CostPolicy.FREE_FIRST): self.default_policy=default_policy
    def policy(self,context):
        raw=str(context.get("cost_policy") or os.getenv("ABS_COST_POLICY") or self.default_policy.value).lower()
        return CostPolicy(raw)
    def admissible(self,c,policy,budget):
        if not c.healthy: return False
        if c.cost_class is CostClass.PAID_API:
            return policy is CostPolicy.PAID_ALLOWED and c.estimated_cost>0 and c.estimated_cost<=budget.remaining
        if c.cost_class is CostClass.SUBSCRIPTION:
            return policy in {CostPolicy.FREE_FIRST,CostPolicy.PAID_ALLOWED}
        return True

class IntelligenceSelector:
    order={CostClass.FREE_LOCAL:0,CostClass.FREE_EXTERNAL:1,CostClass.SUBSCRIPTION:2,CostClass.PAID_API:3}
    def __init__(self,learning=None): self.learning=learning or {}
    def rank(self,candidates,policy,budget,required=None):
        required=required or set(); engine=CostPolicyEngine()
        eligible=[c for c in candidates if required.issubset(set(c.capabilities)) and engine.admissible(c,policy,budget)]
        def key(c):
            learned=self.learning.get(c.id,{})
            failure=learned.get("failures",0); success=learned.get("successes",0)
            reliability=(success+1)/(success+failure+2)
            return (self.order[c.cost_class],-reliability,-c.quality,0 if c.local else 1,c.estimated_cost,c.latency_ms,c.id)
        return sorted(eligible,key=key)

class AdmissionQueue:
    def __init__(self): self._q=deque(); self._lock=threading.RLock()
    def push(self,work_id,priority=0):
        with self._lock: self._q.append((-priority,time.time(),work_id))
    def pop(self):
        with self._lock:
            if not self._q:return None
            best=min(range(len(self._q)),key=lambda i:self._q[i][:2])
            item=self._q[best]
            del self._q[best]
            return item[2]
    def depth(self):
        with self._lock:return len(self._q)

class LlamaCppModelAdapter:
    """Adapter for llama-server router model load/unload lifecycle."""
    def __init__(self, endpoint: str):
        self.endpoint=endpoint.rstrip("/")
    def _post(self, path: str, model: str):
        data=json.dumps({"model":model}).encode()
        req=urllib.request.Request(self.endpoint+path,data=data,headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=10) as resp:
            return json.loads(resp.read().decode() or "{}")
    def load(self, model: str):
        result=self._post("/models/load",model)
        if result.get("success") is False: raise RuntimeError("llama_model_load_failed")
        return result
    def unload(self, model: str):
        result=self._post("/models/unload",model)
        if result.get("success") is False: raise RuntimeError("llama_model_unload_failed")
        return result

class ModelLifecycle:
    """Provider-neutral model lifecycle. llama.cpp/Ollama/vLLM adapters may attach here."""
    def __init__(self): self.models={}; self._lock=threading.RLock()
    def register(self,model_id,loader=None,unloader=None,metadata=None):
        with self._lock:self.models[model_id]={"loaded":False,"loader":loader,"unloader":unloader,"metadata":metadata or {}}
    def ensure_loaded(self,model_id):
        with self._lock:
            m=self.models.get(model_id)
            if not m:return False
            if m["loaded"]: return True
            if m["loader"]: m["loader"]()
            m["loaded"]=True
            return True
    def unload(self,model_id):
        with self._lock:
            m=self.models.get(model_id)
            if not m:return False
            if m["loaded"] and m["unloader"]: m["unloader"]()
            m["loaded"]=False; return True
    def status(self): return {k:{"loaded":v["loaded"],"metadata":v["metadata"]} for k,v in self.models.items()}

class Telemetry:
    def __init__(self): self._lock=threading.RLock(); self.counters={}; self.latencies={}
    def inc(self,key,n=1):
        with self._lock:self.counters[key]=self.counters.get(key,0)+n
    def observe(self,key,value):
        with self._lock:self.latencies[key]=self.latencies.get(key,[])[-99:]+[float(value)]
    def snapshot(self):
        with self._lock:return {"counters":dict(self.counters),"latencies":{k:list(v) for k,v in self.latencies.items()}}

class RecoveryManager:
    def __init__(self,state_store): self.state_store=state_store
    def reconcile(self,work):
        state_value=getattr(getattr(work,"state",None),"value",str(getattr(work,"state",None)))
        self.state_store.event(work.id,"recovery_reconcile",{"state":state_value,"result_present":work.result is not None})
        if state_value == "completed": return "completed"
        if state_value in {"failed","cancelled"}: return "resume_or_replan"
        return "resume_or_replan"

class ABSV3Orchestrator(ABSV2Orchestrator):
    version="v3"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        db_path=getattr(self.store,"path",None) or os.getenv("ABS_DB_PATH","abs.db")
        self.v3_state=V3StateStore(str(db_path))
        self.capacity=CapacityGovernor()
        self.cost_policy=CostPolicyEngine()
        self.selector=IntelligenceSelector(self.v3_state.all_learning())
        self.queue=AdmissionQueue()
        self.lifecycle=ModelLifecycle()
        self.llama_lifecycle = None
        llama_endpoint = os.getenv("ABS_LLAMA_CPP_ROUTER_URL", "").strip()
        if llama_endpoint:
            self.llama_lifecycle = LlamaCppModelAdapter(llama_endpoint)
            specs = os.getenv("ABS_LOCAL_AI_MODELS", "").strip()
            for raw in (specs.split(",") if specs else []):
                parts=[item.strip() for item in raw.split("|")]
                if len(parts)==3 and all(parts):
                    model_id, endpoint, model_name=parts
                    if endpoint.rstrip("/") == llama_endpoint.rstrip("/"):
                        self.lifecycle.register(model_id, loader=lambda m=model_name: self.llama_lifecycle.load(m), unloader=lambda m=model_name: self.llama_lifecycle.unload(m), metadata={"provider":"llama.cpp","model":model_name,"endpoint":llama_endpoint})
        self.telemetry=Telemetry()
        self.recovery=RecoveryManager(self.v3_state)
        self._v3_lock=threading.RLock()
        self._capacity_cv=threading.Condition(self._v3_lock)
        self._active=0
        self._ticket_seq=0
        self._tickets={}
    def status(self):
        s=self.capacity.snapshot(self.queue.depth()); self.v3_state.capacity(s)
        return {"version":"v3","capacity":asdict(s)|{"state":s.state.value},
                "cost_policy_default":self.cost_policy.default_policy.value,
                "queue_depth":self.queue.depth(),"active_executions":self._active,
                "models":self.lifecycle.status(),
                "telemetry":self.telemetry.snapshot()}
    def _acquire_slot(self,work_id,priority):
        with self._capacity_cv:
            self._ticket_seq += 1
            self._tickets[work_id] = (-int(priority), self._ticket_seq)
            while True:
                snap = self.capacity.snapshot(self.queue.depth())
                ordered = sorted(self._tickets.items(), key=lambda kv: kv[1])
                position = next((i for i,(wid,_) in enumerate(ordered) if wid == work_id), len(ordered))
                if position < max(1,snap.concurrency) and self._active < max(1,snap.concurrency):
                    self._active += 1
                    self._tickets.pop(work_id,None)
                    return snap
                self._capacity_cv.wait(timeout=0.25)

    def _release_slot(self):
        with self._capacity_cv:
            self._active = max(0,self._active-1)
            self._capacity_cv.notify_all()

    def _rerank_with_learning(self):
        self.selector.learning = self.v3_state.all_learning()

    def _replan_candidates(self,work,context,failed_id):
        self._rerank_with_learning()
        ai=[self._candidate(c) for c in self.registry.list() if "ai" in str(getattr(c,"kind","")).lower()]
        policy=self.cost_policy.policy(context)
        budget=CostBudget(float(context.get("max_spend",os.getenv("ABS_MAX_SPEND","0")) or 0),float(context.get("spent",0) or 0))
        return [c for c in self.selector.rank(ai,policy,budget,set(context.get("required_capabilities") or ())) if c.id != failed_id]

    def _candidate(self,cap):
        meta=getattr(cap,"metadata",{}) or {}; kind=str(getattr(cap,"kind","")).lower()
        raw=str(meta.get("cost_class") or "").lower()
        if kind == "local_ai" and not raw:
            raw = CostClass.FREE_LOCAL.value
        elif kind == "external_ai" and not raw:
            raw = CostClass.FREE_EXTERNAL.value
        if not raw:
            raw=CostClass.FREE_LOCAL.value if "local" in kind else CostClass.PAID_API.value if "ai" in kind else CostClass.FREE_EXTERNAL.value
        try:cc=CostClass(raw)
        except ValueError:cc=CostClass.FREE_EXTERNAL
        capabilities = tuple(meta.get("capabilities") or ())
        if not capabilities and kind == "local_ai":
            capabilities = ("chat", "reasoning")
        return IntelligenceCandidate(cap.id,cc,capabilities,float(meta.get("estimated_cost",0) or 0),True,float(meta.get("latency_ms",0) or 0),cc is CostClass.FREE_LOCAL,float(meta.get("quality",.5) or .5),int(meta.get("context_window",0) or 0))
    def _gate(self,work,context):
        priority=str(context.get("priority") or "normal")
        snap,allowed=self.capacity.admission(priority,self.queue.depth()); policy=self.cost_policy.policy(context)
        budget=CostBudget(float(context.get("max_spend",os.getenv("ABS_MAX_SPEND","0")) or 0),float(context.get("spent",0) or 0))
        if not allowed:return V3Decision(WorkDisposition.WAIT,None,None,"capacity_critical",snap,policy)
        explicit=str(context.get("capability_id") or "")
        if explicit:
            try:
                cap=self.registry.get(explicit)
                if "ai" not in str(getattr(cap,"kind","")).lower():
                    return V3Decision(WorkDisposition.EXECUTE,explicit,CostClass.FREE_EXTERNAL,"explicit_non_ai_capability",snap,policy)
                candidate=self._candidate(cap)
                if not self.cost_policy.admissible(candidate,policy,budget):
                    return V3Decision(WorkDisposition.WAIT,explicit,candidate.cost_class,"explicit_intelligence_not_admissible",snap,policy)
                return V3Decision(WorkDisposition.EXECUTE,explicit,candidate.cost_class,"explicit_intelligence",snap,policy)
            except KeyError:
                return V3Decision(WorkDisposition.DENY,explicit,None,"unknown_capability",snap,policy)
        ai=[self._candidate(c) for c in self.registry.list() if "ai" in str(getattr(c,"kind","")).lower()]
        ranked=self.selector.rank(ai,policy,budget,set(context.get("required_capabilities") or ()))
        preferred=str(context.get("intelligence_id") or "")
        if preferred:
            preferred_capability = preferred.split(":",1)[1] if preferred.startswith("intelligence:") else preferred
            ranked=sorted(ranked,key=lambda c:(0 if c.id==preferred_capability else 1,c.estimated_cost,c.latency_ms))
        if not ranked:return V3Decision(WorkDisposition.WAIT,None,None,"no_admissible_intelligence",snap,policy)
        c=ranked[0]; return V3Decision(WorkDisposition.EXECUTE,c.id,c.cost_class,"admitted",snap,policy)
    def run(self,work_id,capability_id=None,approved=False):
        start=time.time()
        work=self.store.load(work_id)
        context=dict(work.context)
        if capability_id:
            context["capability_id"]=capability_id
        if getattr(getattr(work,"state",None),"value",None) == "completed":
            self.recovery.reconcile(work)
            return work
        priority=str(context.get("priority") or "normal")
        self._acquire_slot(work_id,10 if priority=="critical" else 0)
        try:
            with self._v3_lock:
                work=self.store.load(work_id)
                context=dict(work.context)
                if capability_id:
                    context["capability_id"]=capability_id
                if getattr(getattr(work,"state",None),"value",None) == "completed":
                    self.recovery.reconcile(work)
                    return work
                decision=self._gate(work,context)
                self.v3_state.event(work_id,"decision",asdict(decision)|{
                    "disposition":decision.disposition.value,
                    "cost_class":decision.cost_class.value if decision.cost_class else None,
                    "policy":decision.policy.value})
                if decision.disposition is WorkDisposition.DENY:
                    work.context["_v3"]={"status":"denied","reason":decision.reason,"policy":decision.policy.value}
                    work.result={"type":"v3_policy_error","error":decision.reason}
                    self.telemetry.inc("denied")
                    self.store.save(work)
                    return work
                if decision.disposition is WorkDisposition.WAIT:
                    self.queue.push(work_id,10 if priority=="critical" else 0)
                    work.context["_v3"]={"status":"waiting","reason":decision.reason,"policy":decision.policy.value}
                    self.store.save(work)
                    self.telemetry.inc("wait")
                    return work
                work.context["_v3"]={
                    "status":"admitted",
                    "selected_intelligence":decision.candidate_id,
                    "cost_class":decision.cost_class.value if decision.cost_class else None,
                    "cost_policy":decision.policy.value,
                    "capacity_state":decision.capacity.state.value,
                    "queue_depth":self.queue.depth(),
                    "active":self._active}
                self.store.save(work)
                candidate_id=decision.candidate_id
            attempts=0
            while True:
                attempts+=1
                execution_start=time.time()
                try:
                    result=super().run(work_id,candidate_id,approved=approved)
                    elapsed=time.time()-execution_start
                    # A result payload alone is not proof of success. The V2/V1
                    # verification state is authoritative for learning and
                    # future routing decisions.
                    state_value=getattr(getattr(result,"state",None),"value",None)
                    success=state_value == "completed"
                    self.telemetry.inc("completed" if success else "failed")
                    self.telemetry.observe("work_seconds",elapsed)
                    amount=float(context.get("estimated_cost",0) or 0) if decision.cost_class is CostClass.PAID_API else 0.0
                    if decision.cost_class:
                        self.v3_state.cost(work_id,candidate_id or "",decision.cost_class,amount)
                    self.v3_state.learn(candidate_id or "unknown",success,elapsed)
                    self._rerank_with_learning()

                    # A verified failure is evidence too. Replan on the observed
                    # Work state, not only on thrown exceptions, and never reuse
                    # the failed intelligence in the same bounded recovery loop.
                    if not success:
                        self.v3_state.event(work_id,"verification_failure",{
                            "candidate":candidate_id,"state":state_value,
                            "result":getattr(result,"result",None),"attempt":attempts})
                        alternatives=self._replan_candidates(work,context,candidate_id)
                        max_replans=max(0,min(int(context.get("max_replans",2) or 0),10))
                        if alternatives and attempts<=max_replans:
                            failed_candidate=candidate_id
                            candidate_id=alternatives[0].id
                            self.telemetry.inc("replan")
                            with self._v3_lock:
                                current=self.store.load(work_id)
                                current.context.setdefault("_v3",{})["replanned_from"]=failed_candidate
                                current.context["_v3"]["selected_intelligence"]=candidate_id
                                current.context["_v3"]["replan_attempt"]=attempts
                                current.context["_v3"]["failure_evidence"]={
                                    "state":state_value,
                                    "result":getattr(result,"result",None),
                                }
                                self.store.save(current)
                            continue
                    return result
                except Exception as exc:
                    elapsed=time.time()-execution_start
                    self.v3_state.learn(candidate_id or "unknown",False,elapsed)
                    self.v3_state.event(work_id,"execution_error",{
                        "error":str(exc),"candidate":candidate_id,"attempt":attempts})
                    alternatives=self._replan_candidates(work,context,candidate_id)
                    if not alternatives or attempts>=int(context.get("max_replans",2) or 2):
                        self.telemetry.inc("error")
                        raise
                    candidate_id=alternatives[0].id
                    self.telemetry.inc("replan")
                    with self._v3_lock:
                        work=self.store.load(work_id)
                        work.context.setdefault("_v3",{})["replanned_from"]=decision.candidate_id
                        work.context["_v3"]["selected_intelligence"]=candidate_id
                        work.context["_v3"]["replan_attempt"]=attempts
                        self.store.save(work)
        finally:
            self._release_slot()

