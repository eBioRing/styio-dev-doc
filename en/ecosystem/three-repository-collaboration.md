# 三仓库协作流程

这页是 `styio`、`styio-spio`、`styio-view` 的跨仓协作流程总览。许可证、依赖商业风险和 secret 扫描的统一规则见 [审计、许可证与依赖合规](../standards/audit-license-and-dependency-policy.md)。

它先在 `styio-dev-doc` 里维护，等流程稳定后再同步到三个项目仓库的本地文档中。同步后，三个项目仓库仍然各自拥有自己的代码、测试、门禁和交付责任；`styio-dev-doc` 只保留跨仓维护手册和流程总览。

## 适用范围

这套流程只覆盖三类仓库：

| 仓库 | 职责 | 当前协作身份 |
| --- | --- | --- |
| `styio` | 语言、编译器、CLI、machine interface、主测试与主规格 | 上游语义和公共接口源头 |
| `styio-spio` | 包管理、resolver、registry、publish、toolchain、`styio-protocol` 消费 | 工具链与包生态消费方 |
| `styio-view` | IDE / 运行视窗、工作区 UI、执行路由、hosted/local adapter | 产品交互与执行可视化消费方 |

如果本地存在 `styio-nightly`，按 `styio` 的 nightly / 个人维护分支处理。流程、门禁和文档同步目标仍归入 `styio`。

## 协作原则

1. `styio` 定义语言语义、公共机器接口和 `styio-protocol`。
2. `styio-spio` 和 `styio-view` 只能消费公开接口，不能反向定义语言语义。
3. 跨仓流程先在 `styio-dev-doc` 起草，稳定后同步到三个仓库。
4. 每个仓库的代码、测试、文档和交付门禁必须在本仓闭环。
5. 跨仓变更必须有兼容窗口、验证矩阵和回滚方案。
6. 审计缺陷不能只写在协作文档里，必须落到对应仓库的 `docs/audit/` 或本仓长期工作项。
7. 许可证、依赖、技术栈清单和 secret 扫描规则由 `styio-audit` 统一审计；跨仓流程只能引用结论，不能绕过 audit gate。

## `styio-protocol` 静态协议边界

`styio-protocol` 是 `styio` 对工具链、包管理器、IDE 和扩展公开的静态协议 / 交接契约，不是运行时套件，也不表示 `styio-spio`、`styio-view` 或扩展可以链接 `styio` 私有模块。

它覆盖这些跨仓可消费面：

1. 公开 CLI 参数、退出码和文件输入 / 输出约定。
2. `styio --machine-info=json` 握手字段、能力声明和版本 / channel 元数据。
3. 已发布的 `styio --compile-plan <path>` schema、执行语义和兼容窗口。
4. JSON / JSONL diagnostics、runtime event、token/range、semantic token、completion、hover 等公共 payload。
5. schema、样例、兼容矩阵、迁移说明和 release protocol 文档。

它不覆盖：

1. `styio` 私有头文件、源码目录、AST / IR 内存布局或内部编译器对象。
2. `styio-spio` 的 registry / resolver / publish 私有实现。
3. `styio-view` 的 Flutter UI 状态、主题系统或产品交互实现。

所有跨仓接口变更都应该先判断是否属于 `styio-protocol`。如果属于，必须在 `styio` 冻结协议形状，并由消费仓通过 contract / adapter tests 验证；如果只是单仓实现细节，就不要把它升级成跨仓协议。

## `styio` 到 `styio-view` 的语法上游关系

当 `styio` 添加 token、关键字、表达式、语句、资源语法、类型语法或诊断形状时，`styio` 是 `styio-view` 的上游。`styio-view` 不重新定义语法，只消费 `styio` 已冻结的语法事实和公共接口。

`styio` 的责任：

1. 在主仓完成语法设计、parser / analyzer / IR / codegen 需要的实现。
2. 提供可验证的样例、诊断、token / block range、AST / IR repr 或 machine-readable 语法事实。
3. 跑通 parser shadow、pipeline、security 和 docs gate。
4. 在 `styio-protocol` 文档或变更草稿里说明 IDE 需要消费的新增语法面。

