from __future__ import annotations

from .tool_knowledge import ToolKnowledge, ToolKnowledgeRegistry


def default_tool_knowledge() -> ToolKnowledgeRegistry:
    registry = ToolKnowledgeRegistry()
    tools = [
        ("chatgpt", "ChatGPT", "ai", ["reasoning", "general", "multimodal"], ["chatgpt-connector"]),
        ("codex", "OpenAI Codex", "code", ["code", "reasoning", "execution"], ["codex-termux"]),
        ("claude", "Claude", "ai", ["reasoning", "writing", "analysis"], ["claude-api"]),
        ("claude-code", "Claude Code", "code", ["code", "terminal", "debugging"], ["claude-api", "local-network"]),
        ("gemini", "Gemini", "ai", ["reasoning", "multimodal", "long-context"], ["gemini-api"]),
        ("github-copilot", "GitHub Copilot", "code", ["code", "autocomplete"], ["github-api"]),
        ("cursor", "Cursor", "code", ["code", "project-editing"], ["local-network"]),
        ("perplexity", "Perplexity AI", "research", ["research", "web"], ["internet-http"]),
        ("midjourney", "Midjourney", "image", ["image-generation", "art-direction"], ["internet-http"]),
        ("flux", "Flux", "image", ["image-generation", "text-rendering"], ["internet-http"]),
        ("sora", "Sora", "video", ["video-generation"], ["internet-http"]),
        ("heygen", "HeyGen", "video", ["avatar-video", "voice"], ["internet-http"]),
        ("suno", "Suno", "audio", ["music-generation"], ["internet-http"]),
    ]
    for tool_id, name, category, capabilities, connections in tools:
        registry.register(ToolKnowledge(
            id=tool_id,
            name=name,
            category=category,
            capabilities=capabilities,
            connection_ids=connections,
            status="catalogued",
            metadata={"source": "abs-initial-tool-catalog"},
        ))
    return registry
