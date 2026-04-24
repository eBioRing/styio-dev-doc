# 审计、许可证与依赖合规

这页记录所有 Styio 相关仓库在开发时必须维护的审计输入。它不是法律意见；它是开发者交付前必须满足的工程门禁。

当前审计框架由 `styio-audit` 维护，并外部扫描这些项目：

- `styio` / 本地 `styio-nightly`
- `styio-spio`
- `styio-view`
- `styio-platform`
- `styio-audit`

`styio-dev-doc` 是开发者手册仓库。它负责记录流程和维护要求，不替代项目仓库自己的 `LICENSE`、`LICENSE-POLICY.md`、`DEPENDENCY-USAGE.md`、docs gate 或 audit gate。

## 许可证基线

Styio 相关源码项目当前统一使用 Apache License, Version 2.0。项目仓库必须能被审计框架证明为 `Apache-2.0`：

1. 顶层必须有 Apache-2.0 `LICENSE` 文件。
2. 如果存在 `pyproject.toml`、`package.json` 或 `pubspec.yaml`，许可证字段必须声明 `Apache-2.0`。
3. 顶层 `LICENSE-POLICY.md`、`NOTICE`、`NOTICE.md`、`README.md` 或 `docs/LICENSE-POLICY.md` 必须包含 Apache License Version 2.0 的 source-distribution notice。

Apache-2.0 不使用 GPL 式 copyleft 继承。开发者不能再把“基于 Styio 源码的衍生工具必须 GPL 开源”写成项目规则。正确边界是：当分发 Styio-family source 或 binary 时，必须保留 Apache-2.0 要求的 license、copyright、NOTICE、修改声明和 patent-license notice。

如果某个仓库仍出现 GPL-3.0 作为 Styio-family 主许可证，或者包元数据与 Apache-2.0 冲突，审计必须失败。

## Manifest 清单是阻塞输入

每个 `styio-audit` 项目模块都必须维护这些非空字段：

1. `technology_stack`
2. `internal_components`
3. `open_source_components`
4. `dependency_manifests`

缺任何一项都不能通过审计。原因很直接：没有技术栈、自研组件、开源组件和 manifest 清单，就无法判断许可证、商业授权、使用边界和 secret 扫描范围是否完整。

当新增或删除语言、SDK、运行时、构建系统、CI、包管理器、平台 runner、第一方模块、外部组件或依赖 manifest 时，必须同时更新：

1. 对应项目仓的 inventory 文档，例如 `docs/specs/TECHNOLOGY-COMPONENT-INVENTORY.md`。
2. `styio-audit` 里的对应 `for-styio*/module.json` 项目模块。
3. 项目仓的 docs index / docs audit 结果。

## 商业风险边界

Styio 项目不使用需要商业授权、付费许可证、订阅、会员制、trial-only、proprietary-use approval 或 private registry access 的依赖。

每个受审计仓库必须维护依赖使用边界文件，优先使用：

1. `DEPENDENCY-USAGE.md`
2. `THIRD-PARTY-NOTICES.md`
3. `docs/DEPENDENCY-USAGE.md`
4. `docs/dependencies.md`
5. `docs/third-party.md`

依赖使用边界至少要说明：

1. 当前依赖来自哪些 manifest。
2. 每个外部组件的使用范围是 runtime、build、test、fixture、prototype 还是 docs tooling。
3. 是否存在商业授权、订阅、会员制、trial-only 或 proprietary-use 风险。
4. 新依赖进入生产使用前要补什么 license evidence 和 usage boundary。

如果 manifest 里出现 commercial license、subscription、membership、trial license、evaluation only、proprietary、商业授权、会员制等风险词，审计必须失败，直到维护者记录可接受的开源许可证证据和明确使用边界。

## Secret 扫描

审计框架会扫描当前工作树中的敏感信息，包括：

- password
- token
- API key
- private key
- client secret
- access key

开发者不能把疑似 secret 值写进文档、日志、测试 fixture 或审计报告。发现问题时，只能记录 rule id、文件位置、fingerprint、长度、first/last commit 等脱敏信息。

需要扫提交历史时，使用：

```bash
python3 -m styio_audit.cli secret-history --repo /path/to/repo --project <project> --format json
```

如果历史中出现真实 secret，不能只改最新文件；必须按项目安全流程轮换凭据、记录影响范围，并决定是否需要历史清理。

## 开发者改动流程

涉及许可证、依赖、技术栈、外部组件或审计规则时，按这个顺序做：

1. 先确认改动属于哪个仓库，别把跨仓规则写进单仓实现细节。
2. 更新项目仓自己的 `LICENSE`、`LICENSE-POLICY.md`、`DEPENDENCY-USAGE.md` 和 inventory 文档。
3. 更新 `styio-audit` 的默认模块或项目模块。
4. 跑 `styio-audit` 的模块校验和单元测试。
5. 对目标仓库跑 `styio-audit gate --framework-only`。
6. 跑目标仓库自己的 docs index、docs audit、repo hygiene 和受影响测试。
7. 推送后检查 GitHub Actions，不能只停在本地通过。

常用命令：

```bash
cd /home/unka/styio-audit
python3 -m unittest discover -s tests -v
python3 -m styio_audit.cli validate-modules
python3 -m styio_audit.cli gate --repo . --project styio-audit --framework-only
python3 -m styio_audit.cli gate --repo /home/unka/styio-nightly --project styio --framework-only
python3 -m styio_audit.cli gate --repo /home/unka/styio-spio --project styio-spio --framework-only
python3 -m styio_audit.cli gate --repo /home/unka/styio-view --project styio-view --framework-only
python3 -m styio_audit.cli gate --repo /home/unka/styio-platform --project styio-platform --framework-only
```

项目仓文档门禁通常是：

```bash
python3 scripts/docs-index.py --write
python3 scripts/docs-audit.py
python3 scripts/repo-hygiene-gate.py --mode tracked
```

## 不能通过审计的典型情况

- 没有 `LICENSE` 或许可证文本不是 Apache-2.0。
- 包元数据声明 GPL、proprietary 或与 Apache-2.0 冲突的许可证。
- 没有 source-distribution notice。
- 项目模块缺 `technology_stack`、`internal_components`、`open_source_components` 或 `dependency_manifests`。
- 新依赖没有 usage boundary。
- 依赖 manifest 出现商业授权、会员制、trial-only 或 proprietary-use 风险词。
- 当前工作树或提交历史混入 password、token、API key、private key、client secret 或 access key。
- 只更新 `styio-dev-doc`，但没有同步项目仓真实 docs/gate 证据。

## 继续阅读

- [仓库矩阵与来源优先级](../ecosystem/repository-matrix.md)
- [三仓库协作流程](../ecosystem/three-repository-collaboration.md)
- [文档与 SSOT 规则](documentation-and-ssot.md)
