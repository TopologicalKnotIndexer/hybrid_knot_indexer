"""Run end-to-end checks against every committed molecular sample."""

from pathlib import Path
import re

import che_file_to_knot_name


SOURCE_DIR = Path(__file__).resolve().parent
DATA_DIR = SOURCE_DIR / "che_data"
_KNOT_NAME = re.compile(r"^m?K\d+[an]\d+(?:,m?K\d+[an]\d+)*$")
_KNOWN_CATALOG_COLLISIONS = {
    "K8a8": ["K10n6", "K8a8"],
}


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


def expected_candidates(path: Path) -> list[str]:
    """Return the exact candidate set expected from both finite catalogs."""

    name = expected_name(path)
    return list(_KNOWN_CATALOG_COLLISIONS.get(name, [name]))


def main(
    *,
    java_path: str | None = None,
    sage_path: str | None = None,
    projection_timeout: float = 120.0,
    khovanov_timeout: float = 120.0,
    homfly_timeout: float = 120.0,
    max_heap: str = "16g",
) -> int:
    failures = 0
    for path in list_all_test_files():
        expected = expected_name(path)
        try:
            candidates = che_file_to_knot_name.che_file_to_knot_name(
                str(path),
                java_path=java_path,
                sage_path=sage_path,
                projection_timeout=projection_timeout,
                khovanov_timeout=khovanov_timeout,
                homfly_timeout=homfly_timeout,
                max_heap=max_heap,
            )
            passed = candidates == expected_candidates(path)
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
