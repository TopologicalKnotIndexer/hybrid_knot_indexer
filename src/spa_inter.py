"""Run the bundled spatial-coordinate converter as a local program."""

from ast import literal_eval
from pathlib import Path
import subprocess
import sys


SOURCE_DIR = Path(__file__).resolve().parent
CONVERTER_MAIN = SOURCE_DIR / "spatial_coord_to_pd_code" / "src" / "main.py"


def to_pdcode(spatial_coord: list[list[float]], *, timeout: float = 120.0) -> list[list[int]]:
    if not isinstance(spatial_coord, list):
        raise TypeError("spatial_coord must be a list")
    completed = subprocess.run(
        [sys.executable, str(CONVERTER_MAIN)],
        input=repr(spatial_coord),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"spatial converter failed: {detail or 'no diagnostic output'}")
    try:
        result = literal_eval(completed.stdout.strip())
    except (SyntaxError, ValueError) as exc:
        raise RuntimeError(f"spatial converter returned invalid output: {completed.stdout!r}") from exc
    if not isinstance(result, list):
        raise RuntimeError("spatial converter did not return a PD-code list")
    return result
