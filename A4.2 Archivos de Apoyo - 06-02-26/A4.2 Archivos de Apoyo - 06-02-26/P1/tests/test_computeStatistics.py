import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT/"P1"/"source"/"computeStatistics.py"


def run(script: Path, input_file: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), str(input_file)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_tc1_runs_and_outputs_results(tmp_path: Path):
    # Crea un input controlado
    data = tmp_path / "tc.txt"
    data.write_text("1\n2\n3\n3\nx\n\n", encoding="utf-8")

    proc = run(SCRIPT, data)
    assert proc.returncode in (0, 1)
    assert "ERROR:" in proc.stdout  # por la 'x'
    assert "Mean:" in proc.stdout
    assert "Median:" in proc.stdout
    assert "Mode:" in proc.stdout
