# Coding and Refactoring Rules

This page is a compressed version of the `AGENT-SPEC.md` rules most likely to affect daily development.

## Formatting

`styio` C++ code must follow the repository root `.clang-format`.

Key constraints:

- 2-space indentation
- no tabs
- `PointerAlignment: Right`
- line break before return type for top-level definitions
- include blocks need regrouping
- braces for class / enum / struct / namespace start on a new line

Common command:

```bash
clang-format -i src/**/*.cpp src/**/*.hpp
```

## Naming Rules

| Object | Rule | Example |
| --- | --- | --- |
| Class / AST node | PascalCase | `NameAST` |
| Free function | snake_case | `parse_main_block_with_engine_latest` |
| Enum type | PascalCase | `StyioTokenType` |
| Member variable | snake_case | `cur_pos` |
| Constant | UPPER_SNAKE | `TokenPrecedenceMap` |

## Dual-Track Refactor Suffixes

Current parser and some refactor work use explicit status suffixes:

| Suffix | Purpose |
| --- | --- |
| `_legacy` | Stable old path |
| `_nightly` | New path / current default |
| `_latest` | Shared dual-track entry |
| `_draft` | Work in progress that has not met the checkpoint |

Practical rules:

- New functions entering dual-track refactor should not keep status-less names.
- Public documentation and CLI should say `nightly`.
- `new` is allowed only as a compatibility alias.

## Header and Include Conventions

Every header should use both:

- `#pragma once`
- traditional include guard

Recommended include grouping:

1. C++ STL
2. Styio
3. LLVM
4. Others

## Comment Rules

- Prefer explaining why something is done, not what a line does.
- Section comments may use `/* ... */`.
- Ordinary single-line comments use `//`.

## Visitor Registration Is Mandatory

When adding AST / IR nodes, synchronize:

- `ASTDecl.hpp`
- `AST.hpp`
- `ToStringVisitor.hpp`
- `ASTAnalyzer.hpp`
- `TypeInfer.cpp`
- `ToStyioIR.cpp`
- `IRDecl.hpp` when needed
- `CodeGenVisitor.hpp` when needed

Missing a visitor registration usually will not produce a friendly error. It often creates template failures.

## CMake Rules

The main repository uses one top-level `CMakeLists.txt`; source files are listed explicitly and not discovered by glob.

This means:

- when adding a `.cpp` file, update `CMakeLists.txt` manually
- do not assume placing a file in a directory makes it part of the build
