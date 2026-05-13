# State / Pulse / Snapshot 改动手册

这页处理 Styio 里另一条核心维护链：`@[...]` state、`$ref`、history probe、snapshot、instant pull，以及它们共享的 pulse ledger 机制。

## 这条链的核心事实

Styio 的状态能力不是几段独立语法，而是一套联动实现：

- parser 产出状态相关 AST
- analyzer 建 `SGPulsePlan`
- lowering 产出 state / snapshot / pull IR
- codegen 用 pulse ledger 和 frame snapshot 执行

如果只改其中一层，通常会直接破坏 frame lock、history 或 snapshot 一致性。

## 适用范围

这页适用于：

- `@[n](...)` 或 `@[name = ...](...)` 的 state 语义
- `$name` snapshot 读取
- `$name[<<, n]` history probe
- `@[name] << @resource` snapshot 声明
- `(<< @resource)` instant pull
- pulse ledger 布局、frame lock、post-pulse history

## 当前源码入口

| 层 | 入口 |
| --- | --- |
| AST | `StateDeclAST`、`StateRefAST`、`HistoryProbeAST`、`SnapshotDeclAST`、`InstantPullAST` |
| Analyzer 状态 | `cur_pulse_plan()`、`active_series_slot()`、`set_post_pulse_hist_context(...)` |
| IR | `SGStateSnapLoad`、`SGStateHistLoad`、`SGSnapshotDecl`、`SGInstantPull` |
| CodeGen | `CodeGenG.cpp`、`CodeGenIO.cpp`、`CodeGenPulse.cpp` |

## 修改顺序

### 1. 先确认你改的是哪种状态能力

| 能力 | 重点 |
| --- | --- |
| state 累加 / track | state slot 分类、commit 规则 |
| history probe | pulse plan、history ring、depth 语义 |
| snapshot | shadow 变量注册、frame lock |
| instant pull | analyzer 资源限制、I/O lowering |

先把类型分清，再改代码。不要把 snapshot、history、instant pull 当成一回事。

### 2. 改 analyzer 的语义边界

至少同步：

- `src/StyioAnalyzer/TypeInfer.cpp`
- `src/StyioAnalyzer/ToStyioIR.cpp`

这里有几条现成约束不能破坏：

- history probe 只允许在 pulse body 里，或在带 pulse 的 foreach / file line iter 之后使用
- `StateRefAST` / `HistoryProbeAST` 的 lowering 依赖 pulse plan 中的 slot 映射
- instant pull 会对资源类型做限制，比如拒绝从 `@stdout` / `@stderr` 读取

### 3. 改 pulse plan 和 slot 布局

至少检查：

- `find_series_intrinsic(...)`
- `classify_state_slot(...)`
- `slot_byte_size(...)`

这些逻辑决定：

- 当前 state 是 `Acc`、`Track` 还是 windowed slot
- ledger 需要分配多少字节
- history ring 和 snapshot 读写的偏移量

### 4. 改 codegen 的 pulse 路径

至少同步：

- `src/StyioCodeGen/CodeGenPulse.cpp`
- `src/StyioCodeGen/CodeGenG.cpp`
- 必要时 `src/StyioCodeGen/CodeGenIO.cpp`

当前 pulse codegen 实际负责：

- ledger -> snap 的复制
- frame 内 `$ref` 的一致读取
- history ring 的读写
- post-loop history 的 ledger region 访问
- snapshot shadow reload

如果这层理解错了，最直接的症状就是同一 pulse 内 `$ref` 不稳定，或者 history 深度错位。

### 5. snapshot / instant pull 要连同资源路径一起看

相关改动至少同步：

- `src/StyioAnalyzer/ToStyioIR.cpp`
- `src/StyioCodeGen/CodeGenIO.cpp`
- `src/StyioCodeGen/CodeGenG.cpp`

典型样例包括：

- `tests/milestones/m7/t03_snapshot.styio`
- `tests/milestones/m7/t06_snapshot_lock.styio`
- `tests/milestones/m7/t09_snapshot_accum.styio`
- `tests/pipeline_cases/p05_snapshot_accum/input.styio`
- `tests/pipeline_cases/p07_instant_pull/input.styio`
- `tests/pipeline_cases/p14_stdin_pull/input.styio`

## 最低验证命令

### 跑 state / history 里程碑

```bash
ctest --test-dir build -R '^m6_' --output-on-failure
```

### 跑 snapshot / instant pull 里程碑

```bash
ctest --test-dir build -R '^m7_' --output-on-failure
```

### 看 history lowering

```bash
./build/bin/styio --styio-ir --file tests/milestones/m6/t04_history.styio
```

### 看 snapshot lowering

```bash
./build/bin/styio --styio-ir --file tests/milestones/m7/t09_snapshot_accum.styio
```

### 跑 pipeline 级回归

```bash
ctest --test-dir build -R 'StyioFiveLayerPipeline.P05_snapshot_accum|StyioFiveLayerPipeline.P07_instant_pull|StyioFiveLayerPipeline.P14_stdin_pull' --output-on-failure
```

### 跑 state inline 回归

```bash
ctest --test-dir build -R 'SingleArgStateFunctionInliningUsesCallArgument|BlockStateFunctionInliningUsesCallArgument|StateInlineMatchCasesFunctionUsesCallArgument|StateInlineInfiniteLiteralFunctionUsesCallArgument' --output-on-failure
```

## 常见漏项

- 改了 state 语义，却没同步 pulse ledger 字节布局
- history probe 只在当前 pulse 能读，post-pulse 路径忘了补
- snapshot 能读，但同一 frame 里读值不一致
- instant pull 只测了 `@file`，没测 `@stdin`
- state inline helper 回归没跑，导致函数参数替换再次失效

## 文档同步规则

这类改动最少同步：

- `docs/design/Styio-Language-Design.md`
- `docs/design/Styio-Symbol-Reference.md`
- 如果牵涉资源拉取，再补 `docs/design/Styio-Resource-Driver.md`

如果只是今天的实现边界变化，不要把未来的资源拓扑目标文档直接当成“当前已经稳定支持”。
