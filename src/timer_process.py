"""Run an arbitrary command with a wall-clock timeout."""

import argparse
import subprocess
import sys
import time


def run_subprocess_with_time_limit(command: list[str], time_limit_sec: float) -> int:
    if not command:
        raise ValueError("command must not be empty")
    if time_limit_sec <= 0:
        raise ValueError("time limit must be positive")
    started = time.perf_counter()
    try:
        completed = subprocess.run(command, timeout=time_limit_sec, check=False)
    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter() - started
        print(f"WARN: subprocess killed after timeout ({elapsed:.3f}s)", file=sys.stderr)
        return 124
    elapsed = time.perf_counter() - started
    print(f"INFO: subprocess returned {completed.returncode} ({elapsed:.3f}s)", file=sys.stderr)
    return completed.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a command with a timeout.")
    parser.add_argument("timeout", type=float)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    try:
        return run_subprocess_with_time_limit(args.command, args.timeout)
    except ValueError as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
