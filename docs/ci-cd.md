# Checks in CI and CD

DocSprout commands are ordinary processes with documented exit codes, so they
fit any continuous-integration runner. This page shows the gates and one
complete GitHub Actions job. [Publish with GitHub Pages](github-pages.md)
covers the managed deployment workflow, and
[Machine-readable contracts](machine-contracts.md#cli-contract) is the exact
command and exit-code reference.

## The gates

Run these from the repository root; every command also accepts
`--root <folder>` when your project lives in a subfolder:

| Command | Passes when | Exit codes |
| --- | --- | --- |
| `docsprout check` | the site can be built: configuration, links and anchors are valid | 0 pass; 1 error |
| `docsprout audit --strict` | the publication checks report no warnings | 0 clean; 1 errors or strict warnings; 2 invalid audit configuration |
| `docsprout doctor` | the project shape and release state are sane | 0 pass; 1 blocking problem |

`audit` never needs a built site: it reads your sources and configuration.
Start locally with `doctor`, then `check`, then `audit --strict`; CI repeats
exactly those commands. See [Audit your documentation](audit.md) for the
finding codes and their fixes.

## GitHub Actions: documentation checks

```yaml
name: Documentation checks
on:
  push:
    branches: [main]
  pull_request:
jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install DocSprout
        run: python -m pip install "https://github.com/ikelaiah/docsprout/archive/refs/tags/v1.1.4.zip"
      - name: Validate the site
        run: docsprout check
      - name: Audit publications
        run: docsprout audit --strict --format json > audit.json
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: docsprout-audit
          path: audit.json
```

Pin a released tag (`v1.1.4` above), never a branch. `--format json` writes the
machine-readable report; the artifact keeps it after the job, including when
the audit fails.

## Historical sites need the full Git history

`check-release` and `build-all` verify and build immutable release tags. The
default shallow checkout does not contain them, so fetch the full history:

```yaml
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
```

## Any other runner

The commands and exit codes are the whole contract; the runner configuration
is yours. The same checks in GitLab CI:

```yaml
docs-checks:
  image: python:3.12
  script:
    - python -m pip install "https://github.com/ikelaiah/docsprout/archive/refs/tags/v1.1.4.zip"
    - docsprout check
    - docsprout audit --strict
```

Git-based release validation additionally needs Git and the repository's tags
available in the job. The install pin is the same archive URL used everywhere
else; see [Machine-readable contracts](machine-contracts.md) for the reusable
Pages workflow inputs when you publish to GitHub Pages.

## CD: deploy the built site anywhere

Publishing to GitHub Pages is one command plus the managed workflow—see
[GitHub Pages in one command](github-pages.md#github-pages-in-one-command).
Other hosts consume the static output directly:

```bash
docsprout build --output dist
```

Upload `dist/` to any static host: object storage, a web server, or a platform
such as Netlify. For a single archive to hand to someone, add
`--offline-archive docs.zip`; [Build and inspect your site](building.md) covers
both options.

## Next steps

- [Pre-publish checklist](pre-publish-checklist.md)
- [Machine-readable contracts](machine-contracts.md)
- [Troubleshooting](troubleshooting.md)
