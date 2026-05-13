# Standard Stream and Resource Capability Change Runbook

This page covers another high-risk change category in Styio: `@stdin`, `@stdout`, `@stderr`, file resources, and handle-related capabilities.

These changes often cross parser, analyzer, codegen, and runtime layers, and they are especially prone to ABI or ownership mismatches.

## First Identify the Layer You Are Changing

| What you are changing | First landing point |
| --- | --- |
| New resource syntax | parser |
| New resource semantic check | analyzer |
| New resource IR node | `IRDecl.hpp` + lowering |
| New standard stream / file behavior | `CodeGenIO.cpp` |
| New external helper / handle semantics | `ExternLib.*` + `StyioJIT_ORC.hpp` |

## Modification Order

### 1. First check whether an AST / IR already exists

Existing resource and standard-stream AST / IR includes:

- `FileResourceAST`
- `StdStreamAST`
- `HandleAcquireAST`
- `ResourceWriteAST`
- `ResourceRedirectAST`
- `InstantPullAST`
- `SIOStdStreamWrite`
- `SIOStdStreamLineIter`
- `SIOStdStreamPull`
- `SGResourceWriteToFile`

If the change is only a semantic extension, prefer reusing these nodes instead of creating a parallel set immediately.

### 2. Change analyzer semantics and lowering

Synchronize at least:

- `src/StyioAnalyzer/ASTAnalyzer.hpp`
- `src/StyioAnalyzer/TypeInfer.cpp`
- `src/StyioAnalyzer/ToStyioIR.cpp`

This step must answer three questions:

- Is this resource expression legal?
- What value type does it produce?
- Which Styio IR should it lower to?

### 3. Change the codegen I/O path

Synchronize at least:

- `src/StyioCodeGen/GetTypeIO.cpp`
- `src/StyioCodeGen/CodeGenIO.cpp`

If pulse / series or generic nodes are involved, also check:

- `CodeGenPulse.cpp`
- `CodeGenG.cpp`

### 4. Change runtime helpers and JIT binding

When adding a helper, synchronize at least:

- `src/StyioExtern/ExternLib.hpp`
- `src/StyioExtern/ExternLib.cpp`
- `src/StyioJIT/StyioJIT_ORC.hpp`

If the change affects handle behavior, also check:

- `src/StyioRuntime/HandleTable.hpp`

Miss one registration and the JIT will fail to find the symbol at runtime.

## Ownership Rules Must Match

Current runtime rules that must not be mixed up:

- `styio_file_read_line` returns a borrowed pointer; do not free it.
- `styio_stdin_read_line` returns a borrowed pointer and returns `nullptr` at EOF.
- `styio_strcat_ab` returns a heap-allocated string and requires `styio_free_cstr`.
- `styio_i64_dec_cstr` / `styio_f64_dec_cstr` return borrowed buffers.

One wrong codegen assumption about these rules can cause a leak, dangling reference, or double free.

## Minimum Validation Commands

### stdout / stderr

```bash
ctest --test-dir build -R '^m9_' --output-on-failure
```

### stdin

```bash
ctest --test-dir build -R '^m10_' --output-on-failure
```

### File resources and side effects

```bash
ctest --test-dir build -R '^m5_' --output-on-failure
```

### Pipeline resource loop

```bash
ctest --test-dir build -L styio_pipeline --output-on-failure
```

### Inspect lowering directly

```bash
./build/bin/styio --styio-ir --file tests/milestones/m10/t02_stdin_pull.styio
```

## Common Omissions

- Analyzer emits a new IR node, but `CodeGenIO.cpp` does not handle it.
- Runtime helper is implemented, but `StyioJIT_ORC.hpp` does not register it.
- Helper return ownership changed, but codegen release strategy did not.
- Only stdout was tested, not stderr / stdin / file paths.
- Resource design document changed, but implementation and tests did not.

## Documentation Synchronization Rules

Resource or standard-stream changes must synchronize at least:

- `docs/design/Styio-Symbol-Reference.md`
- `docs/design/Styio-Resource-Driver.md`
- `docs/design/Styio-Language-Design.md` when needed
- [Resources, `@`, and Standard Streams](../language/resources-and-stdio.md)

If you are only updating today's implementation boundary, do not describe future plugin targets as already supported.
