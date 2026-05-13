# Language and Design SSOT Map

This page tells maintainers what each design document owns.

## Primary Design Documents

| Document | Responsibility |
| --- | --- |
| `Styio-Language-Design.md` | Overall language semantics |
| `Styio-EBNF.md` | Formal grammar |
| `Styio-Symbol-Reference.md` | Symbol-to-token quick reference and semantic summary |
| `Styio-StdLib-Intrinsics.md` | `[op, n]` intrinsic specifications |
| `Styio-Resource-Driver.md` | Resource driver interface goals |
| `Styio-Resource-Topology.md` | `@` and resource topology target design |

## How to Use These Documents

### When changing syntax

Read first:

- `EBNF`
- `Symbol-Reference`
- `Language-Design`

### When changing an intrinsic

Read first:

- `StdLib-Intrinsics`
- corresponding analyzer / codegen implementation

### When changing resources or standard streams

Read first:

- `Language-Design`
- `Symbol-Reference`
- `Resource-Topology`
- current milestones and tests

## Documents That Require Careful Interpretation

Pay special attention to:

- `Resource-Topology.md` includes target design. It does **not** mean the design is fully implemented today.
- `Resource-Driver.md` is also an interface target document and should not be treated as proof that a plugin system already exists in code.

Correct practice:

- read `docs/design/` for design boundaries
- read `src/` and `tests/` for current implementation boundaries

## Requirements for GitBook

GitBook should not repeat another long semantic specification. It should:

- tell maintainers where authoritative definitions live
- tell maintainers which designs are implemented and which are still goals
- organize these entry points without changing the framework
