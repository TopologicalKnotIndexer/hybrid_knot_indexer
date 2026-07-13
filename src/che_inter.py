"""Run the bundled molecular-data converter as a local program."""

from ast import literal_eval
from pathlib import Path
import subprocess
import sys

from mytimer import timer_wrap_gen


SOURCE_DIR = Path(__file__).resolve().parent
CONVERTER_MAIN = SOURCE_DIR / "che_data_to_pd_code" / "src" / "che_data_to_pd_code.py"


@timer_wrap_gen("che_inter")
def che_data_to_pd_code(
    che_data_file_path: str, *, timeout: float = 120.0
) -> list[list[int]]:
    path = Path(che_data_file_path)
    if not path.is_file():
        raise FileNotFoundError(path)
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    completed = subprocess.run(
        [sys.executable, str(CONVERTER_MAIN), str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"molecular converter failed: {detail or 'no diagnostic output'}")
    try:
        result = literal_eval(completed.stdout.strip())
    except (SyntaxError, ValueError) as exc:
        raise RuntimeError(f"molecular converter returned invalid output: {completed.stdout!r}") from exc
    if not isinstance(result, list):
        raise RuntimeError("molecular converter did not return a PD-code list")
    return result
