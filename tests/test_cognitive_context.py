from abs_core.cognitive_context import build_system_context


def test_abs_context_contains_identity_and_current_time():
    context = build_system_context([
        {"id": "github", "name": "GitHub", "kind": "external_service"},
        {"id": "local-ai", "name": "IA local", "kind": "local_ai"},
    ])
    assert "operando dentro do ABS" in context
    assert "Projeto Absoluto" in context
    assert "DATA E HORA ATUAIS" in context
    assert "github: GitHub" in context


def test_external_results_are_contextualized():
    context = build_system_context(
        [{"id": "internet-http", "name": "Internet HTTP", "kind": "network"}],
        [{"type": "tool_result", "tool": "internet-http", "result": {"title": "Example Domain"}}],
    )
    assert "RESULTADOS OBTIDOS PELO ABS" in context
    assert "Example Domain" in context
