from pathlib import Path
import subprocess


def test_local_ai_full_operation_script_has_valid_bash_syntax():
    script = Path(__file__).resolve().parents[1] / "scripts" / "ops" / "local_ai_full_operation.sh"
    result = subprocess.run(
        ["bash", "-n", str(script)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
