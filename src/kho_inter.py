"""Run the bundled Khovanov indexer as a local program."""

from pathlib import Path
import os
import subprocess
import sys

from mytimer import timer_wrap_gen


SOURCE_DIR = Path(__file__).resolve().parent
INDEXER_MAIN = SOURCE_DIR / "khovanov-indexer" / "src" / "main.py"


@timer_wrap_gen("kho_inter")
def to_knotname(
    pd_code: list[list[int]],
    *,
    java_path: str | os.PathLike[str] | None = None,
    timeout: float = 120.0,
    max_heap: str = "16g",
) -> list[str]:
    if not isinstance(pd_code, list):
        raise TypeError("pd_code must be a list")
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    command = [
        sys.executable,
        str(INDEXER_MAIN),
        "--timeout",
        str(timeout),
        "--max-heap",
        max_heap,
    ]
    if java_path is not None:
        command.extend(["--java", os.fspath(java_path)])
    completed = subprocess.run(
        command,
        input=repr(pd_code),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout + 10,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"Khovanov indexer failed: {detail or 'no diagnostic output'}")
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]
