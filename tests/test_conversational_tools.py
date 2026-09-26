from abs_core.conversational_tools import ConversationalToolRuntime
from abs_core.runtime import build_runtime


def test_conversational_github_detection():
    runtime = build_runtime(":memory:")
    tool_runtime = ConversationalToolRuntime(runtime.tool_planner, runtime.resource_dispatcher)

    intent = tool_runtime.detect("Leia o repositório do Projeto Absoluto no GitHub")
    assert intent is not None
    assert intent["tool_id"] == "github"
    assert intent["action"] == "repository"


def test_conversational_github_write_is_not_auto_executed():
    runtime = build_runtime(":memory:")
    tool_runtime = ConversationalToolRuntime(runtime.tool_planner, runtime.resource_dispatcher)

    intent = tool_runtime.detect("Crie um commit no GitHub")
    assert intent is not None
    assert intent["action"] == "unsupported_write"


def test_conversational_internet_url_detection():
    runtime = build_runtime(":memory:")
    tool_runtime = ConversationalToolRuntime(runtime.tool_planner, runtime.resource_dispatcher)

    intent = tool_runtime.detect("Abra e leia https://example.com")
    assert intent is not None
    assert intent["tool_id"] == "internet-http"
    assert intent["action"] == "get"
    assert intent["url"] == "https://example.com"


def test_conversational_internet_has_an_executable_plan():
    runtime = build_runtime(":memory:")
    tool_runtime = ConversationalToolRuntime(runtime.tool_planner, runtime.resource_dispatcher)

    plans = runtime.tool_planner.plan(
        "Abra e leia https://example.com",
        ("http",),
        preferred_categories=("network",),
        tool_id="internet-http",
    )
    assert plans
    assert plans[0].tool_id == "internet-http"
