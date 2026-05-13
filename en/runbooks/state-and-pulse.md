# State / Pulse / Snapshot Change Runbook

This page covers another core Styio maintenance chain: `@[...]` state, `$ref`, history probe, snapshot, instant pull, and their shared pulse ledger mechanism.

## Core Facts of This Chain

Styio state capabilities are not isolated syntax fragments. They form a linked implementation:

- parser emits state-related AST
- analyzer builds `SGPulsePlan`
- lowering emits state / snapshot / pull IR
- codegen executes through pulse ledger and frame snapshot

Changing only one layer usually breaks frame lock, history, or snapshot consistency.

## Scope

This page applies to:

- `@[n](...)` or `@[name = ...](...)` state semantics
- `$name` snapshot reads
- `$name[<<, n]` history probe
- `@[name] << @resource` snapshot declarations
- `(<< @resource)` instant pull
- pulse ledger layout, frame lock, and post-pulse history

## Current Source Entry Points

| Layer | Entry |
| --- | --- |
| AST | `StateDeclAST`, `StateRefAST`, `HistoryProbeAST`, `SnapshotDeclAST`, `InstantPullAST` |
| Analyzer state | `cur_pulse_plan()`, `active_series_slot()`, `set_post_pulse_hist_context(...)` |
| IR | `SGStateSnapLoad`, `SGStateHistLoad`, `SGSnapshotDecl`, `SGInstantPull` |
| CodeGen | `CodeGenG.cpp`, `CodeGenIO.cpp`, `CodeGenPulse.cpp` |

## Modification Order

### 1. Identify which state capability is changing

| Capability | Focus |
| --- | --- |
| state accumulation / tracking | state slot classification and commit rules |
| history probe | pulse plan, history ring, depth semantics |
| snapshot | shadow variable registration and frame lock |
| instant pull | analyzer resource restrictions and I/O lowering |

Classify the change before editing code. Do not treat snapshot, history, and instant pull as the same thing.

### 2. Change analyzer semantic boundaries

Synchronize at least:

- `src/StyioAnalyzer/TypeInfer.cpp`
- `src/StyioAnalyzer/ToStyioIR.cpp`

Existing constraints must remain intact:

- history probes are only allowed in a pulse body or after a foreach / file line iterator with pulse
- lowering for `StateRefAST` / `HistoryProbeAST` depends on slot mapping in the pulse plan
- instant pull restricts resource types, for example rejecting reads from `@stdout` / `@stderr`

### 3. Change pulse plan and slot layout

Check at least:

- `find_series_intrinsic(...)`
- `classify_state_slot(...)`
- `slot_byte_size(...)`

These determine:

- whether current state is `Acc`, `Track`, or a windowed slot
- how many bytes the ledger must allocate
- offsets for history ring and snapshot reads / writes

### 4. Change the codegen pulse path

Synchronize at least:

- `src/StyioCodeGen/CodeGenPulse.cpp`
- `src/StyioCodeGen/CodeGenG.cpp`
- `src/StyioCodeGen/CodeGenIO.cpp` when needed

Current pulse codegen owns:

- copying ledger to snapshot
- stable `$ref` reads within a frame
- history ring reads and writes
- post-loop history ledger-region access
- snapshot shadow reload

If this layer is wrong, the most direct symptom is unstable `$ref` reads in the same pulse or incorrect history depth.

### 5. Inspect snapshot / instant pull with the resource path

Related changes must synchronize at least:

- `src/StyioAnalyzer/ToStyioIR.cpp`
- `src/StyioCodeGen/CodeGenIO.cpp`
- `src/StyioCodeGen/CodeGenG.cpp`

Representative samples:

- `tests/milestones/m7/t03_snapshot.styio`
- `tests/milestones/m7/t06_snapshot_lock.styio`
- `tests/milestones/m7/t09_snapshot_accum.styio`
- `tests/pipeline_cases/p05_snapshot_accum/input.styio`
- `tests/pipeline_cases/p07_instant_pull/input.styio`
- `tests/pipeline_cases/p14_stdin_pull/input.styio`

## Minimum Validation Commands

### Run state / history milestones

```bash
ctest --test-dir build -R '^m6_' --output-on-failure
```

### Run snapshot / instant pull milestones

```bash
ctest --test-dir build -R '^m7_' --output-on-failure
```

### Inspect history lowering

```bash
./build/bin/styio --styio-ir --file tests/milestones/m6/t04_history.styio
```

### Inspect snapshot lowering

```bash
./build/bin/styio --styio-ir --file tests/milestones/m7/t09_snapshot_accum.styio
```

### Run pipeline regressions

```bash
ctest --test-dir build -R 'StyioFiveLayerPipeline.P05_snapshot_accum|StyioFiveLayerPipeline.P07_instant_pull|StyioFiveLayerPipeline.P14_stdin_pull' --output-on-failure
```

### Run state inline regressions

```bash
ctest --test-dir build -R 'SingleArgStateFunctionInliningUsesCallArgument|BlockStateFunctionInliningUsesCallArgument|StateInlineMatchCasesFunctionUsesCallArgument|StateInlineInfiniteLiteralFunctionUsesCallArgument' --output-on-failure
```

## Common Omissions

- State semantics changed, but pulse ledger byte layout was not synchronized.
- History probe works only in the current pulse, but the post-pulse path is missing.
- Snapshot can be read, but multiple reads in one frame are inconsistent.
- Instant pull was tested only for `@file`, not `@stdin`.
- State inline helper regression was not run, causing function-argument substitution to regress again.

## Documentation Synchronization Rules

This class of change must synchronize at least:

- `docs/design/Styio-Language-Design.md`
- `docs/design/Styio-Symbol-Reference.md`
- `docs/design/Styio-Resource-Driver.md` if resource pulling is involved

If only today's implementation boundary changed, do not treat future resource topology targets as currently stable support.
