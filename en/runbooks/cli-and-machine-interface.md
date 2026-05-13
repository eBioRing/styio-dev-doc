# CLI and Machine Interface Change Runbook

This page targets the `src/main.cpp` entry chain, not general language feature changes.

If you change CLI arguments, exit codes, JSONL diagnostics, or the `--machine-info=json` handshake, this page is the minimum loop. Surfaces consumed cross-repository by `Spio`, `Vityo`, or extensions are grouped under `styio-protocol`.

## Current CLI Contract

`main.cpp` currently owns:

- argument parsing
- file reading
- `Lex -> Parse -> TypeInfer -> StyioIR -> LLVM IR -> JIT` driving
- diagnostic classification and exit codes
- `machine-info` output
- parser shadow compare and artifact writing

This means a CLI change is usually not "just one help-text line". It often affects:

- automation scripts
- test assertions
- documentation manuals

## What Counts as CLI / Machine Interface Change

Includes:

- adding or modifying CLI flags
- `styio-nano` packaging / profile related flags
- `--machine-info=json` field changes
- `--error-format` behavior changes
- exit code changes
- diagnostic `category` / `code` / `subcode` changes
- parser shadow artifact parameter changes

## What Not to Change

- Do not modify `src/include/cxxopts.hpp`.

CLI behavior should be adjusted through `main.cpp` configuration and local logic, not by changing the vendored argument library.

## Modification Order

### 1. Change argument definition and constraints first

Synchronize at least:

- `options.add_options()` in `src/main.cpp`
- argument validity checks

Existing constraints include:

- `--error-format` only accepts `text|jsonl`
- `--machine-info` only accepts `json`
- `--parser-engine` only accepts `legacy|nightly`, with `new` as a compatibility alias
- `--parser-shadow-artifact-dir` requires `--parser-shadow-compare`
- `--nano-create` and `--nano-publish` are mutually exclusive
- `styio-nano` packaging arguments must appear with `--nano-create` or `--nano-publish`

### 2. Then change output contracts

Synchronize at least:

- `styio_emit_machine_info_json()`
- `styio_emit_diagnostic(...)`
- `styio_exit_code(...)`

If changing a machine interface, decide first whether existing consumers will break.

### 3. If parser shadow is involved, inspect artifact writing

Synchronize at least:

- `styio_parse_engine_to_repr_latest(...)`
- `styio_write_shadow_artifact_latest(...)`

These changes directly affect:

- `.jsonl` artifacts
- primary / shadow AST payloads
- route detail text

### 4. Add tests and documentation last

Synchronize at least:

- `tests/styio_test.cpp`
- this manual
- [CLI and Debugging Workflow](../toolchain/cli-and-debug-workflow.md)
- [Diagnostics and Error Model Runbook](diagnostics-and-error-model.md) if the error model changed

## Stable Surface of `--machine-info=json`

Current tests assert at least these fields:

- `"tool":"styio"`
- `"compiler_version":"0.0.1"`
- `"channel":"stable"`
- `"supported_contracts":{"compile_plan":[1]}`
- `"machine_info_json"`
- `"single_file_entry"`
- `"jsonl_diagnostics"`
- `"edition_max":"2026"`

Changing these fields requires a clear compatibility reason and synchronized tests.

Two public boundaries are easy to get wrong:

- full `styio` should currently advertise `supported_contracts.compile_plan:[1]`
- nano / non-full profiles still must not pretend to have a compile-plan consumer

Compile-plan executability therefore depends on profile, machine-info, and consuming-repository compatibility matrix all being true.

`styio-protocol` describes these stable consumable machine boundaries. It is not a `styio` service suite that tool repositories can link.

## Minimal Commands

### machine-info handshake

```bash
./build/bin/styio --machine-info json
```

### default CLI run

```bash
./build/bin/styio --file tests/milestones/m1/t01_int_arith.styio
```

### JSONL diagnostics

```bash
./build/bin/styio --error-format jsonl --file some.styio
```

### shadow argument constraint

```bash
./build/bin/styio \
  --parser-engine legacy \
  --parser-shadow-artifact-dir /tmp/styio-shadow \
  --file tests/milestones/m1/t01_int_arith.styio
```

This command should currently report `CliError` because `--parser-shadow-compare` is missing.

## Existing Regression Entry Points

Directly related tests include:

- `StyioDiagnostics.MachineInfoJsonReportsStableHandshakeFields`
- `StyioParserEngine.UnsupportedEngineIsRejected`
- `StyioParserEngine.ShadowArtifactDirRequiresShadowCompareFlag`
- `StyioDiagnostics.RuntimeHelperErrorEmitsJsonlRuntimeDiagnostic`
- `StyioDiagnostics.RuntimeWriteHelperErrorEmitsJsonlRuntimeDiagnostic`

Run them directly:

```bash
ctest --test-dir build -R '^(StyioDiagnostics\\.MachineInfoJsonReportsStableHandshakeFields|StyioParserEngine\\.(UnsupportedEngineIsRejected|ShadowArtifactDirRequiresShadowCompareFlag)|StyioDiagnostics\\.(RuntimeHelperErrorEmitsJsonlRuntimeDiagnostic|RuntimeWriteHelperErrorEmitsJsonlRuntimeDiagnostic))$' --output-on-failure
```

## Common Omissions

- Help text changed, but argument validation did not.
- Exit code changed without updating diagnostic tests.
- `machine-info` field changed without updating stable handshake assertions.
- Shadow artifact field changed without updating related parser tests.
- Documentation only updated the CLI page, but not the error model page.

## Maintenance Rules

CLI / machine interface changes must satisfy three conditions:

1. humans can still understand the terminal behavior
2. machine interfaces remain stable to consume
3. exit codes and error categories remain predictable on failure

Only satisfying the first is not maintainable. Only satisfying the second is not usable enough.
