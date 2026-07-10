#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT_SRC = ROOT.parent
EXE_SUFFIX = ".exe" if os.name == "nt" else ""
DEFAULT_EXE = ROOT / "build" / f"link-pdcode{EXE_SUFFIX}"


def run(cmd: list[str], *, stdin: str | None = None, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, input=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)


def build(exe: Path, rebuild: bool) -> None:
    if exe.exists() and not rebuild:
        return
    proc = run([sys.executable, str(ROOT / "build.py"), "--output", str(exe), "--clean"], timeout=180)
    if proc.returncode != 0:
        print(proc.stdout, end="")
        print(proc.stderr, end="", file=sys.stderr)
        raise SystemExit(proc.returncode)


def coord_text(points: list[tuple[float, float, float]]) -> str:
    lines = [str(len(points))]
    lines += [f"{x:.17g} {y:.17g} {z:.17g}" for x, y, z in points]
    return "\n".join(lines) + "\n"


def parse_pd(text: str) -> list[list[int]]:
    value = ast.literal_eval(text.strip())
    assert isinstance(value, list)
    for row in value:
        assert isinstance(row, list)
        assert len(row) == 4
        assert all(isinstance(x, int) for x in row)
    return value


def assert_valid_pd(pd: list[list[int]]) -> None:
    counts: dict[int, int] = {}
    for row in pd:
        for x in row:
            counts[x] = counts.get(x, 0) + 1
    assert set(counts.values()) <= {2}, counts
    assert sorted(counts) == list(range(1, 2 * len(pd) + 1)), counts


def run_pd(exe: Path, points: list[tuple[float, float, float]], *args: str) -> list[list[int]]:
    proc = run([str(exe), *args], stdin=coord_text(points), timeout=30)
    if proc.returncode != 0:
        raise AssertionError(f"command failed {proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}")
    pd = parse_pd(proc.stdout)
    assert_valid_pd(pd)
    return pd


def test_no_crossing(exe: Path) -> None:
    square = [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)]
    pd = run_pd(exe, square, "--direction", "0", "0", "1")
    assert pd == [], pd
    print("PASS no-crossing")


def test_one_crossing(exe: Path) -> None:
    polygon = [(-1, -1, 0), (1, 1, 0), (1, -1, 1), (-1, 1, 1)]
    pd = run_pd(exe, polygon, "--direction", "0", "0", "1")
    assert len(pd) == 1, pd
    print("PASS one-crossing")


def test_sample_data(exe: Path) -> None:
    sample = PROJECT_SRC / "spatial_coord_to_pd_code" / "src" / "sample_data.txt"
    points: list[tuple[float, float, float]] = []
    for line in sample.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        x, y, z = map(float, line.split())
        points.append((x, y, z))
    pd = run_pd(exe, points)
    assert len(pd) > 0
    print("PASS sample-data")


def test_python_wrapper() -> None:
    wrapper = PROJECT_SRC / "spatial_coord_to_pd_code" / "src" / "main.py"
    polygon = [(-1, -1, 0), (1, 1, 0), (1, -1, 1), (-1, 1, 1)]
    proc = run([sys.executable, str(wrapper)], stdin=repr([list(p) for p in polygon]), timeout=60)
    if proc.returncode != 0:
        raise AssertionError(f"wrapper failed\nstdout={proc.stdout}\nstderr={proc.stderr}")
    pd = parse_pd(proc.stdout)
    assert_valid_pd(pd)
    print("PASS python-wrapper")


def test_nested_python_wrapper() -> None:
    wrapper = PROJECT_SRC / "che_data_to_pd_code" / "src" / "spatial_coord_to_pd_code" / "src" / "main.py"
    polygon = [(-1, -1, 0), (1, 1, 0), (1, -1, 1), (-1, 1, 1)]
    proc = run([sys.executable, str(wrapper)], stdin=repr([list(p) for p in polygon]), timeout=60)
    if proc.returncode != 0:
        raise AssertionError(f"nested wrapper failed\nstdout={proc.stdout}\nstderr={proc.stderr}")
    pd = parse_pd(proc.stdout)
    assert_valid_pd(pd)
    print("PASS nested-python-wrapper")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exe", default=str(DEFAULT_EXE))
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--no-build", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    exe = Path(args.exe).resolve()
    if not args.no_build:
        build(exe, args.rebuild)
    test_no_crossing(exe)
    test_one_crossing(exe)
    test_sample_data(exe)
    test_python_wrapper()
    test_nested_python_wrapper()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
