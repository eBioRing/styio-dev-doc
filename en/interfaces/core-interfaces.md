# 核心接口总览

这一页是接口区入口，不再把所有细节堆在一页里。

## 你应该先看哪张手册

| 你在改什么 | 先看哪里 |
| --- | --- |
| token、lookahead、`legacy/nightly` parser 路由 | [Parser 手册](parser-manual.md) |
| 类型推断、语义约束、AST 到 IR lowering | [Analyzer 手册](analyzer-manual.md) |
| LLVM type / IR 生成、JIT 执行路径 | [CodeGen 手册](codegen-manual.md) |
| FFI、标准流、文件句柄、运行时错误 | [Runtime 手册](runtime-manual.md) |

## 四层接口关系

```text
Tokenizer / Parser
  -> AST
  -> Analyzer (typeInfer + toStyioIR)
  -> StyioIR
  -> CodeGen (toLLVMType + toLLVMIR)
  -> Runtime / JIT
```

## 当前跨层主入口

| 接口 | 位置 | 作用 |
| --- | --- | --- |
| `StyioTokenizer::tokenize` | `src/StyioParser/Tokenizer.hpp` | 源码转 token |
| `parse_main_block_with_engine_latest` | `src/StyioParser/Parser.hpp` | token 转 AST |
| `StyioAnalyzer::typeInfer` | `src/StyioAnalyzer/ASTAnalyzer.hpp` | AST 语义标注 |
| `StyioAnalyzer::toStyioIR` | `src/StyioAnalyzer/ASTAnalyzer.hpp` | AST 转 Styio IR |
| `StyioIR::{toString,toLLVMType,toLLVMIR}` | `src/StyioIR/StyioIR.hpp` | IR 通用虚接口 |
| `StyioToLLVM` | `src/StyioCodeGen/CodeGenVisitor.hpp` | LLVM codegen + execute |
| `StyioJIT_ORC::Create` | `src/StyioJIT/StyioJIT_ORC.hpp` | 创建 ORC JIT |
| `CompilationSession` | `src/StyioSession/CompilationSession.hpp` | 生命周期收口 |

## 继续阅读

- [Parser 手册](parser-manual.md)
- [Analyzer 手册](analyzer-manual.md)
- [CodeGen 手册](codegen-manual.md)
- [Runtime 手册](runtime-manual.md)
- [功能改动矩阵](change-matrix.md)
- [新 Token 或语法改动手册](../runbooks/new-token-or-syntax.md)
- [新 AST 或 IR 节点改动手册](../runbooks/new-ast-or-ir.md)
- [标准流与资源能力改动手册](../runbooks/resources-and-stdio.md)
