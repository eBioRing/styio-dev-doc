# Spio 当前能力与边界

这页不讲抽象“愿景”，只记录 2026-04-12 这轮 GitHub 同步里，`Spio` 当前已经公开了什么、还没公开什么。

本文把 `spio` 与 `styio` 之间的静态交接契约统一称为 `styio-protocol`。它是 CLI / machine-info / compile-plan / diagnostics / compat matrix 组成的公开协议，不是运行时套件。

## 本次核对基线

当前远端公开状态：

- 最新工作线：`eBioRing/Spio@agent-dev` = `b3d044a95857bfe6206ef8fd591df456091e8f92`
- 合并快照：`eBioRing/Spio@main` = `2ce0b8be1839b14d529b0af9c9d69011160456a1`

这轮维护手册默认以 `agent-dev` 作为 `spio` 最新公开实现面。

## 已经公开的命令面

当前 `spio` 已明确公开这些命令族：

- `new`
- `init`
- `check`
- `add`
- `remove`
- `fetch`
- `lock`
- `tree`
- `vendor`
- `build`
- `run`
- `test`
- `pack`
- `publish`
- `tool install`
- `tool use`
- `tool pin`
- `machine-info --json`

这不是“未来打算支持”，而是 `docs/governance/Spio-CLI-Contract.md` 和 `src/SpioCLI/CLI.cpp` 已经列出的公开 surface。

## 今天已经活着的能力

### 1. Native core

当前公开实现已经不是只剩 bootstrap scaffold。native `C++20` + `CMake` 路径已覆盖：

- manifest / lock parse 与 canonical write-back
- `single-version-v1` resolver
- workspace / path / git / registry 依赖源
- tree / fetch / vendor
- deterministic `pack`

### 2. Registry consume / publish

当前已公开：

- registry dependency source
- `file://`
- `http://`
- `https://`
- local filesystem publish
- anonymous HTTP `PUT` publish
- static blob-and-index layout

也就是说，`spio` 当前不仅能本地打包，还已经公开了 registry consume 和 publish transport。

### 3. Managed local Styio toolchain

当前已公开：

- `spio tool install --styio-bin <path>`
- `spio tool use --version <x.y.z> [--channel <channel>]`
- `spio tool pin ...`
- `SPIO_HOME/tools/styio/...`
- project-local `spio-toolchain.toml`

这意味着 `spio` 已经开始承担 **Styio 编译器本地安装、切换、项目级 pin** 的职责，不再只是 dependency resolver。

当 `styio` 发布新版本时，这个职责会被触发：`spio` 需要更新版本托管仓库或 toolchain index，确保新版本可以被发现、安装、切换和 pin，并同步兼容矩阵、registry/publish 元数据和通知消息。

### 4. Compile-plan dry-run

当前已公开：

- `spio build --dry-run`
- `spio run --dry-run`
- `spio test --dry-run`
- 本地 `.spio/build/<cache-key>/plan.json`

这里的关键边界是：

- `spio` 已经公开 **plan generation**
- 并且通过 `styio-protocol` 宣称 compile-plan v1 已 live

## 今天仍未公开完成的能力

以下边界仍然不能写成“已经支持”：

- auth / account / signatures / stronger trust policy
- private security module
- 更激进的多版本 resolver
- compile-plan v1 之外的未来 schema / release matrix

换句话说，当前正确说法是：

- `spio` 已经有真实 package-manager core
- compile-plan v1 compiler-execution `styio-protocol` 已经 live
- 更高版本协议和发布矩阵仍受 `styio` 公共接口发布状态约束

## 现在该看哪些目录

如果你要维护 `spio@agent-dev`，优先看这些目录：

- `docs/governance/`
- `docs/security/`
- `docs/registry/`
- `docs/adr/`
- `docs/operations/`
- `src/SpioCLI/`
- `src/SpioManifest/`
- `src/SpioResolve/`
- `src/SpioPack/`
- `src/SpioPublish/`
- `src/SpioRegistryClient/`
- `src/SpioRegistryServer/`
- `src/SpioSecurity/`
- `src/SpioTool/`
- `src/SpioVendor/`

## 最关键的 gate

除了老的 manifest / compat gate，现在还要把这些 gate 当成一线入口：

- `styio_compile_plan_contract_gate`
- `spio_registry_server_gate`
- `spio_registry_promotion_gate`
- `spio_registry_split_origin_http_gate`
- `spio_cli_gate`
- `spio_extractability_gate`
- `styio_spio_dual_maintenance_gate`
- `styio_contract_compat_gate`

## 和 `styio` 的正确边界

今天 `spio` 对 `styio` 的正确依赖仍然只有：

- `styio --machine-info=json`
- 已发布的 `styio --compile-plan <path>`
- `contracts/compat/styio-support.toml`
- published diagnostics / handshake fields

不要因为 `spio` 自己已经进化出 registry、publish、toolchain lifecycle，就反过来把它写成能读取 compiler internals。

## 继续阅读

- [Spio 开发指引](spio-development.md)
- [仓库矩阵与来源优先级](repository-matrix.md)
- [CLI 与 Machine Interface 改动手册](../runbooks/cli-and-machine-interface.md)
