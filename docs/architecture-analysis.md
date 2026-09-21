# Architectural analysis

This page records the cross-project analysis that led to extracting DocSprout
from the ecosystem's library sites. It is maintainer history, not adoption
guidance: start with [Architecture](architecture.md) for the current design and
[Machine-readable contracts](machine-contracts.md) for the stable surface.

DocSprout is the shared static-site layer for the Free Pascal ecosystem. It
renders project-owned Markdown into a documentation site; it does not parse
Pascal source or extract API declarations.

## Reference comparison

| Repository | Reusable findings | Project-specific findings |
| --- | --- | --- |
| ChronoKit-FP | Markdown rendering, version manifest, detached-worktree historical builds, release checks, CSS/JS shell | ChronoKit pages, banner, date/time release policy and API generation scripts |
| StringKit-FP | Structured `layout.json`, homepage cards/banner, navigation, search, release builds and checks | StringKit navigation/content and teal identity |
| ThreadSafeCollections-FP | Most complete legacy fallback, link/anchor validation, page navigation, deterministic offline archive | Collection guides, purple identity, collection-specific release metadata |
| MathLib-FP | Compact renderer, layout aliases, offline ZIP plus SHA-256, release-qualified output | Math layout conventions, mathematical documentation and qualification tooling |
| PasWeave | Accessible responsive output, search, System/Light/Dark persistence, output manifests and safe incremental-build ideas | Pascal parsing, symbols, documentation directives, API coverage and source traceability |

The four library sites each have their own `build_docs.py`, historical-build
script, validation scripts, site CSS and browser JavaScript. Their file hashes
and sizes differ, demonstrating real divergence rather than a shared component.

## Deliberate extraction boundary

DocSprout centralises Markdown rendering, routing, modern/legacy navigation,
version manifests, immutable-ref builds, validation, generated CSS/JS, search,
themes, offline bundles and Pages integration. A consuming repository keeps
Markdown, its navigation/manifest, branding tokens, banner and Git tags.

PasWeave stays upstream of this boundary. It may emit Markdown that DocSprout
renders alongside handwritten pages, but neither tool depends on the other.

## v0.1 decisions

- Python 3.10+ and the standard library only; this keeps CI and Windows support simple.
- Strict, explicit JSON schema-version validation for modern configuration; legacy trees need only Markdown.
- Published `build-all` materialises every declared release from its `source_ref` with `git archive`, never the current tree.
- Output replacement is allowed only for a directory containing DocSprout's ownership marker.
- Markdown supports the stated safe subset and escapes source text; raw HTML is rendered as text.
- One semantic-token design system owns structure. Projects configure accent colours and optional SVG banners without custom structural CSS.
