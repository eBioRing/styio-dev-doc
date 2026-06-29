# Audit, License, and Dependency Compliance

This page records audit inputs that all Styio-related repositories must maintain during development. It is not legal advice; it is an engineering gate that developers must satisfy before delivery.

The current audit framework is maintained by `styio-audit` and scans these projects externally:

- `styio` / local `styio-nightly`
- `Spio`
- `Vityo`
- `styio-platform`
- `styio-audit`

`styio-dev-doc` is the developer manual repository. It records processes and maintenance requirements, but it does not replace each project repository's own `LICENSE`, `LICENSE-POLICY.md`, `DEPENDENCY-USAGE.md`, docs gate, or audit gate.

## License Baseline

Styio-related source projects currently use Apache License, Version 2.0. Project repositories must be auditable as `Apache-2.0`:

1. The repository root must include an Apache-2.0 `LICENSE` file.
2. If `pyproject.toml`, `package.json`, or `pubspec.yaml` exists, the license field must declare `Apache-2.0`.
3. Root `LICENSE-POLICY.md`, `NOTICE`, `NOTICE.md`, `README.md`, or `docs/LICENSE-POLICY.md` must include the Apache License Version 2.0 source-distribution notice.

Apache-2.0 does not impose GPL-style copyleft inheritance. Developers must not write "derivative tools based on Styio source must be GPL open source" as a project rule. The correct boundary is: when distributing Styio-family source or binaries, preserve the license, copyright, NOTICE, modification statements, and patent-license notices required by Apache-2.0.

If a repository still uses GPL-3.0 as the main Styio-family license, or package metadata conflicts with Apache-2.0, the audit must fail.

## Manifest Inventory Is a Blocking Input

Every `styio-audit` project module must maintain these non-empty fields:

1. `technology_stack`
2. `internal_components`
3. `open_source_components`
4. `dependency_manifests`

Missing any of them prevents the audit from passing. Without technology stack, first-party components, open-source components, and manifest inventory, it is impossible to judge license status, commercial authorization, usage boundaries, or secret scanning coverage.

When adding or removing languages, SDKs, runtimes, build systems, CI, package managers, platform runners, first-party modules, external components, or dependency manifests, update all of the following:

1. The project repository's inventory document, such as `docs/specs/TECHNOLOGY-COMPONENT-INVENTORY.md`.
2. The corresponding `for-styio*/module.json` project module in `styio-audit`.
3. The project repository's docs index / docs audit results.

## Commercial Risk Boundary

Styio projects do not use dependencies that require commercial authorization, paid licenses, subscriptions, memberships, trial-only access, proprietary-use approval, or private registry access.

Every audited repository must maintain a dependency usage boundary file, preferably one of:

1. `DEPENDENCY-USAGE.md`
2. `THIRD-PARTY-NOTICES.md`
3. `docs/DEPENDENCY-USAGE.md`
4. `docs/dependencies.md`
5. `docs/third-party.md`

The dependency usage boundary must at least state:

1. which manifests current dependencies come from
2. whether each external component is runtime, build, test, fixture, prototype, or docs tooling
3. whether commercial authorization, subscription, membership, trial-only, or proprietary-use risk exists
4. what license evidence and usage boundary must be added before a new dependency enters production use

If manifests contain risk terms such as commercial license, subscription, membership, trial license, evaluation only, proprietary, or similar Chinese risk terms, the audit must fail until maintainers record acceptable open-source license evidence and clear usage boundaries.

## Secret Scanning

The audit framework scans the current working tree for sensitive information, including:

- password
- token
- API key
- private key
- client secret
- access key

Developers must not write suspected secret values into documentation, logs, test fixtures, or audit reports. When reporting a problem, record only redacted information such as rule id, file location, fingerprint, length, and first / last commit.

To scan commit history:

```bash
python3 -m styio_audit.cli secret-history --repo /path/to/repo --project <project> --format json
```

If a real secret appears in history, changing the latest file is not enough. The project security process must rotate credentials, record impact scope, and decide whether history cleanup is required.

## Developer Change Flow

For license, dependency, technology stack, external component, or audit rule changes, use this order:

1. Identify which repository owns the change. Do not put cross-repository rules into single-repository implementation details.
2. Update the project repository's `LICENSE`, `LICENSE-POLICY.md`, `DEPENDENCY-USAGE.md`, and inventory documents.
3. Update the default module or project module in `styio-audit`.
4. Run `styio-audit` module validation and unit tests.
5. Run `styio-audit gate --framework-only` against the target repository.
6. Run the target repository's docs index, docs audit, repo hygiene, and affected tests.
7. After pushing, check GitHub Actions. Do not stop at local success.

Common commands:

```bash
cd <styio-workspace>-audit
python3 -m unittest discover -s tests -v
python3 -m styio_audit.cli validate-modules
python3 -m styio_audit.cli gate --repo . --project styio-audit --framework-only
python3 -m styio_audit.cli gate --repo <styio-workspace> --project styio --framework-only
python3 -m styio_audit.cli gate --repo <spio-workspace> --project Spio --framework-only
python3 -m styio_audit.cli gate --repo <vityo-workspace> --project Vityo --framework-only
python3 -m styio_audit.cli gate --repo <styio-platform-workspace> --project styio-platform --framework-only
```

Project documentation gates usually are:

```bash
python3 scripts/docs-index.py --write
python3 scripts/docs-audit.py
python3 scripts/repo-hygiene-gate.py --mode tracked
```

## Typical Audit Failures

- Missing `LICENSE` or license text is not Apache-2.0.
- Package metadata declares GPL, proprietary, or a license conflicting with Apache-2.0.
- Missing source-distribution notice.
- Project module lacks `technology_stack`, `internal_components`, `open_source_components`, or `dependency_manifests`.
- New dependency has no usage boundary.
- Dependency manifest contains commercial authorization, membership, trial-only, or proprietary-use risk terms.
- Current working tree or commit history contains password, token, API key, private key, client secret, or access key.
- Only `styio-dev-doc` is updated, but the real project repository docs / gate evidence is not synchronized.

## Continue Reading

- [Repository Matrix and Source Priority](../ecosystem/repository-matrix.md)
- [Three-Repository Collaboration Workflow](../ecosystem/three-repository-collaboration.md)
- [Documentation and SSOT Rules](documentation-and-ssot.md)
