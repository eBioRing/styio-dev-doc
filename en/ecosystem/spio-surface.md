# Spio Current Capabilities and Boundaries

This page does not describe an abstract "vision". It records what `Spio` has and has not publicly exposed in the 2026-04-12 GitHub synchronization pass.

This manual uses `styio-protocol` as the name for the static handoff contract between `spio` and `styio`. It is the public protocol composed of CLI, machine-info, compile-plan, diagnostics, and compatibility matrix surfaces. It is not a runtime suite.

## Current Stage

This maintainer manual treats `nightly` as the latest public implementation surface for `Spio`.

## Public Command Surface

Current `spio` explicitly exposes these command families:

- `new`
- `init`
- `check`
- `add`
- `remove`
- `fetch`
- `lock`
- `tree`
- `vendor`
- `build`
- `run`
- `test`
- `pack`
- `publish`
- `tool install`
- `tool use`
- `tool pin`
- `machine-info --json`

These are not merely planned features. They are public surface listed in `docs/governance/Spio-CLI-Contract.md` and `src/SpioCLI/CLI.cpp`.

## Capabilities That Are Live Today

### 1. Native core

The public implementation is no longer only a bootstrap scaffold. The native `C++20` + `CMake` path now covers:

- manifest / lock parsing and canonical write-back
- `single-version-v1` resolver
- workspace, path, git, and registry dependency sources
- tree / fetch / vendor
- deterministic `pack`

### 2. Registry consume / publish

The public surface includes:

- registry dependency source
- `file://`
- `http://`
- `https://`
- local filesystem publish
- anonymous HTTP `PUT` publish
- static blob-and-index layout

In other words, `spio` can already package locally and also exposes registry consumption and publishing transports.

### 3. Managed local Styio toolchain

The public surface includes:

- `spio tool install --styio-bin <path>`
- `spio tool use --version <x.y.z> [--channel <channel>]`
- `spio tool pin ...`
- `SPIO_HOME/tools/styio/...`
- project-local `spio-toolchain.toml`

This means `spio` has started to own local installation, switching, and project-level pinning of the Styio compiler. It is no longer only a dependency resolver.

When `styio` releases a new version, this responsibility is triggered: `spio` must update the version hosting repository or toolchain index so the new version can be discovered, installed, selected, and pinned. It must also synchronize the compatibility matrix, registry / publish metadata, and notification messages.

### 4. Compile-plan dry-run

The public surface includes:

- `spio build --dry-run`
- `spio run --dry-run`
- `spio test --dry-run`
- local `.spio/build/<cache-key>/plan.json`

The important boundary is:

- `spio` exposes **plan generation**
- and declares compile-plan v1 as live through `styio-protocol`

## Capabilities Not Yet Publicly Complete

Do not document the following as already supported:

- auth / accounts / signatures / stronger trust policy
- private security module
- more aggressive multi-version resolver
- future schema / release matrix beyond compile-plan v1

The accurate wording today is:

- `spio` has a real package-manager core
- compile-plan v1 compiler-execution `styio-protocol` is live
- higher protocol versions and release matrices remain constrained by the public interface release state of `styio`

## Directories to Inspect Now

When maintaining `Spio@nightly`, start with:

- `docs/governance/`
- `docs/security/`
- `docs/registry/`
- `docs/adr/`
- `docs/operations/`
- `src/SpioCLI/`
- `src/SpioManifest/`
- `src/SpioResolve/`
- `src/SpioPack/`
- `src/SpioPublish/`
- `src/SpioRegistryClient/`
- `src/SpioRegistryServer/`
- `src/SpioSecurity/`
- `src/SpioTool/`
- `src/SpioVendor/`

## Most Important Gates

In addition to the older manifest and compatibility gates, treat these gates as first-line entry points:

- `styio_compile_plan_contract_gate`
- `spio_registry_server_gate`
- `spio_registry_promotion_gate`
- `spio_registry_split_origin_http_gate`
- `spio_cli_gate`
- `spio_extractability_gate`
- `styio_spio_dual_maintenance_gate`
- `styio_contract_compat_gate`

## Correct Boundary with `styio`

Today, `spio` should still depend on `styio` only through:

- `styio --machine-info=json`
- published `styio --compile-plan <path>`
- `contracts/compat/styio-support.toml`
- published diagnostics / handshake fields

Do not describe `spio` as capable of reading compiler internals just because it has evolved registry, publish, and toolchain lifecycle features.

## Continue Reading

- [Spio Development Guide](spio-development.md)
- [Repository Matrix and Source Priority](repository-matrix.md)
- [CLI and Machine Interface Change Runbook](../runbooks/cli-and-machine-interface.md)
