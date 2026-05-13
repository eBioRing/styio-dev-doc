# Analyzer Manual

Analyzer is Styio's real semantic boundary layer. It performs type inference and lowers AST into Styio IR.

## Role Boundary

The Analyzer layer is responsible for:

- type inference
- semantic constraints
- AST to Styio IR lowering
- propagation of certain pulse / state planning information

The Analyzer layer is not responsible for:

- token or syntax decisions
- LLVM IR details
- FFI symbol binding

## Main Interface

File: `src/StyioAnalyzer/ASTAnalyzer.hpp`

Key object: `StyioAnalyzer`

The two most important steps are:

```cpp
analyzer.typeInfer(ast);
StyioIR* ir = analyzer.toStyioIR(ast);
```

`main.cpp` drives the compiler in exactly this order.

## Visitor Surface

The template type list of `StyioAnalyzerVisitor` is effectively the AST surface the analyzer currently recognizes.

This means:

- if a new AST node is not registered here, the analyzer cannot see it
- you must add both `typeInfer(Node*)`
- and `toStyioIR(Node*)`

These two lists are important interfaces, not declaration noise.

## State Fields

Important visible state in `StyioAnalyzer` includes:

| Field / method | Purpose |
| --- | --- |
| `func_defs` | Records function definitions |
| `local_binding_types` | Local binding type table |
| `cur_pulse_plan()` / `set_cur_pulse_plan(...)` | Current pulse plan |
| `active_series_slot()` / `set_active_series_slot(...)` | Current series slot |
| `set_post_pulse_hist_context(...)` | Post-pulse history context |
| `is_snapshot_var(...)` | Checks whether a variable is a snapshot |

These fields explain why the analyzer is not a pure visitor. It is a context-carrying lowering engine.

## Real Responsibilities of `toStyioIR`

`ToStyioIR.cpp` shows that this layer is not a trivial AST translation. It also:

- supplies fallback function return types
- detects state / pulse related patterns
- generates `SIOStdStreamWrite`, `SIOStdStreamLineIter`, and `SIOStdStreamPull`
- builds IR for iterator / stream zip / snapshot / instant pull paths
- decides some match IR shapes

Many answers to "how does this language behavior really land" are in `ToStyioIR.cpp`, not the parser.

## Current Key Lowering Examples

### Standard stream write

`ResourceWriteAST` / `ResourceRedirectAST` lower to:

- `SIOStdStreamWrite`
- or `SGResourceWriteToFile`

### stdin iteration

`@stdin >> #(line) => {...}` lowers to:

- `SIOStdStreamLineIter`

### stdin instant pull

`(<< @stdin)` lowers to:

- `SIOStdStreamPull`

## Minimum Synchronization Scope When Changing Analyzer

### New AST node

- `ASTAnalyzer.hpp`
- `TypeInfer.cpp`
- `ToStyioIR.cpp`
- new `StyioIR` node definition
- related `ToStringVisitor`

### New semantic constraint

Do not only add a local error in `TypeInfer.cpp`. Also check:

- whether lowering branches are affected
- whether milestone semantic-error cases are affected
- whether `Symbol-Reference` / `Language-Design` need updates

### New IR node

At minimum synchronize:

- `IRDecl.hpp`
- `GenIR.hpp` or `IOIR.hpp`
- `ASTAnalyzer.hpp`
- `ToStyioIR.cpp`
- `CodeGenVisitor.hpp`
- concrete codegen files

## Maintenance Principles

- Leave syntax questions to the parser.
- Leave execution questions to codegen and runtime.
- Analyzer's job is to turn "syntactically writable" into "semantically executable".
