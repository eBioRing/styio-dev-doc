# 新 AST 或 IR 节点改动手册

这页把 Styio 里最容易漏注册的一类改动拆成可执行清单：新增 AST 节点，或者为新能力新增 Styio IR 节点。

## 适用范围

这页适用于：

- 新 AST class
- AST 结构字段变化
- 新 Styio IR 节点
- AST 到 IR 的新 lowering 分支

## 新 AST 的最小同步链

源仓库里已经有一份零散清单：`src/StyioAST/add_new_ast.md`。这里把它整理成维护顺序。

### 1. 定义 AST 本体

至少同步：

- `src/StyioAST/ASTDecl.hpp`
- `src/StyioAST/AST.hpp`

### 2. 补 AST 类型枚举和可读名称

至少同步：

- `src/StyioToken/Token.hpp` 里的 `StyioASTType`
- `src/StyioToken/Token.cpp` 里的 `reprASTType`

### 3. 补 AST 可视化

至少同步：

- `src/StyioToString/ToStringVisitor.hpp`
- `src/StyioToString/ToString.cpp`

如果这一步没补，`--styio-ast` 和很多调试路径都会变得不可靠。

### 4. 补 analyzer visitor 面

至少同步：

- `src/StyioAnalyzer/ASTAnalyzer.hpp`
- `src/StyioAnalyzer/TypeInfer.cpp`
- `src/StyioAnalyzer/ToStyioIR.cpp`

实际要求不是“有声明就行”，而是这两套接口都要接住：

- `typeInfer(Node*)`
- `toStyioIR(Node*)`

少一边都不算完成。

## 新 IR 节点的最小同步链

### 1. 声明 IR 类型

至少同步：

- `src/StyioIR/IRDecl.hpp`
- 对应 IR 定义头，例如 `src/StyioIR/StyioIR.hpp`

### 2. 让 analyzer 真正产出它

至少同步：

- `src/StyioAnalyzer/ASTAnalyzer.hpp`
- `src/StyioAnalyzer/ToStyioIR.cpp`

### 3. 让 codegen 真正消费它

至少同步：

- `src/StyioCodeGen/CodeGenVisitor.hpp`
- 对应 `GetType*.cpp`
- 对应 `CodeGen*.cpp`

如果只是把节点声明出来，但没有 `toLLVMType` / `toLLVMIR` 路径，这个节点只是“看起来存在”。

## 典型修改顺序

推荐顺序是：

1. 定 AST / IR 数据结构
2. 补 `ToString`
3. 补 `typeInfer`
4. 补 `toStyioIR`
5. 补 `toLLVMType`
6. 补 `toLLVMIR`
7. 最后补测试和文档

这条顺序的好处是：每一层都能尽快被可视化和单独验证。

## 最低验证命令

### 看 AST 展开

```bash
./build/bin/styio --styio-ast --file tests/milestones/m9/t01_stdout_string.styio
```

### 看 Styio IR 是否落对

```bash
./build/bin/styio --styio-ir --file tests/milestones/m10/t01_stdin_echo.styio
```

### 看 LLVM IR 是否已经接住

```bash
./build/bin/styio --llvm-ir --file tests/milestones/m2/t01_simple_func.styio
```

### 跑 pipeline 和 milestone

```bash
ctest --test-dir build -L styio_pipeline --output-on-failure
ctest --test-dir build -L milestone --output-on-failure
```

## 常见漏项

- AST class 已定义，但 `StyioASTType` 没补
- `ToStringVisitor` 漏注册，导致 AST debug 不可信
- `typeInfer` 补了，`toStyioIR` 没补
- IR 节点能打印，但 `toLLVMType` / `toLLVMIR` 没补齐
- 改了结构却没同步对应测试样例

## 文档同步规则

如果这是语言级能力，而不是纯内部重构，最少同步：

- `docs/design/Styio-Language-Design.md`
- `docs/design/Styio-Symbol-Reference.md`
- 本手册相关页面
