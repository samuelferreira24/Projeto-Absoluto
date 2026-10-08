from abs_core.intelligence import CognitiveRuntime


def test_cognitive_runtime_extracts_final_response_from_v2_envelope():
    result = {
        "type": "v2_result",
        "result": {
            "type": "openclaw_intelligence",
            "final_response": "ABS_V3_CHAT_OK",
        },
    }
    assert CognitiveRuntime._extract_final_response(result) == "ABS_V3_CHAT_OK"


def test_cognitive_runtime_preserves_direct_final_response():
    result = {"final_response": "direct"}
    assert CognitiveRuntime._extract_final_response(result) == "direct"
