# styio-platform Development Guide

This page defines the development process and maintenance boundaries for `styio-platform`, the platform and cloud-services repository.

`styio-platform` is not a local tool repository. It is the service core that supports the ecosystem backend.

## Current Stage

`styio-platform` is infrastructure for the `Spio` registry and remote execution capabilities. Treat it as a highly available, contract-driven distributed system, not as a simple compiler extension.

## Core Platform Responsibilities

`styio-platform` primarily owns:

- **Service core**: core scheduling, authentication, and public APIs.
- **Registry distribution**: cloud package sources, version validation, and package metadata distribution for the package manager.
- **Regional node and worker control**: regional node routing and lifecycle management for cloud execution workers.
- **Delivery gates**: security scanning, compliance audit blocking, and release pipeline control.

It does **not** own:

- local compiler semantics or execution logic, which belong in `styio`
- local project workflow or client CLI experience, which belong in `Spio`

## Development Order and Standards

When building platform capabilities, follow this order:

1. **Align the contract first**: platform-client interaction, including `Spio`, depends heavily on published API contracts and the Registry Protocol. Any I/O change must start with API design agreement.
2. **Respect security audits**: because user assets are involved, any change to authentication, key management, or persisted state must follow data security rules from `styio-audit`.
3. **Document architecture before implementation**: update `docs/design/`, OpenAPI definitions, or GraphQL schemas before backend implementation.

## Relationship to Other Repositories

- **Upstream service for `Spio`**: the platform is the distributor and validator of package data. When a client performs `publish` or `fetch`, the platform makes the final decision.
- **Consumer of `styio-audit` policies**: the platform does not hard-code risk blacklists. It consumes manifest inventory and security policies from the audit framework.
- **Cloud collaboration with `Vityo`**: if endpoints such as iOS use cloud execution as the main path, the platform must provide secure sandboxing and execution routing.

## Validation and Release

Cloud services are much more destructive than local CLIs:

- Local development should use mocks or Docker containers for end-to-end sandbox testing.
- Server deployment requires staged validation, such as staging or canary. Any breaking API change must provide a versioned compatibility window.
- Include load or chaos regression tests for Registry and Worker paths.

## Continue Reading

- [Repository Matrix and Source Priority](repository-matrix.md)
- [Three-Repository Collaboration Workflow](three-repository-collaboration.md)
- [Spio Development Guide](spio-development.md)
