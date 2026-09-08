# Migration

Migrate gradually from local `tools/build_docs.py`, `build_all_docs.py`,
`check_built_docs.py` and `tools/docs_assets/` copies:

1. Pin a released DocKit-FP version.
2. Add `dockit.json` and `layout.json` around the existing Markdown.
3. Reproduce and compare the current site.
4. Add and verify historical `versions.json` entries.
5. Switch the Pages workflow and run `check`, `check-release`, and `build-all`.
6. Delete the old local machinery only after output behaviour matches.

Do not rewrite historical tags or remove the old builder first.

## Configuration compatibility

DocKit-FP configuration is versioned deliberately. v0.5 supports
`"schema_version": 1` for `dockit.json`, `layout.json` and `versions.json`.
Version 1 additions are optional and remain backwards compatible: a project can
adopt presets, identity fields and visual themes one at a time.

Future schema versions will fail clearly rather than being guessed at. A major
schema change will ship with release notes, a migration guide, compatibility
expectations and—when mechanical conversion is safe—a migration command. Keep
each published release manifest on immutable tags while upgrading.

## Upgrade directly from any supported 0.x release

All released 0.x configurations use schema version 1. Upgrade the pinned package
and workflow to v0.18.1, then use this table before running `doctor`, `check`, and
the appropriate publish build.

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

For historical publication, v0.9.0 additionally rejects unsafe release path
segments and option-like refs, requires the current source to match `HEAD`, and
requires documentation changes to be committed. These checks make existing
valid manifests more dependable; they do not change generated routes.

## v0.17.0 to v0.18.0

v0.18.0 is the final pre-1.0 simplification and contract-candidate release.
Most projects need **no configuration change**; the changes below affect
machine consumers and advanced customisation only.

- **New:** optional `theme.custom_css` (repository-local `.css`, loaded after
  DocKit's styles). Adds a feature; existing sites are unchanged. See
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
  `dockit-fp audit --format json` now reports `"schema_version": 1` at the
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

No configuration change is required. `dockit-fp github-pages` prepares safe
Pages configuration and a pinned managed workflow in a Git repository,
without committing, pushing or changing repository settings.

## v0.14.0 to v0.15.0

No configuration change is required. `dockit-fp audit` reports read-only
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
in `layout.json`. Run `dockit-fp check`; add each reported path to an
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

## 0.x to 1.0 upgrade checklist

Version 1.0 is the formal commitment point for the contracts that v0.18
candidates. There is no 1.0 schema change pending. Before adopting 1.0:

1. Upgrade the pinned package and Pages workflow to the latest 1.x release
   following this migration guide's patterns (config-compatible, then
   rebuild).
2. Remove references to any pre-v0.18 generic theme token names
   (`--bg`, `--text`, `--interactive`, …) in custom CSS; the `--dk-*` names
   are the 1.x contract.
3. If a tool consumed the unversioned search-index array, switch it to the
   `{"schema_version": 1, "entries": [...]}` shape.
4. Run `dockit-fp check` and resolve every strict-field diagnostic: fields
   outside the released schema-1 surface are errors from v0.18 onward.
5. Keep `unlisted` and `home` explicit in `layout.json` where you author new
   layouts.
6. Re-run the quality gate: `dockit-fp check`, `dockit-fp audit --strict`,
   a local `serve` preview, and the historical `check-release` +
   `build-all` flow when `versions.json` is configured.
7. Verify the generated search index, `release.json`, audit JSON and version
   output still match your consumers after the first 1.x build.
