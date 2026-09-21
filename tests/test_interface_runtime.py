from abs_core.interface_runtime import InterfaceRuntime


def test_interface_runtime_has_extensible_modes_and_inputs() -> None:
    runtime = InterfaceRuntime()
    assert {"control", "capabilities", "devices", "browser"} <= {
        mode.id for mode in runtime.list_modes()
    }
    assert {"text", "voice", "image", "camera"} <= set(runtime.list_inputs())


def test_interface_runtime_switches_mode_and_input_without_touching_core_contract() -> None:
    runtime = InterfaceRuntime()
    state = runtime.set_mode("browser")
    assert state.mode_id == "browser"
    state = runtime.set_input("voice")
    assert state.input_channel == "voice"


def test_interface_runtime_rejects_unknown_extensions() -> None:
    runtime = InterfaceRuntime()
    try:
        runtime.set_mode("future_mode")
        assert False
    except KeyError:
        pass

    try:
        runtime.set_input("future_sensor")
        assert False
    except KeyError:
        pass


def test_interface_runtime_can_acquire_new_mode_and_input() -> None:
    from abs_core.interface_runtime import InterfaceMode

    runtime = InterfaceRuntime()
    runtime.register_mode(
        InterfaceMode(
            "engineering",
            "Engenharia",
            description="Experiência de engenharia extensível.",
        )
    )
    runtime.register_input("sensor")
    assert runtime.set_mode("engineering").mode_id == "engineering"
    assert runtime.set_input("sensor").input_channel == "sensor"
