import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "P2" / "source" / "convertNumbers.py"


def test_simple_values(tmp_path: Path):
    data = tmp_path / "tc.txt"
    data.write_text("10\n255\n-10\nbad\n", encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(data)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert "ITEM\tDEC\tBIN\tHEX" in proc.stdout
    assert "\t10\t1010\tA" in proc.stdout
    assert "\t255\t11111111\tFF" in proc.stdout
    assert "\t-10\t-1010\t-A" in proc.stdout
    assert "ERROR:" in proc.stdout
