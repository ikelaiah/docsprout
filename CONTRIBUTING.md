# Contributing

DocKit supports Python 3.10–3.14 on Linux, with the minimum and latest stable
versions qualified on Windows and macOS. Python 3.15 pre-release runs as a
non-blocking forward-compatibility signal, not as a support commitment.

Install the local checkout and run the complete suite before proposing a
change:

```powershell
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
dockit-fp check
dockit-fp audit --strict
dockit-fp build --output build/docs-site
```

Before a release, build and inspect both wheel and sdist, qualify each from a
fresh environment outside the checkout, run the historical `check-release` and
`build-all` rehearsal, and follow [the pre-publish checklist](docs/pre-publish-checklist.md).
Release branches are named `release/vX.Y.Z`; tags are annotated and are never
moved after publication. The maintainer opens the release PR against `main`,
waits for all required CI, merges only a green candidate, then tags the merge
commit and publishes the GitHub Release.
