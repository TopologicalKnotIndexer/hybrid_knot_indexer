"""Command-line interface for hybrid_knot_indexer."""

import argparse
import subprocess

import che_file_to_knot_name
import test_all


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Identify a closed molecular chain with Khovanov and HOMFLY-PT catalogs."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--che", metavar="FILE", help="LAMMPS molecular data file")
    group.add_argument("--test", action="store_true", help="run bundled molecular regressions")
    parser.add_argument("--java", help="path or command name for Java")
    parser.add_argument("--sage", help="path or command name for SageMath")
    parser.add_argument("--projection-timeout", type=float, default=120.0)
    parser.add_argument("--khovanov-timeout", type=float, default=120.0)
    parser.add_argument("--homfly-timeout", type=float, default=120.0)
    parser.add_argument("--max-heap", default="16g")
    args = parser.parse_args(argv)
    try:
        if args.test:
            return test_all.main()
        for name in che_file_to_knot_name.che_file_to_knot_name(
            args.che,
            java_path=args.java,
            sage_path=args.sage,
            projection_timeout=args.projection_timeout,
            khovanov_timeout=args.khovanov_timeout,
            homfly_timeout=args.homfly_timeout,
            max_heap=args.max_heap,
        ):
            print(name)
    except (
        FileNotFoundError,
        subprocess.TimeoutExpired,
        TypeError,
        ValueError,
        RuntimeError,
    ) as exc:
        parser.exit(2, f"error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
