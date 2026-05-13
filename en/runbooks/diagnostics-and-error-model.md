# Diagnostics and Error Model Runbook

This page describes a maintainer's first response when diagnosing failures. It is not an end-user manual.

Styio CLI failures are not an undifferentiated stderr blob. They have clear categories, exit codes, and a JSONL diagnostic format.

## Current Error Categories

`src/main.cpp` currently divides failures into four categories:

| Category | code | Exit code |
| --- | --- | --- |
| `LexError` | `STYIO_LEX` | `2` |
| `ParseError` | `STYIO_PARSE` | `3` |
| `TypeError` | `STYIO_TYPE` | `4` |
| `RuntimeError` | `STYIO_RUNTIME` | `5` |

There is also:

- `CliError`: CLI argument error, exit code `6`

The exit code therefore gives an immediate rough location for the failure.

## Diagnostic Output Format

Current supported formats:

- `text`
- `jsonl`

Prefer this format for maintenance and automation:

```bash
./build/bin/styio --error-format jsonl --file some.styio
```

JSONL records currently include at least:

- `category`
- `code`
- `file`
- `message`
- `subcode` in some runtime-error scenarios

## Debugging Order

### 1. First check whether it is a CLI error

These usually include:

- `unsupported --error-format`
- `unsupported --parser-engine`
- `--parser-shadow-artifact-dir requires --parser-shadow-compare`

Inspect the command-line arguments directly. Do not mistake these for parser or analyzer failures.

### 2. If it is `LexError`

Inspect:

- `StyioTokenizer::tokenize`
- corresponding token / string / comment handling

Prefer:

```bash
./build/bin/styio --debug --file some.styio
```

and related security tests:

```bash
ctest --test-dir build -L security --output-on-failure
```

### 3. If it is `ParseError`

Inspect:

- `Parser.cpp`
- `NewParserExpr.cpp`
- `ParserLookahead.*`
- `--parser-engine`
- `--parser-shadow-compare`

Prefer:

```bash
./build/bin/styio --error-format jsonl --styio-ast --file some.styio
```

If the failure relates to dual-track migration, also run:

```bash
./build/bin/styio \
  --parser-engine nightly \
  --parser-shadow-compare \
  --parser-shadow-artifact-dir /tmp/styio-shadow \
  --file some.styio
```

### 4. If it is `TypeError`

Inspect:

- `TypeInfer.cpp`
- `ToStyioIR.cpp`

These errors usually mean:

- the AST is syntactically legal, but semantic constraints failed
- prerequisites for lowering were not met

Prefer:

```bash
./build/bin/styio --error-format jsonl --styio-ast --styio-ir --file some.styio
```

### 5. If it is `RuntimeError`

Inspect:

- `ExternLib.*`
- `CodeGenIO.cpp`
- `StyioJIT_ORC.hpp`

The key value of runtime errors is `subcode`. For example, file-open failure tests currently assert:

- `STYIO_RUNTIME_FILE_OPEN_READ`
- `STYIO_RUNTIME_FILE_OPEN_WRITE`

Prefer:

```bash
./build/bin/styio --error-format jsonl --file some.styio
```

Then use `message` and `subcode` to return to the specific helper.

## Common Debugging Commands

### Machine-readable capability declaration

```bash
./build/bin/styio --machine-info json
```

### AST / IR / LLVM IR observation

```bash
./build/bin/styio --styio-ast --file some.styio
./build/bin/styio --styio-ir --file some.styio
./build/bin/styio --llvm-ir --file some.styio
```

### Default JSONL diagnostics

```bash
./build/bin/styio --error-format jsonl --file some.styio
```

## Existing Regression Entry Points

Existing tests directly related to the diagnostic model include:

- `StyioParserEngine.UnsupportedEngineIsRejected`
- `StyioDiagnostics.RuntimeHelperErrorEmitsJsonlRuntimeDiagnostic`
- `StyioDiagnostics.RuntimeWriteHelperErrorEmitsJsonlRuntimeDiagnostic`
- `StyioDiagnostics.CompoundAssignOnImmutableBindingReportsTypeError`
- `StyioDiagnostics.StreamZipUnsupportedSourceReportsTypeError`
- `StyioDiagnostics.SeriesIntrinsicWindowNonLiteralReportsTypeError`
- `StyioDiagnostics.MalformedStatementPrefixReportsParseErrorWithoutCrash`

Run them directly:

```bash
ctest --test-dir build -R 'Styio(ParserEngine\\.UnsupportedEngineIsRejected|Diagnostics\\.(RuntimeHelperErrorEmitsJsonlRuntimeDiagnostic|RuntimeWriteHelperErrorEmitsJsonlRuntimeDiagnostic|CompoundAssignOnImmutableBindingReportsTypeError|StreamZipUnsupportedSourceReportsTypeError|SeriesIntrinsicWindowNonLiteralReportsTypeError|MalformedStatementPrefixReportsParseErrorWithoutCrash))' --output-on-failure
```

## Common Misdiagnoses

- Treating `CliError` as a parser problem.
- Reading only stderr text and ignoring exit code and `category`.
- Ignoring `subcode` for runtime failures.
- Staring at parser for analyzer errors instead of checking `ToStyioIR.cpp`.

## Maintenance Rules

When adding a failure path, decide at least:

1. which error class it belongs to
2. whether its exit code matches existing classification
3. whether the machine interface needs `subcode`

If these are not clear, later automation and maintenance debugging will degrade.
