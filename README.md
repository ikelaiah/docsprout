# 📚 DocKit

![DocKit banner — Build documentation people can use.](docs/assets/dockit-banner.svg)

Turn Markdown files into a polished documentation website with search, themes,
mobile navigation and optional release history.

DocKit is a small, offline-friendly Markdown documentation-site builder for code
projects. It originated in the Free Pascal ecosystem and remains Pascal-friendly,
but it does not require Pascal source code.

## 🚀 Make your first site in about 10 minutes

You need Python 3.10 or newer and an internet connection for installation. You
do not need Git or a GitHub account for this first preview.

Open a terminal in your project's top-level folder—the folder that normally
contains files such as `README.md`, `src/` or `.git/`—and run:

```bash
python -m pip install "https://github.com/ikelaiah/dockit-fp/archive/refs/tags/v0.17.0.zip"
dockit-fp init
dockit-fp serve
```

`init` inspects the project without changing existing Markdown. It detects a
root `README.md`, Markdown below `docs/`, Git/GitHub metadata and common
ancillary files. It creates only the missing DocKit configuration around those
documents:

```text
docs/
├── dockit.json   # project name and colours
├── layout.json   # navigation order
└── index.md      # only for a project with no existing documentation
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
yours: add, remove, rename and reorder pages without DocKit changing it.
Newly generated layouts use `"unlisted": "exclude"`, so only listed pages are
published; existing layouts retain their strict validation unless you opt in.

For a slower walkthrough with explanations and expected results, follow
[Your first DocKit site](docs/beginners-guide.md).

## 🌐 Publish with GitHub Pages in one command

When this is a Git repository and you are ready to publish, run:

```bash
dockit-fp github-pages
git add .
git commit -m "Add DocKit documentation"
git push
```

DocKit safely creates missing documentation configuration and a pinned GitHub
Pages workflow. It does not commit or push; those remain your decisions. Enable
GitHub Pages with **GitHub Actions** once in the repository settings, then a
push to the repository's default branch publishes the site. See [GitHub Pages
in one command](docs/github-pages.md#github-pages-in-one-command) for updates,
existing projects and advanced historical publishing.

## 🧭 Choose what you want to do next

| Your goal | Read this |
| --- | --- |
| Learn how to write useful documentation | [Write documentation people can use](docs/writing-great-docs.md) |
| Add pages and navigation | [Configuration](docs/configuration.md) |
| Find likely publication mistakes | [Audit your documentation](docs/audit.md) |
| Change colours, themes or home-page presentation | [Themes](docs/themes.md) and [customize the home page](docs/homepage-recipes.md) |
| Publish with the recommended path | [GitHub Pages in one command](docs/github-pages.md#github-pages-in-one-command) |
| Keep documentation for older releases | [GitHub Pages: historical site](docs/github-pages.md#historical-site-for-versioned-projects) |
| Find out what is tested and supported | [Qualification evidence](docs/qualification.md) |
| Understand an unfamiliar term | [Glossary](docs/glossary.md) |

## ✨ What DocKit gives you

- 📱 Responsive pages that work on phones and desktops.
- 🌓 System, Light and Dark colour modes.
- 🎨 Classic, Paper and Midnight visual themes.
- 🔎 Search and keyboard-friendly navigation.
- 📐 Local KaTeX mathematics without a CDN.
- ✅ Checks for broken links, missing pages and unsafe configuration.
- 🏷️ Optional immutable documentation for every tagged release.
- 🚀 A reusable GitHub Pages workflow.

Your repository keeps its Markdown, navigation, project identity and release
tags. DocKit supplies the renderer and shared website machinery. You should
not need to copy its CSS or JavaScript into your project.

## 🚫 What it does not do

DocKit does not read source code and invent API documentation. For Free
Pascal API extraction, use [PasWeave](https://github.com/ikelaiah/pasweave) to
produce Markdown, then let DocKit combine that Markdown with your handwritten
guides.

## 📝 Already have documentation?

You do not need to rewrite it. Keep the Markdown files you have, add the small
configuration files around them, and introduce explicit navigation gradually.
See [Configuration](docs/configuration.md) for the supported files and the
explicit root-README entry.

## 🛠️ Working on DocKit itself

Run the complete test suite from this repository:

```bash
python -m unittest discover -s tests -t . -v
```

Project design details live in [Architecture](docs/architecture.md), and major
decisions are recorded in [docs/decisions](docs/decisions/).

DocKit is released under the MIT licence.
