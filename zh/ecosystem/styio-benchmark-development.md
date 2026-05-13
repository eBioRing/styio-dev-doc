# styio-benchmark 开发与维护指引

这页负责明确 `styio-benchmark`（基准测试与性能追踪）的开发流程。

Styio 对性能的要求极其苛刻。`styio-benchmark` 作为一个独立仓库，目的是将“性能评估”与“功能正确性测试（tests/）”解耦，建立严格的对照基线。

## 核心职责

`styio-benchmark` 负责：

- **编译器吞吐量 (Compiler Throughput)**：测量 Tokenizer、Parser、Analyzer 阶段的耗时。
- **运行时执行速度 (Runtime Execution Speed)**：测量 JIT 执行或编译后二进制的运行效率。
- **内存水位 (Memory Profiling)**：监控编译期和运行期的峰值内存占用。
- **基线与衰退告警 (Baseline & Regression)**：维护历史性能基线，阻断导致性能严重劣化的 PR。

## 与主仓库 (`styio`) 的关系

- `styio` 的 `tests/` 目录负责“算得对不对”。
- `styio-benchmark` 负责“算得快不快、省不省”。
- 每次主仓合并到 `nightly` 前，必须触发 benchmark 仓库的回归检测。

## 维护原则

1. **环境绝对隔离**：基准测试必须在标准化的云环境或严格限制 CPU 调度的裸机上运行，禁止在“开发者自己的笔记本”上截取数据作为最终定论。
2. **统计学置信**：单次运行的数据是无效的，必须采用多次采样、去除噪点后的统计学分布结果（如 P90/P99 耗时）。
3. **真实世界语料 (Real-world Corpus)**：基准测试不能只依赖微基准（Micro-benchmarks，如空循环），必须包含规模足够大的真实 Styio 工程项目。

## 继续阅读

- [测试金字塔与 Case 选型手册](../runbooks/testing-pyramid-and-case-selection.md)
- [仓库矩阵与来源优先级](repository-matrix.md)
