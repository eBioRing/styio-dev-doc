# Styio Core Collaboration Guide

This page describes the recommended collaboration model for development in the main `styio` compiler repository.

To keep each component focused, changes to the compiler repository should be separated logically from adaptation work in surrounding tools such as `Spio` and `Vityo`.

## Branch Collaboration Model

All ecosystem repositories share a common branch model that provides a stable collaboration baseline:

- **`nightly`**: the active development branch. Feature development, bug fixes, and routine maintenance should land here.
- **`stable`**: the stable release branch.
- **`main`**: the long-term maintenance and public presentation branch.

When checking compiler facts or running local validation, prefer the `nightly` working tree.

## Collaboration Scope of the `styio` Repository

The `styio` repository owns these core assets:

- **Language design**: syntax definitions, semantic rules, and core specifications.
- **Compiler core**: parser, analyzer, IR generation, CodeGen, and JIT runtime.
- **Infrastructure**: CLI interfaces, `styio-nano` configuration, and automated tests such as milestone and pipeline suites.
- **Engineering decisions**: ADRs, maintainer manuals, and design documents.

## Recommended Change Loop

Use this development rhythm so contributions can be integrated with high quality:

1. **Align with design**: before changing code, find the relevant specification in `docs/design/` or `docs/specs/`.
2. **Implement in source**: complete the feature logic in the core path.
3. **Validate regressions**: add or update automated tests so the feature behaves as intended without breaking existing paths.
4. **Synchronize documentation**: update the relevant maintainer guidance in this manual so future developers understand the design.

This small, end-to-end loop is the best practice for keeping the compiler healthy over time.

## Roles in Collaboration

The Styio ecosystem follows the "semantic source" principle:

- **Compiler as producer**: defines language facts and exposes capabilities through public interfaces such as `styio-protocol`.
- **Surrounding tools as consumers**: `Spio` and `Vityo` provide package management or IDE support by consuming public interfaces.

If your change affects a public interface, such as `--machine-info` output or diagnostic categories, notify the maintainers of `Spio` and `Vityo`.

## Responding to IDE Service Requirements

Tools such as `Vityo` may ask for new compiler analysis capabilities, including finer token ranges or semantic completion data. In that case:

1. **Make it an interface**: turn the requirement into a stable public compiler service.
2. **Preserve semantic purity**: the compiler owns core language semantics; do not distort the language design for a specific frontend interaction.
3. **Document consumption**: provide clear guidance for frontend developers when exposing the new interface.

## Continue Reading

- [Core Interface Overview](../interfaces/core-interfaces.md)
- [Feature Change Matrix](../interfaces/change-matrix.md)
- [Maintenance Runbook Guide](../README.md)
