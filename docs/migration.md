# Migration

The 1.x upgrades are deliberately boring: v1.0.0 froze the qualified v0.18.1
surface, and every later 1.x release adds no configuration schema change. Pin
the released package and workflow, then run the same checks you already use.
Current guidance targets `v1.1.5`; each section below remains authoritative for
its own step.

## DocKit to DocSprout (1.x rebrand)

DocSprout is the new name for the builder released through v1.0.0 as
DocKit-FP. The 1.x contract is preserved, so this is a branding and
configuration-name transition, not a schema migration:

- `docsprout` is the canonical command; `python -m docsprout` is the canonical
  module entry point. The deprecated `dockit-fp` console script and
  `python -m dockit_fp` module keep working for at least one minor release.
- New projects create `docs/docsprout.json`. Existing `docs/dockit.json`
  files keep loading unchanged. If both files exist, DocSprout fails with an
  actionable ambiguity error instead of choosing one silently; rename the
  legacy file to `docsprout.json` and delete the old name.
- Generated output now uses the `.docsprout-site` ownership marker. Rebuilding
  a directory that carries the old `.dockit-fp-site` marker recognises it,
  replaces the directory, and writes the new marker.
- Fresh GitHub Pages setup creates
  `.github/workflows/docsprout-pages.yml`. An existing managed
  `.github/workflows/dockit-pages.yml` is recognised; `docsprout github-pages
  --update` updates it in place, so a repository never ends up with two
  deployment workflows. Unmanaged workflow files are never overwritten.
- Browser theme preferences migrate automatically from the old
  `dockit-fp-theme` and `dockit-fp-visual-theme` storage keys to the new
  `docsprout-theme` and `docsprout-visual-theme` keys.
- The public `--dk-*` CSS custom-property names are unchanged, as are routes,
  JSON schemas, configuration field names and command behaviour unrelated to
  the rebrand. [Troubleshooting](troubleshooting.md) lists the exact messages
  and fixes for the transition.

Migrate gradually from local `tools/build_docs.py`, `build_all_docs.py`,
`check_built_docs.py` and `tools/docs_assets/` copies:

1. Pin a released DocSprout version.
2. Add `docsprout.json` and `layout.json` around the existing Markdown.
3. Reproduce and compare the current site.
4. Add and verify historical `versions.json` entries.
5. Switch the Pages workflow and run `check`, `check-release`, and `build-all`.
6. Delete the old local machinery only after output behaviour matches.

Do not rewrite historical tags or remove the old builder first.

## Configuration compatibility

DocSprout configuration is versioned deliberately. v0.5 supports
`"schema_version": 1` for the configuration file (released then as
`dockit.json` and now named `docsprout.json`), `layout.json` and
`versions.json`. Version 1 additions are optional and remain backwards
compatible: a project can adopt presets, identity fields and visual themes one
at a time.

Future schema versions will fail clearly rather than being guessed at. A major
schema change will ship with release notes, a migration guide, compatibility
expectations and—when mechanical conversion is safe—a migration command. Keep
each published release manifest on immutable tags while upgrading.

## Upgrade directly from any supported 0.x release

All released 0.x configurations use schema version 1. Upgrade the pinned package
and workflow to the latest 1.x release (`v1.1.5`), then use this table before
running `doctor`, `check`, and the appropriate publish build.

