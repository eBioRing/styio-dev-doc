# 分层架构与职责

Styio 维护难点不在“代码量大”，而在它是一条多阶段编译链。每个阶段都要知道自己该吃什么、吐什么。

## 总体分层

| 层 | 输入 | 输出 | 主要文件 |
| --- | --- | --- | --- |
| CLI / Session | 文件路径、CLI 参数 | 编译流程驱动 | `src/main.cpp`、`src/StyioSession/CompilationSession.hpp` |
| Tokenizer | 源码字符串 | `vector<StyioToken*>` | `src/StyioParser/Tokenizer.*` |
| Parser | token + `StyioContext` | `MainBlockAST*` | `src/StyioParser/Parser.*`、`NewParserExpr.*` |
| AST | 语法树节点 | 供 analyzer 使用 | `src/StyioAST/` |
| Analyzer / Sema | AST | 标注类型后的 AST + `StyioIR*` | `src/StyioAnalyzer/` |
| Styio IR | 统一中间层 | 可打印 / 可 codegen | `src/StyioIR/` |
| LLVM CodeGen | Styio IR | `llvm::Module` / 可执行入口 | `src/StyioCodeGen/` |
| Runtime / JIT | LLVM 模块 + FFI | 实际执行 | `src/StyioExtern/`、`src/StyioJIT/` |

## 各层职责边界

### CLI / Session

负责：

- 读取文件
- 解析 CLI 参数
- 按顺序驱动 tokenization、parse、typeInfer、IR lowering、codegen、JIT
- 统一管理 token / context / AST / IR 生命周期

### Tokenizer

负责：

- maximal munch 分词
- 把符号映射为 token

不负责：

- 语义判断
- AST 结构判断

### Parser

负责：

- 从 token 组装 AST
- `legacy` / `nightly` 双路径选择
- route stats 和 fallback 统计

不负责：

- LLVM 细节
- 最终类型规则

### Analyzer

负责：

- 类型推断
- 语义约束
- AST 到 Styio IR 的 lowering

这是连接“语法世界”和“执行世界”的真正边界层。

### Styio IR

作用是把 AST 的语法形态抽象成更适合 codegen 的结构。维护时不要轻易跳过这层。

### CodeGen

负责：

- LLVM type 映射
- LLVM IR 生成
- 优化 pass 注册
- 最终调用 ORC JIT

### Runtime / FFI

负责：

- 文件 I/O
- 字符串与数值桥接
- stderr / stdin 标准流支持
- JIT 需要绑定的外部符号

## 一个维护上的经验法则

如果你发现自己在某层需要知道太多别层细节，通常说明改动位置选错了。
