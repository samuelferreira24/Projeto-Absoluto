from abs_core.openai_compat import OpenAICompatHandler


def test_gateway_stream_method_exists():
    assert callable(OpenAICompatHandler._send_stream)


def test_gateway_accepts_openai_tool_fields():
    # The handler reads standard OpenAI-compatible tool fields without
    # requiring the local model itself to implement native function calling.
    assert {"stream", "requested_tools", "tool_choice"}.issubset(set(OpenAICompatHandler.do_POST.__code__.co_varnames))
