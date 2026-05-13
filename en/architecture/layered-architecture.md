# Layered Architecture and Responsibilities

The hard part of maintaining Styio is not sheer code size. It is that Styio is a multi-stage compiler chain, and every stage must know what it consumes and what it emits.

## Overall Layers

| Layer | Input | Output | Main files |
| --- | --- | --- | --- |
| CLI / Session | File path, CLI arguments | Compiler flow driver | `src/main.cpp`, `src/StyioSession/CompilationSession.hpp` |
| Tokenizer | Source string | `vector<StyioToken*>` | `src/StyioParser/Tokenizer.*` |
| Parser | Tokens + `StyioContext` | `MainBlockAST*` | `src/StyioParser/Parser.*`, `NewParserExpr.*` |
| AST | Syntax tree nodes | Analyzer input | `src/StyioAST/` |
| Analyzer / Sema | AST | Typed AST + `StyioIR*` | `src/StyioAnalyzer/` |
| Styio IR | Unified intermediate layer | Printable / codegen-ready IR | `src/StyioIR/` |
| LLVM CodeGen | Styio IR | `llvm::Module` / executable entry | `src/StyioCodeGen/` |
| Runtime / JIT | LLVM module + FFI | Actual execution | `src/StyioExtern/`, `src/StyioJIT/` |

## Responsibility Boundaries

### CLI / Session

Responsible for:

- reading files
- parsing CLI arguments
- driving tokenization, parse, type inference, IR lowering, codegen, and JIT in order
- managing the lifecycle of tokens, context, AST, and IR

### Tokenizer

Responsible for:

- maximal-munch tokenization
- mapping symbols to tokens

Not responsible for:

- semantic judgment
- AST structure decisions

### Parser

Responsible for:

- assembling AST from tokens
- selecting between `legacy` and `nightly` paths
- tracking route stats and fallback counts

Not responsible for:

- LLVM details
- final type rules

### Analyzer

Responsible for:

- type inference
- semantic constraints
- AST to Styio IR lowering

This is the real boundary between the syntax world and the execution world.

### Styio IR

Styio IR abstracts AST syntax shape into structures better suited for codegen. Do not bypass this layer casually during maintenance.

### CodeGen

Responsible for:

- LLVM type mapping
- LLVM IR generation
- optimization pass registration
- final ORC JIT invocation

### Runtime / FFI

Responsible for:

- file I/O
- string and numeric bridges
- stderr / stdin standard stream support
- external symbols required by the JIT

## Maintenance Rule of Thumb

If one layer needs to know too many details about another layer, the change is usually being made in the wrong place.
