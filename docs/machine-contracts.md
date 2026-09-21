# Machine-readable contracts

DocSprout produces deterministic generated output for browsers and for tools.
This page documents which output is a public contract, and which parts are
deliberately **not** stable.

## Schema-version-1 configuration

The following field families are the stable customisation contract for 1.x.
Every modern file starts with `"schema_version": 1`; unknown fields are
errors rather than silently ignored. Optional fields may be omitted to keep the
defaults.

| File/object | Stable fields |
| --- | --- |
| `docsprout.json` | `schema_version`, `project`, `theme`, `layout`, `banner`, `identity`, `homepage` |
| `project` | `name`, `description`, `repository_url`, `site_url` |
| `theme` | `preset`, `style`, `accent`, `accent_secondary`, `custom_css` |
| `layout` in `docsprout.json` | `content_width` (`compact`, `comfortable`, `wide`) |
| `banner` | `path`, `alt` |
| `identity` | `logo`, `footer`, `links` |
| `homepage` | `capabilities`, `sections` (`capabilities`, `banner`, `introduction`, `release_context`) |
| `layout.json` | `schema_version`, `home`, `unlisted`, `navigation` |
| page/section entries | `title`, `path`, `source`; section entries contain `pages` |
| `docs/versions.json` | `schema_version`, `current`, `versions` (`release`, `source_ref`) |

`source: "root"` is reserved for the exact repository-root `README.md`.
`theme.custom_css` and `identity.logo` must remain repository-local assets.
The configuration guide gives the editing examples and the validation
diagnostics for each field family.

## CLI contract

The stable command names are `init`, `serve`, `check`, `audit`, `build`,
`doctor`, `github-pages`, `check-release` and `build-all`. All accept
`--root`; the command-specific options are:

| Command | Options |
| --- | --- |
| `build` | `--output`, `--release`, `--offline-archive` |
| `build-all` | `--output` |
| `serve` | `--host`, `--port` |
| `audit` | `--strict`, `--format text\|json` |
| `github-pages` | `--update` |

Successful commands exit 0. A documentation or release validation error exits
1; `audit` uses exit 1 for errors (or strict warnings) and exit 0 for
non-strict warnings; invalid `audit` configuration exits 2. `--version` exits
0 and prints `docsprout <version>`. Argparse usage errors are the usual exit
2. Human-readable sentences may improve without being a compatibility change.

## Reusable workflow inputs

`.github/workflows/publish-docs.yml` is a reusable workflow with two stable
inputs: boolean `versioned` (default `true`) and string `release` (default
`preview`). Versioned builds require immutable `docs/versions.json` refs;
single-version builds use the `release` label. Caller workflows must pin a
released DocSprout tag, never `main`.

## Generated routes

Routes come from the listed Markdown path and the selected home page:

| Document | Route |
| --- | --- |
| The selected home document | `index.html` |
| `docs/index.md` when another document is home | `docs-index.html` |
| any other listed document | `path/with/suffix.html` |

Routes are collision-protected before any output is written. Two listed
documents whose routes would overwrite each other fail the build with an
actionable error. Case-insensitive collisions (`Foo.md` and `foo.md`) are
rejected too, because published sites are also served from case-insensitive
platforms.

## Machine-readable files

### `search-index.json`

The browser search reads this file. Versioned shape:

```json
{
  "schema_version": 1,
  "entries": [
    {
      "title": "Configuration",
      "section": "Shape your site",
      "url": "configuration.html",
      "text": "plain text used for ranking and previews"
    }
  ]
}
```

### `release.json`

Written by every single-release build. Versioned shape:

```json
{
  "schema_version": 1,
  "release": "1.0.0",
  "page_count": 23
}
```

### `versions.json` (build output, not the manifest)

Written at the root of a historical build by `build-all`. It mirrors the
configured `docs/versions.json` manifest:

```json
{
  "schema_version": 1,
  "current": "1.0.0",
  "versions": [
    {"release": "1.0.0", "source_ref": "v1.0.0"}
  ]
}
```

Do not confuse this output with the input manifest `docs/versions.json`,
which has the same versioned shape and is the release-history configuration.

### `docsprout audit --format json`

Deterministic CI-friendly diagnostics. Root fields:

```json
{
  "schema_version": 1,
  "pages": 23,
  "errors": 0,
  "warnings": 0,
  "findings": [
    {
      "code": "DK102",
      "severity": "warning",
      "file": "docs/architecture.md",
      "line": 12,
      "message": "Heading level jumps from H2 to H4",
      "target": "some-heading"
    }
  ]
}
```

`target` is present only when a finding names one. Findings are ordered
deterministically by page order, then source position.

## 1.x compatibility policy

Compatible additions are preferred within 1.x. A deprecation keeps the old
surface working for at least one minor release and is documented in the
changelog and migration guide before removal in the next major release. The
pre-rebrand aliases listed below are deprecated in v1.1.0 and are removed in
v2.0.0. Schema or machine-format changes require a new schema version and an
explicit migration path. A safety fix may reject behavior outside this
documented contract, with a regression test and migration guidance when user
action is needed.

## The compatibility boundary

**Stable for 1.x:**

- documented configuration files and fields (`docsprout.json`, `layout.json`,
  `versions.json` and their schema versions);
- the pre-rebrand `docs/dockit.json` filename, which keeps loading while both
  names never coexist silently;
- the deprecated `dockit-fp` console script and `python -m dockit_fp` module
  entry point;
- CLI commands, options and their exit-code semantics;
- the documented `--dk-*` public token family;
- the custom CSS inclusion mechanism (`theme.custom_css`);
- generated routes and the machine formats above.

The documented `--dk-*` names are the stable customisation contract. Internal
variables that happen to share the prefix are not included.

**Not stable (may change without notice):**

- every internal CSS selector and temporary class name;
- every DOM wrapper and exact HTML whitespace;
- private Python modules, classes and functions;
- exact human-readable CLI prose (commands and options are stable, sentences
  are not);
- the internal visual variables DocSprout uses but does not document (for
  example radii, fonts, spacing scales and control heights), even when their
  names begin with `--dk-`.

## The Python API boundary

DocSprout is primarily a CLI/application package. `docsprout.__version__` is
public and may be used for version inspection. Everything else in the
`docsprout` package—modules, classes, functions, data structures—is an
implementation detail unless this documentation explicitly marks it public.
Do not import internal modules from your own tools; pin the `docsprout`
release and use the CLI and machine formats instead.

## External checks

`audit` never network-checks external URLs; the text report states this
explicitly. Machine-readable consumers should apply their own network policy.
