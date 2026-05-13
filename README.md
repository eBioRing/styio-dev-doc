# Styio Developer Manual / Styio 维护者手册

This repository backs two GitBook spaces. Do not sync GitBook from the repository root.

## GitBook sync roots

| GitBook space | Project directory | Entrypoints |
| --- | --- | --- |
| 简体中文 | `zh` | `zh/README.md`, `zh/SUMMARY.md` |
| English | `en` | `en/README.md`, `en/SUMMARY.md` |

## Maintenance

All GitBook content changes should stay under `zh/` or `en/`. Do not recreate a root `SUMMARY.md`; that mixes both languages into whichever GitBook space syncs the repository root.

Run the full gate before pushing:

```bash
./scripts/verify.sh
```
