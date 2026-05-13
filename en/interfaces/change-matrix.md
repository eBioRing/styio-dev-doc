# Feature Change Matrix

This page answers a common maintainer question: when changing a category of capability, which layers must be synchronized?

This matrix only covers the `styio` core: language, compiler, CLI, and the main test repository. Change loops for `Spio` and `Vityo` belong in their dedicated development guides.

## New Token

Synchronize at least:

- `src/StyioToken/Token.hpp`
- `src/StyioParser/Tokenizer.cpp`
- `src/StyioToken/Token.cpp` or token name mapping
- `docs/design/Styio-EBNF.md`
- `docs/design/Styio-Symbol-Reference.md`
- corresponding lexer / parser tests

## New AST Node

Synchronize at least:

- `src/StyioToken/Token.hpp`
- `src/StyioAST/ASTDecl.hpp`
- `src/StyioAST/AST.hpp`
- `src/StyioToString/ToStringVisitor.hpp`
- `src/StyioAnalyzer/ASTAnalyzer.hpp`
- `src/StyioAnalyzer/TypeInfer.cpp`
- `src/StyioAnalyzer/ToStyioIR.cpp`
- corresponding AST / type inference / IR tests

## Parser Extension

Synchronize at least:

- `src/StyioParser/Parser.hpp`
- `src/StyioParser/Parser.cpp`
- `src/StyioParser/NewParserExpr.cpp`
- `ParserLookahead.*` when needed
- parser shadow tests
- `EBNF` and `Symbol-Reference`

For dual-track logic, also maintain:

- `legacy`
- `nightly`
- `latest`
- route stats / shadow compare behavior

## New Intrinsic

Synchronize at least:

- parser selector recognition
- `TypeInfer.cpp`
- `ToStyioIR.cpp`
- `src/StyioIR/`
- `src/StyioCodeGen/CodeGenPulse.cpp` or related codegen files
- `docs/design/Styio-StdLib-Intrinsics.md`
- milestone / pipeline / C++ tests

## New Resource or Standard Stream Capability

Synchronize at least:

- parser resource atom parsing
- analyzer direction and semantic checks
- IR nodes
- codegen I/O path
- `ExternLib.*`
- `StyioJIT_ORC.hpp`
- `Symbol-Reference`
- corresponding milestone samples and execution tests

## New `.cpp` File

Do not forget:

- the top-level `CMakeLists.txt`

This is currently one of the easiest maintenance steps to miss in Styio.

## Minimum Loop for Any Language-Level Change

At minimum, complete:

1. design or specification synchronization
2. source-code synchronization
3. automated test synchronization
4. corresponding GitBook Markdown page synchronization

"Synchronization" means updating the maintainer manual content, not expanding or refactoring the GitBook framework.

## Related Runbooks

- token / parser change: [New Token or Syntax Change Runbook](../runbooks/new-token-or-syntax.md)
- AST / IR node change: [New AST or IR Node Change Runbook](../runbooks/new-ast-or-ir.md)
- standard stream / resource change: [Standard Stream and Resource Capability Change Runbook](../runbooks/resources-and-stdio.md)
- intrinsic change: [New Intrinsic Change Runbook](../runbooks/new-intrinsic.md)
- state / pulse / snapshot change: [State / Pulse / Snapshot Change Runbook](../runbooks/state-and-pulse.md)
- diagnostics / error model change: [Diagnostics and Error Model Runbook](../runbooks/diagnostics-and-error-model.md)
- parser dual-track migration change: [Parser Shadow and Dual-Track Migration Runbook](../runbooks/parser-shadow-and-dual-track.md)
- test structure / case selection change: [Testing Pyramid and Case Selection Runbook](../runbooks/testing-pyramid-and-case-selection.md)
- CLI / machine interface change: [CLI and Machine Interface Change Runbook](../runbooks/cli-and-machine-interface.md)

If any loop is missing, the change is not truly maintenance-complete.
