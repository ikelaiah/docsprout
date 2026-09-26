# 🌱 DocSprout

[![CI](https://github.com/ikelaiah/docsprout/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ikelaiah/docsprout/actions/workflows/ci.yml?query=branch%3Amain) [![Docs](https://img.shields.io/website?url=https%3A%2F%2Fikelaiah.github.io%2Fdocsprout%2F1.1.8%2F&label=docs)](https://ikelaiah.github.io/docsprout/1.1.8/) [![Latest release](https://img.shields.io/github/v/release/ikelaiah/docsprout?display_name=tag&sort=semver)](https://github.com/ikelaiah/docsprout/releases/latest) [![Python 3.10–3.14](https://img.shields.io/badge/python-3.10%E2%80%933.14-3776AB?logo=python&logoColor=white)](https://github.com/ikelaiah/docsprout/blob/main/docs/qualification.md#supported-python-versions) [![License: MIT](https://img.shields.io/github/license/ikelaiah/docsprout)](https://github.com/ikelaiah/docsprout/blob/main/LICENSE)

![DocSprout banner — Build documentation people can use.](docs/assets/docsprout-banner.svg)

**Grow polished documentation from Markdown.**

Turn Markdown files into a polished documentation website with search, themes,
mobile navigation and optional release history.

DocSprout is a small, offline-friendly Markdown documentation-site builder for
code projects. It originated in the Free Pascal ecosystem and remains
Pascal-friendly, but it does not require Pascal source code.

## 🚀 Make your first site in about 10 minutes

You need supported Python 3.10–3.14 and internet for installation; no Git or
GitHub account is needed for this first preview. Python 3.15 is not supported
yet; it is only checked early to catch future incompatibilities.

Open a terminal in your project's top-level folder—the folder that normally
contains files such as `README.md`, `src/` or `.git/`—and run:

```bash
python -m pip install "https://github.com/ikelaiah/docsprout/archive/refs/tags/v1.1.8.zip"
docsprout init
docsprout serve
```

`init` inspects the project without changing existing Markdown. It detects a
root `README.md`, Markdown below `docs/`, Git/GitHub metadata and common
ancillary files. It creates only the missing DocSprout configuration around
those documents:

```text
docs/
├── docsprout.json   # project name and colours
├── layout.json      # navigation order
└── index.md         # only for a project with no existing documentation
```

Visit <http://127.0.0.1:8000> in a browser. You should see your existing
README and `docs/` pages with navigation, search and theme controls. The preview
watches `README.md` and `docs/`: after a saved change it rebuilds automatically,
so reload the browser without restarting the command. Press `Ctrl+C` in the
terminal to stop the preview server.

That is a complete local documentation site. You can stop here and return when
you are ready to add pages or publish it. `README.md` and `docs/**/*.md`
are the only automatic candidates. `CHANGELOG.md`, `CONTRIBUTING.md`,
`SECURITY.md` and `CODE_OF_CONDUCT.md` are reported for deliberate inclusion,
never published by surprise. Once `docs/layout.json` exists it is entirely
yours: add, remove, rename and reorder pages without DocSprout changing it.
Newly generated layouts use `"unlisted": "exclude"`, so only listed pages are
published; existing layouts retain their strict validation unless you
[opt in](docs/configuration.md#pages-home-page-and-navigation).

### The mental model from here on

Commands perform actions. Configuration describes intent. There are no
DocSprout commands for editing pages, sections or themes:

- **Markdown** (`README.md`, `docs/*.md`) is your content.
- **`docs/layout.json`** decides what is published: page objects, section
  names, titles, order, the home page and the unlisted policy. Add a page by
  adding one page object; reorder by moving objects; rename by changing
  `"title"`; change the home page by editing the top-level `"home"`.
- **`docs/docsprout.json`** decides how it looks: name, colours, visual theme,
  logo, footer, banner and homepage presentation.

`docsprout init` explains exactly this when it finishes. `docsprout serve`
watches `README.md` and everything under `docs/`, including `layout.json` and
`docsprout.json`, so you edit, save and reload.

For a slower walkthrough with explanations and expected results, follow
[Your first DocSprout site](docs/beginners-guide.md).

## 🌐 Publish with GitHub Pages in one command

When this is a Git repository and you are ready to publish, run:

```bash
docsprout github-pages
git add .
git commit -m "Add DocSprout documentation"
git push
```

DocSprout safely creates missing documentation configuration and a pinned
GitHub Pages workflow at `.github/workflows/docsprout-pages.yml`. It does not
commit or push; those remain your decisions. Enable GitHub Pages with **GitHub
Actions** once in the repository settings, then a push to the repository's
default branch publishes the site. See [GitHub Pages in one
command](docs/github-pages.md#github-pages-in-one-command) for updates,
existing projects and advanced historical publishing.

## 🧭 Choose what you want to do next

| Your goal | Read this |
| --- | --- |
| Build static files or an offline ZIP | [Build and inspect your site](docs/building.md) |
| Add DocSprout to an existing repository | [Add to an existing repository](docs/existing-repository.md) |
| Run checks in CI or deploy elsewhere | [Checks in CI and CD](docs/ci-cd.md) |
| Learn how to write useful documentation | [Write documentation people can use](docs/writing-great-docs.md) |
| Add pages and navigation | [Configuration](docs/configuration.md) |
| Add richer content | [Authoring recipes](docs/authoring-recipes.md) |
| Find likely publication mistakes | [Audit your documentation](docs/audit.md) |
| Change colours, themes or home-page presentation | [Themes](docs/themes.md) and [customize the home page](docs/homepage-recipes.md) |
| Publish with the recommended path | [GitHub Pages in one command](docs/github-pages.md#github-pages-in-one-command) |
| Keep documentation for older releases | [GitHub Pages: historical site](docs/github-pages.md#historical-site-for-versioned-projects) |
| Fix a failing command | [Troubleshooting](docs/troubleshooting.md) |
| Find out what is tested and supported | [Qualification evidence](docs/qualification.md) |
| Understand an unfamiliar term | [Glossary](docs/glossary.md) |

## ✨ Five promises

- **Easy to use.** Short commands take a project from Markdown to preview,
  checks, audit and publication.
- **Easy to learn.** The beginner path explains the mental model and the next
  useful edit without hiding decisions in a generator.
- **Easy to look good.** Responsive, keyboard-friendly Classic, Paper,
  E-ink and Glassmorphic sites work with local assets and no custom
  CSS required, and one brand colour becomes a contrast-proven theme.
- **Easy to create from existing repositories.** `init` preserves Markdown,
  discovers ordinary and Pascal-shaped projects, and creates only missing
  configuration.
- **Easy to maintain.** Explicit navigation, machine contracts, release
  checks and pinned Pages workflows keep ownership visible.

Your repository keeps its Markdown, navigation, project identity and release
tags. DocSprout supplies the renderer and shared website machinery. You should
not need to copy its CSS or JavaScript into your project.

## 🚫 What it does not do

DocSprout does not read source code and invent API documentation. For Free
Pascal API extraction, use [PasWeave](https://github.com/ikelaiah/pasweave) to
produce Markdown, then let DocSprout combine that Markdown with your
handwritten guides.

## 📝 Already have documentation?

You do not need to rewrite it. Keep the Markdown files you have, add the small
configuration files around them, and introduce explicit navigation gradually.
See [Configuration](docs/configuration.md) for the supported files and the
explicit root-README entry.

### Upgrading from DocKit

DocSprout is the new name for the 1.x builder released as DocKit. Your existing
project keeps working:

- `dockit-fp` remains a deprecated console-script alias and
  `python -m dockit_fp` remains a deprecated module entry point for at least
  one minor release; use `docsprout` and `python -m docsprout` instead. The
  aliases, the `docs/dockit.json` filename, the `.dockit-fp-site` marker and
  the managed `dockit-pages.yml` path are scheduled for removal in v2.0.0.
- Existing `docs/dockit.json` files keep loading. New projects create
  `docs/docsprout.json`; never keep both, because the ambiguity is an error.
- Managed `dockit-pages.yml` workflows are recognised and updated in place.
- The `--dk-*` CSS tokens are unchanged.

See [Migration](docs/migration.md#dockit-to-docsprout-1x-rebrand) for the full
list.

## 🛠️ Working on DocSprout itself

Run the complete test suite from this repository:

```bash
python -m unittest discover -s tests -t . -v
```

Project design details live in [Architecture](docs/architecture.md), and major
decisions are recorded in [docs/decisions](docs/decisions/).

DocSprout is released under the MIT licence.
