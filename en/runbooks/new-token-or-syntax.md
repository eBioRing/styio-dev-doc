# New Token or Syntax Change Runbook

This page addresses a practical question: when adding a new token, changing an existing symbol, or extending parser syntax in Styio, what is the minimum complete loop?

## Scope

This page applies to:

- adding `StyioTokenType`
- changing symbol-to-token mappings
- adding parser recognition rules
- extending `legacy` / `nightly` / `latest` syntax paths

It does not apply to:

- pure semantic rule changes
- pure IR / codegen changes
- pure runtime helper changes

## First Identify the Change Type

| Change | First landing point |
| --- | --- |
| New character or symbol combination | `src/StyioParser/Tokenizer.cpp` |
| New token type | `src/StyioToken/Token.hpp` |
| Token display name | `src/StyioToken/Token.cpp` |
| New expression / statement structure | `src/StyioParser/Parser.cpp` or `src/StyioParser/NewParserExpr.cpp` |
| New lookahead rule | `src/StyioParser/ParserLookahead.*` |

## Modification Order

### 1. Change the token surface first

Check at least:

- `src/StyioToken/Token.hpp`
- `src/StyioToken/Token.cpp`
- `src/StyioParser/Tokenizer.cpp`

For operators or symbols, also check:

- `TokenPrecedenceMap`
- `TokenStrMap`
- `StrTokenMap`

### 2. Then change parser routing

Check at least:

- `src/StyioParser/Parser.hpp`
- `src/StyioParser/Parser.cpp`
- `src/StyioParser/NewParserExpr.cpp`

If the decision depends on skipping trivia or non-trivia lookahead, do not copy the logic. Reuse:

- `styio_is_trivia_token`
- `styio_skip_trivia_tokens`
- `styio_try_check_non_trivia`

They live in `src/StyioParser/ParserLookahead.*`.

### 3. If a new AST is produced, complete the AST path immediately

Do not wait until parser code is done before thinking about AST. Synchronize at least:

- `src/StyioAST/ASTDecl.hpp`
- `src/StyioAST/AST.hpp`
- `src/StyioToString/ToStringVisitor.hpp`
- `src/StyioToString/ToString.cpp`

Then continue with [New AST / IR Node Change Runbook](new-ast-or-ir.md).

### 4. Synchronize authoritative design documents

Syntax and symbol changes must synchronize at least:

- `docs/design/Styio-EBNF.md`
- `docs/design/Styio-Symbol-Reference.md`

If semantics changed, also update:

- `docs/design/Styio-Language-Design.md`

## Hard Rules for the Dual-Track Parser

If a change lands in the parser layer, check all of:

- `legacy`
- `nightly`
- `latest`
- route stats
- shadow compare

Do not make only `nightly` pass and leave differences for `latest` or the shadow gate to fail in CI.

## Minimum Validation Commands

### Check whether AST is generated as expected

```bash
./build/bin/styio --styio-ast --file tests/milestones/m1/t01_int_arith.styio
```

### Check parser dual-track consistency

```bash
./build/bin/styio \
  --parser-shadow-compare \
  --parser-shadow-artifact-dir /tmp/styio-shadow \
  --file tests/milestones/m7/t04_instant_pull.styio
```

### Run parser-related regressions

```bash
ctest --test-dir build -L shadow_gate --output-on-failure
```

### Run the minimum milestone loop

```bash
ctest --test-dir build -L milestone --output-on-failure
```

## Common Omissions

- New token added only in `Tokenizer.cpp`, but not in `Token.hpp`.
- Token name can print, but precedence or reverse mapping is missing.
- `nightly` path changed, but `latest` was not connected.
- Parser can produce AST, but `ToStringVisitor` is missing.
- Code changed, but `EBNF` and `Symbol-Reference` were not updated.

## Maintenance Advice

If one syntax change touches parser, analyzer, IR, and codegen at the same time, pause and confirm that you are not mixing a syntax problem with a semantic problem.
