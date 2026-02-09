import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "P3" / "source" / "wordCount.py"


def test_counts_words(tmp_path: Path):
    data = tmp_path / "tc.txt"
    data.write_text("Hola hola, mundo!\nMundo mundo.\n", encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(data)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert "Row Labels" in proc.stdout
    # hola = 2, mundo = 3
    assert "mundo\t3" in proc.stdout
    assert "hola\t2" in proc.stdout
