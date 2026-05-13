# New Intrinsic Change Runbook

This page covers the maintenance loop for compiler intrinsics. In this context, an intrinsic is not a normal function call; it is syntax recognized directly by the compiler and lowered inline.

## Distinguish Design Documents from Current Implementation

`docs/design/Styio-StdLib-Intrinsics.md` records a broader target surface. Based on the current published mainline and active implementation, the primary path that currently lowers directly from AST to IR / codegen is the **series intrinsic** chain.

The current source directly confirms these implementation surfaces:

- AST: `SeriesIntrinsicAST`
- operation enum: `SeriesIntrinsicOp::{Avg, Max}`
- state slot kind: `SGStateSlotKind::{WinAvg, WinMax}`
- IR: `SGSeriesAvgStep`, `SGSeriesMaxStep`
- codegen: `GetTypeG.cpp`, `CodeGenPulse.cpp`

If you are documenting other algorithms from `StdLib-Intrinsics`, do not assume that "present in the specification" means "supported by the compiler today".

## Scope

This page applies to:

- adding a `[op, n]` intrinsic
- changing window semantics for an existing series intrinsic
- changing intrinsic handling of `@`
- changing intrinsic pulse ledger layout or lowering

## Current Real Entry Points

| Layer | Entry |
| --- | --- |
| AST | `SeriesIntrinsicAST` in `src/StyioAST/AST.hpp` |
| Analyzer | `src/StyioAnalyzer/TypeInfer.cpp`, `src/StyioAnalyzer/ToStyioIR.cpp` |
| IR | `src/StyioIR/IRDecl.hpp`, `src/StyioIR/GenIR/GenIR.hpp` |
| CodeGen | `src/StyioCodeGen/GetTypeG.cpp`, `src/StyioCodeGen/CodeGenPulse.cpp` |

## Modification Order

### 1. Decide whether this is parser syntax or an extension of an existing intrinsic

If the change extends the existing `[avg, n]` / `[max, n]` path, prefer reusing `SeriesIntrinsicAST`.

If a new selector syntax is required, also synchronize:

- parser recognition path
- `docs/design/Styio-Symbol-Reference.md`
- `docs/design/Styio-EBNF.md`

### 2. Extend AST enum and node

Synchronize at least:

- `src/StyioAST/AST.hpp`
- `src/StyioToken/Token.hpp` when needed
- `src/StyioToString/ToStringVisitor.hpp`
- `src/StyioToString/ToString.cpp`

Current `SeriesIntrinsicOp` has only:

- `Avg`
- `Max`

New operations start here.

### 3. Change analyzer state-slot classification and lowering

Synchronize at least:

- `src/StyioAnalyzer/TypeInfer.cpp`
- `src/StyioAnalyzer/ToStyioIR.cpp`

There are three hard rules:

- `window size for series intrinsic must be integer literal`
- `series intrinsic needs enclosing state slot`
- non-accumulating state must still satisfy the existing `@[n]` header rule

An intrinsic is not an isolated expression. It depends by default on an enclosing state slot and pulse plan.

### 4. Change IR and ledger layout

Synchronize at least:

- `src/StyioIR/IRDecl.hpp`
- `src/StyioIR/GenIR/GenIR.hpp`

If the new intrinsic needs a new state-slot layout, also synchronize analyzer logic:

- `classify_state_slot(...)`
- `slot_byte_size(...)`

Otherwise analyzer and codegen will disagree about ledger layout.

### 5. Change the codegen pulse path

Synchronize at least:

- `src/StyioCodeGen/GetTypeG.cpp`
- `src/StyioCodeGen/CodeGenPulse.cpp`

`CodeGenPulse.cpp` currently owns:

- pulse ledger / snapshot reads and writes
- warm-up `@` behavior
- LLVM IR generation for `WinAvg` / `WinMax`

If you add an intrinsic but do not add `toLLVMIR` here, the frontend recognizes it but the backend cannot execute it.

## Minimum Validation Commands

### Check AST recognition

```bash
./build/bin/styio --styio-ast --file tests/milestones/m6/t03_window_avg.styio
```

### Check Styio IR lowering

```bash
./build/bin/styio --styio-ir --file tests/milestones/m6/t03_window_avg.styio
```

### Check LLVM IR

```bash
./build/bin/styio --llvm-ir --file tests/milestones/m6/t02_running_max.styio
```

### Run M6 milestone

```bash
ctest --test-dir build -R '^m6_' --output-on-failure
```

### Run non-literal window diagnostic

```bash
ctest --test-dir build -R 'SeriesIntrinsicWindowNonLiteralReportsTypeError' --output-on-failure
```

## Common Omissions

- Only `StdLib-Intrinsics` was changed, but compiler implementation was not.
- AST supports a new op, but `classify_state_slot(...)` is missing.
- IR node is declared, but `GetTypeG.cpp` / `CodeGenPulse.cpp` are missing.
- Warm-up `@` behavior is forgotten.
- Non-literal window size is silently accepted, breaking the diagnostic contract.

## Documentation Synchronization Rules

Intrinsic semantic changes must synchronize at least:

- `docs/design/Styio-StdLib-Intrinsics.md`
- `docs/design/Styio-Language-Design.md` when needed
- `Styio-EBNF.md` and `Styio-Symbol-Reference.md` when syntax changes
