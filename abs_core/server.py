from .adapters import EchoCapability
from .capabilities import CapabilityRecord, CapabilityRegistry
from .orchestrator import Orchestrator
from .resources import ResourceManager
from .connections import ConnectionRegistry
from .interface_runtime import InterfaceRuntime
from .store import WorkStore
from .api import serve
from .tool_catalog import default_tool_knowledge
from .tool_knowledge_store import ToolKnowledgeStore
from .tool_learning import ToolLearningEngine
import os


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
    connections = ConnectionRegistry.defaults()
    for module_name, class_name, capability_id, name, env_name in (
        (".ai_adapters", "ClaudeCapability", "claude", "Anthropic Claude API", "ANTHROPIC_API_KEY"),
        (".ai_adapters", "GeminiCapability", "gemini", "Google Gemini API", "GEMINI_API_KEY"),
        (".openai_adapter", "OpenAICapability", "openai-api", "OpenAI API", "OPENAI_API_KEY"),
    ):
        if os.getenv(env_name):
            try:
                module = __import__(module_name, package=__package__, fromlist=[class_name])
                capability = getattr(module, class_name)()
                registry.register(CapabilityRecord(capability_id, name, "external_ai", capability))
            except Exception:
                pass
    tool_knowledge = default_tool_knowledge()
    tool_store = ToolKnowledgeStore("abs.db")
    tool_store.load_into(tool_knowledge)
    tool_learning = ToolLearningEngine(tool_knowledge, tool_store)
    serve(orchestrator, registry, resources=resources, interface_runtime=interface_runtime, connections=connections, tool_knowledge=tool_knowledge, tool_learning=tool_learning)


if __name__ == "__main__":
    main()
