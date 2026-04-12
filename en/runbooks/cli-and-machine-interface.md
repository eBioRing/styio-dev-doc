# CLI 与 Machine Interface 改动手册

这页针对的是 `src/main.cpp` 这条入口链，而不是一般的语言功能改动。

如果你要改 CLI 参数、退出码、JSONL 诊断或 `--machine-info=json` 的握手内容，这页就是最小闭环。

## 当前 CLI 契约

当前 `main.cpp` 负责：

- 参数解析
- 文件读取
- `Lex -> Parse -> TypeInfer -> StyioIR -> LLVM IR -> JIT` 驱动
- 诊断分类与退出码
- `machine-info` 输出
- parser shadow compare 和 artifact 写出

这意味着 CLI 改动不是“只改一行 help 文本”，通常会连带影响：

- 自动化脚本
- 测试断言
- 文档手册

## 哪些内容算 CLI / machine interface 变更

包括：

- 新增 / 修改 CLI flag
- `styio-nano` packaging / profile 相关 flag
- `--machine-info=json` 字段变更
- `--error-format` 行为变更
- 退出码变化
- 诊断 `category` / `code` / `subcode` 变化
- parser shadow artifact 相关参数变化

## 明确不要改的地方

- 不要修改 `src/include/cxxopts.hpp`

CLI 行为应该通过 `main.cpp` 配置和本地逻辑调整，而不是碰 vendored 参数库。

## 修改顺序

### 1. 先改参数定义和约束

至少同步：

- `src/main.cpp` 中的 `options.add_options()`
- 参数合法性校验

当前已有的约束包括：

- `--error-format` 只接受 `text|jsonl`
- `--machine-info` 只接受 `json`
- `--parser-engine` 只接受 `legacy|nightly`，并兼容 `new`
- `--parser-shadow-artifact-dir` 必须和 `--parser-shadow-compare` 一起使用
- `--nano-create` 和 `--nano-publish` 互斥
- `styio-nano` packaging 参数必须跟 `--nano-create` 或 `--nano-publish` 一起出现

### 2. 再改输出契约

至少同步：

- `styio_emit_machine_info_json()`
- `styio_emit_diagnostic(...)`
- `styio_exit_code(...)`

如果你改的是机器接口，先想清楚会不会破坏现有消费者。

### 3. 如果涉及 parser shadow，再看 artifact 写出

至少同步：

- `styio_parse_engine_to_repr_latest(...)`
- `styio_write_shadow_artifact_latest(...)`

这里的变更会直接影响：

- `.jsonl` artifact
- primary/shadow AST payload
- route detail 文本

### 4. 最后补测试和文档

至少同步：

- `tests/styio_test.cpp`
- 本手册
- [CLI 与调试工作流](../toolchain/cli-and-debug-workflow.md)
- 如果错误模型变了，再补 [诊断与错误模型手册](diagnostics-and-error-model.md)

## `--machine-info=json` 的稳定面

当前测试会断言至少这些字段存在：

- `"tool":"styio"`
- `"compiler_version":"0.0.1"`
- `"channel":"stable"`
- `"supported_contracts":{"compile_plan":[]}`
- `"machine_info_json"`
- `"single_file_entry"`
- `"jsonl_diagnostics"`
- `"edition_max":"2026"`

如果你改这些字段，必须有明确的兼容理由，并同步对应测试。

当前公开边界还包括一条容易写错的事实：

- `supported_contracts.compile_plan` 仍然可以是空数组

也就是说，源码里拥有 compile-plan 相关定义，不等于已发布 machine handshake 宣称可执行 compile-plan。

## 最小命令

### machine-info 握手

```bash
./build/bin/styio --machine-info json
```

### 默认 CLI 运行

```bash
./build/bin/styio --file tests/milestones/m1/t01_int_arith.styio
```

### JSONL 诊断

```bash
./build/bin/styio --error-format jsonl --file some.styio
```

### shadow 参数约束

```bash
./build/bin/styio \
  --parser-engine legacy \
  --parser-shadow-artifact-dir /tmp/styio-shadow \
  --file tests/milestones/m1/t01_int_arith.styio
```

这条命令当前应报 `CliError`，因为缺少 `--parser-shadow-compare`。

## 现成回归入口

直接相关的现有测试包括：

- `StyioDiagnostics.MachineInfoJsonReportsStableHandshakeFields`
- `StyioParserEngine.UnsupportedEngineIsRejected`
- `StyioParserEngine.ShadowArtifactDirRequiresShadowCompareFlag`
- `StyioDiagnostics.RuntimeHelperErrorEmitsJsonlRuntimeDiagnostic`
- `StyioDiagnostics.RuntimeWriteHelperErrorEmitsJsonlRuntimeDiagnostic`

直接跑：

```bash
ctest --test-dir build -R '^(StyioDiagnostics\\.MachineInfoJsonReportsStableHandshakeFields|StyioParserEngine\\.(UnsupportedEngineIsRejected|ShadowArtifactDirRequiresShadowCompareFlag)|StyioDiagnostics\\.(RuntimeHelperErrorEmitsJsonlRuntimeDiagnostic|RuntimeWriteHelperErrorEmitsJsonlRuntimeDiagnostic))$' --output-on-failure
```

## 常见漏项

- help 文本改了，但参数校验没改
- 退出码变了，没同步诊断测试
- `machine-info` 字段变了，没同步稳定握手断言
- shadow artifact 字段变了，没同步相关 parser test
- 文档只更新了 CLI 页，没更新错误模型页

## 维护规则

CLI / machine interface 变更默认要满足三件事：

1. 人类在终端里还能理解
2. 机器接口还能稳定消费
3. 失败时退出码和错误分类仍可预测

只满足第一点，不够维护；只满足第二点，也不够可用。
