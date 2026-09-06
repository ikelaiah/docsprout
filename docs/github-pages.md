# Publish with GitHub Pages

DocKit can prepare a normal Git repository for GitHub Pages without requiring
the GitHub CLI, a token, a network connection, or copied workflow YAML. You
keep control of Git commits, pushes and repository settings.

## GitHub Pages in one command

Once in the GitHub repository, enable **Settings → Pages → Source → GitHub
Actions**. DocKit cannot change that repository setting because it does not use
GitHub credentials.

Then, from the top of the existing Git repository, run:

```bash
dockit-fp github-pages
```

For a repository with Markdown but no DocKit setup, this safely reuses the
same conservative discovery as `dockit-fp init`. It creates only missing files:

```text
docs/dockit.json
docs/layout.json
.github/workflows/dockit-pages.yml
```

Existing Markdown remains unchanged. For an existing DocKit project, its
layout, explicit `home`, navigation, identity and theme remain authoritative.
The command validates the result before reporting the next steps:

```bash
git add .
git commit -m "Add DocKit documentation"
git push
```

DocKit prepares GitHub; the maintainer controls Git. It does not commit or push.
If the repository has no GitHub remote yet, setup still succeeds; add a
GitHub remote before the push. The generated workflow runs after a push to the
repository's GitHub default branch and can also be started manually from that
branch. It validates, builds, uploads and deploys the documentation; pushes
from feature branches do not deploy Pages.

### Safe reruns and updates

`dockit-fp github-pages` is safe to rerun. When the configuration and managed
workflow are current, it makes no repository changes.

The generated workflow carries a DocKit ownership marker and pins the reusable
workflow to the installed release, such as `@v0.18.0`. It never follows
`@main`. If a recognised managed workflow is older, ordinary setup reports the
version and leaves it unchanged. Update only that workflow deliberately:

```bash
dockit-fp github-pages --update
```

If `.github/workflows/dockit-pages.yml` exists but is not recognisably
DocKit-managed, DocKit refuses to overwrite it. A malformed managed workflow
also requires manual repair. Neither case changes other repository files.

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
    uses: ikelaiah/dockit-fp/.github/workflows/publish-docs.yml@v0.18.0
    with:
      versioned: false
      release: latest
```

The maintained [single-version example](https://github.com/ikelaiah/dockit-fp/tree/v0.18.0/examples/single-version)
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
    uses: ikelaiah/dockit-fp/.github/workflows/publish-docs.yml@v0.18.0
```

Check a historical release locally after creating its tag and before pushing:

```bash
dockit-fp check
dockit-fp check-release
dockit-fp build-all --output build/docs-site
```

The maintained [historical example](https://github.com/ikelaiah/dockit-fp/tree/v0.18.0/examples/historical)
uses this form. Follow the [pre-publish checklist](pre-publish-checklist.md)
for the exact release order.

## If deployment does not run

- Confirm GitHub Pages uses **GitHub Actions** as its source.
- Confirm the workflow is under `.github/workflows/` and ends in `.yml` or
  `.yaml`.
- For the generated workflow, push the repository's default branch.
- Open the failed Actions step and run `dockit-fp check` locally before retrying.
