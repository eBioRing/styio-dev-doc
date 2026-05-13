# Resources, `@`, and Standard Streams

If you remember only one symbol, remember `@`. It is one of the most important parts of Styio and one of the easiest places for new maintainers to get confused.

## Three Roles of `@`

According to the current design documents, `@` carries at least three semantic roles:

| Role | Meaning | Examples |
| --- | --- | --- |
| Honest missing | Explicit missing value | `@` |
| Resource anchor | External resource or driver entry | `@file{...}`, `@stdin` |
| State container | State, memory, and persistent-slot semantics | `@[n](...)`, target design `@name : [|n|]` |

## Standard Streams That Are Explicitly Available

According to the M9 / M10 freeze on 2026-04-08:

- `@stdout`
- `@stderr`
- `@stdin`

These are not names produced by a user wrapper. They are standard-stream atoms recognized by the compiler.

### Output

Recommended modern syntax:

```text
"Hello" -> @stdout
"Oops" -> @stderr
```

Historical compatibility syntax remains available:

```text
>_("Hello")
```

### Input

Iterating stdin:

```text
@stdin >> #(line) => {
  line -> @stdout
}
```

Instant pull:

```text
value = (<< @stdin)
value -> @stdout
```

## Direction Constraints Are Semantic

Standard streams are not bidirectional free-form resources.

The current frozen rules should reject:

- writing to `@stdin`
- iterating reads from `@stdout`
- performing instant pull on `@stderr`
- acquiring handles for standard streams when such handles should not exist

This shows that the standard-stream model is no longer just syntax sugar. It is enforced by real analyzer and codegen rules.

## Be Careful with Resource Topology v2

`docs/design/Styio-Resource-Topology.md` describes a stronger target design, including:

- top-level `@name : [|n|] := { ... }`
- unified shadow sink syntax `expr -> $name`
- stricter resource topology boundaries

The source documentation also states clearly that **this design is not fully implemented yet**.

In real development:

- implemented behavior is defined by `tests/`, frozen milestones, and current compiler code
- target shape is described by `Resource-Topology.md`
- when they disagree, do not treat the target design as syntax that runs today

## A Practical Check

When you see `@`-related syntax, ask three questions:

1. Is this a missing value, a resource, or state?
2. Is there an example in `tests/`?
3. Is this a frozen rule, or still target syntax in a plan?
