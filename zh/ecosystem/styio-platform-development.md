# styio-platform 开发指引

这页负责明确 `styio-platform`（平台与云服务）的开发流程与维护边界。

`styio-platform` 并不是在本地运行的工具仓，而是支撑整个生态后端的服务内核。

## 当前阶段

`styio-platform` 是支撑 `Spio` registry 和远端执行能力的基础设施。开发时，需要将其视为高可用、契约驱动的独立分布式系统，而不是编译器的简单扩展。

## 平台的核心职责

`styio-platform` 主要负责：

- **服务内核 (Service Core)**：核心调度、鉴权与对外 API。
- **Registry Distribution**：包管理器的云端仓库源、版本校验、包元数据分发。
- **Regional Node & Worker Control**：区域节点路由与云端执行 worker 的生命周期管理。
- **平台交付门禁 (Delivery Gates)**：安全扫描、合规性审计阻断、发布流水线管控。

它**不负责**：

- 本地编译器语义和执行逻辑（应在 `styio`）。
- 本地项目工作流或客户端命令行体验（应在 `Spio`）。

## 开发顺序与规范

开发平台侧能力时，必须遵循以下顺序：

1. **先对齐 Contract (契约)**：平台与客户端（如 `Spio`）的交互高度依赖已发布的 API 契约和 Registry Protocol。任何涉及 I/O 的变动需优先通过 API 设计文档达成一致。
2. **遵守安全审计**：由于涉及用户资产，任何鉴权、密钥管理与状态落盘的改动，必须符合 `styio-audit` 提供的数据安全规范。
3. **文档与架构先行**：先更新 `docs/design/`、OpenAPI 定义或 GraphQL Schema，再进入后端服务实现。

## 与其他仓库的关系

- **作为 `Spio` 的上游服务**：平台是包数据的**分发者**和**校验者**。当客户端发起 `publish` 或 `fetch` 时，平台执行最终裁决。
- **消费 `styio-audit` 策略**：平台不自己硬编码风险黑名单，而是消费审计框架提供的 manifest inventory 和安全策略。
- **与 `Vityo` 的云端协同**：如果 iOS 等端点需要走“云执行主路径”，平台必须提供安全沙箱和执行路由。

## 验证与发布

云端服务的破坏性要远大于本地 CLI：

- 本地开发需利用 Mock 或 Docker 容器完成全链路沙盒测试。
- 服务端部署需要灰度验证（Staging/Canary），任何破坏性接口改动必须提供版本化的兼容窗口。
- 必须包含针对 Registry 和 Worker 的负载或混沌回归测试。

## 继续阅读

- [仓库矩阵与来源优先级](repository-matrix.md)
- [三仓库协作流程](three-repository-collaboration.md)
- [Spio 开发指引](spio-development.md)
