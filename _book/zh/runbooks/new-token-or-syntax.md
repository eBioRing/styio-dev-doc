# 新 Token 或语法改动手册

这页解决一个很现实的问题：如果你要给 Styio 加一个新 token、修改一个已有符号，或者扩展 parser 语法，最小闭环到底是什么。

## 适用范围

这页适用于：

- 新增 `StyioTokenType`
- 修改符号到 token 的映射
- 新增 parser 识别规则
- 扩展 `legacy` / `nightly` / `latest` 的语法路径

不适用于：

- 纯语义规则变更
- 纯 IR / codegen 变更
- 纯 runtime helper 变更

## 先确认你的改动属于哪一类

| 改动 | 第一落点 |
| --- | --- |
| 新字符或符号组合 | `src/StyioParser/Tokenizer.cpp` |
| 新 token 类型 | `src/StyioToken/Token.hpp` |
| token 名称显示 | `src/StyioToken/Token.cpp` |
| 新表达式 / 新语句结构 | `src/StyioParser/Parser.cpp` 或 `src/StyioParser/NewParserExpr.cpp` |
| 新 lookahead 规则 | `src/StyioParser/ParserLookahead.*` |

## 修改顺序

### 1. 先改 token 面

至少检查：

- `src/StyioToken/Token.hpp`
- `src/StyioToken/Token.cpp`
- `src/StyioParser/Tokenizer.cpp`

如果是操作符或符号，还要看：

- `TokenPrecedenceMap`
- `TokenStrMap`
- `StrTokenMap`

### 2. 再改 parser 路由

至少检查：

- `src/StyioParser/Parser.hpp`
- `src/StyioParser/Parser.cpp`
- `src/StyioParser/NewParserExpr.cpp`

如果你的判断依赖跳过 trivia 或非 trivia lookahead，不要自己复制逻辑，优先复用：

- `styio_is_trivia_token`
- `styio_skip_trivia_tokens`
- `styio_try_check_non_trivia`

它们都在 `src/StyioParser/ParserLookahead.*`。

### 3. 如果会产生新 AST，立刻补 AST 链路

别等 parser 写完才想起 AST。至少同步：

- `src/StyioAST/ASTDecl.hpp`
- `src/StyioAST/AST.hpp`
- `src/StyioToString/ToStringVisitor.hpp`
- `src/StyioToString/ToString.cpp`

之后继续走 [新 AST / IR 节点改动手册](new-ast-or-ir.md)。

### 4. 同步权威设计文档

语法和符号变动最少要同步：

- `docs/design/Styio-EBNF.md`
- `docs/design/Styio-Symbol-Reference.md`

如果语义也变了，再补：

- `docs/design/Styio-Language-Design.md`

## 双轨 parser 的硬规则

如果改动落在 parser 层，默认都要检查：

- `legacy`
- `nightly`
- `latest`
- route stats
- shadow compare

不要只让 `nightly` 跑通，然后把差异留给 `latest` 或 shadow gate 在 CI 里爆。

## 最低验证命令

### 看 AST 是否真的按预期生成

```bash
./build/bin/styio --styio-ast --file tests/milestones/m1/t01_int_arith.styio
```

### 看 parser 双轨是否一致

```bash
./build/bin/styio \
  --parser-shadow-compare \
  --parser-shadow-artifact-dir /tmp/styio-shadow \
  --file tests/milestones/m7/t04_instant_pull.styio
```

### 跑 parser 相关回归

```bash
ctest --test-dir build -L shadow_gate --output-on-failure
```

### 跑里程碑最小闭环

```bash
ctest --test-dir build -L milestone --output-on-failure
```

## 常见漏项

- 新 token 只加在 `Tokenizer.cpp`，没进 `Token.hpp`
- token 能打印名字，但 precedence / 反向映射没补
- `nightly` 路径改了，`latest` 没接上
- parser 能出 AST，但 `ToStringVisitor` 没补
- 只改代码，不改 `EBNF` 和 `Symbol-Reference`

## 维护建议

如果你发现一次语法改动同时要碰 parser、analyzer、IR、codegen 四层，先停一下，确认你不是把“语法问题”和“语义问题”混在一起做了。
