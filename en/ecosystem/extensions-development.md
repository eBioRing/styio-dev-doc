# Extensions 开发指引

这页写的是 **Styio Extension** 的通用开发约束，不只服务 `styio-ext-vsc`。

当前具体参考实现是云端仓库 `eBioRing/styio-ext-vsc`，但后续如果出现别的编辑器扩展，也应默认遵守这一页的边界。

## 当前事实来源

按 2026-04-12 核对：

- 当前工作区里没有本地 `styio-ext-vsc` 工作树
- 当前可见参考仓库是 `eBioRing/styio-ext-vsc`
- 该仓库目前只有极薄的 `README.md`

所以这页的职责不是替扩展仓凭空发明一套产品设计，而是给维护者一套稳定的 Extension 边界和开发顺序。

## Extension 负责什么

Extension 仓默认只负责宿主编辑器集成，例如：

- 语法高亮
- snippets / language configuration
- 命令入口、任务入口、设置项
- 调用 `styio` / `spio` 二进制
- 渲染 diagnostics、输出面板和基础开发体验

## Extension 不负责什么

Extension 仓不负责：

- 语言语义 SSOT
- parser / analyzer / codegen / runtime 实现
- 包管理器核心逻辑
- 反向定义 “Styio 程序应该怎样被解释”

如果一个扩展需求要求你先修改语言定义，那正确动作是先回 `styio` 主仓补公共接口，而不是在扩展里偷偷假设语义。

## 只能消费公开边界

Extension 应当优先消费：

- `styio` CLI
- `styio --error-format jsonl`
- `styio --machine-info=json`
- 稳定的文件输入 / 输出行为
- 已发布的 `spio` CLI 或 machine contract

不要依赖：

- `styio` 私有头文件
- `styio` 内部 AST / IR 内存布局
- 未文档化的 parser 分支行为
- 一份自己维护的语法副本来定义真实语言规则

## 和 `styio-view` 的区别

`styio-view` 是 Styio 自己的产品级 IDE / 运行视窗。

Extension 仓是宿主编辑器里的适配层。它的目标是把现有能力接进 VS Code 或未来别的编辑器，而不是承载整套产品交互和平台执行策略。

因此：

- 产品交互和平台边界优先回 `styio-view`
- 语言、CLI、diagnostics、machine interface 优先回 `styio`
- 宿主编辑器的命令、设置项、集成方式才回 Extension 仓

## 推荐开发顺序

1. 先确认宿主编辑器能力和扩展清单
2. 再确认 `styio` / `spio` 是否已经暴露足够的公共接口
3. 公共接口不够时，先回源仓补接口
4. 然后实现扩展侧命令、设置和渲染
5. 最后补扩展仓自己的 README、示例和回归验证

## 兼容性原则

- 优先允许用户显式配置本地 `styio` / `spio` 二进制路径
- 能靠 `--machine-info=json` 判能力，就不要写死版本判断
- 能降级就降级，不要因为一个高级能力缺失就让整个扩展失效
- 不要把编译器私有实现细节变成扩展的稳定契约

## 当前对 `styio-ext-vsc` 的使用方式

在这本手册里，`styio-ext-vsc` 当前只作为：

- Extension 家族的现有参考仓
- VS Code 场景下的命名实例

不要把它误当成整个编辑器生态的唯一形态。以后有新的 Extension 仓，这页仍然适用。

## 继续阅读

- [仓库矩阵与来源优先级](repository-matrix.md)
- [Styio 本体开发流程](styio-core-workflow.md)
- [styio-view 开发指引](styio-view-development.md)
- [CLI 与 Machine Interface 改动手册](../runbooks/cli-and-machine-interface.md)
