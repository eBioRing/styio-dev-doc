# 文档与 SSOT 规则

这一页只关注“文档应该服务维护”，不是“文档越多越好”。

## 文档维护的基本原则

`DOCUMENTATION-POLICY.md` 的核心其实很简单：

- 能并入已有权威文档，就不要新开平行长文
- 同一细节被三处以上实质性重复解释时，必须指定唯一 SSOT
- GitBook 负责归纳，不负责制造第二套真相

## 维护者最常用的 SSOT 表

| 主题 | 权威位置 |
| --- | --- |
| 语言总语义 | `docs/design/Styio-Language-Design.md` |
| EBNF | `docs/design/Styio-EBNF.md` |
| 符号与 token | `docs/design/Styio-Symbol-Reference.md` |
| intrinsic 规范 | `docs/design/Styio-StdLib-Intrinsics.md` |
| 资源驱动接口 | `docs/design/Styio-Resource-Driver.md` |
| 贡献与实现规则 | `docs/specs/AGENT-SPEC.md` |
| 文档政策 | `docs/specs/DOCUMENTATION-POLICY.md` |
| 依赖清单 | `docs/specs/THIRD-PARTY.md` |
| 实际验收 | `tests/` |

## 跨仓库更新优先级

更新这份 GitBook 前，默认按以下顺序取最新事实：

1. 本地工作树
2. `Unka-Malloc/*`
3. `eBioRing/*`

这条规则当前尤其适用于：

- `styio`
- `styio-spio`
- `styio-view`

如果本地工作树已经比云端更前，不要再拿旧的 GitHub 页面覆盖本地事实。

更具体的仓库边界和来源优先级，见：

- [仓库矩阵与来源优先级](../ecosystem/repository-matrix.md)

## 什么时候必须同步文档

| 代码改动 | 必改文档 |
| --- | --- |
| 新语法 / 新符号 | `Language-Design` + `EBNF` + `Symbol-Reference` |
| 新 intrinsic | `StdLib-Intrinsics` |
| 新 driver 接口变化 | `Resource-Driver` |
| 文档结构变化 | `DOCUMENTATION-POLICY` 和相关索引 |
| 外部依赖变化 | `THIRD-PARTY` |

## 对 GitBook 的要求

这份 GitBook 应该优先维护：

- 最佳开发实践
- 必须遵守的规范
- 分层结构
- 主接口说明
- 实际调试和测试命令

而不是：

- 大量开发日记
- 过期 milestone 过程描述
- 平行的语义长文

## GitBook 框架边界

后续维护者默认只应该改：

- `en/**/*.md`
- `en/SUMMARY.md`

非必要不要改：

- GitBook / HonKit 框架相关配置
- 验证脚本以外的渲染链路

这里的原则很简单：

- 这份仓库服务的是文档内容，不是文档框架研发
- 只要页面可构建、可跳转、可正常渲染，就不要扩写框架层
- 如果只是更新接口、规范、示例或目录，应该停留在 Markdown 层

## 文档验证命令

完整性检查 + build：

```bash
./scripts/test_docs.sh
```

加浏览器渲染烟测：

```bash
./scripts/test_docs.sh --with-browser
```

这套检查的目标只是确认原有 GitBook 框架没有被破坏。当前覆盖：

- Markdown 内部链接
- 页面从首页 / `SUMMARY` 的可达性
- HonKit 构建
- 关键页面的 headless 浏览器截图与 DOM 文本断言

## 关于历史文档

历史文档可以存在，但它的职责是归档，不是主导航入口。

如果某条历史记录不再影响今天的维护决策，就不应该占据 GitBook 的核心位置。
