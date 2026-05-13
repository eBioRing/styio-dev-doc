# Compiler Pipeline

If you are reading the `styio` source for the first time, the best entry point is not a specific `.cpp` file. First memorize the pipeline.

## Current Main Path

```text
Source (.styio)
  -> Tokenizer
  -> Parser
  -> Type Inference / Semantic Analysis
  -> Styio IR Lowering
  -> LLVM IR CodeGen
  -> ORC JIT Execution
```

## Modules by Stage

| Stage | Main directory | Notes |
| --- | --- | --- |
| Lexing | `src/StyioParser/Tokenizer.*` | Tokenizes source |
| Parsing | `src/StyioParser/Parser.*`, `ParserLookahead.*`, `NewParserExpr.*` | Hand-written recursive descent parser; defaults to `nightly` |
| AST | `src/StyioAST/` | Syntax tree node definitions |
| Semantic analysis | `src/StyioAnalyzer/` | Type inference, semantic checks, AST to Styio IR |
| Intermediate representation | `src/StyioIR/` | Compiler-owned IR layer |
| LLVM code generation | `src/StyioCodeGen/` | Styio IR to LLVM IR |
| Runtime bridge | `src/StyioExtern/`, `src/StyioJIT/` | FFI symbol registration and ORC JIT |
| CLI entry | `src/main.cpp` | Argument parsing and pipeline driver |

## How to Observe Each Layer During Development

| What you want to inspect | Command |
| --- | --- |
| AST | `./build/bin/styio --styio-ast --file ...` |
| Styio IR | `./build/bin/styio --styio-ir --file ...` |
| LLVM IR | `./build/bin/styio --llvm-ir --file ...` |
| Parser dual-engine consistency | `--parser-shadow-compare` |

## Parser Reality

The current repository explicitly keeps two parser paths:

- `legacy`
- `nightly`

The default is already `nightly`. Tests also include multiple shadow compare and zero-fallback gates. The project is in the phase where the new parser has taken over but remains tightly checked against previous behavior.

## Recommended Source Reading Order

1. `src/main.cpp`
2. `src/StyioParser/`
3. `src/StyioAST/`
4. `src/StyioAnalyzer/`
5. `src/StyioIR/`
6. `src/StyioCodeGen/`
7. `src/StyioExtern/` and `src/StyioJIT/`

This order follows the path from input source to executable result.
