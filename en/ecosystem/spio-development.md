# Spio Collaboration Guide

This page describes the recommended development process and collaboration principles for the `Spio` repository.

`Spio` is Styio's project workflow and package management tool. It is intended to provide a smooth experience for project initialization, dependency management, and publishing.

## Evolution Stage

`Spio` is migrating from a Python bootstrap program toward a native `C++20` core. When contributing, follow this collaboration model:

- **Active development line**: prefer the `nightly` branch; it is the front line for feature evolution.
- **Technology direction**: new features should preferably be implemented in the native `C++20` core.
- **Historical compatibility**: the Python bootstrap remains in the tree as migration reference. Avoid major feature expansion there.

## Core Responsibilities of `Spio`

In ecosystem collaboration, `Spio` focuses on:

- **Project management**: parsing `spio.toml`, resolving dependency trees, and fetching sources.
- **Workflow orchestration**: providing unified build, run, test, and publish commands.
- **Toolchain management**: managing the lifecycle of the local `styio` compiler.
- **Protocol consumption**: consuming `styio-protocol` and interacting with the compiler through machine interfaces.

## Decoupling Agreement

To keep `Spio` independently evolvable, maintain healthy distance between repositories:

- **Process-level interaction**: `Spio` should handshake with the compiler through public CLI interfaces rather than link private implementation libraries.
- **Contract-driven compatibility**: prefer `styio --machine-info=json` and compatibility matrices under `contracts/` when deciding compatibility.
- **Version decoupling**: design features with adaptation across compiler versions in mind.

## `styio-protocol` Collaboration Details

`styio-protocol` is the common language between `Spio` and the compiler. For cross-repository feature changes:

1. **Align interfaces**: confirm that `styio` already provides stable JSON / JSONL diagnostics or compile-plan interfaces.
2. **Validate consumption**: verify parsing logic in `Spio` through contract tests.
3. **Close the feedback loop**: if the existing protocol cannot support a new workflow, request an interface extension on the compiler side.

## Recommended Validation Flow

Before submitting changes, use these checks to improve compliance:

- **Isolated validation**: test new behavior in a temporary directory so it does not depend on local path assumptions.
- **Interface compatibility**: run automation around `styio_contract_compat_gate`.
- **Native core check**: use `./scripts/native-check.sh` to validate native C++ code quality.

## Collaboration Summary

- **Contract first**: authoritative collaboration boundaries live in `docs/governance/`.
- **Prefer decoupling**: use `styio-protocol` for cross-repository coordination when adding capabilities.
- **Synchronize updates**: when the compiler publishes a new version, help update `Spio` toolchain indexes and compatibility matrices promptly.

## Continue Reading

- [Repository Matrix and Source Priority](repository-matrix.md)
- [Spio Current Capability Snapshot](spio-surface.md)
- [CLI Interface Change Runbook](../runbooks/cli-and-machine-interface.md)
