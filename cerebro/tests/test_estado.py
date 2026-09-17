from cerebro.estado import EstadoSistema, SCHEMA_VERSION, validar_estado


def test_estado_roundtrip_json():
    estado = EstadoSistema(
        project_id="PROJETO-ABSOLUTO",
        state_id="ESTADO-0001",
        architecture_version="FUNDACAO-V0.2",
        active_capabilities=["registro_versionado"],
        in_construction=["rastreabilidade"],
        next_priority="testar",
    )
    restaurado = EstadoSistema.from_json(estado.to_json())
    assert restaurado.project_id == estado.project_id
    assert restaurado.active_capabilities == ["registro_versionado"]
    assert restaurado.next_priority == "testar"


def test_estado_rejeita_schema_incompativel():
    try:
        EstadoSistema.from_dict({"schema_version": "9.9", "project_id": "x", "state_id": "y", "architecture_version": "z"})
    except ValueError as exc:
        assert "schema_version" in str(exc)
    else:
        raise AssertionError("schema incompatível deveria ser rejeitado")


def test_validar_estado_detecta_campos():
    erros = validar_estado({"schema_version": SCHEMA_VERSION})
    assert "campo obrigatorio ausente: project_id" in erros
