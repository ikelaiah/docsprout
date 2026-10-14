# Build and inspect your site

`docsprout serve` is the fastest way to read your site while writing. Use
`docsprout build` when you want the static files: a folder you can archive,
upload to any static host, or inspect without the preview server.

## Build once

```bash
docsprout build
```

The build validates the configuration first, then writes the complete site to
`build/docs-site` and prints the page count. The output is offline-ready: every
asset is local, and `index.html` opens directly in a browser.

Search loads a local JSON index, which browsers may block for pages opened
directly from disk. Use `docsprout serve`, or [serve the built folder
locally](troubleshooting.md#search-says-search-is-unavailable), for working
search without an internet connection.

Single-site builds prepare their files beside the output folder and replace it
only after rendering succeeds. If a link, configuration or rendering error
stops a rebuild, the previous site stays available. A first build that fails
does not leave a partial site. This also keeps a working `serve` preview
readable while you fix the source.

The preview watches `README.md`, `docs/`, and the configured logo, banner and
custom stylesheet even when those assets live elsewhere in the repository.

| Option | Effect |
| --- | --- |
| `--output <folder>` | Write somewhere else, such as `dist/site`. DocSprout marks generated folders with `.docsprout-site` and refuses to replace a folder it does not own. |
| `--release <name>` | Set the release label shown on the home page. Without `docs/versions.json`, the default label is `preview`; with a manifest, the default is its `current` release. |
| `--root <folder>` | Build a project in another folder instead of the current one. Every command accepts `--root`; the maintained [visual fixture](visual-fixtures.md) uses it in its build recipe. |
| `--offline-archive <file.zip>` | Also write a deterministic ZIP of the site plus a `.sha256` sidecar file. |

## Ship a ZIP

```bash
docsprout build --release 1.4.0 --offline-archive dist/docsprout-docs-1.4.0.zip
```

The release label used for an offline archive must start with a letter or
number and otherwise contain only letters, numbers, dots, underscores or
hyphens. The archive stores the built pages under `docsprout-docs-<release>/`
with fixed metadata, so building the same content twice produces byte-identical files. The
ownership marker is not included. The sidecar `...zip.sha256` records the
digest for verification.

## Build every release

When `docs/versions.json` exists, `docsprout build-all` builds the current
documentation and every declared historical release into one site, each under
its own path. The [historical documentation guide](historical-docs.md) covers
the release order, and `docsprout check-release` validates the manifest first.

`build-all` stages the complete versioned site and replaces its output only
after every release succeeds. If any historical release fails to build, the
previous complete site remains available.

## Start with `doctor`

`docsprout doctor` inspects the project without changing files. Its output is a
plain list:

- `Project root:` the folder being inspected;
- `Documentation:` modern configuration with a page count, or legacy discovery;
- `WARNING:` advisory lines, such as a legacy `docs/dockit.json` filename;
- `Versions:` either a manifest summary with `Status: versioned release
  configured`, or `no versions.json (single-release preview only)`,
  `Status: preview-ready`;
- `Release refs:` verification that each tag or SHA resolves; the current
  release must also match `HEAD`;
- `GitHub Pages workflow:` or `Pages:` the managed workflow state, an update
  hint, or a note that no DocSprout workflow was detected;
- `ERROR:` blocking problems. The command exits `1` when any appears.

Use it before `serve`, `build` or `github-pages` to confirm the shape of the
project. The [troubleshooting guide](troubleshooting.md) maps its messages to
fixes.

## Fix the most likely failures

- The output folder exists and is not owned by DocSprout:
  [Build and output](troubleshooting.md#build-and-output).
- A link or heading anchor fails validation:
  [Audit your documentation](audit.md).
