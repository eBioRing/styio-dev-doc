# Parser Manual

This page covers only the interfaces, boundaries, and change points that parser maintainers touch directly.

## Role Boundary

The Parser layer is responsible for:

- converting the token stream produced by `StyioTokenizer` into AST
- maintaining routing among `legacy`, `nightly`, and `latest`
- performing required lookahead, fallback, and shadow compare statistics

The Parser layer is not responsible for:

- LLVM types
- final semantic correctness
- runtime resource implementation

## Entry Objects

### Tokenizer

File: `src/StyioParser/Tokenizer.hpp`

```cpp
class StyioTokenizer
{
public:
  static std::vector<StyioToken *> tokenize(std::string code);
};
```

This is the only standard entry point before parser execution. Every new token starts in the tokenizer.

### `StyioContext`

File: `src/StyioParser/Parser.hpp`

`StyioContext` is the parser workbench. It holds:

- source text
- line split information
- token vector
- token cursor
- route stats pointer

Frequently used methods:

| Method | Purpose |
| --- | --- |
| `cur_tok()` | Read the current token |
| `cur_tok_type()` | Read the current token type |
| `move_forward(...)` | Advance |
| `save_cursor()` / `restore_cursor()` | Backtrack |
| `skip()` | Skip trivia |
| `skip_spaces_no_linebreak()` | Skip spaces without crossing line breaks |
| `try_check(...)` | Non-trivia lookahead |
| `match(...)` / `match_panic(...)` | Consume a token |
| `try_match(...)` / `try_match_panic(...)` | Match after skipping trivia |

## Lookahead Helpers

File: `src/StyioParser/ParserLookahead.hpp`

```cpp
bool styio_is_trivia_token(StyioTokenType type);
size_t styio_skip_trivia_tokens(const std::vector<StyioToken*>& tokens, size_t index);
bool styio_try_check_non_trivia(const std::vector<StyioToken*>& tokens, size_t index, StyioTokenType target);
```

When adding parser checks, prefer these helpers instead of writing another trivia-skipping implementation.

## Parser Main Entry

File: `src/StyioParser/Parser.hpp`

```cpp
bool styio_parse_parser_engine_latest(const std::string& raw, StyioParserEngine& out);
const char* styio_parser_engine_name_latest(StyioParserEngine engine);

MainBlockAST* parse_main_block_with_engine_latest(
  StyioContext& context,
  StyioParserEngine engine,
  StyioParserRouteStats* route_stats = nullptr);
```

Relevant enum:

```cpp
enum class StyioParserEngine
{
  Legacy,
  Nightly,
  New = Nightly,
};
```

Relevant stats:

```cpp
struct StyioParserRouteStats
{
  size_t nightly_subset_statements = 0;
  size_t legacy_fallback_statements = 0;
  size_t nightly_internal_legacy_bridges = 0;
};
```

## Runtime Path

`main.cpp` currently calls parser logic in this order:

1. `StyioTokenizer::tokenize(...)`
2. `StyioContext::Create(...)`
3. `parse_main_block_with_engine_latest(...)`
4. if `--parser-shadow-compare` is enabled, run the shadow parser path as well

Parser changes therefore directly affect:

- normal CLI execution
- shadow compare
- artifact output
- parse-error diagnostic paths

## Code Organization

Common file responsibilities:

| File | Purpose |
| --- | --- |
| `Tokenizer.cpp` | Tokenization |
| `Parser.cpp` | Parser core and shared paths |
| `NewParserExpr.cpp` | `nightly` expressions and subpaths |
| `ParserLookahead.*` | Lookahead / trivia helpers |
| `BinExprMapper.hpp` | Binary expression mapping |

## Minimum Synchronization Scope for Parser Changes

### New token

- `Token.hpp`
- `Tokenizer.cpp`
- `Token.cpp` / token name mapping
- `EBNF`
- `Symbol-Reference`

### New syntax

- `ASTDecl.hpp`
- `AST.hpp`
- `Parser.hpp`
- `Parser.cpp`
- `NewParserExpr.cpp`
- related `ToStringVisitor`
- corresponding parser tests

### Dual-track logic

Do not modify only the `nightly` path and forget:

- `legacy`
- `latest`
- shadow compare
- route stats

## Parser Maintenance Principles

- Use lookahead helpers instead of copying trivia logic locally.
- Prefer the `_nightly` / `_latest` naming system when it applies.
- If behavior changes, check whether parser shadow gates will fail.
