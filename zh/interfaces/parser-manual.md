# Parser 手册

这页只写 parser 维护者会直接碰到的接口、边界和改动点。

## 角色边界

Parser 层负责：

- 把 `StyioTokenizer` 产出的 token 流转成 AST
- 维护 `legacy` / `nightly` / `latest` 的路由
- 做必要的 lookahead、fallback 和 shadow compare 统计

Parser 层不负责：

- LLVM 类型
- 最终语义正确性
- 运行时资源实现

## 入口对象

### Tokenizer

文件：`src/StyioParser/Tokenizer.hpp`

```cpp
class StyioTokenizer
{
public:
  static std::vector<StyioToken *> tokenize(std::string code);
};
```

这是 parser 之前唯一标准入口。任何新 token 的第一落点都在 tokenizer。

### `StyioContext`

文件：`src/StyioParser/Parser.hpp`

`StyioContext` 是 parser 的工作台。它同时持有：

- 源代码文本
- 行分隔信息
- token 向量
- token cursor
- route stats 指针

高频方法：

| 方法 | 用途 |
| --- | --- |
| `cur_tok()` | 读当前 token |
| `cur_tok_type()` | 读当前 token 类型 |
| `move_forward(...)` | 前进 |
| `save_cursor()` / `restore_cursor()` | 回溯 |
| `skip()` | 跳 trivia |
| `skip_spaces_no_linebreak()` | 只跳空格，不跨行 |
| `try_check(...)` | 非 trivia lookahead |
| `match(...)` / `match_panic(...)` | 消费 token |
| `try_match(...)` / `try_match_panic(...)` | 跳过 trivia 后匹配 |

## lookahead 辅助接口

文件：`src/StyioParser/ParserLookahead.hpp`

```cpp
bool styio_is_trivia_token(StyioTokenType type);
size_t styio_skip_trivia_tokens(const std::vector<StyioToken*>& tokens, size_t index);
bool styio_try_check_non_trivia(const std::vector<StyioToken*>& tokens, size_t index, StyioTokenType target);
```

如果你要加新的 parser 判定，优先复用这些函数，而不是自己再写一套 trivia 跳过逻辑。

## parser 主入口

文件：`src/StyioParser/Parser.hpp`

```cpp
bool styio_parse_parser_engine_latest(const std::string& raw, StyioParserEngine& out);
const char* styio_parser_engine_name_latest(StyioParserEngine engine);

MainBlockAST* parse_main_block_with_engine_latest(
  StyioContext& context,
  StyioParserEngine engine,
  StyioParserRouteStats* route_stats = nullptr);
```

相关枚举：

```cpp
enum class StyioParserEngine
{
  Legacy,
  Nightly,
  New = Nightly,
};
```

相关统计：

```cpp
struct StyioParserRouteStats
{
  size_t nightly_subset_statements = 0;
  size_t legacy_fallback_statements = 0;
  size_t nightly_internal_legacy_bridges = 0;
};
```

## 运行路径

`main.cpp` 当前的 parser 相关调用顺序是：

1. `StyioTokenizer::tokenize(...)`
2. `StyioContext::Create(...)`
3. `parse_main_block_with_engine_latest(...)`
4. 如果打开 `--parser-shadow-compare`，再跑一遍 shadow parser

这意味着 parser 改动会直接影响：

- CLI 正常执行
- shadow compare
- artifact 输出
- parse error 的诊断路径

## 代码组织

常见文件分工：

| 文件 | 用途 |
| --- | --- |
| `Tokenizer.cpp` | 分词 |
| `Parser.cpp` | parser 主体和共享路径 |
| `NewParserExpr.cpp` | `nightly` 表达式与子路径 |
| `ParserLookahead.*` | lookahead/trivia helper |
| `BinExprMapper.hpp` | 二元表达式映射 |

## 改 parser 时的最低同步范围

### 新 token

- `Token.hpp`
- `Tokenizer.cpp`
- `Token.cpp` / token 名映射
- `EBNF`
- `Symbol-Reference`

### 新语法

- `ASTDecl.hpp`
- `AST.hpp`
- `Parser.hpp`
- `Parser.cpp`
- `NewParserExpr.cpp`
- 相关 `ToStringVisitor`
- 对应 parser 测试

### 双轨逻辑

不要只改 `nightly` 路径然后忘记：

- `legacy`
- `latest`
- shadow compare
- route stats

## parser 层的维护原则

- 能用 lookahead helper，就不要本地复制 trivia 逻辑
- 能放在 `_nightly` / `_latest` 命名体系里，就不要再造无状态函数名
- 如果行为变了，先看 parser shadow gate 会不会被打爆
