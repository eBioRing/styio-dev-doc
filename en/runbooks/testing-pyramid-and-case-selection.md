# Testing Pyramid and Case Selection Runbook

This page answers a common maintainer question: for a given change, which test layer should receive the case?

Styio is not a "just add one case" project. Tests are divided into multiple layers, each with a distinct responsibility.

## Current Test Layers

By maintenance purpose, the current test surface is roughly:

| Layer | Location | Primary purpose |
| --- | --- | --- |
| milestone fixtures | `tests/milestones/` | Freeze language capabilities and CLI executable results |
| five-layer pipeline | `tests/pipeline_cases/` + `tests/styio_test.cpp` | Freeze AST / Styio IR / LLVM IR / output end-to-end |
| unit / diagnostics | `tests/styio_test.cpp` | Precise regression for parser / analyzer / CLI / diagnostics behavior |
| security | `tests/security/styio_security_test.cpp` | Crash, bounds, handle misuse, security semantics |
| soak | `tests/soak/styio_soak_test.cpp` | Long run, RSS growth, repeated execution stability |
| fuzz | `tests/fuzz/` | Unexpected input and parser / lexer robustness |
| docs audit | `scripts/docs-audit.py` + `ctest -L docs` | Documentation and repository reference integrity |

## Selection Rules

### 1. First ask what you need to freeze

| What you need to freeze | Best first layer |
| --- | --- |
| User-visible language output | milestone |
| Intermediate products in the five-layer pipeline | pipeline |
| Specific error code / diagnostic text / shadow artifact | `styio_test.cpp` |
| Resource, handle, memory safety | security |
| Stability after long repeated execution | soak |
| Unstructured abnormal input | fuzz |

### 2. What milestones are good for

Good for:

- whether new syntax ultimately runs
- whether stdout / stderr / side-effect files match expectations
- whether a milestone capability boundary is frozen

Not good for:

- only validating one internal diagnostic string
- only validating a machine-info handshake field
- only validating shadow artifact JSONL details

## What Pipeline Cases Are Good For

Good for:

- changes affecting AST, Styio IR, LLVM IR, and final output at the same time
- freezing intermediate snapshots together
- verifying that lowering is not merely "accidentally producing the right output"

Current examples include:

- `p05_snapshot_accum`
- `p07_instant_pull`
- `p14_stdin_pull`

## What `styio_test.cpp` Is Good For

Good for:

- stable fields in `--machine-info=json`
- invalid `--parser-engine` values
- missing compare flag for `--parser-shadow-artifact-dir`
- `category` / `code` / `subcode` in JSONL diagnostics
- shadow artifact detail / route stats

If you care about CLI contract, diagnostic text, or artifact metadata, write the case here first instead of in milestones.

## What Security Tests Are Good For

Good for:

- extreme lexer inputs
- handle misuse
- runtime helper error boundaries
- AST / session lifecycle safety

The current module explanation is not duplicated here. It is consolidated in:

- `docs/review/2026-03-30/security-tests.md`

## What Soak Tests Are Good For

Good for:

- memory growth boundaries
- high-frequency repeated open / close / concat / read / write
- long-run regressions for fixed bugs
- state inline / stream programs that pass once but fail over time

Default PR lane:

- `soak_smoke`

Heavier nightly lane:

- `soak_deep`

## What Fuzz Tests Are Good For

Good for:

- tokenizer / parser unstructured inputs
- crash, hang, undefined behavior
- seed return flow and failing sample packaging

Current parser fuzz already drives:

- `legacy`
- `nightly`

It no longer fuzzes only legacy.

## Choosing the Oracle

The common oracles are:

| Oracle | Best for |
| --- | --- |
| stdout golden | Normal language feature output |
| stderr golden | Standard error output |
| side-effect file comparison | File resources and redirects |
| intermediate snapshot | AST / Styio IR / LLVM IR |

Do not force an intermediate-product problem into stdout golden just to save effort.

## Minimal Commands

### milestone

```bash
ctest --test-dir build -L milestone --output-on-failure
```

### five-layer pipeline

```bash
ctest --test-dir build -L styio_pipeline --output-on-failure
```

### security

```bash
ctest --test-dir build -L security --output-on-failure
```

### soak smoke

```bash
ctest --test-dir build -L soak_smoke --output-on-failure
```

### fuzz smoke

```bash
ctest --test-dir build-fuzz -L fuzz_smoke --output-on-failure
```

### docs audit

```bash
ctest --test-dir build -L docs --output-on-failure
```

## Common Selection Errors

- Trying to validate JSONL fields with only a milestone.
- Changing lowering without pipeline snapshots.
- Testing resource / handle behavior only through functional examples, not security tests.
- Writing one-shot unit tests for bugs that surface only after long runs.
- Adding one large slow test without a minimal localizing regression.

## Maintenance Rules

Every change should make tests answer two questions:

1. Is the user-visible behavior frozen correctly?
2. Is the most likely regression layer pinned separately?

Answering only the first makes regressions slow to locate. Answering only the second lets language behavior drift.
