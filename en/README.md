# Styio Maintainer Manual

This manual is the developer documentation for the Styio ecosystem. It provides maintenance guidance and collaboration conventions for the `styio` compiler repository and for ecosystem repositories that build on Styio public interfaces, including `Spio`, `Vityo`, and related tools.

*Last updated: 2026-05-12*

## Maintainer Guide

This manual contains 39 core chapters. To read efficiently, choose the path that matches your maintenance goal.

### Essential: New Maintainer Onboarding

If this is your first time maintaining the ecosystem, read these foundation pages in order:

1. [Contributor Collaboration Rules](standards/contributor-contract.md) - mandatory development restrictions and constraints.
2. [Documentation and SSOT Rules](standards/documentation-and-ssot.md) - where the single source of truth lives.
3. [Repository Matrix and Source Priority](ecosystem/repository-matrix.md) - which repository is authoritative for which facts.
4. [Three-Repository Collaboration Guide](ecosystem/three-repository-collaboration.md) - how to coordinate updates across `styio`, `Spio`, and `Vityo`.
5. [Styio Core Collaboration Guide](ecosystem/styio-core-workflow.md) - the compiler repository change loop.
6. [styio-community Guide](ecosystem/styio-community-development.md) - RFC process and technical decision mechanics.

### Advanced: Architecture and Toolchain

When you are ready to change code, first understand the system context:

- **Layering and pipeline**: [Layered Architecture](architecture/layered-architecture.md) | [Compiler Pipeline](architecture/compiler-pipeline.md) | [Source Tree Map](architecture/source-tree.md)
- **Environment and foundations**: [Build Toolchain](toolchain/build-toolchain.md) | [styio-dev-env Purpose](ecosystem/styio-dev-env-development.md)
- **Standards and compliance**: [Coding and Refactoring Rules](standards/coding-and-refactor-rules.md) | [styio-audit Collaboration Guide](ecosystem/styio-audit-development.md) | [Audit and Compliance](standards/audit-license-and-dependency-policy.md)
- **Quality and performance**: [Testing and Regression Strategy](standards/testing-and-regression.md) | [styio-benchmark Collaboration Guide](ecosystem/styio-benchmark-development.md) | [CLI and Debugging](toolchain/cli-and-debug-workflow.md)

### Practice: Compiler Maintenance Track

Use these pages when maintaining concrete compiler modules:

- **Parser / AST**: [Parser Manual](interfaces/parser-manual.md) | [New Token or Syntax Change](runbooks/new-token-or-syntax.md) | [New AST or IR Node](runbooks/new-ast-or-ir.md) | [Parser Shadow Migration](runbooks/parser-shadow-and-dual-track.md)
- **Semantics and IR**: [Analyzer Manual](interfaces/analyzer-manual.md) | [Core Interface Overview](interfaces/core-interfaces.md) | [State / Pulse / Snapshot Change](runbooks/state-and-pulse.md)
- **CodeGen / Runtime**: [CodeGen Manual](interfaces/codegen-manual.md) | [Runtime Manual](interfaces/runtime-manual.md) | [New Intrinsic Change](runbooks/new-intrinsic.md)
- **I/O and standard streams**: [Standard Stream and Resource Capability](runbooks/resources-and-stdio.md) | [Resources, `@`, and Standard Streams](language/resources-and-stdio.md)

### Practice: Tooling Maintenance Track

Use these pages when maintaining package management, cloud services, or editor integrations:

- **Package manager**: [Spio Collaboration Guide](ecosystem/spio-development.md) | [Spio Capabilities and Boundaries](ecosystem/spio-surface.md)
- **IDE and UI**: [Vityo Collaboration Guide](ecosystem/vityo-development.md) | [Extensions Collaboration Guide](ecosystem/extensions-development.md)
- **Platform and cloud**: [styio-platform Collaboration Guide](ecosystem/styio-platform-development.md)
- **External interfaces**: [CLI and Machine Interface Change](runbooks/cli-and-machine-interface.md) | [Diagnostics and Error Model](runbooks/diagnostics-and-error-model.md)

### Reference

- [Feature Change Matrix](interfaces/change-matrix.md)
- [Testing Pyramid and Case Selection](runbooks/testing-pyramid-and-case-selection.md)
- [Language and Design SSOT Map](language/ssot-map.md)

---

## Maintenance Boundaries and Discipline

This manual defines several core boundaries:

- **Do** provide rules, responsibility boundaries, toolchain instructions, reproducible commands, and primary interface references.
- **Do not** accumulate historical logs, maintain a parallel language specification, or overuse conceptual introductions.

Before making any change, first identify which repository you are maintaining:

- **Language semantics, compiler, and tests**: use the [Styio Core Collaboration Guide](ecosystem/styio-core-workflow.md).
- **License, dependency, and security compliance**: use [Audit, License, and Dependency Compliance](standards/audit-license-and-dependency-policy.md).
- **Package management and workflow commands**: use the [Spio Collaboration Guide](ecosystem/spio-development.md).
- **Editor, UI, and AI panels**: use the [Vityo Collaboration Guide](ecosystem/vityo-development.md).

Do not invert the dependency direction: tool repository requirements must not distort the compiler's core design or language semantics.

## Authoritative SSOT Index

When writing documentation or developing features, network links are only navigation aids. Prefer the local source tree as the authority. Repositories in the ecosystem share these branch conventions:

- `nightly`: the active development branch. New features, fixes, and routine maintenance should land here.
- `stable`: the stable release branch. It only accepts fixes carried from `nightly`.
- `main`: the long-term maintenance and public presentation branch.

Core upstream entry points:

- **Semantics and specification**: [`docs/design/`](https://github.com/eBioRing/styio/tree/nightly/docs/design)
- **Development policy**: [`docs/specs/AGENT-SPEC.md`](https://github.com/eBioRing/styio/blob/nightly/docs/specs/AGENT-SPEC.md)
- **Acceptance criteria**: [`src/`](https://github.com/eBioRing/styio/tree/nightly/src) and [`tests/`](https://github.com/eBioRing/styio/tree/nightly/tests)
- **Package manager interface requirements**: [`Styio-External-Interface-Requirement-Spec.md`](https://github.com/eBioRing/Spio/blob/nightly/docs/styio/Styio-External-Interface-Requirement-Spec.md)
