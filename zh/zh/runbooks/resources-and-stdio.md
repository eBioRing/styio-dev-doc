# 标准流与资源能力改动手册

这页处理 Styio 另一类高风险改动：`@stdin`、`@stdout`、`@stderr`、文件资源和句柄相关能力。

这类改动经常跨 parser、analyzer、codegen、runtime 四层，而且最容易因为 ABI 或所有权约定不一致而出错。

## 先分清你改的是哪一层

| 你在改什么 | 第一落点 |
| --- | --- |
| 新资源语法 | parser |
| 新资源语义检查 | analyzer |
| 新资源 IR 节点 | `IRDecl.hpp` + lowering |
| 新标准流 / 文件行为 | `CodeGenIO.cpp` |
| 新外部 helper / 句柄语义 | `ExternLib.*` + `StyioJIT_ORC.hpp` |

## 修改顺序

### 1. 先确认是否已有现成 AST / IR

和资源、标准流相关的现有 AST / IR 包括：

- `FileResourceAST`
- `StdStreamAST`
- `HandleAcquireAST`
- `ResourceWriteAST`
- `ResourceRedirectAST`
- `InstantPullAST`
- `SIOStdStreamWrite`
- `SIOStdStreamLineIter`
- `SIOStdStreamPull`
- `SGResourceWriteToFile`

如果只是语义扩展，优先复用这些节点，而不是立刻新建一套平行节点。

### 2. 改 analyzer 的语义与 lowering

至少同步：

- `src/StyioAnalyzer/ASTAnalyzer.hpp`
- `src/StyioAnalyzer/TypeInfer.cpp`
- `src/StyioAnalyzer/ToStyioIR.cpp`

这一步要回答三个问题：

- 这个资源表达式是否合法
- 它产出的值类型是什么
- 它应该落成哪种 Styio IR

### 3. 改 codegen I/O 路径

至少同步：

- `src/StyioCodeGen/GetTypeIO.cpp`
- `src/StyioCodeGen/CodeGenIO.cpp`

如果牵涉 pulse / series 或通用节点，也可能还要碰：

- `CodeGenPulse.cpp`
- `CodeGenG.cpp`

### 4. 改 runtime helper 和 JIT 绑定

新增 helper 时至少同步：

- `src/StyioExtern/ExternLib.hpp`
- `src/StyioExtern/ExternLib.cpp`
- `src/StyioJIT/StyioJIT_ORC.hpp`

如果改的是 handle 行为，还要检查：

- `src/StyioRuntime/HandleTable.hpp`

少注册一处，JIT 就会在运行时找不到符号。

## 所有权规则必须对齐

当前 runtime 已经有几条不能碰混的约定：

- `styio_file_read_line` 返回借用指针，不能释放
- `styio_stdin_read_line` 返回借用指针，EOF 返回 `nullptr`
- `styio_strcat_ab` 返回堆分配字符串，需要 `styio_free_cstr`
- `styio_i64_dec_cstr` / `styio_f64_dec_cstr` 返回借用缓冲

只要 codegen 侧对这些约定理解错一次，就会直接变成泄漏、悬挂引用或重复释放。

## 最低验证命令

### stdout / stderr

```bash
ctest --test-dir build -R '^m9_' --output-on-failure
```

### stdin

```bash
ctest --test-dir build -R '^m10_' --output-on-failure
```

### 文件资源和副作用

```bash
ctest --test-dir build -R '^m5_' --output-on-failure
```

### pipeline 资源闭环

```bash
ctest --test-dir build -L styio_pipeline --output-on-failure
```

### 单独看 lowering

```bash
./build/bin/styio --styio-ir --file tests/milestones/m10/t02_stdin_pull.styio
```

## 常见漏项

- analyzer 已经产出新 IR，但 `CodeGenIO.cpp` 没接
- runtime helper 已写好，但 `StyioJIT_ORC.hpp` 没注册
- 改了 helper 返回值所有权，却没同步 codegen 释放策略
- 只改 stdout，用例没覆盖 stderr / stdin / 文件路径
- 资源设计文档改了，但当前实现和测试没跟上

## 文档同步规则

资源或标准流能力变化，最少同步：

- `docs/design/Styio-Symbol-Reference.md`
- `docs/design/Styio-Resource-Driver.md`
- 必要时 `docs/design/Styio-Language-Design.md`
- [资源、`@` 与标准流](../language/resources-and-stdio.md)

如果只是更新了今天的实现边界，不要把未来插件化目标误写成“当前已经支持”。
