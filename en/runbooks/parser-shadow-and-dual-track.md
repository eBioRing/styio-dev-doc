# Parser Shadow and Dual-Track Migration Runbook

This page serves parser migration maintainers only. It is not about "how to write a parser"; it is about keeping the repository healthy while `legacy` and `nightly` parser paths coexist.

## Current Dual-Track Contract

Styio's parser naming and entry points are explicit:

- `legacy`: old path
- `nightly`: new path and current default
- `latest`: unified entry

`src/main.cpp` currently drives parser execution through:

- `parse_main_block_with_engine_latest(...)`

It does not call `parse_main_block_legacy(...)` directly.

## What Shadow Compare Does

Enable it with:

```bash
./build/bin/styio \
  --parser-shadow-compare \
  --parser-shadow-artifact-dir /tmp/styio-shadow \
  --file some.styio
```

Current behavior:

1. Run the primary parser and produce AST repr.
2. Run the other parser path.
3. Compare AST repr.
4. Write an artifact.

Possible statuses include:

- `match`
- `mismatch`
- `shadow_error`

## Meaning of Route Stats

When the primary parser is `nightly`, current stats record:

- `nightly_subset_statements`
- `legacy_fallback_statements`
- `nightly_internal_legacy_bridges`

This is not debug noise. It is a migration KPI.

The maintenance goals are:

- fewer fallbacks
- fewer internal legacy bridges
- strict zero values where gates require them

## Artifact Contents

When `--parser-shadow-artifact-dir` is configured, the current implementation writes:

- one `.jsonl` metadata record
- source payload for mismatch / error cases
- primary AST text
- shadow AST text
- shadow error text

For `match`, it usually keeps only the metadata record.

## When Shadow Must Run

Run shadow by default for changes to:

- `Parser.cpp`
- `NewParserExpr.cpp`
- `ParserLookahead.*`
- `Parser.hpp`
- parser routing logic
- subset coverage extension

If you changed parser code and did not run shadow compare, the change loop is incomplete.

## Minimal Commands

### Single-file shadow compare

```bash
./build/bin/styio \
  --parser-engine nightly \
  --parser-shadow-compare \
  --parser-shadow-artifact-dir /tmp/styio-shadow \
  --file tests/milestones/m7/t04_instant_pull.styio
```

### Legacy primary path comparison

```bash
./build/bin/styio \
  --parser-engine legacy \
  --parser-shadow-compare \
  --parser-shadow-artifact-dir /tmp/styio-shadow \
  --file tests/milestones/m1/t01_int_arith.styio
```

### CTest shadow gate

```bash
ctest --test-dir build -L shadow_gate --output-on-failure
```

### Legacy entry audit

```bash
ctest --test-dir build -R '^parser_legacy_entry_audit$' --output-on-failure
```

### Parser migration checks in checkpoint-health

```bash
./scripts/checkpoint-health.sh --no-asan --no-fuzz
```

## What the Gate Script Really Checks

`scripts/parser-shadow-suite-gate.sh` currently:

- runs every `t*.styio` under the suite with both `legacy` and `nightly`
- forces shadow compare on
- collects artifacts
- counts `match` / `mismatch` / `shadow_error`
- optionally requires zero fallback
- optionally requires zero internal bridges

If the suite contains `shadow-expected-nonzero.txt`, the script treats those cases as an allowed-failure manifest instead of ordinary regressions.

## What Legacy Entry Audit Checks

`scripts/parser-legacy-entry-audit.sh` guards three things:

1. `parse_main_block_legacy(...)` must not be called directly outside parser core.
2. `src/StyioTesting` must remain nightly-first and must not secretly depend on legacy routing again.
3. `src/main.cpp` must continue converging through `parse_main_block_with_engine_latest(...)`.

This is an architecture constraint, not only a grep script.

## Existing Regression Entry Points

Directly related checks include:

- `parser_shadow_gate_m1_zero_fallback_and_internal_bridges`
- `parser_shadow_gate_m2_zero_fallback_and_internal_bridges`
- `parser_shadow_gate_m5_dual_zero_expected_nonzero`
- `parser_shadow_gate_m7_zero_fallback`
- `parser_shadow_gate_m7_zero_internal_bridges`
- `parser_legacy_entry_audit`
- `StyioParserEngine.DefaultEngineIsNightlyInShadowArtifact`
- `StyioParserEngine.ShadowCompareWritesArtifactRecordWhenDirConfigured`

Run them directly:

```bash
ctest --test-dir build -R '^(parser_shadow_gate_.*|parser_legacy_entry_audit|StyioParserEngine\\.(DefaultEngineIsNightlyInShadowArtifact|ShadowCompareWritesArtifactRecordWhenDirConfigured))$' --output-on-failure
```

## Common Omissions

- New subset is implemented, but route stats still show fallback.
- `nightly` secretly bridges back into `legacy` and no one treats it as a problem.
- `--parser-shadow-artifact-dir` is set without `--parser-shadow-compare`.
- Tests or tools directly reintroduce `parse_main_block_legacy(...)`.
- Only command success is checked, not route detail inside artifacts.

## Maintenance Rules

Dual-track migration is not "nightly can run, so it is done". It must keep reducing:

- fallback
- internal legacy bridge
- direct legacy entry points

As long as these numbers do not converge, the migration is not complete.
