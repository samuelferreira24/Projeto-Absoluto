import tempfile

from cerebro.nucleo import RepositorioJSONL, novo_registro


def test_busca_por_metadados_e_campos_do_registro():
    with tempfile.TemporaryDirectory() as tmp:
        repo = RepositorioJSONL(tmp)
        a = novo_registro(repo, "PESQUISA", "Pesquisa A", metadata={"area": "arquitetura", "ano": 2026})
        b = novo_registro(repo, "IDEIA", "Ideia B", metadata={"area": "produto", "ano": 2026})
        repo.salvar(a)
        repo.salvar(b)

        assert [r.id for r in repo.buscar_por_metadados({"area": "arquitetura"})] == [a.id]
        assert [r.id for r in repo.buscar_por_metadados({"kind": "IDEIA", "ano": 2026})] == [b.id]
        assert repo.buscar_por_metadados({"state": "NOVO"})
        assert repo.buscar_por_metadados({"source": None})
