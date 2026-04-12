# 编码与重构规则

这一页是 `AGENT-SPEC.md` 里最容易在日常开发中直接踩到的规则压缩版。

## 格式化

`styio` 的 C++ 代码必须符合仓库根目录 `.clang-format`。

关键约束：

- 2 空格缩进
- 不使用 tab
- `PointerAlignment: Right`
- 顶层定义的返回类型换行
- include block 需要 regroup
- class / enum / struct / namespace 大括号另起一行

常用命令：

```bash
clang-format -i src/**/*.cpp src/**/*.hpp
```

## 命名规则

| 对象 | 规则 | 例子 |
| --- | --- | --- |
| 类 / AST 节点 | PascalCase | `NameAST` |
| 自由函数 | snake_case | `parse_main_block_with_engine_latest` |
| 枚举类型 | PascalCase | `StyioTokenType` |
| 成员变量 | snake_case | `cur_pos` |
| 常量 | UPPER_SNAKE | `TokenPrecedenceMap` |

## 双轨重构后缀

当前 parser 和部分重构工作明确使用状态后缀：

| 后缀 | 用途 |
| --- | --- |
| `_legacy` | 稳定旧路径 |
| `_nightly` | 新路径 / 现默认路径 |
| `_latest` | 双轨共享入口 |
| `_draft` | 尚未满足 checkpoint 的在改实现 |

实际规则：

- 新进入双轨重构的函数，不要继续保留无状态命名
- 对外文档和 CLI 统一说 `nightly`
- `new` 只允许作为兼容别名出现

## 头文件与 include 约定

每个头文件都要同时使用：

- `#pragma once`
- 传统 include guard

include 分组建议：

1. C++ STL
2. Styio
3. LLVM
4. Others

## 注释规则

- 优先写说明“为什么这样做”，不要写“这行代码做了什么”
- 分节注释可以用 `/* ... */`
- 普通单行注释用 `//`

## visitor 注册是硬要求

新增 AST / IR 节点时，必须同步这些位置：

- `ASTDecl.hpp`
- `AST.hpp`
- `ToStringVisitor.hpp`
- `ASTAnalyzer.hpp`
- `TypeInfer.cpp`
- `ToStyioIR.cpp`
- 必要时 `IRDecl.hpp`
- 必要时 `CodeGenVisitor.hpp`

少注册一个 visitor，通常不会给你友好的错误信息，只会制造模板地狱。

## CMake 规则

主仓库用单个顶层 `CMakeLists.txt`，源码是显式列出的，不靠 glob。

这意味着：

- 新增 `.cpp` 后，必须手动加到 `CMakeLists.txt`
- 不要假设“文件放进目录里就会自动参与构建”