`styio-view` 的责任：

1. 更新语法高亮、token 分类、block / range 呈现和错误定位。
2. 更新补全、snippet、hover、inline help 或命令面板提示。
3. 更新编辑器状态机，确保新语法不会破坏 source buffer canonical source 约束。
4. 更新 Flutter / editor tests，覆盖新语法的高亮、补全、诊断呈现和运行入口。
5. 如果 `styio` 暂未提供稳定接口，先向 `styio` 提出接口需求，不在 `styio-view` 内复制一套语法判定。

闭环标准：`styio` 的语法 gate 通过，并且 `styio-view` 的 IDE 相关测试能证明新语法在编辑、提示、诊断和运行入口上可用。

## `styio-view` 到 `styio` IDE 维护组件的需求上游关系

当 `styio-view` 在实现前端编辑器、运行视窗、补全、高亮、outline、diagnostic navigation 或 AI 辅助时，发现 `styio` 的基础 IDE 套件缺少必要的语法分析、增量解析、range、semantic token、completion source、hover source 或 diagnostic API，`styio-view` 是 `styio` IDE 维护组件的需求上游。

这条上游关系只适用于 IDE 能力需求，不改变语言语义的归属：语言语义仍由 `styio` 定义，`styio-view` 负责提出前端可用性和交互需求。

`styio-view` 的责任：

1. 用产品场景描述缺口，例如高亮、补全、outline、诊断跳转、运行视图或 AI 面板需要哪类语法事实。
2. 提供最小前端样例、期望的 token / range / diagnostic / completion 形状，以及 Flutter / editor 测试预期。
3. 说明当前 fallback 为什么不足，避免在前端长期复制 parser 或语义判定。
4. 在自己的计划或设计文档里记录依赖的 `styio` IDE 能力。

`styio` IDE 维护组件的责任：

1. 在 `styio` 主仓内优化基础 IDE / LSP / workspace / parser service，而不是要求 `styio-view` 读取私有编译器结构。
2. 将新增能力做成稳定、可测试、可版本化的公共接口，例如 token/range stream、semantic token、completion item、hover payload、diagnostic shape 或 workspace query。
3. 保持 parser / analyzer / IDE service 的生命周期状态机清晰，支持取消、增量更新、错误恢复和大文件边界。
4. 更新 `styio` 的 IDE/LSP/security/docs gate，并为 `styio-view` 提供消费说明。

闭环标准：`styio-view` 的前端需求有可复现样例，`styio` 的基础 IDE 套件提供稳定接口并通过本仓 gate，`styio-view` 再消费该接口并通过对应 Flutter / editor 测试。

## `styio` 到 `styio-spio` 的版本发布上游关系

当 `styio` 发布新版本时，`styio` 是 `styio-spio` 的上游。`styio-spio` 不决定编译器版本事实，但必须把新版本纳入包管理、工具链托管和生态通知流程。

`styio` 的责任：

1. 冻结版本号、channel、tag、commit、构建产物和校验信息。
2. 发布或记录 `styio-protocol` 变化，包括 `styio --machine-info=json`、compile-plan、diagnostics、runtime event 和兼容矩阵。
3. 提供版本发布说明、迁移说明和破坏性变更标记。
4. 说明 `styio-spio` 需要更新的托管仓库、toolchain manifest、registry 元数据或 `styio-protocol` contract 文件。

`styio-spio` 的责任：

1. 更新版本托管仓库或 toolchain index，让 `spio tool install/use/pin` 能发现并选择新 `styio` 版本。
2. 更新 `contracts/compat/styio-support.toml` 或等价兼容矩阵，标注支持的 `styio` 版本、channel 和接口能力。
3. 更新 registry / publish / package metadata 中引用的 compiler 版本范围。
4. 推送版本消息、registry 通知、release feed 或操作公告，让下游项目知道新编译器版本可用。
5. 运行 `styio_contract_compat_gate`、tool lifecycle tests、registry / publish gates 和受影响 workflow tests。
6. 如果新版本包含破坏性接口变化，在 `styio-spio` 内保留兼容窗口、迁移诊断和回滚路径。

