# Styio 维护者手册

这份 GitBook 不是项目年表，也不是聊天记录归档。它的主目标仍然是帮助开发者持续维护 `styio` 主仓库，同时为直接围绕 `styio` 公共接口开发的工具仓库提供维护指引。

本次内容基于 **2026-04-12** 的本地工作树核对。默认来源优先级是：

1. 本地已检出的工作树
2. 同名 `Unka-Malloc/*` 仓库
3. `eBioRing/*` 仓库或镜像

也就是说，这本手册优先描述你机器上当前真实存在的 `styio`、`styio-spio`、`styio-view` 状态，而不是某个旧的云端快照。

## 本次 GitHub 同步基线

这轮补文档时，我额外核对了你刚上传到 GitHub 的已发布分支，作为“远端公开事实”：

- `eBioRing/styio` `main` = `193f36b48e55e076d05c750d58e2850300ad6e43`
- `eBioRing/styio` `dev` = `09e93c7fd6056fc2cbc2afab09353657d28a032b`
- `eBioRing/styio-spio` `agent-dev` = `b3d044a95857bfe6206ef8fd591df456091e8f92`
- `eBioRing/styio-spio` `main` = `2ce0b8be1839b14d529b0af9c9d69011160456a1`

当前这本手册把：

- `styio` 的最新已发布编译器主线视为 `eBioRing/styio@main`
- `styio-spio` 的最新工作线视为 `eBioRing/styio-spio@agent-dev`

## 这本手册应该提供什么

- 必须遵守的开发规范
- 跨仓库的职责边界和来源优先级
- 可复现的工具链与命令
- 编译器分层、边界和每层的主接口
- 改动某类能力时必须同步的文件与测试
- 哪些文档是权威真相，哪些只是补充说明

## 这本手册不应该做什么

- 不把大量历史记录放进主导航
- 不平行维护另一份语言规范
- 不用过期设计草案覆盖当前代码与测试
- 不用“概念介绍”替代具体接口和维护步骤
- 非必要不改 GitBook 框架，只改文档内容并验证渲染

## 维护者阅读顺序

1. [贡献者契约](standards/contributor-contract.md)
2. [文档与 SSOT 规则](standards/documentation-and-ssot.md)
3. [审计、许可证与依赖合规](standards/audit-license-and-dependency-policy.md)
4. [仓库矩阵与来源优先级](ecosystem/repository-matrix.md)
5. [三仓库协作流程](ecosystem/three-repository-collaboration.md)
6. [Styio 本体开发流程](ecosystem/styio-core-workflow.md)
7. [styio-spio 开发指引](ecosystem/styio-spio-development.md)
8. [styio-spio 当前能力与边界](ecosystem/styio-spio-surface.md)
9. [styio-view 开发指引](ecosystem/styio-view-development.md)
10. [Extensions 开发指引](ecosystem/extensions-development.md)
11. [编码与重构规则](standards/coding-and-refactor-rules.md)
12. [测试与回归策略](standards/testing-and-regression.md)
13. [构建工具链](toolchain/build-toolchain.md)
14. [CLI 与调试工作流](toolchain/cli-and-debug-workflow.md)
15. [分层架构与职责](architecture/layered-architecture.md)
16. [核心接口总览](interfaces/core-interfaces.md)
17. [Parser 手册](interfaces/parser-manual.md)
18. [Analyzer 手册](interfaces/analyzer-manual.md)
19. [CodeGen 手册](interfaces/codegen-manual.md)
20. [Runtime 手册](interfaces/runtime-manual.md)
21. [功能改动矩阵](interfaces/change-matrix.md)
22. [新 Token 或语法改动手册](runbooks/new-token-or-syntax.md)
23. [新 AST 或 IR 节点改动手册](runbooks/new-ast-or-ir.md)
24. [标准流与资源能力改动手册](runbooks/resources-and-stdio.md)
25. [新增 Intrinsic 改动手册](runbooks/new-intrinsic.md)
26. [State / Pulse / Snapshot 改动手册](runbooks/state-and-pulse.md)
27. [诊断与错误模型手册](runbooks/diagnostics-and-error-model.md)
28. [Parser Shadow 与双轨迁移手册](runbooks/parser-shadow-and-dual-track.md)
29. [测试金字塔与 Case 选型手册](runbooks/testing-pyramid-and-case-selection.md)
30. [CLI 与 Machine Interface 改动手册](runbooks/cli-and-machine-interface.md)

## 先分清你在维护哪个仓

- 如果你在改语言语义、编译器实现、CLI、测试，先走 [Styio 本体开发流程](ecosystem/styio-core-workflow.md)
- 如果你在改许可证、依赖、技术栈清单、商业风险边界或 secret 扫描规则，先走 [审计、许可证与依赖合规](standards/audit-license-and-dependency-policy.md)
- 如果你在改动会同时影响 `styio`、`styio-spio`、`styio-view`，先在 [三仓库协作流程](ecosystem/three-repository-collaboration.md) 写清责任和同步顺序
- 如果你在改包管理、resolver、contract 兼容或工作流命令，先走 [styio-spio 开发指引](ecosystem/styio-spio-development.md)
- 如果你在改 `spio` 的 registry、publish、managed toolchain 或 compile-plan dry-run，先补看 [styio-spio 当前能力与边界](ecosystem/styio-spio-surface.md)
- 如果你在改编辑器、运行视图、AI 面板或平台执行策略，先走 [styio-view 开发指引](ecosystem/styio-view-development.md)
- 如果你在改 VS Code 或未来别的宿主编辑器集成，先走 [Extensions 开发指引](ecosystem/extensions-development.md)

不要先改工具仓再倒推语言语义，也不要把 IDE / 包管理器文档写进编译器本体流程里。

## 权威来源

下面这些网络链接只作为入口索引。真正写文档时，仍然先看你本地已检出的工作树；如果要核对本轮公开同步，则看这里列的已发布分支。

- `styio` 语言语义：[`docs/design/`](https://github.com/eBioRing/styio/tree/main/docs/design)
- `styio` 维护规范：[`docs/specs/AGENT-SPEC.md`](https://github.com/eBioRing/styio/blob/main/docs/specs/AGENT-SPEC.md)
- `styio` 文档政策：[`docs/specs/DOCUMENTATION-POLICY.md`](https://github.com/eBioRing/styio/blob/main/docs/specs/DOCUMENTATION-POLICY.md)
- `styio` 依赖与许可证：[`docs/specs/THIRD-PARTY.md`](https://github.com/eBioRing/styio/blob/main/docs/specs/THIRD-PARTY.md)
- `styio` 实现与验收：[`src/`](https://github.com/eBioRing/styio/tree/main/src) 与 [`tests/`](https://github.com/eBioRing/styio/tree/main/tests)
- `styio-spio` CLI / governance：[`docs/governance/`](https://github.com/eBioRing/styio-spio/tree/agent-dev/docs/governance)
- `styio-spio` registry / publish：[`docs/registry/`](https://github.com/eBioRing/styio-spio/tree/agent-dev/docs/registry)
- `styio-spio` 对 `styio` 的公开接口要求：[`docs/styio/Styio-External-Interface-Requirement-Spec.md`](https://github.com/eBioRing/styio-spio/blob/agent-dev/docs/styio/Styio-External-Interface-Requirement-Spec.md)
