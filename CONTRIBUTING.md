# Contributing

DocSprout supports Python 3.10–3.14 on Linux, with the minimum and latest stable
versions qualified on Windows and macOS. Python 3.15 pre-release runs as a
non-blocking forward-compatibility signal, not as a support commitment.

Install the local checkout and run the complete suite before proposing a
change:

```powershell
python -m pip install -e ".[dev]"
python -m unittest discover -s tests -t . -v
ruff check .
```

Keep changes dependency-free unless there is a documented reason otherwise.
Changes to CLI options, JSON schemas, generated paths, theme token names,
search-index format, audit JSON, route behavior or reusable-workflow inputs are
compatibility changes. They need a regression test, an accompanying
documentation/migration update, and review against
[Machine-readable contracts](docs/machine-contracts.md).

For documentation changes, also run:

```powershell
docsprout check
docsprout audit --strict
docsprout build --output build/docs-site
```

## Code map

| Module | Responsibility | Main tests |
| --- | --- | --- |
| `docsprout/cli.py` | command surface and `init`/`serve`/`doctor` orchestration | `test_cli`, `test_qualification_cli` |
| `docsprout/config.py` | configuration discovery, validation and the legacy `dockit.json` filename | `test_config`, `test_compatibility_corpus` |
| `docsprout/build.py` | page rendering, routes, assets and the search index | `test_build`, `test_route_collisions` |
| `docsprout/markdown.py` | safe Markdown subset and heading slugs | `test_markdown` |
| `docsprout/layout_markdown.py` | Markdown navigation outlines and line-specific diagnostics | `test_layout_markdown` |
| `docsprout/palette.py` | derived colours and contrast checks | `test_palette` |
| `docsprout/highlight.py` | offline syntax highlighting | `test_markdown` |
| `docsprout/audit.py` | read-only publication diagnostics | `test_audit` |
| `docsprout/github_pages.py` | managed Pages workflow rendering and inspection | `test_github_pages`, `test_github_pages_cli` |
| `docsprout/safety.py` | owned-output markers and replacement | `test_safety` |
| `docsprout/versions.py` | version manifests, `check-release` and `build-all` | `test_versions`, `test_custom_css` |
| `docsprout/discovery.py` | read-only repository discovery | `test_cli`, `test_qualification_ecosystem` |
| `docsprout/archive.py` | deterministic offline ZIP output | `test_archive` |
| `docsprout/assets.py` | shared CSS and browser JavaScript | `test_accessibility`, `test_custom_css` |
| `docsprout/models.py` | configuration data models | `test_route_collisions` |
| `docsprout/errors.py` | error type and the deprecated `DocKitError` alias | `test_rebrand_compatibility` |

`tests/helper.py` runs the CLI in a subprocess; `tests/qualification_installed.py`
and `tests/qualification_artifacts.py` verify packaged installs and archives.
Preview documentation changes with `docsprout serve`, and follow
[Troubleshooting](docs/troubleshooting.md) when a command reports an error.

## Make a small, verifiable improvement

For a renderer change, start with a failing example and run the focused tests:

```powershell
python -m unittest tests.test_markdown tests.test_inline_contexts -v
```

Keep raw Markdown, generated HTML and HTML attributes separate. Add cases for
quotes, code, math, image descriptions and link targets when changing inline
syntax. The [rendering boundary](docs/architecture.md#keep-rendering-contexts-separate)
explains why those combinations matter.

For a browser change, build `examples/visual-fixtures` and follow the
[visual inspection matrix](docs/visual-fixtures.md). Exercise a phone width,
keyboard navigation, light and dark modes, and the relevant empty or error
state. Generated-string assertions cannot prove that scrolling, focus or
layout works in a browser. Record what you actually observed, including any
tools or platforms you could not check.

Finish with the complete tests and lint, then the documentation checks above
when content or generated output changes. Explain the reader-visible result
and its verification in the change description.

## Repeat the browser reader checks

`tests/browser_reader.mjs` builds and serves the site under a path prefix, then
checks Chromium, Firefox and WebKit. It exercises real keyboard search,
nested links, delayed and invalid indexes, accessible controls and the build
diagram at four widths in four themes and both colour modes. Screenshots and
one JSON results file go to `build/reader-artifacts/`. GitHub Actions runs an
isolated job for each browser and keeps those artifacts for 14 days.

Use Node.js 24, as in CI, and install the development-only browser dependency:

```text
npm ci
npx playwright install chromium firefox webkit
npm run test:browser
```

Playwright downloads separate browser automation builds. These checks verify
Chromium, Firefox, and WebKit behavior; WebKit automation is not qualification
of the Safari app. They do not replace screen-reader testing. Use a dedicated
browser profile for any manual headed run.

If a browser executable is missing, install its Playwright build with
`npx playwright install <browser>`. For launch or page errors, inspect
`results.json`, `build.log`, `run.log`, `console.log` and the per-browser logs
in `build/reader-artifacts/`; a process-spawn failure may be an operating
system restriction that reinstalling cannot fix. CI uploads the logs with the
phone and desktop screenshots, including after a failed check. Screenshots
still need a human to judge text legibility. The browser suite complements the
[visual inspection matrix](docs/visual-fixtures.md).

For detailed local browser-startup diagnostics in PowerShell, set
`$env:DEBUG='pw:browser*'` before `npm run test:browser`.

## Before a release

Before a release, build and inspect both wheel and sdist, qualify each from a
fresh environment outside the checkout, run the historical `check-release` and
`build-all` rehearsal, and follow [the pre-publish checklist](docs/pre-publish-checklist.md).
Release branches are named `dev/vX.Y.Z`. Tags are annotated and never moved
after publication. The maintainer opens the release PR against `main`, waits
for all required CI, merges only a green candidate, then tags the merge commit
and publishes the GitHub Release.
