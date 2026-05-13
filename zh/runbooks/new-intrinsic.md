# 新增 Intrinsic 改动手册

这页专门写 compiler intrinsic 的维护闭环。这里说的 intrinsic，不是普通函数调用，而是编译器直接识别并内联 lowering 的语法能力。

## 先分清设计文档和当前实现

`docs/design/Styio-StdLib-Intrinsics.md` 记录的是更大的目标面。按当前已发布主线和活跃实现核对，已经能从 AST 直接落到 IR / codegen 的主要是 **series intrinsic** 这条链。

当前源码里可以直接确认的实现面包括：

- AST：`SeriesIntrinsicAST`
- 操作枚举：`SeriesIntrinsicOp::{Avg, Max}`
- 状态槽类型：`SGStateSlotKind::{WinAvg, WinMax}`
- IR：`SGSeriesAvgStep`、`SGSeriesMaxStep`
- codegen：`GetTypeG.cpp`、`CodeGenPulse.cpp`

如果你要写的是 `StdLib-Intrinsics` 文档里的其他算法，不要先假定“规范里有，编译器就已经支持”。

## 适用范围

这页适用于：

- 新增 `[op, n]` 一类 intrinsic
- 修改已有 series intrinsic 的 window 语义
- 修改 intrinsic 对 `@` 的处理
- 修改 intrinsic 的 pulse ledger 布局或 lowering

## 当前链路的真实入口

| 层 | 入口 |
| --- | --- |
| AST | `src/StyioAST/AST.hpp` 里的 `SeriesIntrinsicAST` |
| Analyzer | `src/StyioAnalyzer/TypeInfer.cpp`、`src/StyioAnalyzer/ToStyioIR.cpp` |
| IR | `src/StyioIR/IRDecl.hpp`、`src/StyioIR/GenIR/GenIR.hpp` |
| CodeGen | `src/StyioCodeGen/GetTypeG.cpp`、`src/StyioCodeGen/CodeGenPulse.cpp` |

## 修改顺序

### 1. 先确认这是 parser 语法，还是现有 intrinsic 扩展

如果只是给已有 `[avg, n]` / `[max, n]` 路径补能力，优先复用现有 `SeriesIntrinsicAST`。

如果要新增新的 selector 语法，再额外同步：

- parser 识别路径
- `docs/design/Styio-Symbol-Reference.md`
- `docs/design/Styio-EBNF.md`

### 2. 扩 AST 枚举和节点

至少同步：

- `src/StyioAST/AST.hpp`
- 必要时 `src/StyioToken/Token.hpp`
- `src/StyioToString/ToStringVisitor.hpp`
- `src/StyioToString/ToString.cpp`

当前 `SeriesIntrinsicOp` 实际只有：

- `Avg`
- `Max`

新增操作时，这里是第一落点。

### 3. 改 analyzer 的状态槽分类和 lowering

至少同步：

- `src/StyioAnalyzer/TypeInfer.cpp`
- `src/StyioAnalyzer/ToStyioIR.cpp`

这里有三条硬规则：

- `window size for series intrinsic must be integer literal`
- `series intrinsic needs enclosing state slot`
- 对非累加 state，仍要满足现有 `@[n]` header 规则

也就是说，intrinsic 不是孤立表达式，它默认依赖 enclosing state slot 和 pulse plan。

### 4. 改 IR 和 ledger 布局

至少同步：

- `src/StyioIR/IRDecl.hpp`
- `src/StyioIR/GenIR/GenIR.hpp`

如果新增 intrinsic 需要新的状态槽布局，还要同步 analyzer 里的：

- `classify_state_slot(...)`
- `slot_byte_size(...)`

否则 analyzer 和 codegen 会对 ledger layout 理解不一致。

### 5. 改 codegen pulse 路径

至少同步：

- `src/StyioCodeGen/GetTypeG.cpp`
- `src/StyioCodeGen/CodeGenPulse.cpp`

当前 `CodeGenPulse.cpp` 负责：

- pulse ledger / snapshot 读写
- warm-up 阶段的 `@` 行为
- `WinAvg` / `WinMax` 对应的 LLVM IR 生成

如果你新增 intrinsic，但没在这里补 `toLLVMIR`，那它只是“前端认得，后端不会跑”。

## 最低验证命令

### 看 AST 是否识别成 intrinsic

```bash
./build/bin/styio --styio-ast --file tests/milestones/m6/t03_window_avg.styio
```

### 看 Styio IR lowering

```bash
./build/bin/styio --styio-ir --file tests/milestones/m6/t03_window_avg.styio
```

### 看 LLVM IR

```bash
./build/bin/styio --llvm-ir --file tests/milestones/m6/t02_running_max.styio
```

### 跑 M6 里程碑

```bash
ctest --test-dir build -R '^m6_' --output-on-failure
```

### 跑非字面量 window 诊断

```bash
ctest --test-dir build -R 'SeriesIntrinsicWindowNonLiteralReportsTypeError' --output-on-failure
```

## 常见漏项

- 只改 `StdLib-Intrinsics` 设计文档，没改编译器实现
- AST 已支持新 op，但 `classify_state_slot(...)` 没补
- IR 节点已声明，但 `GetTypeG.cpp` / `CodeGenPulse.cpp` 没补
- 忘了 warm-up 阶段的 `@` 处理
- 把非字面量窗口大小悄悄放过去，破坏现有诊断契约

## 文档同步规则

intrinsic 语义变更最少同步：

- `docs/design/Styio-StdLib-Intrinsics.md`
- 必要时 `docs/design/Styio-Language-Design.md`
- 如果语法有变，再补 `Styio-EBNF.md` 和 `Styio-Symbol-Reference.md`
