# Styio 本体开发流程

这页只写 `styio` 主仓库，也就是语言与编译器本体的开发流程。

不要把它和 `styio-spio`、`styio-view` 的流程混在一起。

## 当前已发布主线

按 2026-04-12 远端核对，`eBioRing/styio` 当前最新公开编译器主线是：

- `main` = `193f36b48e55e076d05c750d58e2850300ad6e43`

同仓的 `dev` 仍存在，但这轮公开同步里不应把它当成最新编译器事实来源。

## `styio` 本体负责什么

`styio` 主仓库当前拥有：

- 语言设计与语义
- parser / analyzer / IR / codegen / runtime / JIT
- CLI 与 machine interface
- `styio-nano` profile / packaging 相关 CLI 与配置
- milestone、pipeline、安全与回归测试
- 主仓库内部设计、规格、ADR、workflow assets 与历史文档

如果你改的是这些东西，开发流程应当在 `styio` 主仓库内闭环，而不是先去改工具仓。

## 本体开发的顺序

`styio` 的标准顺序是：

1. 先确认 SSOT
2. 再改源码
3. 再补测试
4. 最后同步文档

其中第一步通常落在：

- `docs/design/`
- `docs/specs/`
- `docs/assets/`
- `docs/for_spio/`
- `src/`
- `tests/`

## 本体开发的最小闭环

语言或编译器功能改动至少应覆盖：

- 设计或规格
- 主仓源码
- 自动化测试
- 这份开发者文档中的对应维护页

如果只改了源码和一两个样例，不算真正维护完成。

## 现在还要一起看的三类维护资产

除了编译器源码本身，`styio@main` 现在还有三类经常被漏看的东西：

- `docs/assets/`
  - 工作流、测试目录、repo hygiene、模板
- `docs/for_spio/`
  - 给 `spio` 的公开接口交接包
- `configs/styio-nano-*.toml`
  - `styio-nano` profile / package / publish 配置样例

如果你改的是 machine interface、测试目录、`styio-nano` packaging 或对外 handoff，不看这三类文件，文档就会写残。

## 本体仓最常见的改动类型

| 改动类型 | 先看哪里 |
| --- | --- |
| 新 token / 新语法 | parser、token、设计文档 |
| 新 AST / IR 节点 | AST、analyzer、IR、codegen |
| 新 intrinsic | analyzer、pulse、IR、codegen |
| state / snapshot / history | analyzer、pulse ledger、codegen |
| CLI / machine interface | `main.cpp`、diagnostics、测试 |
| `styio-nano` profile / packaging | `main.cpp`、`configs/styio-nano-*.toml`、`scripts/gen-styio-nano-profile.py` |
| docs index / docs audit | `docs/README.md`、`scripts/docs-index.py`、`scripts/docs-audit.py`、`tests/CMakeLists.txt` |

这些具体流程已经在本书的 runbook 区里拆开了。

## 本体仓的回归优先级

`styio` 改动优先看这些测试层：

- `milestone`
- `styio_pipeline`
- `security`
- `soak`
- `docs`

如果改 parser，还要看：

- `shadow_gate`
- `parser_legacy_entry_audit`

## 什么时候才去动工具仓

只有当本体改动影响到**公共接口**时，才需要同步工具仓文档或实现。典型例子：

- `--machine-info=json` 字段变化
- 诊断 `category` / `code` / `subcode` 变化
- 新增 compile-plan / machine contract
- `docs/for_spio/` 中的 handoff 要求变化
- 新的 diagnostics/token/block range 对 IDE 可用

否则，不要让工具仓反向驱动语言本体。

## 本体开发的维护原则

- 语言真相在 `styio`
- 编译器验收在 `styio/tests`
- 工具仓只能消费公共接口，不能定义语言语义

## 继续阅读

- [核心接口总览](../interfaces/core-interfaces.md)
- [功能改动矩阵](../interfaces/change-matrix.md)
- [维护任务](../README.md)
