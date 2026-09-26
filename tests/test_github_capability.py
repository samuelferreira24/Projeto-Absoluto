from __future__ import annotations

from abs_core.github_adapter import GitHubCapability
from abs_core.runtime import build_runtime


class FakeGitHub(GitHubCapability):
    def _request(self, path, *, query=None):
        if path == "repos/samuelferreira24/Projeto-Absoluto":
            return {"full_name": "samuelferreira24/Projeto-Absoluto", "default_branch": "main"}
        if path == "repos/samuelferreira24/Projeto-Absoluto/contents/README.md":
            return {
                "encoding": "base64",
                "content": "UkVBRF9PSw==",
                "sha": "abc",
                "html_url": "https://github.com/samuelferreira24/Projeto-Absoluto/blob/main/README.md",
            }
        raise AssertionError((path, query))


def test_github_read_capability_repository_and_file():
    capability = FakeGitHub()
    repo = capability.execute("inspect repository", {"action": "repository"})
    assert repo["repository"]["full_name"] == "samuelferreira24/Projeto-Absoluto"

    file_result = capability.execute(
        "read README",
        {"action": "file", "path": "README.md"},
    )
    assert file_result["content"] == "READ_OK"
    assert file_result["sha"] == "abc"


def test_runtime_registers_github_capability():
    runtime = build_runtime(":memory:")
    capability = runtime.registry.get("github")
    assert capability.id == "github"
    assert "repository" in capability.metadata["capabilities"]
