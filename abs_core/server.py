from .adapters import EchoCapability
from .capabilities import CapabilityRecord, CapabilityRegistry
from .orchestrator import Orchestrator
from .resources import ResourceManager
from .connections import ConnectionRegistry
from .accounts import AccountRegistry
from .interface_runtime import InterfaceRuntime
from .store import WorkStore
from .api import serve
from .tool_catalog import default_tool_knowledge
from .tool_knowledge_store import ToolKnowledgeStore
from .tool_learning import ToolLearningEngine
from .tool_planner import ToolPlanner
from .resource_router import ResourceRouter
from .resource_dispatcher import ResourceDispatcher
from .intelligence import IntelligenceRegistry, CognitiveRuntime
import os


def build_registry():
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("echo", "Echo test capability", "test", EchoCapability()))
    try:
        from .internet_adapter import InternetHTTPCapability
        registry.register(CapabilityRecord("internet-http", "Internet HTTP", "network", InternetHTTPCapability()))
    except Exception:
        pass
    try:
        from .local_ai_adapter import LocalAICapability
        if os.getenv("ABS_LOCAL_AI_URL"):
            registry.register(CapabilityRecord("local-ai", "IA local", "local_ai", LocalAICapability()))
    except Exception:
        pass
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
    accounts = AccountRegistry(os.getenv("ABS_DB_PATH", "abs.db"))
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
    intelligence = IntelligenceRegistry()
    intelligence.discover_from_capabilities(registry, connections)
    cognitive_runtime = CognitiveRuntime(
        registry, intelligence,
        store_path=os.getenv("ABS_DB_PATH", "abs.db"),
    )
    serve(orchestrator, registry, resources=resources, interface_runtime=interface_runtime, connections=connections, accounts=accounts, tool_knowledge=tool_knowledge, tool_planner=ToolPlanner(tool_knowledge, ResourceRouter(connections)), tool_learning=tool_learning, cognitive_runtime=cognitive_runtime)


if __name__ == "__main__":
    main()
