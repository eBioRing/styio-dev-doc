# Source Tree Map

This project has many directories, but the areas maintainers read most often are concentrated.

## Top-Level Directories

| Directory | How to understand it |
| --- | --- |
| `src/` | Compiler, CLI, IR, and JIT implementation |
| `tests/` | Regression safety net; critical for reading currently implemented behavior |
| `sample/` | Minimal runnable examples and scripts |
| `docs/` | Internal design, specifications, ADRs, and milestones in the main repository |
| `scripts/` | Documentation audit, parser gates, and regression tools |
| `templates/` | Documentation workflow templates, not compiler core logic |

## Key Subdirectories Under `src/`

| Directory | Responsibility |
| --- | --- |
| `StyioToken` | Tokens, node types, and base enums |
| `StyioParser` | Tokenizer, parser, lookahead, parser subpaths |
| `StyioAST` | AST node definitions |
| `StyioAnalyzer` | Type inference, semantic checks, IR lowering |
| `StyioIR` | Styio IR node hierarchy |
| `StyioCodeGen` | LLVM codegen and type mapping |
| `StyioExtern` | External functions called by the JIT |
| `StyioJIT` | ORC JIT wrapper layer |
| `StyioTesting` | Five-layer pipeline check helpers |
| `Deprecated` | Historical code; reference only, do not extend |

## High-Value Areas Under `tests/`

| Directory | Purpose |
| --- | --- |
| `tests/milestones/` | Frozen samples for staged capabilities |
| `tests/pipeline_cases/` | Five-layer pipeline comparison samples |
| `tests/security/` | Lexer / FFI / boundary safety tests |
| `tests/soak/` | Long-running single-thread regression |
| `tests/fuzz/` | Fuzz entry points and corpus |
| `tests/lit_cases/` | Fine-grained parsing / codegen fixtures |

## High-Value Areas Under `docs/`

| Directory | Purpose |
| --- | --- |
| `docs/design/` | Language and compiler design SSOT |
| `docs/specs/` | Repository boundaries, documentation policy, dependency notes |
| `docs/milestones/` | Frozen milestone descriptions |
| `docs/adr/` | Key architecture decision records |
| `docs/plans/` | Plans and roadmaps; not necessarily current reality |

## If You Add a New Syntax Point

You will probably touch these areas:

- `src/StyioToken/`
- `src/StyioParser/`
- `src/StyioAST/`
- `src/StyioAnalyzer/`
- `src/StyioIR/`
- `src/StyioCodeGen/`
- `tests/`
- `docs/design/`

Styio is not a "change one file and done" architecture. Language-surface changes usually pass through the entire chain.
