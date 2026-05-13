# Analyzer 手册

Analyzer 是 Styio 真正的语义边界层。它既要做 type inference，也要把 AST 降成 Styio IR。

## 角色边界

Analyzer 层负责：

- 类型推断
- 语义约束
- AST 到 Styio IR lowering
- 某些 pulse/state 规划信息的传递

Analyzer 层不负责：

- token / 语法判定
- LLVM IR 细节
- FFI 符号绑定

## 主接口

文件：`src/StyioAnalyzer/ASTAnalyzer.hpp`

关键对象：`StyioAnalyzer`

最重要的两步：

```cpp
analyzer.typeInfer(ast);
StyioIR* ir = analyzer.toStyioIR(ast);
```

`main.cpp` 当前就是按这个顺序驱动的。

## visitor 面

`StyioAnalyzerVisitor` 的模板类型列表基本就是 analyzer 当前承认的 AST 面。

这意味着：

- 新 AST 节点如果不进这里，analyzer 看不见它
- 不仅要补 `typeInfer(Node*)`
- 还要补 `toStyioIR(Node*)`

这两个列表本身就是重要接口，不只是声明噪音。

## 状态字段

`StyioAnalyzer` 里当前可见的关键状态包括：

| 字段 / 方法 | 作用 |
| --- | --- |
| `func_defs` | 记录函数定义 |
| `local_binding_types` | 局部绑定类型表 |
| `cur_pulse_plan()` / `set_cur_pulse_plan(...)` | 当前 pulse plan |
| `active_series_slot()` / `set_active_series_slot(...)` | 当前 series slot |
| `set_post_pulse_hist_context(...)` | post-pulse history 上下文 |
| `is_snapshot_var(...)` | 判断 snapshot 变量 |

这些状态解释了 analyzer 为什么不只是“纯 visitor”，而是带上下文的 lowering 引擎。

## `toStyioIR` 的现实职责

从 `ToStyioIR.cpp` 可以直接看出来，这层不只是简单 AST 翻译，它还会：

- 为函数返回类型兜底
- 识别 state / pulse 相关模式
- 生成 `SIOStdStreamWrite`、`SIOStdStreamLineIter`、`SIOStdStreamPull`
- 为 iterator / stream zip / snapshot / instant pull 建 IR
- 决定某些 match 的 IR 形态

也就是说，很多“语言行为现在到底怎么落”的答案，其实不在 parser，而在 `ToStyioIR.cpp`。

## 当前关键 lowering 例子

### 标准流写

`ResourceWriteAST` / `ResourceRedirectAST` 会被 lowering 成：

- `SIOStdStreamWrite`
- 或 `SGResourceWriteToFile`

### stdin 迭代

`@stdin >> #(line) => {...}` 会落成：

- `SIOStdStreamLineIter`

### stdin instant pull

`(<< @stdin)` 会落成：

- `SIOStdStreamPull`

## 改 analyzer 时的最低同步范围

### 新 AST 节点

- `ASTAnalyzer.hpp`
- `TypeInfer.cpp`
- `ToStyioIR.cpp`
- `StyioIR` 新节点定义
- 对应 `ToStringVisitor`

### 新语义约束

不要只改 `TypeInfer.cpp` 的局部报错，还要看：

- 是否影响 lowering 分支
- 是否影响 milestone 语义错误用例
- 是否要补 `Symbol-Reference` / `Language-Design`

### 新 IR 节点

至少同步：

- `IRDecl.hpp`
- `GenIR.hpp` 或 `IOIR.hpp`
- `ASTAnalyzer.hpp`
- `ToStyioIR.cpp`
- `CodeGenVisitor.hpp`
- 具体 codegen 文件

## 维护原则

- 把语法问题留给 parser
- 把执行问题留给 codegen/runtime
- analyzer 负责把“语法上能写”收束成“语义上可执行”
