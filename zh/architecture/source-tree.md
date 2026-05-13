# 源码目录地图

这个项目的目录不少，但真正高频会读的区域其实很集中。

## 顶层目录

| 目录 | 应该怎么理解 |
| --- | --- |
| `src/` | 编译器、CLI、IR、JIT 主体 |
| `tests/` | 回归保护网，读当前已实现能力时非常重要 |
| `sample/` | 最小可运行示例和脚本 |
| `docs/` | 主仓库内部设计、规格、ADR、里程碑 |
| `scripts/` | 文档审计、parser gate、回归工具 |
| `templates/` | 文档工作流模板，不是编译器主逻辑 |

## `src/` 里的关键子目录

| 目录 | 负责什么 |
| --- | --- |
| `StyioToken` | token、节点类型、基础枚举 |
| `StyioParser` | tokenizer、parser、lookahead、parser 子路径 |
| `StyioAST` | AST 节点定义 |
| `StyioAnalyzer` | 类型推断、语义检查、IR lowering |
| `StyioIR` | Styio IR 节点体系 |
| `StyioCodeGen` | LLVM codegen 和类型映射 |
| `StyioExtern` | JIT 需要调用的外部函数 |
| `StyioJIT` | ORC JIT 包装层 |
| `StyioTesting` | 五层流水线检查辅助 |
| `Deprecated` | 历史代码，只能参考，不能继续扩展 |

## `tests/` 里的高价值区域

| 目录 | 作用 |
| --- | --- |
| `tests/milestones/` | 阶段能力冻结样例 |
| `tests/pipeline_cases/` | 五层流水线对照样例 |
| `tests/security/` | lexer / FFI / 边界安全测试 |
| `tests/soak/` | 单线程长时间回归 |
| `tests/fuzz/` | fuzz 入口和 corpus |
| `tests/lit_cases/` | 细粒度 parsing / codegen fixture |

## `docs/` 里的高价值区域

| 目录 | 作用 |
| --- | --- |
| `docs/design/` | 语言与编译器设计 SSOT |
| `docs/specs/` | 仓库边界、文档政策、依赖说明 |
| `docs/milestones/` | 冻结里程碑说明 |
| `docs/adr/` | 关键架构决策记录 |
| `docs/plans/` | 计划文档，更多是路线，不一定等于现状 |

## 如果你要改一个新语法点

大概率会同时碰到这些位置：

- `src/StyioToken/`
- `src/StyioParser/`
- `src/StyioAST/`
- `src/StyioAnalyzer/`
- `src/StyioIR/`
- `src/StyioCodeGen/`
- `tests/`
- `docs/design/`

Styio 当前不是“单点改完就行”的架构，任何语言面修改通常都要串过整条链路。
