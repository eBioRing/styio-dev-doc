# CodeGen Manual

The CodeGen layer turns Styio IR into LLVM IR and hands it to ORC JIT for execution.

## Role Boundary

CodeGen is responsible for:

- mapping IR nodes to LLVM types
- generating LLVM instructions from IR nodes
- assembling optimization passes
- entering JIT execution

CodeGen is not responsible for:

- token / AST semantic decisions
- parser fallback
- concrete FFI implementation details

## Main Interface

File: `src/StyioCodeGen/CodeGenVisitor.hpp`

Key object: `StyioToLLVM`

Core capabilities:

| Method | Purpose |
| --- | --- |
| `Create(std::unique_ptr<StyioJIT_ORC>)` | Creates the codegen context |
| `toLLVMType(...)` | Resolves LLVM type |
| `toLLVMIR(...)` | Generates LLVM IR |
| `dump_llvm_ir()` | Exports textual IR |
| `print_llvm_ir()` | Prints IR |
| `execute()` | Calls ORC JIT execution |

## IR Boundary

The Styio IR base class in `src/StyioIR/StyioIR.hpp` defines three required operations:

```cpp
virtual std::string toString(StyioRepr* visitor, int indent = 0) = 0;
virtual llvm::Type* toLLVMType(StyioToLLVM* visitor) = 0;
virtual llvm::Value* toLLVMIR(StyioToLLVM* visitor) = 0;
```

When adding an IR node, CodeGen must at least handle:

- `toLLVMType`
- `toLLVMIR`

## Code Organization

| File | Purpose |
| --- | --- |
| `CodeGen.cpp` | Core codegen |
| `CodeGenG.cpp` | Generic nodes |
| `CodeGenIO.cpp` | I/O and standard streams |
| `CodeGenPulse.cpp` | Pulse / series related logic |
| `GetTypeG.cpp` | Generic type mapping |
| `GetTypeIO.cpp` | I/O type mapping |

## Current I/O CodeGen Realities

From `CodeGenIO.cpp`:

- the stdout path of `SIOStdStreamWrite` largely reuses the type-dispatched output branches of `SIOPrint`
- the stderr path first converts values to cstr, then calls `styio_stderr_write_cstr`
- `SIOStdStreamLineIter` generates basic blocks such as `stdin_hdr`, `stdin_body`, and `stdin_exit`
- `SIOStdStreamPull` currently keeps the `cstr -> i64` convention

This means standard-stream changes usually touch:

- analyzer lowering
- `CodeGenIO.cpp`
- `ExternLib.*`
- `StyioJIT_ORC.hpp`

## CodeGen Execution Order in `main.cpp`

The current order is:

1. `StyioJIT_ORC::Create()`
2. `StyioToLLVM generator(...)`
3. `session.ir()->toLLVMIR(&generator)`
4. optional `print_llvm_ir()`
5. `generator.execute()`
6. check `styio_runtime_has_error()`

So CodeGen output must not only be printable IR; it must close the loop through runtime error checking.

## Minimum Synchronization Scope for New IR Nodes

- `IRDecl.hpp`
- `GenIR.hpp` / `IOIR.hpp`
- `CodeGenVisitor.hpp`
- corresponding `GetType*.cpp`
- corresponding `CodeGen*.cpp`
- `ToStringVisitor`
- analyzer lowering

## Maintenance Principles

- If an existing runtime helper is sufficient, do not introduce a hidden new ABI.
- Value ownership must match runtime helper conventions.
- If a new node only implements `toLLVMIR` but not `toLLVMType`, it will usually fail elsewhere later.
