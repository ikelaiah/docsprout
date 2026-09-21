# Publish with GitHub Pages

DocSprout can prepare a normal Git repository for GitHub Pages without requiring
the GitHub CLI, a token, a network connection, or copied workflow YAML. You
keep control of Git commits, pushes and repository settings.

## GitHub Pages in one command

Once in the GitHub repository, enable **Settings → Pages → Source → GitHub
Actions**. DocSprout cannot change that repository setting because it does not use
GitHub credentials.

Then, from the top of the existing Git repository, run:

```bash
docsprout github-pages
```

For a repository with Markdown but no DocSprout setup, this safely reuses the
same conservative discovery as `docsprout init`. It creates only missing files:

```text
docs/docsprout.json
docs/layout.json
.github/workflows/docsprout-pages.yml
```

Existing Markdown remains unchanged. For an existing DocSprout project, its
layout, explicit `home`, navigation, identity and theme remain authoritative.
The command validates the result before reporting the next steps:

```bash
git add .
git commit -m "Add DocSprout documentation"
git push
```

DocSprout prepares GitHub; the maintainer controls Git. It does not commit or push.
If the repository has no GitHub remote yet, setup still succeeds; add a
GitHub remote before the push. The generated workflow runs after a push to the
repository's GitHub default branch and can also be started manually from that
branch. It validates, builds, uploads and deploys the documentation; pushes
from feature branches do not deploy Pages.

### Safe reruns and updates

`docsprout github-pages` is safe to rerun. When the configuration and managed
workflow are current, it makes no repository changes.

The generated workflow carries a DocSprout ownership marker and pins the reusable
workflow to the installed release, such as `@v1.1.0`. It never follows
`@main`. If a recognised managed workflow is older, ordinary setup reports the
version and leaves it unchanged. Update only that workflow deliberately:

```bash
docsprout github-pages --update
```

If `.github/workflows/docsprout-pages.yml` exists but is not recognisably
DocSprout-managed, DocSprout refuses to overwrite it. A malformed managed workflow
also requires manual repair. Neither case changes other repository files.

### Pre-rebrand workflows

A repository prepared before the DocSprout rename may already own a managed
`.github/workflows/dockit-pages.yml`. DocSprout recognises it through its
ownership marker: ordinary setup reports the pinned version, and

```bash
docsprout github-pages --update
```

updates that recognised workflow in place. It never writes a second
`docsprout-pages.yml` next to an existing managed legacy workflow, and it never
overwrites an unmanaged file at either path. When both managed paths exist,
setup stops with a clear error so you can remove one deliberately.

## Advanced: manual and historical workflows

The one-command path builds a single, current site from the default branch. It
is the recommended choice for most repositories. Keep the following manual
workflow forms when you need a different filename, a custom workflow layout or
immutable documentation for release tags.

### Single-version site

Do not create `docs/versions.json` for this path. Create a workflow such as
`.github/workflows/documentation.yml`:

```yaml
name: Documentation

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  documentation:
    permissions:
      contents: read
      pages: write
      id-token: write
    uses: ikelaiah/docsprout/.github/workflows/publish-docs.yml@v1.1.0
    with:
      versioned: false
      release: latest
```

The maintained [single-version example](https://github.com/ikelaiah/docsprout/tree/v1.1.0/examples/single-version)
uses this form.

## Historical site for versioned projects

Choose this path when readers need several released versions. It needs Git tags
and `docs/versions.json`; see [Historical documentation](historical-docs.md).

```yaml
name: Documentation

on:
  push:
    tags: ["v*"]
  workflow_dispatch:

jobs:
  documentation:
    permissions:
      contents: read
      pages: write
      id-token: write
    uses: ikelaiah/docsprout/.github/workflows/publish-docs.yml@v1.1.0
```

Check a historical release locally after creating its tag and before pushing:

```bash
docsprout check
docsprout check-release
docsprout build-all --output build/docs-site
```

The maintained [historical example](https://github.com/ikelaiah/docsprout/tree/v1.1.0/examples/historical)
uses this form. Follow the [pre-publish checklist](pre-publish-checklist.md)
for the exact release order.

## If deployment does not run

- Confirm GitHub Pages uses **GitHub Actions** as its source.
- Confirm the workflow is under `.github/workflows/` and ends in `.yml` or
  `.yaml`.
- For the generated workflow, push the repository's default branch.
- Open the failed Actions step and run `docsprout check` locally before retrying.
