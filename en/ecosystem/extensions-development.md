# Extensions Development Guide

This page defines general development constraints for **Styio Extensions**. It is not limited to `styio-ext-vsc`.

The current concrete reference implementation is the cloud repository `eBioRing/styio-ext-vsc`. Future editor extensions should follow the same boundaries by default.

## Current Fact Sources

As verified on 2026-04-12:

- there is no local `styio-ext-vsc` working tree in the current workspace
- the visible reference repository is `eBioRing/styio-ext-vsc`
- that repository currently has only a very thin `README.md`

Therefore this page must not invent a product design for extension repositories. Its job is to give maintainers stable extension boundaries and an implementation order.

## What Extensions Own

Extension repositories should only own host editor integration, such as:

- syntax highlighting
- snippets / language configuration
- command entries, task entries, and settings
- invoking `styio` / `spio` binaries
- rendering diagnostics, output panels, and basic developer experience

## What Extensions Do Not Own

Extension repositories do not own:

- the language semantics SSOT
- parser / analyzer / codegen / runtime implementation
- core package-manager logic
- reverse definitions of how a Styio program should be interpreted

If an extension requirement first requires changing the language definition, the correct action is to add a public interface in the `styio` repository, not to make private semantic assumptions inside the extension.

## Consume Only Public Boundaries

Extensions should prefer consuming:

- `styio` CLI
- `styio --error-format jsonl`
- `styio --machine-info=json`
- stable file input / output behavior
- published `spio` CLI or `styio-protocol`

Do not depend on:

- private `styio` headers
- internal AST / IR memory layout
- undocumented parser branch behavior
- a locally maintained syntax copy as the source of real language rules

## Difference from `Vityo`

`Vityo` is Styio's product-level IDE and runtime viewport.

An extension repository is an adapter layer inside a host editor. Its goal is to connect existing capabilities to VS Code or future editors, not to own the full product interaction model or platform execution strategy.

Therefore:

- product interaction and platform boundaries go back to `Vityo`
- language, CLI, diagnostics, and machine interface go back to `styio`
- host editor commands, settings, and integration mechanics go back to the extension repository

## Recommended Development Order

1. Confirm host editor capabilities and extension manifest requirements.
2. Confirm whether `styio` / `spio` already expose sufficient public interfaces.
3. If public interfaces are insufficient, add them in the source repository first.
4. Implement extension-side commands, settings, and rendering.
5. Add the extension repository's README, examples, and regression checks.

## Compatibility Principles

- Prefer allowing users to explicitly configure local `styio` / `spio` binary paths.
- Use `--machine-info=json` for capability detection instead of hard-coded version checks.
- Degrade gracefully when possible; do not break the entire extension because one advanced capability is unavailable.
- Do not turn compiler private implementation details into stable extension contracts.

## Current Use of `styio-ext-vsc`

In this manual, `styio-ext-vsc` is currently only:

- the existing reference repository for the extension family
- the named instance for VS Code scenarios

Do not treat it as the only possible form of the editor ecosystem. This page remains applicable when new extension repositories appear.

## Continue Reading

- [Repository Matrix and Source Priority](repository-matrix.md)
- [Styio Core Development Workflow](styio-core-workflow.md)
- [Vityo Development Guide](vityo-development.md)
- [CLI and Machine Interface Change Runbook](../runbooks/cli-and-machine-interface.md)
