# 诊断与错误模型手册

这页写的是维护者排查失败时的第一反应，而不是终端用户说明书。

Styio 当前的 CLI 失败不是一团模糊 stderr，而是有明确类别、退出码和 JSONL 诊断格式的。

## 当前错误分类

`src/main.cpp` 当前把失败分成四类：

| 类别 | code | 退出码 |
| --- | --- | --- |
| `LexError` | `STYIO_LEX` | `2` |
| `ParseError` | `STYIO_PARSE` | `3` |
| `TypeError` | `STYIO_TYPE` | `4` |
| `RuntimeError` | `STYIO_RUNTIME` | `5` |

另外还有：

- `CliError`：CLI 参数错误，退出码 `6`

这意味着你先看退出码，就能大致知道故障落在哪一层。

## 诊断输出格式

当前支持两种：

- `text`
- `jsonl`

维护和自动化场景默认优先用：

```bash
./build/bin/styio --error-format jsonl --file some.styio
```

JSONL 记录当前至少会带：

- `category`
- `code`
- `file`
- `message`
- 运行时错误场景下可能有 `subcode`

## 排查顺序

### 1. 先判断是不是 CLI 自身错误

这类问题通常是：

- `unsupported --error-format`
- `unsupported --parser-engine`
- `--parser-shadow-artifact-dir requires --parser-shadow-compare`

先直接看命令行参数，不要误以为是 parser 或 analyzer 崩了。

### 2. 如果是 `LexError`

先查：

- `StyioTokenizer::tokenize`
- 对应 token / 字符串 / 注释处理

优先跑：

```bash
./build/bin/styio --debug --file some.styio
```

以及相关安全测试：

```bash
ctest --test-dir build -L security --output-on-failure
```

### 3. 如果是 `ParseError`

先查：

- `Parser.cpp`
- `NewParserExpr.cpp`
- `ParserLookahead.*`
- `--parser-engine`
- `--parser-shadow-compare`

优先跑：

```bash
./build/bin/styio --error-format jsonl --styio-ast --file some.styio
```

如果和双轨迁移相关，再补：

```bash
./build/bin/styio \
  --parser-engine nightly \
  --parser-shadow-compare \
  --parser-shadow-artifact-dir /tmp/styio-shadow \
  --file some.styio
```

### 4. 如果是 `TypeError`

先查：

- `TypeInfer.cpp`
- `ToStyioIR.cpp`

这类错误通常说明：

- AST 语法合法，但语义约束不成立
- lowering 所需前提不满足

优先跑：

```bash
./build/bin/styio --error-format jsonl --styio-ast --styio-ir --file some.styio
```

### 5. 如果是 `RuntimeError`

先查：

- `ExternLib.*`
- `CodeGenIO.cpp`
- `StyioJIT_ORC.hpp`

运行时错误的关键价值是 `subcode`。例如文件打开失败时，当前测试会断言：

- `STYIO_RUNTIME_FILE_OPEN_READ`
- `STYIO_RUNTIME_FILE_OPEN_WRITE`

优先跑：

```bash
./build/bin/styio --error-format jsonl --file some.styio
```

再结合 `message` 和 `subcode` 回到具体 helper。

## 常用排查命令

### 机器可读能力声明

```bash
./build/bin/styio --machine-info json
```

### AST / IR / LLVM IR 三层观测

```bash
./build/bin/styio --styio-ast --file some.styio
./build/bin/styio --styio-ir --file some.styio
./build/bin/styio --llvm-ir --file some.styio
```

### 默认 JSONL 诊断

```bash
./build/bin/styio --error-format jsonl --file some.styio
```

## 现成回归入口

和诊断模型直接相关的现有测试包括：

- `StyioParserEngine.UnsupportedEngineIsRejected`
- `StyioDiagnostics.RuntimeHelperErrorEmitsJsonlRuntimeDiagnostic`
- `StyioDiagnostics.RuntimeWriteHelperErrorEmitsJsonlRuntimeDiagnostic`
- `StyioDiagnostics.CompoundAssignOnImmutableBindingReportsTypeError`
- `StyioDiagnostics.StreamZipUnsupportedSourceReportsTypeError`
- `StyioDiagnostics.SeriesIntrinsicWindowNonLiteralReportsTypeError`
- `StyioDiagnostics.MalformedStatementPrefixReportsParseErrorWithoutCrash`

直接跑：

```bash
ctest --test-dir build -R 'Styio(ParserEngine\\.UnsupportedEngineIsRejected|Diagnostics\\.(RuntimeHelperErrorEmitsJsonlRuntimeDiagnostic|RuntimeWriteHelperErrorEmitsJsonlRuntimeDiagnostic|CompoundAssignOnImmutableBindingReportsTypeError|StreamZipUnsupportedSourceReportsTypeError|SeriesIntrinsicWindowNonLiteralReportsTypeError|MalformedStatementPrefixReportsParseErrorWithoutCrash))' --output-on-failure
```

## 常见误判

- 把 `CliError` 当成 parser 问题
- 只看 stderr 文本，不看退出码和 `category`
- runtime 失败时忽略 `subcode`
- analyzer 报错时只盯 parser，不看 `ToStyioIR.cpp`

## 维护规则

如果你新增了一个失败路径，至少要决定三件事：

1. 它属于哪一类错误
2. 它的退出码是否符合现有分类
3. 机器接口是否需要 `subcode`

不把这三件事定清楚，后面的自动化和维护排查都会变差。
