# Three-Repository Collaboration Guide

This page provides a recommended process overview for cross-repository collaboration among `styio`, `Spio`, and `Vityo`. By clarifying semantic boundaries and collaboration agreements, it aims to improve coordination across the ecosystem.

For shared standards such as license and dependency compliance, see [Audit and Compliance](../standards/audit-license-and-dependency-policy.md).

## Collaboration Model

The Styio ecosystem keeps repositories decoupled through the following collaboration roles:

| Repository | Core role | Collaboration agreement |
| --- | --- | --- |
| `styio` | Upstream semantic source | Defines core syntax, semantics, and public `styio-protocol` interfaces. |
| `Spio` | Package ecosystem consumer | Owns package management and workflow, and interacts with the compiler through public contracts. |
| `Vityo` | Interaction and view consumer | Provides IDE and visualization capabilities, consuming analysis facts produced by the compiler. |

## Collaboration Principles

1. **Contract-driven**: `styio` defines stable public interfaces and `styio-protocol`; other tools build services on top of those interfaces.
2. **Clear responsibility**: `Spio` and `Vityo` focus on their own domains and do not modify the core semantics of the language in reverse.
3. **Process capture**: Discuss shared collaboration flows here first, then move stable conclusions into each project's local documentation.
4. **Independent closure**: Each repository maintains its own code, tests, and delivery gates.
5. **Smooth evolution**: Cross-repository changes should include compatibility windows and validation plans to reduce migration cost.

## `styio-protocol`: The Ecosystem Handoff

`styio-protocol` is the static protocol between the compiler and surrounding tools. It defines how components handshake without coupling at the source-code level.

It covers these collaboration surfaces:

1. **CLI contract**: public CLI arguments, exit codes, and file interaction conventions.
2. **Capability handshake**: version and feature metadata from `styio --machine-info=json`.
3. **Compile plan**: schema and execution semantics for `styio --compile-plan <path>`.
4. **Semantic payloads**: public JSON / JSONL data such as diagnostics, runtime events, and token ranges.

This allows package managers and IDEs to call core compiler capabilities without linking private compiler modules.

## Coordinating Syntax Updates

When `styio` introduces new syntax, coordinate `Vityo` and `Spio` updates as follows:

- **Upstream (`styio`)**: after implementing the syntax, provide verifiable examples, machine-readable facts such as token ranges, and protocol documentation updates.
- **Downstream (`Vityo` / `Spio`)**: use stable compiler-provided facts to update highlighting, completion, diagnostic presentation, or workflow logic.
- **Feedback loop**: if downstream tools need finer-grained analysis for product interaction, request an interface improvement in `styio` instead of bypassing the interface downstream.

## Recommended Workflow Stages

For large changes, use these collaboration stages:

1. **Draft consensus**: define the change goal, affected interfaces, and each repository's responsibility in `styio-dev-doc`.
2. **Interface first**: stabilize the interface shape in `styio` before downstream implementation begins.
3. **Independent implementation**: each repository completes its local feature loop and automated validation.
4. **Documentation synchronization**: move final collaboration decisions into local project documentation and update the corresponding maintainer manual pages.

## Change Type Matrix

| Change scenario | Driver | Collaborator | Recommended validation |
| --- | --- | --- | --- |
| Syntax / diagnostic update | `styio` | `Vityo` (interaction) | Run the compiler pipeline and IDE interaction tests |
| New compiler release | `styio` | `Spio` (hosting) | Update the compatibility matrix and verify the toolchain lifecycle |
| Deep IDE analysis requirement | `Vityo` | `styio` (interface) | Extend IDE service interfaces and run adapter tests |
| Package management policy change | `Spio` | `styio` (protocol) | Validate registry interaction and resolver logic |

Use this matrix to identify affected nodes quickly and avoid gaps in coordination.
