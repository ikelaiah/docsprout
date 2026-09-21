# Contributing

DocSprout supports Python 3.10–3.14 on Linux, with the minimum and latest stable
versions qualified on Windows and macOS. Python 3.15 pre-release runs as a
non-blocking forward-compatibility signal, not as a support commitment.

Install the local checkout and run the complete suite before proposing a
change:

```powershell
python -m pip install -e .
python -m unittest discover -s tests -t . -v
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

Before a release, build and inspect both wheel and sdist, qualify each from a
fresh environment outside the checkout, run the historical `check-release` and
`build-all` rehearsal, and follow [the pre-publish checklist](docs/pre-publish-checklist.md).
Release branches are named `release/vX.Y.Z`; tags are annotated and are never
moved after publication. The maintainer opens the release PR against `main`,
waits for all required CI, merges only a green candidate, then tags the merge
commit and publishes the GitHub Release.
