# styio-benchmark Development and Maintenance Guide

This page defines the development process for `styio-benchmark`, the benchmark and performance-tracking repository.

Styio has strict performance requirements. `styio-benchmark` exists as a separate repository to decouple performance evaluation from functional correctness tests under `tests/`, and to maintain rigorous comparison baselines.

## Core Responsibilities

`styio-benchmark` owns:

- **Compiler throughput**: measures the time spent in Tokenizer, Parser, and Analyzer stages.
- **Runtime execution speed**: measures JIT execution or compiled binary performance.
- **Memory profiling**: tracks peak memory usage during compilation and runtime.
- **Baseline and regression alerts**: maintains historical performance baselines and blocks PRs that cause severe regressions.

## Relationship to the Main `styio` Repository

- `styio/tests/` answers whether the compiler computes the right result.
- `styio-benchmark` answers whether it computes quickly and efficiently.
- Before the main repository merges into `nightly`, benchmark regressions must be triggered.

## Maintenance Principles

1. **Strict environment isolation**: benchmarks must run in standardized cloud environments or tightly controlled bare-metal environments. Do not use measurements from a developer laptop as final evidence.
2. **Statistical confidence**: a single run is not valid. Use repeated samples and noise-reduced distributions such as P90 / P99 timings.
3. **Real-world corpus**: benchmarks must not rely only on micro-benchmarks such as empty loops. They must include sufficiently large real Styio projects.

## Continue Reading

- [Testing Pyramid and Case Selection Runbook](../runbooks/testing-pyramid-and-case-selection.md)
- [Repository Matrix and Source Priority](repository-matrix.md)
