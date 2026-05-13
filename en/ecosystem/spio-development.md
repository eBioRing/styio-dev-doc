# Spio 开发指引

这页只写 `Spio` 的开发流程和约束。

`Spio` 是 Styio 的包管理器和项目工作流工具，不是编译器子模块。

## 当前阶段

按 2026-04-12 GitHub 核对，`Spio` 现在应按这些已发布事实来理解：

- `eBioRing/Spio@agent-dev` 是当前最新公开工作线
- native `C++20` + `CMake` core 已经承载真实 CLI / resolver / pack / publish / tool lifecycle
- Python bootstrap 仍在树内，但只作为迁移参考

所以维护 `Spio` 时，不要再把它写成“只有 bootstrap 想法”的工具仓。更准确的说法是：

- 它已经有真实 package-manager surface
- 同时仍保留 bootstrap 到 native 的迁移包袱

## `Spio` 负责什么

当前职责包括：

- `spio.toml` / `spio.lock`
- 依赖解析
- source fetch
- registry consume / publish
- project workflow 命令
- managed local `styio` tool lifecycle
- `styio-protocol` 消费
- compile-plan 生成、schema 和兼容矩阵

不负责：

- 语言语义
- parser / analyzer / codegen
- 直接读取 `styio` 私有源码结构

## 文档优先级

`Spio/docs/README.md` 当前给出的优先级是：

1. `governance/`
2. `security/`
3. `registry/`
4. `adr/`
5. `operations/`
6. `planning/`
7. `styio/`

也就是说，开发时先看规范、安全和 registry contract，再看 ADR / operations / planning，最后才看对 `styio` 的外部知识包。

## 不可违反的边界

`Spio-Version-Decoupling-Constraints.md` 当前冻结了这些硬约束：

- 不能链接 `styio` 私有实现库
- 不能包含 `styio` 私有头文件
- 不能自己维护一份 Styio grammar fork
- 只能通过机器握手和公开 `styio-protocol` 跟 `styio` 交互
- 兼容性必须通过 `styio --machine-info=json` 和 `contracts/compat/styio-support.toml` 判定

这意味着 `spio` 和 `styio` 的关系默认是：

- **进程边界**
- **版本解耦**
- **契约驱动**

不是源码级耦合。

## `styio-protocol` 是什么

`styio-protocol` 是 `spio` 消费 `styio` 的静态协议边界，不是运行时套件，也不是可链接的 `styio` 服务模块。

它至少包括：

- `styio --machine-info=json` 能力握手
- 已发布的 `styio --compile-plan <path>` contract
- JSON / JSONL diagnostics 和公开退出码
- compiler version、channel、compat matrix 和迁移窗口
- `spio` 需要验证的 schema、样例和 contract tests

只要需求越过进程边界，就先判断它是不是 `styio-protocol` 变更。是协议变更时，由 `styio` 冻结生产者事实，`Spio` 只负责消费、校验和兼容策略；不是协议变更时，不要把 `styio` 内部实现拿进 `spio`。

## 代码树怎么读

当前本地 `src/` 已经体现出原生实现方向：

- `SpioCLI/`
- `SpioCompat/`
- `SpioCore/`
- `SpioManifest/`
- `SpioPack/`
- `SpioPlan/`
- `SpioPublish/`
- `SpioRegistryClient/`
- `SpioRegistryServer/`
- `SpioResolve/`
- `SpioSecurity/`
- `SpioTool/`
- `SpioTree/`
- `SpioVendor/`
- `SpioWorkflow/`

同时还保留：

- `src/spio_bootstrap/`

这说明今天的正确策略是：

- 新工作优先落到原生 `C++20` 路径
- 旧 Python bootstrap 只作为参考，不应继续扩张成长期主线

## `Spio` 的开发顺序

推荐顺序是：

1. 先看 `governance/` 里的 contract 和 decoupling 规则
2. 再看 `adr/` 是否已有决策
3. 再改 `src/` 和 `contracts/`
4. 再跑验证矩阵与 preflight
5. 最后同步 `docs/`

## 测试与验证规则

`tests/README.md` 当前明确要求：

- 每次测试都要用新的临时 `SPIO_HOME`
- integration test 必须通过 `SPIO_STYIO_BIN` 指向外部 `styio`
- 不得假设能直接访问 `styio` 源码树

这类隔离不是形式主义，而是为了证明 `spio` 真能独立维护。

## 当前关键 gate

最重要的命名 gate 包括：

- `spio_manifest_lock_gate`
- `styio_contract_compat_gate`
- `styio_compile_plan_contract_gate`
- `contract_schema_gate`
- `spio_cli_gate`
- `spio_registry_server_gate`
- `spio_registry_promotion_gate`
- `spio_registry_split_origin_http_gate`
- `spio_extractability_gate`
- `styio_spio_dual_maintenance_gate`

常用命令先看：

```text
./scripts/native-check.sh
./scripts/preflight-readiness-check.py --styio-bin /absolute/path/to/styio
```

## 当前公开能力边界

今天可以直接写成“已公开”的是：

- registry dependency source
- `pack`
- `publish --dry-run`
- local / `file://` / `http(s)` registry publish transport
- `tool install/use/pin`
- `build/run/test --dry-run`

今天还不能写成“已公开完成”的是：

- `styio --compile-plan <path>` 驱动下的公开非 dry-run 编译执行
- auth / signatures / private security module
- 放宽 `single-version-v1` 约束的 resolver 演进

## 和 `styio` 主仓的正确关系

`Spio` 只能消费这些公开边界：

- `styio --machine-info=json`
- 已发布的 `styio-protocol` compile-plan contract
- 兼容矩阵声明

如果你发现一个 `spio` 需求只能通过读取 `styio/src` 或 `styio/tests` 才能实现，正确动作不是加耦合，而是回到 `styio` 主仓补公共接口。

## `styio` 新版本发布后的跟进责任

当 `styio` 发布新版本时，`styio` 是上游，`Spio` 是版本托管和包生态消费方。`Spio` 不能自定义编译器版本事实，但必须把新版本同步到自己的工具链和 registry 工作流。

每次 `styio` 发版后，`Spio` 至少检查这些项：

1. 版本托管仓库或 toolchain index 是否新增该 `styio` 版本。
2. `spio tool install/use/pin` 是否能安装、选择和固定该版本。
3. `contracts/compat/styio-support.toml` 或等价兼容矩阵是否更新。
4. registry / publish / package metadata 是否引用正确的 compiler 版本范围。
5. release feed、registry 通知、操作公告或推送消息是否发出。
6. 破坏性变更是否有兼容窗口、迁移诊断和回滚路径。

对应验证至少覆盖：

1. `styio_contract_compat_gate`
2. tool lifecycle tests
3. registry / publish gates
4. 受影响的 workflow dry-run 或 `styio-protocol` compile-plan contract tests

## 维护原则

- `spio` 的权威边界在它自己的 `docs/governance/`
- 和 `styio` 的集成必须通过 `styio-protocol` contract，不通过源码内省
- 新增行为先问“会不会破坏版本解耦”
- `styio` 发版后，`spio` 必须跟进版本托管、兼容矩阵和生态通知

## 继续阅读

- [仓库矩阵与来源优先级](repository-matrix.md)
- [Spio 当前能力与边界](spio-surface.md)
- [CLI 与 Machine Interface 改动手册](../runbooks/cli-and-machine-interface.md)
