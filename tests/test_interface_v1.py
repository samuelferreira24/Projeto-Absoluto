from pathlib import Path

from abs_core import api
from abs_core.resources import ResourceManager


def test_interface_v1_assets_and_routes_exist() -> None:
    assert api.WEB_INDEX.exists()
    assert api.WEB_MANIFEST.exists()
    assert api.WEB_SW.exists()
    html = api.WEB_INDEX.read_text(encoding="utf-8")
    for marker in ("/health", "/capabilities", "/devices", "/works", "Executar no ABS"):
        assert marker in html
    assert api.ABSHandler.do_GET is not None
    assert api.ABSHandler.do_POST is not None


def test_resource_manager_registers_local_device_and_remote_devices() -> None:
    manager = ResourceManager()
    assert len(manager.list()) == 1
    device = manager.register(
        name="Computador",
        kind="computer",
        endpoint="http://192.0.2.10:8787",
        capabilities=["codex"],
    )
    assert device.status == "online"
    assert device.capabilities == ["codex"]
    assert manager.summary()["total"] == 2
    manager.heartbeat(device.id, "degraded")
    assert manager.get(device.id).status == "degraded"


def test_interface_exposes_tool_planning_discovery_and_voice_controls():
    html = Path("20_interface/web/index.html").read_text(encoding="utf-8")
    for marker in ("/tools/knowledge", "/tools/plan", "/resources/dispatch", "/tools/discover", "SpeechRecognition", "Conversa com uma IA", "Sala de Inteligências", "room-ai", "abs-chat-history", "MAPA ABS", "absMap", "data-depth", "abs-node", "absControlDock", "absPanelOpen", "data-uxmode", "absCreate", "absUndo", "absRedo", "abs-workspace-v4"):
        assert marker in html

def test_interactive_workspace_state_controls_present():
    html = (ROOT / "20_interface" / "web" / "index.html").read_text()
    for marker in (
        "abs-workspace-v4",
        "readState",
        "data-uxmode",
        "absPanelOpen",
        "absCreate",
        "absConnect",
        "absUndo",
        "absRedo",
        "absResetWorkspace",
        "abs-panel-pinned",
    ):
        assert marker in html


def test_interactive_workspace_is_visual_only_by_default():
    html = (ROOT / "20_interface" / "web" / "index.html").read_text()
    assert "Construção visual: o ABS real não é alterado." in html
    assert "Operação: ações reais exigem comando explícito." in html
