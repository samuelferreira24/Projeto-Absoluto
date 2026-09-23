from abs_core.nodes import ABSNode, NodeRegistry
from abs_core.transports import Transport, select
from abs_core.node_gateway import NodeGateway

def test_node_registry_and_heartbeat(tmp_path):
    r=NodeRegistry(tmp_path/"nodes.json"); r.register(ABSNode("app-1","App",capabilities=("inference",)))
    assert r.by_capability("inference")[0].id=="app-1"
    assert r.heartbeat("app-1")

def test_transport_selection():
    t=select([Transport("local","local","device",cost=0),Transport("internet","http","remote",cost=2)],require_bidirectional=True)
    assert t.id=="local"

def test_node_gateway_roundtrip():
    g=NodeGateway(); w=g.enqueue("inference",{"x":1}); assert g.next().id==w.id; g.complete(w.id,success=True,result={"ok":1}); assert g.result(w.id)["success"]
