# Add DocSprout to an existing repository

Most projects already have a `README.md`, a `docs/` folder, or both. DocSprout
adopts those files in place: it never rewrites, moves or copies your Markdown.
This page covers the adoption path. [Your first DocSprout site](beginners-guide.md)
covers the same ground for a practice project that starts empty.

## Before you begin

You need a supported Python version and an internet connection for
installation; see the quick start in the project README. Git is not required
for the local preview. Git is required later for `github-pages`,
`check-release` and `build-all`.

## 1. Install and adopt

Run both commands from the repository's top-level folder—the one that contains
`README.md` or `.git/`:

```bash
python -m pip install "https://github.com/ikelaiah/docsprout/archive/refs/tags/v1.1.8.zip"
docsprout init
```

A first run reports what it found and creates only the missing configuration:

```text
Initialised docs
Detected: Git repository, GitHub remote https://github.com/example/library, root README.md, 4 Markdown document(s) under docs/.
Created: docs/docsprout.json, docs/layout.json.
Available for explicit inclusion: CHANGELOG.md, CONTRIBUTING.md.
Existing Markdown was left untouched.
Navigation sections: Overview (1 page), Documentation (1 page), Guides (3 pages).
DocSprout is ready.
  Write documentation: README.md and docs/*.md
  Add, rename, group or reorder pages:  docs/layout.json
  Change colours, logo and presentation:  docs/docsprout.json
  Preview:  docsprout serve
```

Your exact output differs: the detected list, the created list and the section
names all come from your repository. A non-Git project simply reports
`non-Git project`.

## What `init` looks at

- a root `README.md`;
- Markdown under `docs/`, grouped into sections by subfolder;
- whether this is a Git repository and whether it has a GitHub remote;
- existing DocSprout configuration;
- ancillary root files (`CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`,
  `CODE_OF_CONDUCT.md`), which it reports but never publishes.

Only `README.md` and `docs/**/*.md` are automatic candidates. A root
`CHANGELOG.md` cannot become a page until you deliberately copy or author a
docs version and list it—detection is not permission to publish.

## What it creates, and what it never touches

| File | Created when | Purpose |
| --- | --- | --- |
| `docs/docsprout.json` | missing | project name, description, an inferred GitHub repository URL, default colours |
| `docs/layout.json` | missing | the published pages and their order; `init` writes it once and it is yours from then on |
| `docs/index.md` | the project has no Markdown at all | a placeholder first page |

- Existing Markdown is never modified, moved or copied.
- Existing configuration is left authoritative. A rerun changes nothing and
  prints `Existing configuration was left authoritative; no files were changed.`
- The generated `home` selects your root `README.md` when it exists, otherwise
  `docs/index.md`, otherwise the first listed page.
- Generated layouts use `"unlisted": "exclude"`: only listed pages publish.

> [!NOTE] A project that already carries a legacy `docs/dockit.json` keeps
> loading it. Rename it to `docs/docsprout.json` when convenient; the
> [migration guide](migration.md#dockit-to-docsprout-1x-rebrand) has the full
> list of renames and compatibility guarantees.

## 2. Check and preview

```bash
docsprout check
docsprout serve
```

`check` validates the configuration and links without writing a site; `serve`
builds a local-only preview at <http://127.0.0.1:8000> and watches the files
you edit. Keep it running while you work and reload the browser after a save.

## 3. Shape the site around what you already have

- Add, reorder or rename pages in `docs/layout.json` —
  [Configuration](configuration.md).
- Set the project name, colours, style and logo in `docs/docsprout.json` —
  [Themes](themes.md) and [sections and identity](customisation.md).
- Add richer Markdown — [Authoring recipes](authoring-recipes.md).
- Keep older releases — [Historical documentation](historical-docs.md).

## Adopting from an old local builder

If the repository currently builds docs with local scripts such as
`tools/build_docs.py`, pin DocSprout, reproduce the site beside the old one,
compare the output, and only then remove the old machinery. The
[Migration guide](migration.md) has the step list.

## Next steps

- Publish with the recommended path:
  [GitHub Pages in one command](github-pages.md#github-pages-in-one-command).
- Add the same gates to your pipeline:
  [Checks in CI and CD](ci-cd.md).
