# CodeGen 手册

CodeGen 层负责把 Styio IR 变成 LLVM IR，并把它交给 ORC JIT 执行。

## 角色边界

CodeGen 负责：

- IR 节点到 LLVM 类型映射
- IR 节点到 LLVM 指令生成
- 优化 pass 组装
- JIT 执行入口

CodeGen 不负责：

- token / AST 语义判断
- parser fallback
- FFI 具体实现细节

## 主接口

文件：`src/StyioCodeGen/CodeGenVisitor.hpp`

关键对象：`StyioToLLVM`

核心能力：

| 方法 | 作用 |
| --- | --- |
| `Create(std::unique_ptr<StyioJIT_ORC>)` | 创建 codegen 上下文 |
| `toLLVMType(...)` | 求 LLVM 类型 |
| `toLLVMIR(...)` | 生成 LLVM IR |
| `dump_llvm_ir()` | 导出纯文本 IR |
| `print_llvm_ir()` | 打印 IR |
| `execute()` | 调用 ORC JIT 执行 |

## IR 边界

Styio IR 基类在 `src/StyioIR/StyioIR.hpp` 里定义了三件必须做的事：

```cpp
virtual std::string toString(StyioRepr* visitor, int indent = 0) = 0;
virtual llvm::Type* toLLVMType(StyioToLLVM* visitor) = 0;
virtual llvm::Value* toLLVMIR(StyioToLLVM* visitor) = 0;
```

所以新增 IR 节点时，CodeGen 侧至少要保证：

- `toLLVMType`
- `toLLVMIR`

都能接住。

## 代码组织

| 文件 | 作用 |
| --- | --- |
| `CodeGen.cpp` | 核心 codegen |
| `CodeGenG.cpp` | 通用节点 |
| `CodeGenIO.cpp` | I/O 与标准流 |
| `CodeGenPulse.cpp` | pulse / series 相关 |
| `GetTypeG.cpp` | 通用类型映射 |
| `GetTypeIO.cpp` | I/O 类型映射 |

## 当前 I/O codegen 的关键现实

从 `CodeGenIO.cpp` 可以直接看到：

- `SIOStdStreamWrite` 的 stdout 路径基本复用了 `SIOPrint` 的分类型输出分支
- stderr 路径会先把值转成 cstr，再调用 `styio_stderr_write_cstr`
- `SIOStdStreamLineIter` 会生成 `stdin_hdr` / `stdin_body` / `stdin_exit` 这类 basic block
- `SIOStdStreamPull` 当前仍维持 `cstr -> i64` 约定

这意味着标准流相关改动通常同时牵涉：

- analyzer lowering
- `CodeGenIO.cpp`
- `ExternLib.*`
- `StyioJIT_ORC.hpp`

## `main.cpp` 中的 codegen 执行顺序

当前顺序是：

1. `StyioJIT_ORC::Create()`
2. `StyioToLLVM generator(...)`
3. `session.ir()->toLLVMIR(&generator)`
4. 可选 `print_llvm_ir()`
5. `generator.execute()`
6. 检查 `styio_runtime_has_error()`

所以 codegen 的产出不只是“IR 能打印”，还必须能在 runtime 错误检查链上闭环。

## 新 IR 节点接入时的最低同步范围

- `IRDecl.hpp`
- `GenIR.hpp` / `IOIR.hpp`
- `CodeGenVisitor.hpp`
- 对应 `GetType*.cpp`
- 对应 `CodeGen*.cpp`
- `ToStringVisitor`
- analyzer lowering

## 维护原则

- 能用现有 runtime helper，就不要偷偷生成新的 ABI
- 值的所有权必须和 runtime helper 的约定一致
- 新节点如果只在 `toLLVMIR` 接了、`toLLVMType` 没接，通常迟早会在别处炸
