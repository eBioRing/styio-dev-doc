# 测试金字塔与 Case 选型手册

这页回答维护者最常见的问题：一个改动，测试到底该加在哪一层。

Styio 当前不是“加一个用例就行”的项目。测试已经分成多层，每层的职责不同。

## 当前测试层次

按维护用途看，当前测试面大致是：

| 层 | 位置 | 主要用途 |
| --- | --- | --- |
| milestone fixtures | `tests/milestones/` | 冻结语言能力和 CLI 可执行结果 |
| five-layer pipeline | `tests/pipeline_cases/` + `tests/styio_test.cpp` | 冻结 AST / Styio IR / LLVM IR / 输出的全链路 |
| unit / diagnostics | `tests/styio_test.cpp` | 精准回归某个 parser / analyzer / CLI / 诊断行为 |
| security | `tests/security/styio_security_test.cpp` | 崩溃、越界、句柄误用、安全语义 |
| soak | `tests/soak/styio_soak_test.cpp` | 长跑、RSS 增长、重复执行稳定性 |
| fuzz | `tests/fuzz/` | 非预期输入和 parser/lexer 鲁棒性 |
| docs audit | `scripts/docs-audit.py` + `ctest -L docs` | 文档和仓库引用完整性 |

## 选型规则

### 1. 先问自己要冻结什么

| 你要冻结什么 | 应该先加哪层 |
| --- | --- |
| 语言功能的用户可见输出 | milestone |
| 五层流水线中间产物 | pipeline |
| 具体错误码 / 诊断文本 / shadow artifact | `styio_test.cpp` |
| 资源、句柄、内存安全 | security |
| 长时间重复执行后的稳定性 | soak |
| 非结构化异常输入 | fuzz |

### 2. milestone 适合什么

适合：

- 新语法最终是否能跑通
- stdout / stderr / 副作用文件是否符合预期
- 某个 milestone 能力边界是否被冻结

不适合：

- 只验证一条内部诊断字符串
- 只验证 machine-info 握手字段
- 只验证 shadow artifact JSONL 细节

## pipeline case 适合什么

适合：

- 改动同时影响 AST / Styio IR / LLVM IR / 最终输出
- 你想把中间层快照一并冻住
- 你需要验证 lowering 不是“碰巧跑出来对”

典型例子就是当前的：

- `p05_snapshot_accum`
- `p07_instant_pull`
- `p14_stdin_pull`

## `styio_test.cpp` 适合什么

适合：

- `--machine-info=json` 的稳定字段
- `--parser-engine` 非法值
- `--parser-shadow-artifact-dir` 缺少 compare flag
- JSONL 诊断里的 `category` / `code` / `subcode`
- shadow artifact detail / route stats

如果你关心的是 CLI 契约、诊断文本或 artifact 元数据，优先写这里，而不是 milestone。

## security 适合什么

适合：

- lexer 极端输入
- 句柄误用
- runtime helper 错误边界
- AST / session 生命周期安全

当前模块说明不在本目录重复维护，而是收口在：

- `docs/review/2026-03-30/security-tests.md`

## soak 适合什么

适合：

- 内存增长边界
- 高频重复打开 / 关闭 / 拼接 / 读写
- 已修复 bug 的长跑回归
- state inline / stream program 这类“单次能过、长跑才坏”的问题

默认 PR 跑的是：

- `soak_smoke`

更重的夜间档位是：

- `soak_deep`

## fuzz 适合什么

适合：

- tokenizer / parser 的非结构化输入
- crash、hang、未定义行为
- seed 回流和失败样本打包

当前 parser fuzz 已经会顺序驱动：

- `legacy`
- `nightly`

不再只 fuzz legacy。

## Oracle 该怎么选

当前最常见的 oracle 有四种：

| Oracle | 适合场景 |
| --- | --- |
| stdout golden | 常规语言功能输出 |
| stderr golden | 标准错误输出 |
| 文件副作用比对 | 文件资源和重定向 |
| 中间产物快照 | AST / Styio IR / LLVM IR |

不要为了省事，把本该用中间产物快照的问题硬压成 stdout golden。

## 最小命令

### milestone

```bash
ctest --test-dir build -L milestone --output-on-failure
```

### five-layer pipeline

```bash
ctest --test-dir build -L styio_pipeline --output-on-failure
```

### security

```bash
ctest --test-dir build -L security --output-on-failure
```

### soak smoke

```bash
ctest --test-dir build -L soak_smoke --output-on-failure
```

### fuzz smoke

```bash
ctest --test-dir build-fuzz -L fuzz_smoke --output-on-failure
```

### docs audit

```bash
ctest --test-dir build -L docs --output-on-failure
```

## 常见选型错误

- 想验证 JSONL 字段，却只写 milestone
- 改了 lowering，却没有 pipeline 快照
- 资源/句柄问题只跑功能例子，不跑 security
- 长跑才会暴露的问题只写一次性单测
- 只补一个大而慢的测试，不补最小可定位回归

## 维护规则

每次改动至少要让测试回答两件事：

1. 用户可见行为有没有被正确冻结
2. 最容易复发的那一层，有没有被单独钉住

只回答第一件事，回归定位会很慢；只回答第二件事，语言行为会漂。