| Starting release | Required compatibility work |
| --- | --- |
| v0.1.0 | For modern configuration, list every Markdown file in `layout.json`; keep legacy config-free documentation as-is. |
| v0.2.0 | List every modern Markdown file in navigation; existing project colours remain valid. |
| v0.3.0 | List every modern Markdown file in navigation; identity and preset fields remain valid. |
| v0.4.0 | List every modern Markdown file in navigation; Classic, Paper and Midnight names remain valid. |
| v0.5.0 | List every modern Markdown file in navigation; task lists and schema-version-1 files remain valid. |
| v0.6.0 | List every modern Markdown file in navigation; homepage settings remain optional and compatible. |
| v0.7.0, v0.7.1 or v0.7.2 | No configuration change is required. Keep immutable historical tags. |
| v0.8.0 | No configuration change is required; `layout.content_width` remains optional. |
| v0.9.0 | No configuration change is required; v0.9.1 improves guides and examples. |
| v0.9.1 | No configuration change is required; v0.9.2 keeps wrapped list items and callouts together. |
| v0.9.2 | No configuration change is required; v0.10.0 adds offline syntax highlighting. |
| v0.10.0 | No configuration change is required; v0.11.0 adds existing-repository adoption and `serve`. |
| v0.11.x | No configuration change is required; `"unlisted": "exclude"` is optional and newly generated layouts use it. |
| v0.12.x | No configuration change is required; `identity.logo` and `identity.footer`/`links` are optional. |
| v0.13.0 | No configuration change is required; `layout.json.home` is optional but recommended for new layouts. |
| v0.14.0 | No configuration change is required; `github-pages` adds the managed workflow. |
| v0.15.0 | No configuration change is required; `audit` is read-only and optional. |
| v0.16.x | No configuration change is required; v0.16 aligned guides and examples on explicit `home` and `unlisted`. |
| v0.17.0 | No configuration change is required; v0.17 qualified the supported matrix. |
| v0.18.0 | No configuration change is required; optional `theme.custom_css` and the `--dk-*` token names are documented. |
| v0.18.1 | No configuration change is required; ordinary images now shrink to the prose column by default. |

For historical publication, v0.9.0 additionally rejects unsafe release path
segments and option-like refs, requires the current source to match `HEAD`, and
requires documentation changes to be committed. These checks make existing
valid manifests more dependable; they do not change generated routes.

## v1.1.4 to v1.1.5

No configuration change is required. Update the package archive or source pin
and any caller workflow pin to `v1.1.5`. The sidebar release groups section
pages into collapsible subgroups: a section's `pages` entry now accepts either
`"path"` for a directly listed page or `"pages"` for a subgroup with one level
of child pages, with an optional boolean `"expanded"` to keep a group open on
every page. Existing flat layouts load unchanged and all routes are preserved.
The Markdown renderer additionally covers blockquotes (`> quote`),
strikethrough (`~~deleted~~`) and horizontal rules (`---` on its own line).
Capability cards keep the border highlight on hover without the inset top
eyebrow.

## v1.1.3 to v1.1.4

No configuration change is required, but review the built result once: update
the package archive or source pin and any caller workflow pin to `v1.1.4`. The
brand-hero release gives the home page one designed hero built from the same
Markdown, derives **Get started** and **Repository** actions and decorative
card icons, and renders a configured banner as hero artwork. Link and focus
colours are computed from `theme.accent` and proven against every reading
surface; when an explicit accent has no `accent_secondary`, an analogous
secondary is derived instead of inheriting the preset colour. A failing light
accent is reported by `check` and `audit` (`DK104`) while the built site uses a
verification-safe link colour. The documented `--dk-*` token names are
unchanged.

## v1.1.2 to v1.1.3

No configuration change is required. Update the package archive or source pin
and any caller workflow pin to `v1.1.3`. This patch changes documentation and
its regression tests only: the guides now demonstrate the home-page banner,
require referenced assets to exist before building, cover common configuration
and Markdown errors, document `docsprout build` options, offline archives,
`--root` and `doctor`, and add the navigation, theme and command vocabulary to
the glossary.

## v1.1.1 to v1.1.2

No configuration change is required. Update the package archive or source pin
and any caller workflow pin to `v1.1.2`. The typography release changes
presentation only: cross-platform system font stacks, a complete heading and
outline scale, running-text typography, a print stylesheet and typographic
punctuation in prose. Markdown that relied on literal `--`, `---`, `...` or
straight quotes in prose now renders them as en dash, em dash, ellipsis and
curly quotes; put those characters in a code span when they must stay exact.
Repeated headings now receive unique `-2`, `-3` anchor suffixes.

## v1.1.0 to v1.1.1

No configuration change is required. Update the package archive or source pin
and any caller workflow pin to `v1.1.1`. The patch adds the legacy-configuration
guidance fix, a troubleshooting guide, repository health files, a dev-only
`ruff` lint gate, and a byte-identical refactor of the document template.

## v1.0.0 to v1.1.0

The rebrand release. There is no configuration or schema migration and no
generated-route change:

1. Update the package archive or source installation pin to `v1.1.0`.
2. Update caller workflows to `publish-docs.yml@v1.1.0`, or run
   `docsprout github-pages --update` where a managed caller already exists.
3. Optionally rename `docs/dockit.json` to `docs/docsprout.json`. Never keep
   both names: the ambiguity is an error.
