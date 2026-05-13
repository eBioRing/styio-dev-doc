# 贡献者契约

这一页只写维护 `styio` 本体时必须先接受的约束。

如果你当前改的是 `Spio` 或 `Vityo`，不要把这页当成它们的直接规范入口，先回到各自的开发指引确认仓库边界。

## 开始改代码前先读什么

如果改动涉及语言层，请先读：

- `docs/design/Styio-Language-Design.md`
- `docs/design/Styio-EBNF.md`
- `docs/design/Styio-Symbol-Reference.md`
- `docs/design/Styio-StdLib-Intrinsics.md`
- `docs/design/Styio-Resource-Driver.md`
- `docs/specs/AGENT-SPEC.md`
- `docs/specs/DOCUMENTATION-POLICY.md`

这不是形式主义。Styio 现在同时有设计文档、冻结样例和迁移中的实现，不先确认边界，很容易把目标设计误改成当前实现，或者反过来。

## 阶段边界必须守住

编译器主链路是：

```text
Source -> Tokenizer -> Parser -> TypeInfer -> StyioIR -> LLVM IR -> ORC JIT
```

维护时不要跨层偷渡：

- Parser 不碰 LLVM 类型
- CodeGen 不改 AST
- 不能跳过 `AST -> StyioIR -> LLVM IR` 这条链

## 明确禁止的事

- 不要引入 `if`、`while`、`for`、`return`、`fn`、`let` 这类关键字式扩展
- 不要修改 `src/include/cxxopts.hpp`
- 不要继续扩展 `src/Deprecated/`
- 不要让现有测试无故失效
- 不要跳过 visitor 注册
- 不要在生成代码里引入运行时堆分配

## Golden Cross 守则

`AGENT-SPEC.md` 把 Golden Cross 示例视为语言层“宪法示例”。任何改动如果会破坏这条示例，必须明确说明理由，而不是默默改掉。

## 维护者的工作方式

推荐顺序：

1. 先确认这次改动属于哪个层级
2. 先找对应 SSOT
3. 再改源码
4. 补测试
5. 同步文档

如果你跳过最后两步，短期可能还能编过，但会直接拉低仓库可维护性。
