# 功能改动矩阵

这页回答一个维护者最常见的问题：改某类能力时，到底要同步哪些层。

这里的矩阵默认只覆盖 `styio` 本体，也就是语言、编译器、CLI 与主测试仓。`Spio` 和 `Vityo` 的改动闭环要回到各自的开发指引。

## 新 token

至少同步：

- `src/StyioToken/Token.hpp`
- `src/StyioParser/Tokenizer.cpp`
- `src/StyioToken/Token.cpp` 或 token 名映射
- `docs/design/Styio-EBNF.md`
- `docs/design/Styio-Symbol-Reference.md`
- 对应 lexer / parser 测试

## 新 AST 节点

至少同步：

- `src/StyioToken/Token.hpp`
- `src/StyioAST/ASTDecl.hpp`
- `src/StyioAST/AST.hpp`
- `src/StyioToString/ToStringVisitor.hpp`
- `src/StyioAnalyzer/ASTAnalyzer.hpp`
- `src/StyioAnalyzer/TypeInfer.cpp`
- `src/StyioAnalyzer/ToStyioIR.cpp`
- 对应 AST / type infer / IR 测试

## parser 扩展

至少同步：

- `src/StyioParser/Parser.hpp`
- `src/StyioParser/Parser.cpp`
- `src/StyioParser/NewParserExpr.cpp`
- 必要时 `ParserLookahead.*`
- parser shadow 相关测试
- `EBNF` 和 `Symbol-Reference`

如果是双轨逻辑，别忘了维护：

- `legacy`
- `nightly`
- `latest`
- route stats / shadow compare 行为

## 新 intrinsic

至少同步：

- parser 的 selector 识别
- `TypeInfer.cpp`
- `ToStyioIR.cpp`
- `src/StyioIR/`
- `src/StyioCodeGen/CodeGenPulse.cpp` 或相关 codegen 文件
- `docs/design/Styio-StdLib-Intrinsics.md`
- milestone / pipeline / C++ 测试

## 新资源或标准流能力

至少同步：

- parser 的资源原子解析
- analyzer 的方向与语义校验
- IR 节点
- codegen I/O 路径
- `ExternLib.*`
- `StyioJIT_ORC.hpp`
- `Symbol-Reference`
- 对应 milestone 样例和执行测试

## 新 `.cpp` 文件

不要忘：

- 顶层 `CMakeLists.txt`

这是 Styio 当前最容易漏的一类维护动作。

## 任何语言级改动的最小闭环

最低限度应形成：

1. 设计或规格同步
2. 源码同步
3. 自动化测试同步
4. GitBook 对应 Markdown 页面同步

这里的“同步”指更新维护手册内容，不是扩写或重构 GitBook 框架。

## 对应任务手册

- token / parser 变更： [新 Token 或语法改动手册](../runbooks/new-token-or-syntax.md)
- AST / IR 节点变更： [新 AST 或 IR 节点改动手册](../runbooks/new-ast-or-ir.md)
- 标准流 / 资源变更： [标准流与资源能力改动手册](../runbooks/resources-and-stdio.md)
- intrinsic 变更： [新增 Intrinsic 改动手册](../runbooks/new-intrinsic.md)
- state / pulse / snapshot 变更： [State / Pulse / Snapshot 改动手册](../runbooks/state-and-pulse.md)
- 诊断 / 错误模型变更： [诊断与错误模型手册](../runbooks/diagnostics-and-error-model.md)
- parser 双轨迁移变更： [Parser Shadow 与双轨迁移手册](../runbooks/parser-shadow-and-dual-track.md)
- 测试结构 / case 选型变更： [测试金字塔与 Case 选型手册](../runbooks/testing-pyramid-and-case-selection.md)
- CLI / machine interface 变更： [CLI 与 Machine Interface 改动手册](../runbooks/cli-and-machine-interface.md)

如果缺任一环，这个改动都还不算真正“维护完成”。
