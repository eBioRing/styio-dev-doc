# 测试与回归策略

Styio 的维护不能靠肉眼看 diff。每次改动至少要能落到某一类自动化检查上。

## 改动必须覆盖哪些测试

按 `AGENT-SPEC.md` 的要求，任何功能改动至少要考虑：

| 改动类型 | 最低验证 |
| --- | --- |
| 新 token | lexer 样例，必要时 `--debug` |
| 新语法 | parser 样例，`--styio-ast` |
| 类型系统改动 | type infer 验证，`--styio-ast` |
| IR / codegen 改动 | `--styio-ir` / `--llvm-ir` / 执行结果 |
| 运行时行为改动 | JIT 实跑结果、相关 C++ 测试 |

## 当前测试面

主仓库当前至少有这些层级：

- `tests/milestones/`
- `tests/pipeline_cases/`
- `tests/security/`
- `tests/soak/`
- `tests/fuzz/`
- `tests/lit_cases/`

以及 CTest 注册的：

- `docs_audit`
- milestone 测试
- parser shadow gates
- `styio_test`
- `styio_security_test`
- `styio_soak_test`

当前 `styio@main` 还把：

- `docs/assets/workflow/TEST-CATALOG.md`
- `scripts/docs-index.py`
- `scripts/docs-audit.py`

当成正式维护资产。也就是说，测试面不只包括源码和 golden，还包括 docs tree 自己的结构一致性。

## 维护时最常用的命令

全量：

```bash
ctest --test-dir build --output-on-failure
```

里程碑：

```bash
ctest --test-dir build -L milestone --output-on-failure
```

五层流水线 / shadow：

```bash
ctest --test-dir build -L styio_pipeline --output-on-failure
```

安全回归：

```bash
ctest --test-dir build -L security --output-on-failure
```

soak smoke：

```bash
ctest --test-dir build -L soak_smoke --output-on-failure
```

某个单例：

```bash
ctest --test-dir build -R '^m10_t01_stdin_echo$' --output-on-failure
```

文档审计：

```bash
ctest --test-dir build -L docs --output-on-failure
```

重建 docs 索引：

```bash
python3 scripts/docs-index.py --write
python3 scripts/docs-audit.py
```

## 回归规则

一条核心原则：

**已有测试不应被无说明地破坏。**

如果必须改已有测试，你至少要同步：

- 改动理由
- 对应设计/规格文档
- 相关 golden
- 测试目录或测试目录说明

## milestone 的正确角色

里程碑文档不是为了讲历史，而是为了冻结验收边界。

真正有维护价值的是：

- 哪个能力已经被冻结
- 对应样例在哪
- 它是 stdout 对比、stderr 对比，还是副作用文件比对
- 它对应哪个 `ctest` label 或 gate

## 五层流水线为什么重要

Styio 现在并不只有“跑出来对”这一种检查。五层流水线把这些层都显式冻住了：

- token
- AST
- Styio IR
- LLVM IR
- 最终输出

这对改 parser、IR lowering 和 codegen 的人尤其重要。

## 现在还要把文档测试当真

`styio@main` 当前已经把 docs tree 维护流程正式化：

- `docs/README.md` 规定目录边界
- `docs/INDEX.md` 由脚本生成
- `docs_audit` 进入 `ctest`
- `TEST-CATALOG.md` 作为测试地图

所以如果你改的是：

- docs tree 结构
- 测试目录
- 里程碑编排
- handoff / workflow 资产

那你的最小闭环不只是一条 `ctest -L milestone`，还应包括 docs index 和 docs audit。

## 继续阅读

- [测试金字塔与 Case 选型手册](../runbooks/testing-pyramid-and-case-selection.md)
- [诊断与错误模型手册](../runbooks/diagnostics-and-error-model.md)
