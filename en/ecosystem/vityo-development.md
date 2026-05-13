# Vityo 开发指引

这页只写 `Vityo` 的开发流程和规范。

`Vityo` 不是主编译器仓，而是 Styio 的专属 IDE、运行视窗和 AI 协作前端。

如果你要维护的是 VS Code 或别的宿主编辑器 Extension，不要走这页，先看 [Extensions 开发指引](extensions-development.md)。

## 当前阶段

按 2026-04-12 本地核对，`Vityo` 现在仍处于：

- `architecture bootstrap`
- docs-first
- 先冻结产品规格、系统架构、ADR、计划和平台边界，再进入实现

这意味着维护 `Vityo` 时，默认先动 `docs/`，不是先开 UI 代码。

## `Vityo` 负责什么

当前职责包括：

- 专属编辑器引擎
- 运行视图与可视化
- AI 面板
- 主题系统
- 模块宿主与 staged update
- 平台执行策略

不负责：

- 语言语义 SSOT
- parser / analyzer / IR / codegen 核心实现
- 反向改写 `styio` 语言规则

## 文档入口

当前本地 `docs/` 已经有明确入口：

- 产品规格：`docs/design/Styio-Vitrio-Product-Spec.md`
- 系统架构：`docs/design/Styio-Vitrio-System-Architecture.md`
- 协作规范：`docs/specs/CONTRIBUTOR-AND-AGENT-SPEC.md`
- 实施计划：`docs/plans/Styio-Vitrio-Implementation-Plan.md`
- ADR 索引：`docs/adr/INDEX.md`

所以 `Vityo` 的开发顺序应该由这些文档驱动，而不是从 README 直接跳到实现。

## 不可违反的产品和架构约束

当前 `CONTRIBUTOR-AND-AGENT-SPEC.md` 与架构文档已经冻结了几条硬规则：

- Source Buffer 永远是 canonical source
- visual substitution 不能静默改写用户源码
- 不能把 `Vityo` 退化成纯 Web 壳或传统 IDE 皮肤
- 不能在没有平台策略文档前承诺 iOS unrestricted 本地 JIT
- 新架构边界必须写 ADR，不能只改 README
- 新模块必须同时声明 manifest、capability matrix 和生命周期

## 当前架构主线

`Styio-Vitrio-System-Architecture.md` 当前的主线是：

- Flutter UI Runtime
- Custom Editor Engine
- Language Workspace Service
- `styio-core-c` Bridge
- Native Core / Execution Backends
- Module Host Runtime

这意味着 `Vityo` 和 `styio` 的正确关系不是“直接绑 C++ ABI”，而是：

- 通过稳定 C ABI 暴露能力
- 由 UI 和运行视图消费 token / block / diagnostic / event 等公共接口

## `Vityo` 的开发顺序

推荐顺序是：

1. 先改产品规格
2. 再改系统架构
3. 必要时补 ADR
4. 再改计划 / 里程碑 / 测试映射
5. 最后才进入实现

如果你跳过前四步直接改代码，后面很容易出现：

- 产品语义和平台策略冲突
- 桌面与移动端交互混线
- 本地执行与云执行边界失控

## 平台策略要单独看

当前文档已经把平台执行策略分开：

- Desktop：本地优先
- Android：本地优先，分阶段到位
- iOS：云执行主路径，不暴露本地编译模块
- Web：轻量查看和演示，不是首发全功能主平台

因此 `Vityo` 的开发指引必须始终带着平台约束走，不能把桌面方案直接复制到移动端。

## 与 `styio` 主仓的正确边界

`Vityo` 应当消费：

- diagnostics
- token / block ranges
- AST / IR 文本 repr
- compile / run 触发接口
- runtime event stream

但不应自行定义：

- 语言语义
- parser 接受什么程序
- type system 的真正判定

如果 IDE 需要一个新能力，而当前 `styio` 没有稳定公共接口，正确动作是回主仓补接口，而不是在 `Vityo` 自己假设一份语义。

## 语法新特性的 IDE 适配责任

当 `styio` 主仓添加新 token、新关键字、新表达式、新语句、新资源语法或新的诊断形状时，`styio` 是上游，`Vityo` 是 IDE 消费方。

`Vityo` 必须针对新语法检查这些面：

1. 语法高亮和 token 分类。
2. 补全、snippet、hover 和上下文提示。
3. 诊断 range、错误文本呈现和 quick navigation。
4. block / outline / runtime surface 是否能正确识别新结构。
5. 编辑器测试和 Flutter 测试是否覆盖新语法样例。

如果 `Vityo` 发现当前公共接口不足以实现高亮或补全，不允许在前端复制 parser 规则作为长期方案。正确流程是回到 `styio` 补充稳定的 token、range、diagnostic 或 repr 接口，再由 `Vityo` 消费。

## 对 `styio` IDE 组件的需求上游责任

`Vityo` 实现前端时，如果发现 `styio` 的基础 IDE 套件缺少必要能力，`Vityo` 是 `styio` IDE 维护组件的需求上游。这里的“上游”是需求上游，不是语言语义上游。

典型触发条件：

1. 高亮需要更细的 token 分类或 semantic token。
2. 补全需要 parser / analyzer 暴露稳定 completion source。
3. outline、breadcrumb 或 block navigation 需要稳定 block / symbol range。
4. diagnostic navigation 需要更精确的 range、severity、code、subcode 或 fix hint。
5. AI 面板需要可审计的 AST / IR / runtime event 摘要，而不是自由文本猜测。

`Vityo` 需要给出产品场景、最小样例、期望 payload 和测试预期；`styio` 需要在 IDE / LSP / workspace / parser service 内补稳定公共接口。`Vityo` 不应把临时 workaround 固化成自己的语言分析实现。

## 维护原则

- docs-first
- spec / architecture / ADR 先于实现
- 平台策略和模块生命周期必须先落文档
- 语言真相始终回到 `styio`
- 语法高亮和补全跟随 `styio`，不得反向定义语言规则
- 前端 IDE 缺口可以上行驱动 `styio` IDE 组件，但不能反向改写语言语义

## 继续阅读

- [仓库矩阵与来源优先级](repository-matrix.md)
- [三仓库协作流程](three-repository-collaboration.md)
- [Styio 本体开发流程](styio-core-workflow.md)
