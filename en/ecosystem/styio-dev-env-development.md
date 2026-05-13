# styio-dev-env Purpose

This page briefly explains the purpose of the `styio-dev-env` repository.

`styio-dev-env` is a static repository for standard development environment configuration. It does not contain complex business logic or independent development governance rules.

## Repository Purpose

Its core purpose is to eliminate development environment drift by providing:

- **Toolchain bootstrap**: scripts for one-command installation of compilers such as LLVM and CMake, plus required dependencies.
- **Standard container configuration**: official `Dockerfile` and VS Code `devcontainer.json` configuration files.
- **CI/CD environment base**: shared build-environment image configuration for GitHub Actions or self-hosted runners.

## How to Use It

- Developers can run initialization scripts from this repository when cloning main code repositories such as `styio` or `Spio`.
- CI pipelines pull Docker images defined here as build containers.
- When environment configuration such as Clang or system library versions needs an upgrade, update this repository's configuration files directly.

## Continue Reading

- [Build Toolchain](../toolchain/build-toolchain.md)
- [Repository Matrix and Source Priority](repository-matrix.md)
