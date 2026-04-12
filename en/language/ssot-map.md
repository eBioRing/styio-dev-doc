# 语言与设计 SSOT 地图

这一页只告诉维护者：不同设计文档各自负责什么。

## 主设计文档

| 文档 | 负责什么 |
| --- | --- |
| `Styio-Language-Design.md` | 语言语义总说明 |
| `Styio-EBNF.md` | 形式文法 |
| `Styio-Symbol-Reference.md` | 符号到 token 的速查与语义摘要 |
| `Styio-StdLib-Intrinsics.md` | `[op, n]` 类 intrinsic 规范 |
| `Styio-Resource-Driver.md` | 资源驱动接口目标 |
| `Styio-Resource-Topology.md` | `@` 与资源拓扑目标设计 |

## 如何使用这些文档

### 你在改语法

先看：

- `EBNF`
- `Symbol-Reference`
- `Language-Design`

### 你在改 intrinsic

先看：

- `StdLib-Intrinsics`
- 对应 analyzer / codegen 实现

### 你在改资源或标准流

先看：

- `Language-Design`
- `Symbol-Reference`
- `Resource-Topology`
- 当前 milestone 与测试

## 哪些文档要谨慎理解

尤其要注意：

- `Resource-Topology.md` 包含一部分目标设计，**不等于当前完全实现**
- `Resource-Driver.md` 也是接口目标文档，不应直接当成“今天代码里已有插件系统”

正确做法是：

- 设计边界看 `docs/design/`
- 当前实现边界看 `src/` 和 `tests/`

## 对 GitBook 的要求

GitBook 不应该再重复写一份长篇语义说明。它应当做的是：

- 告诉维护者该去哪里看权威定义
- 告诉维护者哪些设计已经实装，哪些仍是目标
- 在不动框架的前提下，把这些入口组织得更易读
