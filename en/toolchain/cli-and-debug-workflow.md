# CLI and Debugging Workflow

This page only covers the `styio` compiler CLI and debugging workflow.

When maintaining Styio, the CLI is not a secondary feature for terminal users. It is the most direct observation window into the compiler. Command surfaces and debugging workflows for `Spio` and `Vityo` belong in their own development guides.

## Minimal Run

```bash
./build/bin/styio --file tests/milestones/m1/t01_int_arith.styio
```

During local verification on 2026-04-12, this command printed:

```text
10
```

## Common CLI Arguments

| Argument | Purpose |
| --- | --- |
| `--file <path>` | Compile and execute a `.styio` file |
| `--styio-ast` | Print AST before and after type inference |
| `--styio-ir` | Print Styio IR |
| `--llvm-ir` | Print LLVM IR |
| `--debug` | Emit more debug information |
| `--error-format text|jsonl` | Diagnostic format |
| `--machine-info json` | Emit machine-readable capability information |
| `--parser-engine legacy|nightly` | Select the parser |
| `--parser-shadow-compare` | Compare both parser paths |
| `--parser-shadow-artifact-dir <dir>` | Write shadow artifacts |
| `--nano-create` / `--nano-publish` | Materialize / publish `styio-nano` packages |

## Recommended Debugging Paths

### Inspect lexer / parser

```bash
./build/bin/styio --styio-ast --file tests/milestones/m9/t01_stdout_string.styio
```

### Inspect IR lowering

```bash
./build/bin/styio --styio-ir --file tests/milestones/m10/t01_stdin_echo.styio
```

### Inspect LLVM generation

```bash
./build/bin/styio --llvm-ir --file tests/milestones/m2/t01_simple_func.styio
```

### Inspect parser dual-track differences

```bash
./build/bin/styio \
  --parser-shadow-compare \
  --parser-shadow-artifact-dir /tmp/styio-shadow \
  --file tests/milestones/m7/t04_instant_pull.styio
```

## Diagnostic Format

The current CLI supports:

- `text`
- `jsonl`

Prefer the machine-interface format for automation:

```bash
./build/bin/styio --error-format jsonl --file some.styio
```

## Realities Around `styio-nano`

The current remote `nightly` branch has merged `styio-nano` packaging commands into the full compiler CLI.

Keep these boundaries in mind:

- `--nano-create` / `--nano-publish` are only available in full `styio`.
- `styio-nano` itself may disable `--machine-info` by profile.
- `styio-nano` itself may disable `--debug` by profile.
- `styio-nano` itself may disable `--styio-ast` / `--styio-ir` / `--llvm-ir` by profile.
- `styio-nano` itself may disable `--parser-engine` / shadow compare by profile.

When maintaining CLI behavior, do not assume every flag available in the full compiler is also available in `styio-nano`.

## Realities Maintainers Must Remember

- The default parser is already `nightly`.
- Shadow compare is not an experiment; it is a key safety net for the current parser migration.
- The CLI entry point is part of both testing and documentation. Argument changes must be synchronized into documentation.

## Continue Reading

- [CLI and Machine Interface Change Runbook](../runbooks/cli-and-machine-interface.md)
- [Diagnostics and Error Model Runbook](../runbooks/diagnostics-and-error-model.md)
- [Parser Shadow and Dual-Track Migration Runbook](../runbooks/parser-shadow-and-dual-track.md)
