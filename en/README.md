# Styio 维护者手册

这份 GitBook 不是项目年表，也不是聊天记录归档。它的主目标仍然是帮助开发者持续维护 `styio` 主仓库，同时为直接围绕 `styio` 公共接口开发的工具仓库提供维护指引。

本次内容基于 **2026-05-12** 的本地工作树核对。默认来源优先级是：本地已检出的工作树 > 同名 `Unka-Malloc/*` 仓库 > `eBioRing/*` 仓库或镜像。这意味着本手册优先描述你机器上当前真实存在的状态。

## 🧭 维护者导引

这份手册包含 39 个核心章节。为了提高阅读效率，请根据你的维护目标选择对应路径：

### 🏁 必读：新维护者入门
如果你是第一次参与维护，请务必按顺序阅读以下基石文档：
1. [贡献者契约](standards/contributor-contract.md) - 必须遵守的开发禁令与约束
2. [文档与 SSOT 规则](standards/documentation-and-ssot.md) - 搞清哪里才是“唯一真相”
3. [仓库矩阵与来源优先级](ecosystem/repository-matrix.md) - 弄清多个仓库谁听谁的
4. [三仓库协作流程](ecosystem/three-repository-collaboration.md) - 如何同步更新 styio/spio/view
5. [Styio 本体开发流程](ecosystem/styio-core-workflow.md) - 编译器主仓的改动闭环
6. [styio-community 治理指引](ecosystem/styio-community-development.md) - RFC 流程与技术决策机制

### 🏗️ 进阶：架构与工具链
当你准备开始改动代码，需要理解全局背景：
- **分层与流水线**：[分层架构](architecture/layered-architecture.md) | [编译器流水线](architecture/compiler-pipeline.md) | [源码目录地图](architecture/source-tree.md)
- **环境与基础**：[构建工具链](toolchain/build-toolchain.md) | [styio-dev-env 用途说明](ecosystem/styio-dev-env-development.md)
- **规范与合规**：[编码与重构规则](standards/coding-and-refactor-rules.md) | [styio-audit 开发指引](ecosystem/styio-audit-development.md) | [审计与合规](standards/audit-license-and-dependency-policy.md)
- **质量与性能**：[测试与回归策略](standards/testing-and-regression.md) | [styio-benchmark 开发指引](ecosystem/styio-benchmark-development.md) | [CLI 与调试](toolchain/cli-and-debug-workflow.md)

### 🛠️ 实战：编译器本体维护 (Compiler Track)
针对具体编译器模块的维护指引：
- **Parser/AST**：[Parser 手册](interfaces/parser-manual.md) | [新 Token 或语法改动](runbooks/new-token-or-syntax.md) | [新 AST 或 IR 节点](runbooks/new-ast-or-ir.md) | [Parser Shadow 迁移](runbooks/parser-shadow-and-dual-track.md)
- **语义与 IR**：[Analyzer 手册](interfaces/analyzer-manual.md) | [核心接口总览](interfaces/core-interfaces.md) | [State / Pulse / Snapshot 改动](runbooks/state-and-pulse.md)
- **CodeGen/运行时**：[CodeGen 手册](interfaces/codegen-manual.md) | [Runtime 手册](interfaces/runtime-manual.md) | [新增 Intrinsic 改动](runbooks/new-intrinsic.md)
- **IO 与标准流**：[标准流与资源能力](runbooks/resources-and-stdio.md) | [资源、`@` 与标准流](language/resources-and-stdio.md)

### 🧰 实战：生态工具维护 (Tooling Track)
针对包管理器、云服务和 IDE 扩展的维护指引：
- **Package Manager**：[Spio 开发指引](ecosystem/spio-development.md) | [Spio 能力与边界](ecosystem/spio-surface.md)
- **IDE & UI**：[Vityo 开发指引](ecosystem/vityo-development.md) | [Extensions 开发指引](ecosystem/extensions-development.md)
- **Platform & Cloud**：[styio-platform 开发指引](ecosystem/styio-platform-development.md)
- **外部接口**：[CLI 与 Machine Interface 改动](runbooks/cli-and-machine-interface.md) | [诊断与错误模型](runbooks/diagnostics-and-error-model.md)

### 📖 查阅：维护者手册 (Reference)
- [功能改动矩阵](interfaces/change-matrix.md)
- [测试金字塔与 Case 选型](runbooks/testing-pyramid-and-case-selection.md)
- [语言与设计 SSOT 地图](language/ssot-map.md)

---

## 🚦 维护边界与纪律

这本手册明确了以下核心边界：

- **应该做**：提供规范、界定职责边界、说明工具链、列出可复现命令和主接口。
- **不该做**：不堆砌历史记录、不平行维护语言规范、不滥用概念介绍。

**在开始任何改动前，请先确认你在维护哪个仓库：**
- **语言语义、编译器、测试** ➡️ 走 [Styio 本体开发流程](ecosystem/styio-core-workflow.md)
- **许可证、依赖、安全合规** ➡️ 走 [审计与合规](standards/audit-license-and-dependency-policy.md)
- **包管理、流程命令** ➡️ 走 [Spio 开发指引](ecosystem/spio-development.md)
- **编辑器、UI、AI 面板** ➡️ 走 [Vityo 开发指引](ecosystem/vityo-development.md)

*严禁倒置：不要为了工具仓的需求，去反向扭曲编译器的本体设计与语言语义。*

## 🔗 权威 SSOT 索引

写文档或开发时，网络链接仅作为防走失索引，**优先以本地代码树为准**。当前 GitHub 远端对齐事实如下：

- `styio` 最新主线：`eBioRing/styio@main` (`193f36b48e`)
- `Spio` 最新工作线：`eBioRing/Spio@agent-dev` (`b3d044a958`)

**核心上游资产入口：**
- **语义与规范**：[`docs/design/`](https://github.com/eBioRing/styio/tree/main/docs/design)
- **开发政策**：[`docs/specs/AGENT-SPEC.md`](https://github.com/eBioRing/styio/blob/main/docs/specs/AGENT-SPEC.md)
- **验收标准**：[`src/`](https://github.com/eBioRing/styio/tree/main/src) 与 [`tests/`](https://github.com/eBioRing/styio/tree/main/tests)
- **包管理接口要求**：[`Styio-External-Interface-Requirement-Spec.md`](https://github.com/eBioRing/Spio/blob/agent-dev/docs/styio/Styio-External-Interface-Requirement-Spec.md)
