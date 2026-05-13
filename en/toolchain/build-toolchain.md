# Build Toolchain

This page records only the toolchain contract required to maintain the `styio` compiler itself.

If you are maintaining `Spio` or `Vityo`, first go to their dedicated development guides. Do not treat this page as a general ecosystem toolchain reference.

## Core Dependencies

According to `CMakeLists.txt` and `THIRD-PARTY.md`, the current primary dependencies are:

| Dependency | Version / form | Purpose |
| --- | --- | --- |
| CMake | `>= 3.14` | Build system |
| C++ compiler | `C++20` | Builds the main project |
| LLVM | `18.1.0+` | IR, ORC JIT, native target |
| Python 3 | `find_package(Python3)` | Generates `styio-nano` profiles |
| ICU | Optional | Unicode and CLI Unicode support |
| GoogleTest | `FetchContent` | C++ tests |
| cxxopts | vendored single header | CLI parsing |

## Key CMake Options

The current remote `nightly` branch exposes these frequently used options:

| Option | Default | Purpose |
| --- | --- | --- |
| `STYIO_USE_ICU` | `OFF` | Enables ICU-backed Unicode |
| `STYIO_BUILD_NANO` | `ON` | Also builds `styio-nano` |
| `STYIO_NANO_OPTIMIZE_FOR_SIZE` | `ON` | Uses size-oriented optimization for `styio-nano` |
| `STYIO_NANO_PROFILE` | `configs/styio-nano-default.toml` | Selects the `styio-nano` profile |

## Build Commands

Standard build:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j
```

Enable ICU:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug -DSTYIO_USE_ICU=ON
cmake --build build -j
```

Disable `styio-nano`:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug -DSTYIO_BUILD_NANO=OFF
cmake --build build -j
```

Use a custom `styio-nano` profile:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug \
  -DSTYIO_NANO_PROFILE=$PWD/configs/styio-nano-default.toml
cmake --build build -j
```

## Main Artifacts

- `build/bin/styio`
- `build/bin/styio-nano`
- `build/bin/styio_test`
- `build/bin/styio_security_test`
- `build/bin/styio_soak_test`

## Current Toolchain Notes

`AGENT-SPEC.md` explicitly calls out several risks:

- source file lists are not auto-discovered
- new `.cpp` files must be added to `CMakeLists.txt` manually
- `styio-nano` profiles are generated during configure, so missing Python 3 blocks configuration
- on some machines, GoogleTest builds may be affected by LLVM / standard-library header conflicts
- `tests/CMakeLists.txt` still includes `docs_audit`, so the documentation tree is part of the formal test surface

Maintenance priority is usually:

1. ensure the `styio` core builds
2. ensure key `ctest` labels run
3. then address platform-specific extra test issues

## Correct Order for Dependency Changes

When changing external dependencies:

1. Update `CMakeLists.txt` or `tests/CMakeLists.txt`.
2. Synchronize `docs/specs/THIRD-PARTY.md`.
3. Synchronize the corresponding page in this manual.
