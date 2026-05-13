# styio-audit Security and Compliance Guide

This page explains how `styio-audit`, the audit framework, provides compliance and security support across the ecosystem.

`styio-audit` acts as the ecosystem's security guardrail. It does not implement product behavior directly; instead, it reduces commercial and security risk through automated compliance checks.

## Core Assurance Responsibilities

`styio-audit` focuses on:

- **License compliance**: helps evaluate open-source license compatibility and identify potential commercial legal risk.
- **Dependency tracking**: maintains transparent third-party dependency inventories so the supply chain is traceable.
- **Security scanning**: provides automated secret and credential scanning to prevent accidental leakage.
- **Quality gates**: provides reusable security validation scripts for CI/CD so release flows remain robust.

## Collaboration with Other Repositories

- **Serving every repository**: checks provided by `styio-audit` should become a security copilot in each repository's release process.
- **Supporting `styio-platform`**: during package distribution, the platform calls audit rules to verify package compliance and protect users.
- **Enabling `Spio`**: audit policies provide reference baselines for package-manager security checks and help build a trusted package ecosystem.

## Collaboration Principles

1. **Security consensus**: when compliance policy conflicts with development convenience, prefer establishing security consensus first.
2. **Automation-driven**: turn audit rules into machine-readable configuration, or Policy as Code, to reduce manual intervention and improve feedback speed.
3. **Minimal dependencies**: keep the audit tool lightweight to reduce its own infrastructure attack surface.

## Recommended Reading

- [Audit, License, and Dependency Compliance](../standards/audit-license-and-dependency-policy.md)
- [Repository Matrix and Source Priority](repository-matrix.md)
