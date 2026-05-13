# Repository Matrix and Source Priority

This page reuses the ecosystem entry matrix from the `styio` repository `README.md` and makes one additional maintainer concern explicit: **when updating documentation, which repository should be trusted first.**

## Ecosystem Matrix

The following responsibility boundaries are organized from `styio/README.md` and `styio/docs/specs/REPOSITORY-MAP.md`:

| Repository | Role | Primary responsibility |
| --- | --- | --- |
| `styio` | Language and compiler repository | Language semantics, compiler implementation, CLI, tests, primary design and specification documents |
| `Spio` | Package manager | Manifest, lockfile, resolver, workflow, and consumption of `styio-protocol` |
| `styio-platform` | Platform and cloud services | Service core, registry distribution, regional nodes, worker control, and platform delivery gates |
| `styio-audit` | Audit framework | Cross-repository audit gates, license policy, commercial risk, manifest inventory, and secret scanning |
| `styio-dev-doc` | Developer documentation | Cross-repository maintainer manual, development process, and collaboration rules |
| `styio-dev-env` | Standard development environment | Toolchain bootstrap, environment scripts, and shared environment conventions |
| `styio-book` | Product white paper | Public narrative, vision, and product-level explanation |
| `Vityo` | Dedicated IDE / runtime viewport | Editor, runtime visualization, AI panels, theme system, and platform execution policy |
| `styio-examples` / `styio-example` | Example projects | Runnable examples, templates, and best-practice samples |
| `styio-ext-vsc` / future extensions | Extension | Host editor integration, highlighting, plugin commands, settings, and diagnostic presentation |

## Source Priority When Updating Documentation

When maintaining this GitBook, use the newest facts in this order by default:

1. **The locally checked-out working tree**
2. **Same-name `Unka-Malloc/*` repositories**
3. **`eBioRing/*` repositories or mirrors**

This rule is not abstract advice; it reflects the current ecosystem:

- `Unka-Malloc` branches are often ahead of `eBioRing`.
- Local working trees are often ahead of cloud repositories.

Before writing documentation, do not rely only on GitHub pages. Inspect what is actually present in the local checkout.

## Branch and Synchronization Strategy

All ecosystem repositories share a common branch model. When reading or updating documentation, choose the branch that matches your goal:

- **`nightly`**: active development. Prefer this branch for local development and fact verification. All routine features and fixes should land here.
- **`stable`**: stable release branch. Use it when checking officially released capabilities.
- **`main`**: long-term maintenance and public presentation. Do not use it as the default baseline for active development.

This means:

- Documentation verification should first inspect `README.md`, `docs/`, `src/`, and `tests/` under the local `nightly` checkout.
- Published facts should be checked against the target repository's `stable` branch.
- Only fall back to remote GitHub pages when there is no local fact source.
- Extension documentation without a local working tree should first inspect the current reference repository, then fall back to public interfaces in `styio` and `Spio`.

## Minimal Check Before Updating Documentation

Before updating cross-repository documentation, at least do the following:

1. Read the main repository or tool repository `README.md`.
2. Read that repository's `docs/README.md` or `docs/specs/`.
3. Check the current branch and whether the working tree has uncommitted changes.
4. Fall back to GitHub repository pages only when no local fact source exists.

## How to Resolve Conflicts

When multiple repositories disagree about the same topic:

1. Language, compiler, and test acceptance: return to `styio`.
2. Package management, resolver, and contract compatibility: return to `Spio`.
3. Platform services, registry distribution, regional nodes, and worker control: return to `styio-platform`.
4. Audit framework, license policy, commercial risk, manifest inventory, and secret scanning: return to `styio-audit`.
5. IDE product interaction, runtime views, themes, and platform execution policy: return to `Vityo`.
6. VS Code or other host editor settings, commands, and integration: return to the corresponding extension repository.
7. This GitBook summarizes and maintains process guidance; it does not override each repository's own SSOT.

## Continue Reading

- [Styio Core Development Workflow](styio-core-workflow.md)
- [Audit, License, and Dependency Compliance](../standards/audit-license-and-dependency-policy.md)
- [Three-Repository Collaboration Workflow](three-repository-collaboration.md)
- [Spio Development Guide](spio-development.md)
- [Spio Current Capabilities and Boundaries](spio-surface.md)
- [Vityo Development Guide](vityo-development.md)
- [Extensions Development Guide](extensions-development.md)
