# 贡献者协作准则

本页旨在为参与 `styio` 本体开发的开发者提供核心协作原则与共识。

如果你当前正在维护 `Spio` 或 `Vityo`，建议优先参考各自仓库的专属开发指引。

## 开发前的准备建议

为了确保改动能顺利集成，建议在涉及语言层修改前，先查阅以下核心设计文档：

- `docs/design/Styio-Language-Design.md`
- `docs/design/Styio-EBNF.md`
- `docs/design/Styio-Symbol-Reference.md`
- `docs/design/Styio-StdLib-Intrinsics.md`
- `docs/design/Styio-Resource-Driver.md`
- `docs/specs/AGENT-SPEC.md`
- `docs/specs/DOCUMENTATION-POLICY.md`

Styio 生态正处于快速演进中，查阅这些文档有助于区分“当前已实现的能力”与“未来设计目标”，从而让你的开发工作更加聚焦。

## 保持编译器架构的一致性

为了维护编译器长期可读性，建议在开发中遵循各阶段的职责边界：

```text
Source -> Tokenizer -> Parser -> TypeInfer -> StyioIR -> LLVM IR -> ORC JIT
```

在协作中，我们倾向于保持各层的纯粹性：
- 语法分析层（Parser）专注于 AST 的构建，不直接涉及底层的 LLVM 类型。
- 代码生成层（CodeGen）专注于消费 IR，不反向修改 AST 结构。
- 遵循完整的 `AST -> StyioIR -> LLVM IR` 流水线。

## 开发惯例

在 Styio 社区中，我们通过以下习惯来保持项目的高质量：

- **语法扩展**：优先考虑语言的一致性。建议避免引入 `if`、`while`、`fn` 等传统关键字风格的扩展，转而使用符合 Styio 语义逻辑的表达方式。
- **第三方库**：保持 `src/include/cxxopts.hpp` 等核心依赖的稳定性。
- **遗留代码**：新的功能逻辑应尽量避免在 `src/Deprecated/` 中扩展。
- **质量保障**：在提交改动前，请确保相关的自动化测试通过。
- **逻辑解耦**：通过 Visitor 注册机制来实现节点处理逻辑，保持代码的解耦。

## 核心示例（Golden Cross）

`AGENT-SPEC.md` 中定义的 Golden Cross 被视为验证语言能力的基准示例。如果你的改动涉及此处，请详细说明你的考量，以便社区共同评估其对现有语义的影响。

## 推荐的开发闭环

为了让你的改动更具可持续性，建议遵循以下流程：

1. **确定层级**：明确改动所属的编译器层级。
2. **查阅 SSOT**：在对应的权威设计文档中找到设计依据。
3. **实现功能**：修改源码实现。
4. **验证改动**：补全并运行自动化测试。
5. **更新指南**：同步更新本项目中的维护手册。

这种方式能最大程度地帮助其他开发者理解并延续你的工作成果。
