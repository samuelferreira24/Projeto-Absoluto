import unittest

from cerebro.github_controle import (
    GitHubExecution,
    classificar_estado,
    correlation_id,
    idempotency_key,
    json_canonico,
    normalizar_execucao,
    registro_evento,
)


class TestGithubControle(unittest.TestCase):
    def test_ids_sao_deterministicos(self):
        self.assertEqual(correlation_id("repo", "main", "abc"), correlation_id("repo", "main", "abc"))
        self.assertNotEqual(correlation_id("repo", "main", "abc"), correlation_id("repo", "dev", "abc"))
        self.assertEqual(idempotency_key("repo", "main", "test"), idempotency_key("repo", "main", "test"))

    def test_normaliza_execucao_com_payload_do_github(self):
        execucao = normalizar_execucao(
            {"id": 123, "head_sha": "abc123", "head_branch": "base-cerebro-v0.1", "name": "CI", "status": "completed", "conclusion": "success"},
            repository="samuelferreira24/Projeto-Absoluto",
        )
        self.assertEqual(execucao.run_id, 123)
        self.assertEqual(execucao.commit, "abc123")
        self.assertTrue(execucao.successful)
        self.assertEqual(classificar_estado(execucao), "VALIDADO_CI")

    def test_falha_e_execucao_em_andamento(self):
        falha = GitHubExecution("repo", "main", "abc", "CI", 1, "completed", "failure", "c", "now")
        andamento = GitHubExecution("repo", "main", "abc", "CI", 2, "in_progress", None, "d", "now")
        self.assertTrue(falha.failed)
        self.assertEqual(classificar_estado(falha), "FALHOU_CI")
        self.assertEqual(classificar_estado(andamento), "EM_VALIDACAO_CI")

    def test_evento_preserva_correlacao_e_evidencia(self):
        execucao = normalizar_execucao(
            {"id": 9, "head_sha": "abc", "head_branch": "base-cerebro-v0.1", "status": "completed", "conclusion": "success"},
            repository="repo",
        )
        evento = registro_evento(execucao, event_type="workflow.validation", result="success", evidence=["run:9"])
        self.assertEqual(evento["correlation_id"], execucao.correlation_id)
        self.assertEqual(evento["evidence"], ["run:9"])
        self.assertIn("idempotency_key", evento)

    def test_serializacao_canonica(self):
        self.assertEqual(json_canonico({"b": 2, "a": 1}), '{"a":1,"b":2}')


if __name__ == "__main__":
    unittest.main()
