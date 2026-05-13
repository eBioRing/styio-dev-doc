# Vityo Collaboration Guide

This page describes the development consensus and collaboration guidance for the `Vityo` repository.

`Vityo` is Styio's dedicated IDE, runtime viewport, and AI collaboration frontend. Its goal is to provide an intuitive code authoring and execution experience.

## Evolution Stage

`Vityo` is currently in the **Architecture Bootstrap** stage. During this stage, prefer a **docs-first** collaboration model:

1. **Align specifications**: define product specifications, system architecture, and platform boundaries under `docs/` first.
2. **Capture consensus**: record major architecture decisions through ADRs.
3. **Implement in stages**: after specifications are frozen, develop UI and backend logic incrementally.

This model helps clarify complex platform strategies and cross-device interactions early.

## Core Responsibilities of `Vityo`

In ecosystem collaboration, `Vityo` focuses on:

- **Interaction engine**: dedicated editor engine, runtime visualization, and AI collaboration panels.
- **Theme and presentation**: visual system, UI component library, and theme extensions.
- **Execution routing**: adaptation logic for desktop, mobile, and cloud execution.
- **Module host**: dynamic loading and staged updates for functional modules.

## Decoupling Agreement

To preserve compiler semantic authority, `Vityo` and `styio` follow these agreements:

- **Interface-driven**: `Vityo` should consume standard public compiler interfaces such as token ranges, diagnostic payloads, and runtime event streams.
- **Semantics stay upstream**: core language semantics, including syntax decisions and type inference, are defined by `styio`. `Vityo` presents and interacts with those facts.
- **Smooth collaboration**: when the IDE needs deeper syntax analysis, extend the compiler-side IDE service interface instead of duplicating semantics in the frontend.

## Platform Execution Strategy

Because JIT and AOT constraints differ by platform, use this strategy as a baseline:

- **Desktop**: prefer local execution.
- **iOS**: prefer cloud execution as the main path.
- **Android**: support staged local execution adaptation.
- **Web**: focus on lightweight viewing and demonstration.

## Synchronization Rhythm for Syntax Updates

When `styio` introduces new syntax, adapt `Vityo` through these checks:

1. **Visual presentation**: update syntax highlighting and token classification.
2. **Assistive features**: synchronize snippets, completion hints, and hover information.
3. **Quality feedback**: improve diagnostic range placement for the new syntax.
4. **Navigation adaptation**: ensure the outline view recognizes the new syntax structure.

## Collaboration Summary

- **Docs first**: specifications and architecture should precede implementation.
- **Contract-based collaboration**: expose capabilities through `styio-protocol` and stable C ABI surfaces.
- **Escalate requirements upstream**: turn IDE capability gaps into compiler public service requirements.

## Continue Reading

- [Repository Matrix and Source Priority](repository-matrix.md)
- [Three-Repository Collaboration Guide](three-repository-collaboration.md)
- [Styio Core Collaboration Guide](styio-core-workflow.md)
