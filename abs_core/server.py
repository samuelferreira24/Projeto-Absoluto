from .adapters import EchoCapability
from .capabilities import CapabilityRecord, CapabilityRegistry
from .orchestrator import Orchestrator
from .resources import ResourceManager
from .interface_runtime import InterfaceRuntime
from .store import WorkStore
from .api import serve


def build_registry():
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("echo", "Echo test capability", "test", EchoCapability()))
    try:
        from .codex_adapter import CodexCapability
        registry.register(CapabilityRecord("codex", "OpenAI Codex", "external_ai", CodexCapability()))
    except Exception:
        pass
    return registry


def main():
    registry = build_registry()
    orchestrator = Orchestrator(registry, WorkStore("abs.db"))
    resources = ResourceManager()
    interface_runtime = InterfaceRuntime()
    serve(orchestrator, registry, resources=resources, interface_runtime=interface_runtime)


if __name__ == "__main__":
    main()
