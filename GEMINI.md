# Project Instructions: styio-dev-doc

This repository contains the developer manual for the Styio ecosystem. It is built using HonKit (a GitBook fork).

## Maintenance Workflows

### Documentation Updates
- All documentation is located in the `en/` directory.
- Content is primarily in Chinese, despite the `en/` prefix.
- The entry point is `en/README.md`, which contains a curated "Maintainer Reading Order".
- `en/SUMMARY.md` defines the GitBook structure and navigation.

### Validation
- Run `bash scripts/test_docs.sh` to validate links, reachability, and build status.
- The `scripts/check_docs.py` script ensures:
    1. No broken internal links.
    2. All markdown files are reachable from `README.md` or `SUMMARY.md`.

### Conventions
- **SSOT (Single Source of Truth):** Follow the rules in `en/standards/documentation-and-ssot.md`.
- **Reading Order:** When adding a new page, ensure it is added to both `en/SUMMARY.md` and the "Maintainer Reading Order" in `en/README.md`.
- **Date:** Update the "last checked" date in `en/README.md` when performing a major review.

## Architecture
- `architecture/`: High-level system design and source tree maps.
- `ecosystem/`: Collaboration between `styio`, `Spio`, and `Vityo`.
- `interfaces/`: Manuals for each compiler stage (Parser, Analyzer, etc.).
- `runbooks/`: Step-by-step guides for common maintenance tasks.
- `standards/`: Coding, testing, and documentation policies.
- `toolchain/`: Build and debug workflows.
