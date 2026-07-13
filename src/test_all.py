"""Run end-to-end checks against every committed molecular sample."""

from pathlib import Path
import re

import che_file_to_knot_name


SOURCE_DIR = Path(__file__).resolve().parent
DATA_DIR = SOURCE_DIR / "che_data"
_KNOT_NAME = re.compile(r"^m?K\d+[an]\d+(?:,m?K\d+[an]\d+)*$")


def list_all_test_files() -> list[Path]:
    if not DATA_DIR.is_dir():
        raise FileNotFoundError(DATA_DIR)
    return sorted(
        (path for path in DATA_DIR.glob("*/*") if path.is_file()),
        key=lambda path: (path.parent.name, path.name),
    )


def expected_name(path: Path) -> str:
    name = path.parent.name
    if not _KNOT_NAME.fullmatch(name):
        raise ValueError(f"invalid expected-name directory: {name}")
    return name


def main() -> int:
    failures = 0
    for path in list_all_test_files():
        expected = expected_name(path)
        try:
            candidates = che_file_to_knot_name.che_file_to_knot_name(str(path))
            passed = expected in candidates
            detail = ", ".join(candidates) if candidates else "no candidates"
        except Exception as exc:  # A regression runner must report all samples.
            passed = False
            detail = f"{type(exc).__name__}: {exc}"
        print(f"{'PASS' if passed else 'FAIL'} {expected}: {detail}")
        failures += not passed
    print(f"checked {len(list_all_test_files())} samples; failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
