# SymPolicy Organization Constitution: AI Assistance and Commit Signatures

**Status:** Long-term organization-wide governance rule for **all** SymPolicy repositories.

**Scope:** Every managed repository under `SymPolicy/*` (language, toolchain, docs, community, platform, and examples). Downstream personal mirrors must follow the same rule when contributing into the org.

## Articles

1. **AI cannot be responsible for code**, and therefore **AI must not sign code**.
2. Do not merge commits onto managed branches whose Git **author** or **committer** is an AI or bot identity (for example, Cursor Agent, Claude Code / Claude, Copilot, or similar coding agents).
3. When a human uses AI to generate or assist with changes, that human must sign and submit under their own identity. AI may produce drafts only; it must not appear as the signed author.
4. Pull requests that still contain AI- or bot-signed commits are **drafts**: re-author under a human signature before merge. Do not merge them onto the default branch as-is.
5. This rule does not depend on which AI tool was used. Merges that violate it are governance defects and must be rolled back or re-signed.

## Enforcement

- Documentation SSOT: contributor contracts in `styio-dev-doc` (EN/ZH) reference this constitution.
- Repository guardrails: per-repo checks may reject Cursor/bot authors; org rulesets strengthen this when available.
- Operating practice: treat Cloud Agent / automation PRs as drafts and re-author as a human before merge.
