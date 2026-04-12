# CLI 与调试工作流

这页只写 `styio` 本体 CLI 与调试工作流。

维护 Styio 时，CLI 不是给终端用户看的附属品，而是最直接的编译器观测窗口。`styio-spio` 和 `styio-view` 的命令面与调试流程应各看自己的开发指引。

## 最小运行

```bash
./build/bin/styio --file tests/milestones/m1/t01_int_arith.styio
```

2026-04-12 本地核对时，这个命令输出：

```text
10
```

## 常用 CLI 参数

| 参数 | 用途 |
| --- | --- |
| `--file <path>` | 编译并执行 `.styio` 文件 |
| `--styio-ast` | 打印类型推断前后 AST |
| `--styio-ir` | 打印 Styio IR |
| `--llvm-ir` | 打印 LLVM IR |
| `--debug` | 输出更多调试信息 |
| `--error-format text|jsonl` | 诊断格式 |
| `--machine-info json` | 输出机器可读能力信息 |
| `--parser-engine legacy|nightly` | 指定 parser |
| `--parser-shadow-compare` | 双 parser 对照 |
| `--parser-shadow-artifact-dir <dir>` | 写 shadow artifact |
| `--nano-create` / `--nano-publish` | `styio-nano` package materialize / publish |

## 推荐调试路径

### 查 lexer / parser

```bash
./build/bin/styio --styio-ast --file tests/milestones/m9/t01_stdout_string.styio
```

### 查 IR lowering

```bash
./build/bin/styio --styio-ir --file tests/milestones/m10/t01_stdin_echo.styio
```

### 查 LLVM 生成

```bash
./build/bin/styio --llvm-ir --file tests/milestones/m2/t01_simple_func.styio
```

### 查 parser 双轨差异

```bash
./build/bin/styio \
  --parser-shadow-compare \
  --parser-shadow-artifact-dir /tmp/styio-shadow \
  --file tests/milestones/m7/t04_instant_pull.styio
```

## 诊断格式

当前 CLI 支持：

- `text`
- `jsonl`

机器接口场景优先用：

```bash
./build/bin/styio --error-format jsonl --file some.styio
```

## `styio-nano` 相关现实

当前远端 `main` 已经把 `styio-nano` packaging 命令并进了 full compiler CLI。

要记住这几个边界：

- `--nano-create` / `--nano-publish` 只在 full `styio` 可用
- `styio-nano` 自身可以按 profile 禁掉 `--machine-info`
- `styio-nano` 自身可以按 profile 禁掉 `--debug`
- `styio-nano` 自身可以按 profile 禁掉 `--styio-ast` / `--styio-ir` / `--llvm-ir`
- `styio-nano` 自身可以按 profile 禁掉 `--parser-engine` / shadow compare

所以维护 CLI 时，不要默认“full compiler 上有的 flag，`styio-nano` 也一定有”。

## 维护者需要记住的现实

- 默认 parser 已经是 `nightly`
- shadow compare 不是实验玩具，而是当前 parser 迁移的重要保护网
- CLI 入口本身就是测试和文档的一部分，参数变化必须同步文档

## 继续阅读

- [CLI 与 Machine Interface 改动手册](../runbooks/cli-and-machine-interface.md)
- [诊断与错误模型手册](../runbooks/diagnostics-and-error-model.md)
- [Parser Shadow 与双轨迁移手册](../runbooks/parser-shadow-and-dual-track.md)
