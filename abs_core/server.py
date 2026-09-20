from .adapters import EchoCapability
from .capabilities import CapabilityRecord, CapabilityRegistry
from .orchestrator import Orchestrator
from .store import WorkStore
from .api import serve


def build_registry():
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("echo", "Echo test capability", "test", EchoCapability()))
    try:
        from .codex_adapter import CodexCapability
        registry.register(CapabilityRecord("codex", "OpenAI Codex", "external_ai", CodexCapability()))
    except Exception:
        # Keep the ABS core usable when the optional Codex SDK is not installed.
        pass
    return registry


def main():
    registry = build_registry()
    orchestrator = Orchestrator(registry, WorkStore("abs.db"))
    serve(orchestrator, registry)


if __name__ == "__main__":
    main()
