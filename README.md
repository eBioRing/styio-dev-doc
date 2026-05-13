# Styio Developer Manual / Styio 维护者手册

This repository backs two GitBook spaces. Do not sync GitBook from the repository root.

## GitBook sync roots

| GitBook space | Project directory | Config | Entrypoints |
| --- | --- | --- | --- |
| 简体中文 | `zh` | `zh/.gitbook.yaml` | `zh/README.md`, `zh/SUMMARY.md` |
| English | `en` | `en/.gitbook.yaml` | `en/README.md`, `en/SUMMARY.md` |

## Maintenance

All GitBook content changes should stay under `zh/` or `en/`. Do not recreate a root `SUMMARY.md`; that mixes both languages into whichever GitBook space syncs the repository root.

GitBook configuration must stay in each Project directory as `.gitbook.yaml`; do not add `gitbook.yaml`, `.gitbook.yml`, or a root-level GitBook config.

Run the full gate before pushing:

```bash
./scripts/verify.sh
```