闭环标准：`styio` 版本发布门禁通过，并且 `styio-spio` 能通过托管版本发现、安装 / 切换 / pin、兼容矩阵、registry/publish 和通知相关验证。

### compile-plan v1 联动闭环

当 `styio` 广告 `supported_contracts.compile_plan:[1]` 时，`styio-spio` 可以把 compile-plan v1 视为已 live baseline，但必须同时满足三件事：

1. `contracts/compat/styio-support.toml` 或等价兼容矩阵启用对应版本。
2. `spio build/run/test` 非 dry-run 只通过 `styio --compile-plan <path>` 执行，不读取 `styio` 私有源码结构。
3. 黑盒门禁验证 `spio` 生成 plan、`styio` 消费 plan，并写出输出目录、diagnostics 和 receipt。

闭环标准：`styio --machine-info=json`、`spio check`、`spio build/run/test` 和 `styio-interface-gate --require-compile-plan` 对同一个本地或发布版编译器给出一致的 compile-plan v1 结果。

## 标准工作流

### 1. 草稿阶段

在 `styio-dev-doc` 中先写清楚：

1. 变更目标。
2. 涉及的仓库。
3. 受影响的公共接口。
4. 每个仓库的实现责任。
5. 需要新增或收紧的测试。
6. 需要同步的文档入口。
7. 发布、回滚和兼容策略。

草稿必须用当前本地工作树核对，不要只根据远端 GitHub 页面写流程。

### 2. 接口冻结阶段

如果变更影响跨仓接口，先在 `styio` 冻结接口形状：

1. CLI 参数和退出码。
2. JSON / JSONL payload。
3. diagnostics category / code / subcode。
4. compile-plan 字段。
5. machine-info 字段。
6. runtime event family。
7. `styio-protocol` schema、样例和文档文件。

接口冻结后，`styio-spio` 和 `styio-view` 才能分别更新消费逻辑。

### 3. 仓库内实现阶段

每个仓库独立闭环：

| 仓库 | 必须闭环的内容 |
| --- | --- |
| `styio` | 设计 / specs、源码、pipeline/security/parser shadow/docs gate |
| `styio-spio` | governance / registry docs、resolver / registry / process tests、interop gates |
| `styio-view` | contracts / design docs、Flutter tests、prototype / hosted / execution adapter tests |

不要把仓库内门禁挪到 `styio-dev-doc`。这本手册只记录流程，不替项目仓库交付质量。

### 4. 同步阶段

从 `styio-dev-doc` 同步到三个仓库时，按这个顺序：

1. 同步共同流程摘要到每个仓库的 `docs/` 协作入口。
2. 在每个仓库添加本仓责任清单，不复制不属于本仓的实现细节。
3. 更新每个仓库的 docs index。
4. 运行每个仓库自己的 docs gate。
5. 运行每个仓库受影响的测试和交付 gate。
6. 在 `styio-dev-doc` 记录同步完成状态和差异。

同步不是简单复制整页。同步后的仓库文档必须指向本仓真实命令、真实测试和真实 owner。

## 变更类型矩阵