4. Keep using `docsprout`, or migrate away from the deprecated `dockit-fp` and
   `python -m dockit_fp` aliases before v2.0.0 removes them.

## v0.17.0 to v0.18.0

v0.18.0 is the final pre-1.0 simplification and contract-candidate release.
Most projects need **no configuration change**; the changes below affect
machine consumers and advanced customisation only.

- **New:** optional `theme.custom_css` (repository-local `.css`, loaded after
  DocSprout's styles). Adds a feature; existing sites are unchanged. See
  [Custom CSS](custom-css.md).
- **Renamed tokens (pre-1.0):** the generic semantic colour tokens are now
  namespaced. `--bg`, `--surface`, `--text`, `--muted`, `--border`, `--code`,
  `--code-text`, `--raised`, `--focus-ring` and `--interactive` became
  `--dk-bg`, `--dk-surface`, `--dk-text`, `--dk-muted`, `--dk-border`,
  `--dk-code-bg`, `--dk-code-text`, `--dk-raised`, `--dk-focus-ring` and
  `--dk-interactive`. If you referenced the old names in a custom stylesheet,
  rename them. The generated site consumers (themes and modes) were updated
  internally; no project configuration references these names.
- **Versioned machine formats:** `search-index.json` is now
  `{"schema_version": 1, "entries": [...]}`, and
  `docsprout audit --format json` now reports `"schema_version": 1` at the
  root. `release.json` and built-site `versions.json` were already versioned.
  Tools that consumed the old unversioned search-index array must read
  `entries`.
- **Stricter diagnostics:** fields that were never part of a released
  schema-1 configuration are now rejected with a `Did you mean` suggestion.
  A previously silent typo such as `"presett"` now fails `check`. Valid
  configuration from every supported release keeps loading (verified by the
  automated compatibility corpus).
- **Route protection:** if two listed documents would generate the same
  route (for example `docs/index.md` and `docs/docs-index.md` when another
  page is home, or case-only filename differences), the build now fails with
  an actionable error instead of silently overwriting output. Rename or move
  one of the documents.

## v0.18.0 to v0.18.1

No configuration change is required. Ordinary Markdown images now shrink to
the prose column by default while smaller images retain their intrinsic size;
configured banners and existing custom CSS behavior remain compatible.

## v0.18.1 to v1.0.0

No configuration migration is required. v1.0.0 is the stable commitment to
the contract qualified by v0.18.1:

1. Pin the package archive or source installation to `v1.0.0` and pin the
   reusable Pages workflow to `@v1.0.0`; never use `main`. For a new upgrade
   today, pin the latest 1.x release (`v1.1.5`) instead.
2. Keep `"schema_version": 1` in `docsprout.json`, `layout.json` and
   `versions.json`. There is no schema rewrite or generated-route migration.
3. If custom CSS still uses pre-v0.18 generic names such as `--bg`, `--text`
   or `--interactive`, rename them to their documented `--dk-*` equivalents.
4. Machine consumers must use the schema-1 `search-index.json`, `release.json`,
   built `versions.json` and `audit --format json` shapes documented in
   [Machine-readable contracts](machine-contracts.md).
5. Run `doctor`, `check`, `audit --strict`, a local `serve` preview, and the
   historical `check-release` + `build-all` flow when version history is used.

The v1.x policy is additive within the major release. Deprecations remain
available for at least one minor release and are documented before removal in a
future major release; schema or machine-format changes require a new schema
version and migration guidance.

## v0.10.0 to v0.11.0

Modern documentation trees can adopt the optional
`"unlisted": "exclude"` publication policy; existing layouts keep strict
validation. `init` becomes safe existing-repository adoption: it discovers a
root README and Markdown under `docs/` without modifying either, and derived
layouts are maintainer-owned. `serve` provides a validated localhost preview.

## v0.11.0 to v0.12.0

No configuration change is required. Adopt the optional `identity.logo`
(repository-local SVG or PNG), refined homepage presentation and preview
rebuilds when convenient.

## v0.12.0 to v0.13.0

No configuration change is required. The top-level `layout.json.home` object
selects the published home page explicitly, including the repository-root
`README.md` with `"source": "root"`. Existing layouts without `home` keep the
established fallback (root README, then `docs/index.md`, then the first
listed page).

## v0.13.0 to v0.14.0

No configuration change is required. `docsprout github-pages` prepares safe
Pages configuration and a pinned managed workflow in a Git repository,
without committing, pushing or changing repository settings.

## v0.14.0 to v0.15.0

No configuration change is required. `docsprout audit` reports read-only
publication diagnostics; `audit --strict` is the CI-warning gate option.
`check` remains the buildability gate.

## v0.15.0 to v0.16.0

No configuration change is required. v0.16 aligned the beginner path, guides
and maintained examples on the explicit `home` and `"unlisted": "exclude"`
contract; newly generated layouts already used those values.

## v0.16.x to v0.17.0

No configuration change is required. v0.17 qualified Python 3.10–3.14 on
Linux, representative Windows/macOS, package forms, the CLI journey and
generated-site accessibility fundamentals; see
[Qualification evidence](qualification.md).

## The remaining 0.x sections

The v0.5.0 to v0.10.0 sections below remain authoritative for their own
steps, unchanged by later releases.

## v0.5.0 to v0.6.0

No migration is required. Existing homepages retain their v0.5.0 output.
Adopt the optional `homepage` object only when you want to replace capability
cards or control homepage sections.

## v0.6.0 to v0.7.0

Modern documentation trees now require every `docs/**/*.md` file to be listed
in `layout.json`. Run `docsprout check`; add each reported path to an
appropriate section, or remove documentation that should no longer ship.
Existing Markdown rendering remains compatible, and definition lists are an
optional authoring feature.

## v0.7.0 to v0.7.1

No migration is required. v0.7.1 restores successful `build-all` publication
when an immutable historical tag contains modern documentation authored before
v0.7.0's strict navigation-completeness check. Current documentation remains
subject to that check.

## v0.7.1 to v0.7.2

No migration is required. When the Classic visual theme is selected, System
colour mode now follows a dark operating-system preference as documented.

## v0.7.2 to v0.8.0

No migration is required. Existing sites retain the comfortable content width.
Adopt the optional `layout.content_width` setting only when a compact tutorial
or wide reference layout better suits the documentation. Theme polish applies
through the existing semantic token contract and requires no CSS copies.

## v0.8.0 to v0.9.0

Existing versioned workflow callers remain in historical mode by default. The
new `versioned: false` input is only for single-version sites. Update workflow
action pins by consuming the v0.9.0 reusable workflow, run `doctor`, and resolve
any newly reported missing tag, mismatched `HEAD`, uncommitted docs or moving
workflow ref before publication.

## v0.9.0 to v0.9.1

No configuration change is required. Update package and workflow pins to
v0.9.1. The generated site and release validation remain compatible; this
patch release makes the learning and publishing instructions easier to follow.

## v0.9.1 to v0.9.2

No configuration change is required. Update package and workflow pins to
v0.9.2, then rebuild the site. Wrapped list-item text and multi-line
GitHub-style callouts now render as one readable component.

## v0.9.2 to v0.10.0

No configuration change is required. Update package and workflow pins to
v0.10.0, then rebuild the site. Fenced JSON, Pascal, Python, Bash, YAML and
Markdown blocks receive local syntax highlighting; other fence languages stay
safe, readable plain code.

## 0.x to 1.x upgrade checklist

Version 1.0 is the formal commitment point for the contracts that v0.18.1
qualified, and later 1.x releases keep that contract. There is no schema change.
Before adopting the latest 1.x release (`v1.1.5`):

1. Upgrade the pinned package and Pages workflow to `v1.1.5` following this
   guide's patterns (config-compatible, then rebuild).
2. Remove references to any pre-v0.18 generic theme token names
   (`--bg`, `--text`, `--interactive`, …) in custom CSS; the `--dk-*` names
   are the 1.x contract.
3. If a tool consumed the unversioned search-index array, switch it to the
   `{"schema_version": 1, "entries": [...]}` shape.
4. Run `docsprout check` and resolve every strict-field diagnostic: fields
   outside the released schema-1 surface are errors from v0.18 onward.
5. Keep `unlisted` and `home` explicit in `layout.json` where you author new
   layouts.
6. Re-run the quality gate: `docsprout check`, `docsprout audit --strict`,
   a local `serve` preview, and the historical `check-release` +
   `build-all` flow when `versions.json` is configured.
7. Verify the generated search index, `release.json`, audit JSON and version
   output still match your consumers after the first 1.x build.
