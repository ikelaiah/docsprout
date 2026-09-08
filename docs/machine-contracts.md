# Machine-readable contracts

DocKit produces deterministic generated output for browsers and for tools.
This page documents which output is a public contract, and which parts are
deliberately **not** stable.

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
  "release": "0.18.1",
  "page_count": 23
}
```

### `versions.json` (build output, not the manifest)

Written at the root of a historical build by `build-all`. It mirrors the
configured `docs/versions.json` manifest:

```json
{
  "schema_version": 1,
  "current": "0.18.1",
  "versions": [
    {"release": "0.18.1", "source_ref": "v0.18.1"}
  ]
}
```

Do not confuse this output with the input manifest `docs/versions.json`,
which has the same versioned shape and is the release-history configuration.

### `dockit-fp audit --format json`

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

## The compatibility boundary

**Stable for 1.x:**

- documented configuration files and fields (`dockit.json`, `layout.json`,
  `versions.json` and their schema versions);
- CLI commands, options and their exit-code semantics;
- the documented `--dk-*` public token family;
- the custom CSS inclusion mechanism (`theme.custom_css`);
- generated routes and the machine formats above.

**Not stable (may change without notice):**

- every internal CSS selector and temporary class name;
- every DOM wrapper and exact HTML whitespace;
- private Python modules, classes and functions;
- exact human-readable CLI prose (commands and options are stable, sentences
  are not);
- the internal visual variables DocKit uses but does not document (for
  example radii, fonts, spacing scales and control heights), even when their
  names begin with `--dk-`.

## The Python API boundary

DocKit-FP is primarily a CLI/application package. `dockit_fp.__version__` is
public and may be used for version inspection. Everything else in the
`dockit_fp` package—modules, classes, functions, data structures—is an
implementation detail unless this documentation explicitly marks it public.
Do not import internal modules from your own tools; pin the `dockit-fp`
release and use the CLI and machine formats instead.

## External checks

`audit` never network-checks external URLs; the text report states this
explicitly. Machine-readable consumers should apply their own network policy.
