from sandbox_runtime import Mission, SandboxRuntime, fixture
from abs_core.connections import ConnectionRegistry
from abs_core.resource_router import ResourceRouter


def test_real_registries_under_modes():
    caps, router = fixture()
    rt = SandboxRuntime(caps, router)
    for mode in ("DIRECT", "WORKFLOW", "RESEARCH", "AGENT", "MULTIAGENT", "RECOVERY"):
        result = rt.run(Mission("x", mode))
        assert result.status == "success"
        assert result.capability


def test_no_resource_is_not_execution():
    caps, _ = fixture()
    rt = SandboxRuntime(caps, ResourceRouter(ConnectionRegistry()))
    result = rt.run(Mission("x", "AGENT"))
    assert result.status == "RESOURCE_UNAVAILABLE"


if __name__ == "__main__":
    test_real_registries_under_modes()
    test_no_resource_is_not_execution()
    print("SANDBOX_RUNTIME: PASS")
