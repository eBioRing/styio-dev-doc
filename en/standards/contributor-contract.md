# Contributor Collaboration Rules

This page provides core collaboration principles and shared expectations for developers working on the `styio` core.

If you are currently maintaining `Spio` or `Vityo`, consult the dedicated development guide for that repository first.

## Preparation Before Development

Before making language-layer changes, read these core design documents:

- `docs/design/Styio-Language-Design.md`
- `docs/design/Styio-EBNF.md`
- `docs/design/Styio-Symbol-Reference.md`
- `docs/design/Styio-StdLib-Intrinsics.md`
- `docs/design/Styio-Resource-Driver.md`
- `docs/specs/AGENT-SPEC.md`
- `docs/specs/DOCUMENTATION-POLICY.md`

The Styio ecosystem is evolving quickly. These documents help distinguish currently implemented capabilities from future design targets, so development work stays focused.

## Preserve Compiler Architecture Consistency

To keep the compiler readable over the long term, maintain the responsibility boundaries of each stage:

```text
Source -> Tokenizer -> Parser -> TypeInfer -> StyioIR -> LLVM IR -> ORC JIT
```

In collaboration, keep each layer focused:

- The syntax analysis layer, Parser, focuses on AST construction and should not directly handle low-level LLVM types.
- The code generation layer, CodeGen, consumes IR and should not modify AST structure in reverse.
- Follow the complete `AST -> StyioIR -> LLVM IR` pipeline.

## Development Conventions

The Styio community maintains project quality through these habits:

- **Syntax extensions**: prefer language consistency. Avoid traditional keyword-style additions such as `if`, `while`, and `fn` unless they fit Styio semantics.
- **Third-party libraries**: keep core dependencies such as `src/include/cxxopts.hpp` stable.
- **Legacy code**: avoid extending new feature logic inside `src/Deprecated/`.
- **Quality assurance**: make sure related automated tests pass before submitting changes.
- **Logic decoupling**: use visitor registration to keep node handling decoupled.

## Core Example: Golden Cross

`AGENT-SPEC.md` defines Golden Cross as a baseline example for validating language capability. If your change affects it, explain your reasoning clearly so the community can evaluate semantic impact.

## Recommended Development Loop

Use this flow for sustainable changes:

1. **Identify the layer**: determine which compiler layer the change belongs to.
2. **Read the SSOT**: find the design basis in the corresponding authoritative document.
3. **Implement**: modify the source implementation.
4. **Validate**: add or run automated tests.
5. **Update guidance**: synchronize this maintainer manual.

This helps other developers understand and continue your work.


## AI Assistance and Commit Signatures

AI systems cannot be responsible for code, and therefore must not sign code.

- Do not land commits on managed branches whose Git **author** or **committer** is an AI or bot identity (for example, Cursor Agent).
- When a human uses AI to generate or assist with changes, that human must sign and submit the commits under their own identity. AI may produce drafts only; it must not appear as the signed author.
- Pull requests that still contain AI- or bot-signed commits are drafts: re-author them under a human signature before merge. Do not merge them onto the default branch as-is.
- This rule applies across managed Styio-ecosystem repositories and does not depend on which AI tool was used.

For the full organization constitution, see [AI Assistance and Commit Signatures (Organization Constitution)](./ai-authorship-constitution.md). This rule binds every SymPolicy repository.
