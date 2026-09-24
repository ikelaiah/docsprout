# Decision 0012: Brand hero and contrast-proven accent derivation

The home page opens with one designed hero, and one configured accent colour
becomes a complete, verified theme. Both decisions are visual: no schema field,
route, machine format or documented `--dk-*` token name changes.

## Context

Visitors compare documentation sites with Material for MkDocs and
Docusaurus/Starlight. Those tools reach landing-page quality only through MDX
components, custom HTML or multi-value palette configuration, and their
custom brand colours are the maintainer's accessibility problem. DocSprout
already promised offline assets, explicit configuration and honest diagnostics.

## Decision

- The home page renders a hero from the ordinary Markdown the project already
  has: the `h1`, the first paragraph and the optional release label. Two
  actions are derived rather than configured: **Get started** targets the first
  listed page that is not the home page, and **Repository** targets an http(s)
  `project.repository_url`. A configured banner renders as a full-width band
  at the top of the hero bundle. Capability cards gain decorative icons chosen
  from their titles.
  The backdrop, icons and hover lift are CSS and inline SVG, so a landing page
  needs no MDX, component framework or custom HTML.
- `theme.accent` alone is a complete theme. When `accent_secondary` is absent
  for an explicit accent, an analogous secondary is derived. For every visual
  style and colour mode, DocSprout computes `--dk-interactive` and
  `--dk-focus-ring` values that meet WCAG AA text contrast (4.5:1) and UI
  contrast (3:1) against the shipped reading surfaces, substituting a
  verification-safe variant only where the exact accent cannot pass. Filled
  actions use an internal `--dk-on-interactive` foreground.
- A failing light-page accent is reported, not hidden: `check` prints a note
  and `audit` adds warning `DK104`. Decorative surfaces continue to use the
  exact configured accent, and the documented token names and meanings stay
  the stable contract.

## Consequences

- Existing projects keep loading every schema-1 configuration; their generated
  look may improve, and a secondary is now derived for accent-only projects
  instead of inheriting an unrelated preset colour.
- Custom CSS keeps working: the documented tokens stay available, and the
  computed values only override their defaults.
- Contrast is proven at build time against the maintained surface constants,
  with a regression test keeping `palette.py` and `assets.py` in sync.
