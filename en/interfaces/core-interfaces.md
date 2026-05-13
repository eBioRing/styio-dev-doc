# Core Interface Overview

This page is the entry point for the interface section. It no longer tries to pack every detail into one page.

## Which Manual Should You Read First?

| What you are changing | Read first |
| --- | --- |
| Tokens, lookahead, `legacy/nightly` parser routing | [Parser Manual](parser-manual.md) |
| Type inference, semantic constraints, AST to IR lowering | [Analyzer Manual](analyzer-manual.md) |
| LLVM type / IR generation and JIT execution path | [CodeGen Manual](codegen-manual.md) |
| FFI, standard streams, file handles, runtime errors | [Runtime Manual](runtime-manual.md) |

## Four-Layer Interface Relationship

```text
Tokenizer / Parser
  -> AST
  -> Analyzer (typeInfer + toStyioIR)
  -> StyioIR
  -> CodeGen (toLLVMType + toLLVMIR)
  -> Runtime / JIT
```

## Current Cross-Layer Entry Points

| Interface | Location | Purpose |
| --- | --- | --- |
| `StyioTokenizer::tokenize` | `src/StyioParser/Tokenizer.hpp` | Source to tokens |
| `parse_main_block_with_engine_latest` | `src/StyioParser/Parser.hpp` | Tokens to AST |
| `StyioAnalyzer::typeInfer` | `src/StyioAnalyzer/ASTAnalyzer.hpp` | Semantic annotation of AST |
| `StyioAnalyzer::toStyioIR` | `src/StyioAnalyzer/ASTAnalyzer.hpp` | AST to Styio IR |
| `StyioIR::{toString,toLLVMType,toLLVMIR}` | `src/StyioIR/StyioIR.hpp` | Shared virtual IR interface |
| `StyioToLLVM` | `src/StyioCodeGen/CodeGenVisitor.hpp` | LLVM codegen and execution |
| `StyioJIT_ORC::Create` | `src/StyioJIT/StyioJIT_ORC.hpp` | Creates the ORC JIT |
| `CompilationSession` | `src/StyioSession/CompilationSession.hpp` | Lifecycle convergence |

## Continue Reading

- [Parser Manual](parser-manual.md)
- [Analyzer Manual](analyzer-manual.md)
- [CodeGen Manual](codegen-manual.md)
- [Runtime Manual](runtime-manual.md)
- [Feature Change Matrix](change-matrix.md)
- [New Token or Syntax Change Runbook](../runbooks/new-token-or-syntax.md)
- [New AST or IR Node Change Runbook](../runbooks/new-ast-or-ir.md)
- [Standard Stream and Resource Capability Change Runbook](../runbooks/resources-and-stdio.md)
