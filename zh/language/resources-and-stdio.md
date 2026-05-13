# 资源、`@` 与标准流

如果只记一个符号，请先记住 `@`。它是 Styio 里最容易让新人困惑、但也最核心的部分之一。

## `@` 的三种角色

根据当前设计文档，`@` 至少承担三种语义角色：

| 角色 | 含义 | 例子 |
| --- | --- | --- |
| Honest missing | 显式缺失值 | `@` |
| Resource anchor | 外部资源或驱动入口 | `@file{...}`、`@stdin` |
| State container | 状态、记忆、持久槽位相关语义 | `@[n](...)`、设计中的 `@name : [|n|]` |

## 已经明确可用的标准流

根据 2026-04-08 冻结的 M9/M10：

- `@stdout`
- `@stderr`
- `@stdin`

这些不是用户自己包一层 wrapper 得到的名字，而是编译器识别的标准流原子。

### 输出

推荐的现代写法：

```text
"Hello" -> @stdout
"Oops" -> @stderr
```

历史兼容写法仍然保留：

```text
>_("Hello")
```

### 输入

遍历 stdin：

```text
@stdin >> #(line) => {
  line -> @stdout
}
```

即时拉取：

```text
value = (<< @stdin)
value -> @stdout
```

## 方向约束已经进入语义层

标准流不是双向随便用的资源。

当前冻结规则里，以下行为应当报错：

- 向 `@stdin` 写
- 从 `@stdout` 迭代读取
- 对 `@stderr` 做 instant pull
- 对标准流做不该存在的 handle acquire

这说明标准流模型已经不只是语法糖，而是进入了 analyzer 和 codegen 的真实规则。

## 资源拓扑 v2 需要特别小心

`docs/design/Styio-Resource-Topology.md` 描述了一套更强的目标设计，例如：

- 顶层 `@name : [|n|] := { ... }`
- 统一的 shadow sink 写法 `expr -> $name`
- 更严格的资源拓扑边界

但源码文档也明确写了：**这套设计还没有完全实现。**

因此实际开发时请这样理解：

- 已实现行为：以 `tests/`、已冻结 milestone、当前编译器代码为准
- 目标形态：以 `Resource-Topology.md` 为准
- 两者不一致时，不要擅自把目标设计当成“今天就能跑”的语法

## 一个实用判断法

当你看到某个 `@` 相关语法时，先问自己三件事：

1. 这是缺失值、资源还是状态
2. 这个写法在 `tests/` 里有没有样例
3. 这是一条已经冻结的规则，还是还在计划里的目标语法
