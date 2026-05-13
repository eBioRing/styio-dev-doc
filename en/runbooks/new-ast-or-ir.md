# New AST or IR Node Change Runbook

This page turns one of the easiest Styio change types to under-register into an executable checklist: adding an AST node or adding a Styio IR node for a new capability.

## Scope

This page applies to:

- new AST class
- AST structure field changes
- new Styio IR node
- new AST-to-IR lowering branch

## Minimum Synchronization Chain for a New AST

The source repository has a scattered checklist in `src/StyioAST/add_new_ast.md`. This page organizes it into a maintenance order.

### 1. Define the AST object

Synchronize at least:

- `src/StyioAST/ASTDecl.hpp`
- `src/StyioAST/AST.hpp`

### 2. Add AST type enum and readable name

Synchronize at least:

- `StyioASTType` in `src/StyioToken/Token.hpp`
- `reprASTType` in `src/StyioToken/Token.cpp`

### 3. Add AST visualization

Synchronize at least:

- `src/StyioToString/ToStringVisitor.hpp`
- `src/StyioToString/ToString.cpp`

If this step is missing, `--styio-ast` and many debugging paths become unreliable.

### 4. Add analyzer visitor surface

Synchronize at least:

- `src/StyioAnalyzer/ASTAnalyzer.hpp`
- `src/StyioAnalyzer/TypeInfer.cpp`
- `src/StyioAnalyzer/ToStyioIR.cpp`

The real requirement is not just "there is a declaration". Both of these interfaces must handle it:

- `typeInfer(Node*)`
- `toStyioIR(Node*)`

Missing either side is not complete.

## Minimum Synchronization Chain for a New IR Node

### 1. Declare the IR type

Synchronize at least:

- `src/StyioIR/IRDecl.hpp`
- corresponding IR definition header, such as `src/StyioIR/StyioIR.hpp`

### 2. Make analyzer actually emit it

Synchronize at least:

- `src/StyioAnalyzer/ASTAnalyzer.hpp`
- `src/StyioAnalyzer/ToStyioIR.cpp`

### 3. Make codegen actually consume it

Synchronize at least:

- `src/StyioCodeGen/CodeGenVisitor.hpp`
- corresponding `GetType*.cpp`
- corresponding `CodeGen*.cpp`

If the node is declared but has no `toLLVMType` / `toLLVMIR` path, it only appears to exist.

## Typical Modification Order

Recommended order:

1. define AST / IR data structures
2. add `ToString`
3. add `typeInfer`
4. add `toStyioIR`
5. add `toLLVMType`
6. add `toLLVMIR`
7. add tests and documentation last

This order makes each layer visible and individually verifiable as early as possible.

## Minimum Validation Commands

### Inspect AST expansion

```bash
./build/bin/styio --styio-ast --file tests/milestones/m9/t01_stdout_string.styio
```

### Check Styio IR lowering

```bash
./build/bin/styio --styio-ir --file tests/milestones/m10/t01_stdin_echo.styio
```

### Check LLVM IR coverage

```bash
./build/bin/styio --llvm-ir --file tests/milestones/m2/t01_simple_func.styio
```

### Run pipeline and milestone tests

```bash
ctest --test-dir build -L styio_pipeline --output-on-failure
ctest --test-dir build -L milestone --output-on-failure
```

## Common Omissions

- AST class is defined, but `StyioASTType` is not updated.
- `ToStringVisitor` is not registered, making AST debug output untrustworthy.
- `typeInfer` is added, but `toStyioIR` is not.
- IR node can print, but `toLLVMType` / `toLLVMIR` are incomplete.
- Structure changed, but corresponding test samples were not updated.

## Documentation Synchronization Rules

If this is a language-level capability and not only an internal refactor, synchronize at least:

- `docs/design/Styio-Language-Design.md`
- `docs/design/Styio-Symbol-Reference.md`
- related pages in this manual
