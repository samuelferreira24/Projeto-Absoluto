from .adapters import EchoCapability
from .capabilities import CapabilityRecord, CapabilityRegistry
from .orchestrator import Orchestrator
from .store import WorkStore
from .api import serve

def main():
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("echo", "Echo test capability", "test", EchoCapability()))
    orchestrator = Orchestrator(registry, WorkStore("abs.db"))
    serve(orchestrator, registry)

if __name__ == "__main__": main()
