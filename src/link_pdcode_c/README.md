# link_pdcode_c

Standalone C11 project for converting a closed polygonal 3D knot into a
KnotTheory/Sage-style compact PD_CODE.

Input is one closed component with `n` vertices. The final vertex is connected
back to the first. The command-line tool reads:

```text
n
x0 y0 z0
x1 y1 z1
...
```

and writes a compact Python-style PD list such as:

```text
[[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
```

## Build

```sh
python src/link_pdcode_c/build.py
```

The script finds a C compiler automatically from `--cc`, `CC`, then common
names such as `gcc`, `clang`, and `cc`. Default release flags are `-O3` and
`-DNDEBUG`; the script probes optional flags such as `-march=native` and
`-flto` before using them. Use `--portable` to disable native CPU flags.

## Test

```sh
python src/link_pdcode_c/test.py --rebuild
```

The tests cover unknot/no-crossing input, a one-crossing projection, sample
data parsing, wrapper compatibility, and PD label validity.

## Notes

The old project kept a Linux/x86_64-oriented `knot-pdcode` binary path behind a
Python wrapper. This project replaces that path with portable C source and a
deterministic projection search.

The implementation follows the same compact PD-code convention as the bundled
Python/C++ projection pipeline and can be validated independently.
