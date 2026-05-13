# styio-audit 开发与维护指引

这页负责明确 `styio-audit`（审计框架）的维护边界和规则。

`styio-audit` 是 Styio 生态的“合规与安全大闸”，它不产生业务代码，但它拥有阻断构建和发布的最高权限。

## 核心职责

`styio-audit` 负责：

- **许可证策略 (License Policy)**：定义哪些开源协议是允许的、哪些是禁止的（商业风险拦截）。
- **依赖合规 (Dependency Compliance)**：检查第三方依赖的引入是否符合合规要求，维护 Manifest Inventory。
- **密钥与凭证扫描 (Secret Scanning)**：跨越整个生态仓库的防泄漏扫描。
- **跨仓合规门禁 (Cross-repo Audit Gates)**：提供可被 CI/CD 和 `styio-platform` 消费的审计脚本和规则库。

## 与其他仓库的关系

- **对于所有仓库**：`styio-audit` 定义的 CI gate 是不可绕过的。
- **与 `styio-platform`**：平台服务在允许 Registry 发布新包时，必须调用 `styio-audit` 的策略引擎进行检查。
- **与 `Spio`**：包管理器在生成 lockfile 时，其安全检查逻辑受 `styio-audit` 规范约束。

## 维护原则

1. **一票否决权**：如果合规策略发生冲突，以 `styio-audit` 的定义为最高优先级。
2. **规则代码化 (Policy as Code)**：审计规则必须是机器可读的（如 YAML/JSON 策略文件或 Python 检查脚本），避免纯文本的人工审计。
3. **隔离性**：审计工具自身的依赖必须极简，避免引入安全风险。

## 继续阅读

- [审计、许可证与依赖合规](../standards/audit-license-and-dependency-policy.md)
- [仓库矩阵与来源优先级](repository-matrix.md)
