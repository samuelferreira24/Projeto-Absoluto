from pathlib import Path

from abs_core import api


def test_interface_v1_assets_and_routes_exist() -> None:
    assert api.WEB_INDEX.exists()
    html = api.WEB_INDEX.read_text(encoding="utf-8")
    for marker in ("/health", "/capabilities", "/works", "Executar capacidade"):
        assert marker in html
    assert api.ABSHandler.do_GET is not None
    assert api.ABSHandler.do_POST is not None
