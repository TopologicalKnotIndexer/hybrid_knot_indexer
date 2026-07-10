#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import platform
import shutil
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXE_SUFFIX = ".exe" if os.name == "nt" else ""
TARGET_NAME = f"link-pdcode{EXE_SUFFIX}"
SOURCES = ["main.c", "link_pdcode.c"]


def split_command(value: str) -> list[str]:
    return shlex.split(value, posix=(os.name != "nt"))


def run_quiet(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)


def compiler_version(cc: list[str]) -> str:
    try:
        proc = run_quiet(cc + ["--version"])
    except (OSError, subprocess.SubprocessError):
        return ""
    return (proc.stdout + proc.stderr).strip()


def find_compiler(user_cc: str | None) -> list[str]:
    candidates: list[list[str]] = []
    if user_cc:
        candidates.append(split_command(user_cc))
    elif os.environ.get("CC"):
        candidates.append(split_command(os.environ["CC"]))

    names = ["gcc", "clang", "cc"]
    if os.name == "nt":
        names = ["gcc.exe", "clang.exe", "cc.exe", "gcc", "clang", "cc"]
    for name in names:
        path = shutil.which(name)
        if path:
            candidates.append([path])

    seen: set[tuple[str, ...]] = set()
    for candidate in candidates:
        key = tuple(candidate)
        if not candidate or key in seen:
            continue
        seen.add(key)
        if compiler_version(candidate):
            return candidate
    raise SystemExit("ERROR: no C compiler found; pass --cc or set CC")


def test_flag(cc: list[str], flags: list[str], flag: str, link_flags: list[str]) -> bool:
    with tempfile.TemporaryDirectory(prefix="link_pdcode_probe_") as tmp:
        src = Path(tmp) / "probe.c"
        out = Path(tmp) / ("probe" + EXE_SUFFIX)
        src.write_text("int main(void){return 0;}\n", encoding="utf-8")
        proc = subprocess.run(cc + flags + [flag, str(src), "-o", str(out)] + link_flags,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return proc.returncode == 0


def build_flags(args: argparse.Namespace, cc: list[str]) -> tuple[list[str], list[str]]:
    flags = ["-std=c11"]
    flags += ["-O0", "-g"] if args.debug else ["-O3", "-DNDEBUG"]
    link_flags = ["-lm"]
    if not args.debug:
        for flag in ["-pipe"]:
            if test_flag(cc, flags, flag, link_flags):
                flags.append(flag)
        if not args.portable:
            for flag in ["-march=native", "-mtune=native"]:
                if test_flag(cc, flags, flag, link_flags):
                    flags.append(flag)
        if not args.no_lto and test_flag(cc, flags, "-flto", link_flags):
            flags.append("-flto")
        if platform.system().lower() not in ("windows", "darwin") and test_flag(cc, flags, "-fno-plt", link_flags):
            flags.append("-fno-plt")
    flags.extend(args.extra_cflag)
    link_flags.extend(args.extra_ldflag)
    return flags, link_flags


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build link-pdcode C project.")
    parser.add_argument("--cc", help="C compiler command.")
    parser.add_argument("--build-dir", default=str(ROOT / "build"))
    parser.add_argument("--output", help="Output executable path.")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--portable", "--no-native", action="store_true")
    parser.add_argument("--no-lto", action="store_true")
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--show-command", action="store_true")
    parser.add_argument("--extra-cflag", action="append", default=[])
    parser.add_argument("--extra-ldflag", action="append", default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cc = find_compiler(args.cc)
    build_dir = Path(args.build_dir).resolve()
    output = Path(args.output).resolve() if args.output else build_dir / TARGET_NAME
    if args.clean and build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    flags, link_flags = build_flags(args, cc)
    cmd = cc + flags + [str(ROOT / src) for src in SOURCES] + ["-o", str(output)] + link_flags
    print(f"INFO: compiler: {compiler_version(cc).splitlines()[0]}")
    print(f"INFO: output: {output}")
    if args.show_command:
        print(" ".join(shlex.quote(x) for x in cmd))
    proc = subprocess.run(cmd)
    if proc.returncode == 0:
        print(f"INFO: built {output}")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
