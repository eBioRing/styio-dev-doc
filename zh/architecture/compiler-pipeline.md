# 编译器流水线

如果你第一次读 `styio` 源码，最好的入口不是从某个 `.cpp` 文件开始，而是先把流水线记清楚。

## 当前主链路

```text
Source (.styio)
  -> Tokenizer
  -> Parser
  -> Type Inference / Semantic Analysis
  -> Styio IR Lowering
  -> LLVM IR CodeGen
  -> ORC JIT Execution
```

## 各阶段对应模块

| 阶段 | 主要目录 | 说明 |
| --- | --- | --- |
| 词法分析 | `src/StyioParser/Tokenizer.*` | 负责 token 化 |
| 语法分析 | `src/StyioParser/Parser.*`、`ParserLookahead.*`、`NewParserExpr.*` | 手写递归下降 parser，默认走 `nightly` |
| AST | `src/StyioAST/` | 语法树节点定义 |
| 语义分析 | `src/StyioAnalyzer/` | 类型推断、语义检查、AST 到 Styio IR |
| 中间表示 | `src/StyioIR/` | 编译器自己的 IR 层 |
| LLVM 代码生成 | `src/StyioCodeGen/` | Styio IR 到 LLVM IR |
| 运行时桥接 | `src/StyioExtern/`、`src/StyioJIT/` | FFI 符号注册和 ORC JIT |
| CLI 入口 | `src/main.cpp` | 参数解析、驱动整条流水线 |

## 开发时如何观测每一层

| 你想看什么 | 命令 |
| --- | --- |
| AST | `./build/bin/styio --styio-ast --file ...` |
| Styio IR | `./build/bin/styio --styio-ir --file ...` |
| LLVM IR | `./build/bin/styio --llvm-ir --file ...` |
| parser 双引擎一致性 | `--parser-shadow-compare` |

## parser 的现实情况

当前仓库显式保留了两套 parser 路径：

- `legacy`
- `nightly`

但默认值已经是 `nightly`。同时，测试里存在多条 shadow compare 和 zero fallback gate，说明项目当前正处在“新 parser 接管，但还在严密对照旧行为”的阶段。

## 阅读源码的推荐顺序

1. `src/main.cpp`
2. `src/StyioParser/`
3. `src/StyioAST/`
4. `src/StyioAnalyzer/`
5. `src/StyioIR/`
6. `src/StyioCodeGen/`
7. `src/StyioExtern/` 和 `src/StyioJIT/`

这样读能把“输入是怎么一路落到可执行结果”的路径串起来。