| 变更类型 | 先改 | 再改 | 必跑验证 |
| --- | --- | --- | --- |
| 新 token / 新语法 / 语法诊断 | `styio` | `styio-view` 高亮、补全、hover、diagnostic range；`styio-spio` 仅在 workflow 或 contract 受影响时跟进 | `styio` parser shadow/pipeline/security + `styio-view` editor/highlight/completion tests |
| 前端 IDE 需要基础语法分析能力 | `styio-view` 提需求 | `styio` IDE/LSP/workspace/parser service 补公共接口，`styio-view` 再消费 | `styio` IDE/LSP/security/docs gates + `styio-view` Flutter/editor tests |
| `styio` 新版本发布 | `styio` | `styio-spio` 版本托管仓库、toolchain index、compat matrix、registry/publish 元数据、通知消息 | `styio` release gates + `styio-spio` tool lifecycle/compat/registry/publish gates |
| 语言语义 / AST / IR | `styio` | `styio-spio`、`styio-view` 仅在接口受影响时跟进 | `styio` pipeline/security/parser shadow |
| `styio-protocol` / CLI / machine-info | `styio` | `styio-spio` contract、`styio-view` adapter | CLI diagnostics + consumer contract tests |
| `styio-protocol` / compile-plan | `styio` | `styio-spio` workflow、`styio-view` execution route | compile-plan tests + spio/view adapter tests |
| registry / publish | `styio-spio` | `styio` 仅在 `styio-protocol` 变化时跟进，`styio-view` 仅消费状态 | registry interop + resolver/process tests |
| IDE execution route | `styio-view` | `styio-spio` / `styio` 只在接口不足时补公开能力 | Flutter execution/hosted/local tests |
| 审计框架 / 缺陷流程 | `styio-audit` 或各项目仓 | 三仓只同步本仓审计入口和缺陷状态 | audit gate + docs gate |
| 许可证 / 依赖商业风险 / secret 扫描 | `styio-audit` 定义规则，各项目仓维护证据 | `styio-dev-doc` 只同步开发流程说明 | audit gate + docs gate + repo hygiene |

## 跨仓门禁要求

每次跨仓协作至少记录这些门禁结果：

1. `styio`：受影响 CMake targets、`ctest` labels、`checkpoint-health` 是否需要运行。
2. `styio-spio`：native tests、Python unit tests、interop gates、contract gates。
3. `styio-view`：Flutter unit tests、prototype tests、hosted/local adapter tests、CI lane。
4. 文档：`styio-dev-doc` 的 GitBook link check，三个项目仓的 docs index / docs audit。
5. 审计：外部 `styio-audit` 的 framework-only gate，以及 full gate 是否被开放 defect record 阻塞。
6. 许可证和依赖：Apache-2.0 证据、`DEPENDENCY-USAGE.md`、manifest inventory 和 secret-history 结果是否需要更新。

如果某个 gate 当前无法通过，不能在流程里写成“已闭环”。必须写清楚：

1. 失败命令。
2. 失败原因。
3. 是否质量 gate 本身正确。
4. 需要哪个仓库负责修复。

## 文档同步位置建议

稳定后同步到三仓时，建议落点如下：

| 仓库 | 建议同步文件 |
| --- | --- |
| `styio` | `docs/specs/` 或 `docs/teams/COORDINATION-RUNBOOK.md` |
| `styio-spio` | `docs/governance/` 或 `docs/planning/` |
| `styio-view` | `docs/design/` 或 `docs/plans/` |

如果仓库已有 `docs/audit/`，审计结论仍放在 `docs/audit/`。协作流程只引用审计结论，不替代缺陷记录。

## 最小草稿模板

```md
# Cross-Repository Change Draft

## Goal

## Affected Repositories

## Public Interface Impact

## Styio-Protocol Impact

## Repository Responsibilities

## Syntax / IDE Adaptation Plan

## IDE Service Requirement Backlog

## Version Hosting And Release Notification Plan

## Required Tests And Gates

## Documentation Sync Plan

## Audit And Defect Status

## Rollback Plan
```

## 当前状态

这页是第一版流程。下一步同步前，需要为三个仓库分别补本仓版本：

1. `styio`：强调上游语义、`styio-protocol` / machine interface、checkpoint gate。
2. `styio-spio`：强调 contract 消费、版本托管、发布通知、resolver/registry/process lifecycle、interop gates。
3. `styio-view`：强调 UI/adapter/runtime state machine、IDE service 需求、Flutter tests、hosted/local execution route。

## 继续阅读

- [仓库矩阵与来源优先级](repository-matrix.md)
- [审计、许可证与依赖合规](../standards/audit-license-and-dependency-policy.md)
- [Styio 本体开发流程](styio-core-workflow.md)
- [styio-spio 开发指引](styio-spio-development.md)
- [styio-view 开发指引](styio-view-development.md)
