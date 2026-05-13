# 仓库矩阵与来源优先级

这页复用 `styio` 主仓库 `README.md` 的生态入口矩阵，并把维护者真正需要的另一件事写清楚：**更新文档时，应该先信哪个仓库。**

## 生态矩阵

以下职责边界以 `styio/README.md` 和 `styio/docs/specs/REPOSITORY-MAP.md` 为基线整理：

| Repository | Role | 主职责 |
| --- | --- | --- |
| `styio` | 语言与编译器主仓库 | 语言语义、编译器实现、CLI、测试、主设计/规格文档 |
| `Spio` | 包管理器 | manifest、lockfile、resolver、workflow、`styio-protocol` 消费 |
| `styio-platform` | 平台与云服务 | 服务内核、registry distribution、regional node、worker control、平台交付门禁 |
| `styio-audit` | 审计框架 | 跨仓库 audit gate、许可证策略、商业风险、manifest inventory、secret 扫描 |
| `styio-dev-doc` | 开发者文档 | 跨仓库维护手册、开发流程、协作规范 |
| `styio-dev-env` | 标准开发环境 | toolchain bootstrap、环境脚本、统一环境约定 |
| `styio-book` | 产品白皮书 | 对外叙述、愿景、产品级说明 |
| `Vityo` | 专属 IDE / 运行视窗 | 编辑器、运行可视化、AI 面板、主题系统、平台执行策略 |
| `styio-examples` / `styio-example` | 示例工程 | 可运行样例、模板、最佳实践示例 |
| `styio-ext-vsc` / future extensions | Extension | 宿主编辑器集成、高亮、插件命令、设置项与诊断呈现 |

## 更新文档时的来源优先级

维护这份 GitBook 时，默认按以下顺序取最新事实：

1. **本地已检出的工作树**
2. **同名 `Unka-Malloc/*` 仓库**
3. **`eBioRing/*` 仓库或镜像**

这条规则不是抽象建议，而是当前生态的现实：

- `Unka-Malloc` 分支通常比 `eBioRing` 更靠前
- 本地工作树通常又比云端仓库更靠前

所以在写文档前，不要只看 GitHub 页面，要先看你本地现在到底有什么。

## 本次远端同步基线

当维护者明确要求“按 GitHub 最新公开状态补文档”时，不要只说“最新”，要把 branch 和 commit 记下来。

本轮核对结果是：

- `eBioRing/styio` `main` = `193f36b48e55e076d05c750d58e2850300ad6e43`
- `eBioRing/styio` `dev` = `09e93c7fd6056fc2cbc2afab09353657d28a032b`
- `eBioRing/Spio` `agent-dev` = `b3d044a95857bfe6206ef8fd591df456091e8f92`
- `eBioRing/Spio` `main` = `2ce0b8be1839b14d529b0af9c9d69011160456a1`

当前这次 GitBook 同步默认按：

1. `styio`：`eBioRing/styio@main`
2. `Spio`：`eBioRing/Spio@agent-dev`

## 2026-04-12 本地核对快照

当前本地可见的核心工作树状态是：

- `styio`：`agent-dev`，活跃实现仓，工作树比云端更前
- `Spio`：本地工作树仍在演进，但已发布远端 `agent-dev` 现在也有完整 native `C++20` surface、registry、publish 和 tool management
- `Vityo`：`agent-dev`，处于 architecture bootstrap，当前以 `docs/` 为主要事实来源
- `styio-ext-vsc`：当前工作区未见本地仓，文档回退到云端 `eBioRing/styio-ext-vsc`，其 `README.md` 目前极简
- `styio-dev-doc`：`agent-dev`，当前这本 GitBook 的工作树

这意味着：

- `styio` 文档应先看本地 `README.md`、`docs/`、`src/`、`tests/`
- 如果你要同步已发布编译器事实，`styio` 先看 `eBioRing/styio@main`
- `Spio` 文档应先看本地 `README.md`、`docs/`、`src/`；若同步已发布 package-manager surface，先看 `eBioRing/Spio@agent-dev`
- `Vityo` 文档应先看本地 `README.md`、`docs/`
- Extension 文档若无本地工作树，先看当前参考仓，再回到 `styio` / `Spio` 的公开接口

## 文档更新前的最小检查

每次更新跨仓库文档前，至少做这四步：

1. 看主仓或工具仓的 `README.md`
2. 看该仓的 `docs/README.md` 或 `docs/specs/`
3. 看当前分支和工作树是否有未提交变更
4. 只有在本地没有事实来源时，才回退到 GitHub 仓库页面

## 冲突时怎么判

当多个仓库对同一问题说法不一致时：

1. 语言、编译器、测试验收：回到 `styio`
2. 包管理、resolver、contract 兼容：回到 `Spio`
3. 平台服务、registry distribution、regional node、worker control：回到 `styio-platform`
4. 审计框架、许可证策略、商业风险、manifest inventory、secret 扫描：回到 `styio-audit`
5. IDE 产品交互、运行视图、主题和平台执行策略：回到 `Vityo`
6. VS Code 或别的宿主编辑器设置、命令和集成方式：回到对应 Extension 仓
7. 这份 GitBook 只负责归纳和维护流程，不反向覆盖各仓自己的 SSOT

## 继续阅读

- [Styio 本体开发流程](styio-core-workflow.md)
- [审计、许可证与依赖合规](../standards/audit-license-and-dependency-policy.md)
- [三仓库协作流程](three-repository-collaboration.md)
- [Spio 开发指引](spio-development.md)
- [Spio 当前能力与边界](spio-surface.md)
- [Vityo 开发指引](vityo-development.md)
- [Extensions 开发指引](extensions-development.md)
