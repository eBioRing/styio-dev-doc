# Parser Shadow 与双轨迁移手册

这页只服务 parser 迁移维护者。它关注的不是“怎么写 parser”，而是“怎么在 `legacy` / `nightly` 双轨并存时不把仓库拖坏”。

## 当前双轨契约

Styio 当前的 parser 相关命名和入口已经很明确：

- `legacy`：旧路径
- `nightly`：新路径，也是当前默认路径
- `latest`：统一入口

`src/main.cpp` 当前通过：

- `parse_main_block_with_engine_latest(...)`

驱动 parser，而不是直接调 `parse_main_block_legacy(...)`。

## Shadow Compare 是什么

打开：

```bash
./build/bin/styio \
  --parser-shadow-compare \
  --parser-shadow-artifact-dir /tmp/styio-shadow \
  --file some.styio
```

当前行为是：

1. 先用主 parser 产出 AST repr
2. 再用另一条 parser 路径跑一次
3. 比较 AST repr
4. 把结果写成 artifact

状态可能包括：

- `match`
- `mismatch`
- `shadow_error`

## Route Stats 的意义

当主 parser 是 `nightly` 时，当前还会记录：

- `nightly_subset_statements`
- `legacy_fallback_statements`
- `nightly_internal_legacy_bridges`

这不是调试噪音，而是迁移 KPI。

维护上的基本目标是：

- fallback 越少越好
- internal legacy bridge 越少越好
- 某些 gate 要求严格为零

## Artifact 里有什么

如果配置了 `--parser-shadow-artifact-dir`，当前会写：

- 一条 `.jsonl` 元记录
- mismatch / error 场景下的源码 payload
- primary AST 文本
- shadow AST 文本
- shadow error 文本

如果只是 `match`，通常只保留元记录。

## 什么时候必须跑 shadow

以下改动默认都要跑：

- `Parser.cpp`
- `NewParserExpr.cpp`
- `ParserLookahead.*`
- `Parser.hpp`
- parser 路由逻辑
- subset 覆盖扩展

如果你改的是 parser，但没跑 shadow compare，这次改动就还没闭环。

## 最小命令

### 单文件 shadow compare

```bash
./build/bin/styio \
  --parser-engine nightly \
  --parser-shadow-compare \
  --parser-shadow-artifact-dir /tmp/styio-shadow \
  --file tests/milestones/m7/t04_instant_pull.styio
```

### legacy 主路径对照

```bash
./build/bin/styio \
  --parser-engine legacy \
  --parser-shadow-compare \
  --parser-shadow-artifact-dir /tmp/styio-shadow \
  --file tests/milestones/m1/t01_int_arith.styio
```

### CTest shadow gate

```bash
ctest --test-dir build -L shadow_gate --output-on-failure
```

### legacy entry 审计

```bash
ctest --test-dir build -R '^parser_legacy_entry_audit$' --output-on-failure
```

### checkpoint-health 的 parser 迁移检查

```bash
./scripts/checkpoint-health.sh --no-asan --no-fuzz
```

## Gate 脚本真正检查什么

`scripts/parser-shadow-suite-gate.sh` 当前会：

- 对 suite 下每个 `t*.styio` 用 `legacy` 和 `nightly` 都跑一遍
- 强制打开 shadow compare
- 收集 artifact
- 统计 `match` / `mismatch` / `shadow_error`
- 可选要求 zero fallback
- 可选要求 zero internal bridges

如果 suite 里有 `shadow-expected-nonzero.txt`，脚本还会把那些用例视为允许失败的 manifest，而不是普通回归失败。

## Legacy Entry Audit 检查什么

`scripts/parser-legacy-entry-audit.sh` 当前在守三件事：

1. `parse_main_block_legacy(...)` 不能在 parser 核心之外被直接调用
2. `src/StyioTesting` 必须保持 nightly-first，不能偷偷重新依赖 legacy 路由
3. `src/main.cpp` 仍然必须通过 `parse_main_block_with_engine_latest(...)` 收口

这是一条架构约束，不只是 grep 小脚本。

## 现成回归入口

直接相关的现有检查包括：

- `parser_shadow_gate_m1_zero_fallback_and_internal_bridges`
- `parser_shadow_gate_m2_zero_fallback_and_internal_bridges`
- `parser_shadow_gate_m5_dual_zero_expected_nonzero`
- `parser_shadow_gate_m7_zero_fallback`
- `parser_shadow_gate_m7_zero_internal_bridges`
- `parser_legacy_entry_audit`
- `StyioParserEngine.DefaultEngineIsNightlyInShadowArtifact`
- `StyioParserEngine.ShadowCompareWritesArtifactRecordWhenDirConfigured`

直接跑：

```bash
ctest --test-dir build -R '^(parser_shadow_gate_.*|parser_legacy_entry_audit|StyioParserEngine\\.(DefaultEngineIsNightlyInShadowArtifact|ShadowCompareWritesArtifactRecordWhenDirConfigured))$' --output-on-failure
```

## 常见漏项

- 新 subset 已经实现，但 route stats 仍显示 fallback
- `nightly` 内部偷偷桥回 `legacy`，没有被当回事
- 调了 `--parser-shadow-artifact-dir` 却忘了同时开 `--parser-shadow-compare`
- 在测试或工具代码里直接重新引入 `parse_main_block_legacy(...)`
- 只看命令是否成功，不看 artifact 里的 route detail

## 维护规则

双轨迁移不是“nightly 能跑就行”，而是要持续压缩：

- fallback
- internal legacy bridge
- direct legacy entry points

只要这些数字不收敛，迁移就还没有真正完成。
