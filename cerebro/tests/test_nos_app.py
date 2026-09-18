from cerebro.nos_app import NoApp, RegistroNosApp

def test_registro_de_dois_apps(tmp_path):
    r = RegistroNosApp(tmp_path / "nos.json")
    r.registrar(NoApp("celular-a", "App A", ambiente="android", capacidades=("inferencia",)))
    r.registrar(NoApp("celular-b", "App B", ambiente="android", capacidades=("inferencia", "camera")))
    assert len(r.listar()) == 2
    assert len(r.por_capacidade("inferencia")) == 2
    assert len(r.por_capacidade("camera")) == 1

def test_sinal_do_no(tmp_path):
    r = RegistroNosApp(tmp_path / "nos.json")
    r.registrar(NoApp("a", "A"))
    assert r.sinalizar("a")
    assert not r.sinalizar("inexistente")
