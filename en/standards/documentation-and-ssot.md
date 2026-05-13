# Documentation and SSOT Rules

This page focuses on documentation that serves maintenance. More documentation is not automatically better.

## Basic Documentation Maintenance Principles

The core of `DOCUMENTATION-POLICY.md` is simple:

- If content can be merged into an existing authoritative document, do not create a parallel long-form document.
- If the same detail is explained in three or more places, designate a single SSOT.
- GitBook summarizes; it does not create a second truth.

## Common SSOT Table for Maintainers

| Topic | Authoritative location |
| --- | --- |
| Overall language semantics | `docs/design/Styio-Language-Design.md` |
| EBNF | `docs/design/Styio-EBNF.md` |
| Symbols and tokens | `docs/design/Styio-Symbol-Reference.md` |
| Intrinsic specifications | `docs/design/Styio-StdLib-Intrinsics.md` |
| Resource driver interface | `docs/design/Styio-Resource-Driver.md` |
| Contribution and implementation rules | `docs/specs/AGENT-SPEC.md` |
| Documentation policy | `docs/specs/DOCUMENTATION-POLICY.md` |
| Dependency list | `docs/specs/THIRD-PARTY.md` |
| Actual acceptance | `tests/` |

## Cross-Repository Update Priority

Before updating this GitBook, use the latest facts in this order:

1. local working tree
2. `Unka-Malloc/*`
3. `eBioRing/*`

This especially applies to:

- `styio`
- `Spio`
- `Vityo`

If the local working tree is ahead of the cloud repository, do not overwrite local facts with stale GitHub pages.

For more specific repository boundaries and source priorities, see:

- [Repository Matrix and Source Priority](../ecosystem/repository-matrix.md)
- [Audit, License, and Dependency Compliance](audit-license-and-dependency-policy.md)

## When Documentation Must Be Synchronized

| Code change | Required documentation |
| --- | --- |
| New syntax / new symbol | `Language-Design` + `EBNF` + `Symbol-Reference` |
| New intrinsic | `StdLib-Intrinsics` |
| New driver interface change | `Resource-Driver` |
| Documentation structure change | `DOCUMENTATION-POLICY` and related indexes |
| External dependency change | `THIRD-PARTY` |
| Audit, license, or commercial-risk policy change | `styio-audit` module + project `LICENSE-POLICY.md` / `DEPENDENCY-USAGE.md` / inventory documents |

## Requirements for GitBook

This GitBook should primarily maintain:

- best development practices
- mandatory rules
- layered structure
- primary interface descriptions
- practical debugging and testing commands

It should not maintain:

- extensive development diaries
- stale milestone process notes
- parallel long-form semantic specifications

## GitBook Framework Boundary

Future maintainers should normally edit only:

- `zh/**/*.md`
- `en/**/*.md`
- `zh/SUMMARY.md`
- `en/SUMMARY.md`

Avoid changing these unless necessary:

- GitBook / HonKit framework configuration
- rendering pipeline other than verification scripts
- repository-root `SUMMARY.md`

The principle is straightforward:

- this repository serves documentation content, not documentation framework development
- if pages build, link, and render normally, do not expand the framework layer
- interface, standard, example, or table-of-contents updates should stay in Markdown
- the two GitBook backend Spaces must sync `zh` and `en` as separate Project directories; do not sync the repository root

## Documentation Verification Commands

Completeness check and build:

```bash
./scripts/test_docs.sh
```

With browser rendering smoke test:

```bash
./scripts/test_docs.sh --with-browser
```

This check only confirms that the existing GitBook framework is not broken. Current coverage includes:

- internal Markdown links
- reachability from home / `SUMMARY`
- HonKit build
- key-page headless browser screenshots and DOM text assertions

## Historical Documentation

Historical documents may exist, but their role is archive, not primary navigation.

If a historical record no longer affects maintenance decisions today, it should not occupy the core GitBook path.
