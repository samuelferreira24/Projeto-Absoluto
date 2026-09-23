from __future__ import annotations

"""Single composition root for every ABS runtime surface."""

import os
from dataclasses import dataclass

from .accounts import AccountRegistry
from .connections import ConnectionRegistry
from .interface_runtime import InterfaceRuntime
from .orchestrator import Orchestrator
from .resource_dispatcher import ResourceDispatcher
from .resource_router import ResourceRouter
from .resources import ResourceManager
from .store import WorkStore
from .tool_catalog import default_tool_knowledge
from .tool_discovery import ToolDiscovery
from .tool_knowledge_store import ToolKnowledgeStore
from .tool_learning import ToolLearningEngine
from .tool_planner import ToolPlanner
from .capabilities import CapabilityRecord, CapabilityRegistry
from .adapters import EchoCapability
from .intelligence import CognitiveRuntime, IntelligenceRegistry


@dataclass
class ABSRuntime:
    registry: CapabilityRegistry
    orchestrator: Orchestrator
    resources: ResourceManager
    interface_runtime: InterfaceRuntime
    connections: ConnectionRegistry
    accounts: AccountRegistry
    tool_knowledge: object
    tool_store: ToolKnowledgeStore
    tool_learning: ToolLearningEngine
    tool_discovery: ToolDiscovery
    tool_planner: ToolPlanner
    resource_router: ResourceRouter
    resource_dispatcher: ResourceDispatcher
    intelligence: IntelligenceRegistry
    cognitive_runtime: CognitiveRuntime


def build_registry() -> CapabilityRegistry:
    registry = CapabilityRegistry()
    registry.register(CapabilityRecord("echo", "Echo test capability", "test", EchoCapability()))

    # Core local/network capabilities are structural ABS capabilities and must
    # remain discoverable even when optional credentials are absent.
    from .codex_adapter import CodexCapability
    from .internet_adapter import InternetHTTPCapability

    registry.register(CapabilityRecord("codex", "OpenAI Codex CLI", "external_ai", CodexCapability()))
    registry.register(CapabilityRecord("internet-http", "Internet HTTP", "network", InternetHTTPCapability()))

    optional = (
        (".local_ai_adapter", "LocalAICapability", "local-ai", "IA local", "local_ai", "ABS_LOCAL_AI_URL"),
        (".ai_adapters", "ClaudeCapability", "claude", "Anthropic Claude API", "external_ai", "ANTHROPIC_API_KEY"),
        (".ai_adapters", "GeminiCapability", "gemini", "Google Gemini API", "external_ai", "GEMINI_API_KEY"),
        (".openai_adapter", "OpenAICapability", "openai-api", "OpenAI API", "external_ai", "OPENAI_API_KEY"),
    )
    for module_name, class_name, capability_id, name, kind, env_name in optional:
        if env_name and not os.getenv(env_name):
            continue
        try:
            module = __import__(module_name, package=__package__, fromlist=[class_name])
            registry.register(CapabilityRecord(capability_id, name, kind, getattr(module, class_name)()))
        except Exception:
            continue
    return registry


def build_runtime(db_path: str | None = None) -> ABSRuntime:
    db_path = db_path or os.getenv("ABS_DB_PATH", "abs.db")
    registry = build_registry()
    store = WorkStore(db_path)
    store.recover_interrupted()
    orchestrator = Orchestrator(registry, store)

    resources = ResourceManager()
    interface_runtime = InterfaceRuntime()
    connections = ConnectionRegistry.defaults()
    accounts = AccountRegistry(db_path)

    knowledge = default_tool_knowledge()
    tool_store = ToolKnowledgeStore(db_path)
    tool_store.load_into(knowledge)
    learning = ToolLearningEngine(knowledge, tool_store)
    discovery = ToolDiscovery()
    router = ResourceRouter(connections)
    planner = ToolPlanner(knowledge, router)

    intelligence = IntelligenceRegistry()
    intelligence.discover_from_capabilities(registry, connections)
    cognitive = CognitiveRuntime(registry, intelligence, orchestrator, store_path=db_path)

    dispatcher = ResourceDispatcher(router, planner, registry, knowledge, learning)
    dispatcher.orchestrator = orchestrator

    return ABSRuntime(
        registry, orchestrator, resources, interface_runtime, connections, accounts,
        knowledge, tool_store, learning, discovery, planner, router, dispatcher,
        intelligence, cognitive,
    )
