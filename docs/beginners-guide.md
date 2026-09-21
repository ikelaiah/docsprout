# Your first DocSprout site

This guide starts from an ordinary code project and ends with a documentation
site running on your computer. The example name is Pascal-flavoured, but the
steps work for any project that uses Markdown.

Allow about 10 minutes. You can stop after the preview works; publishing is a
separate task for another day.

## Before you begin

You need:

- Python 3.10–3.14 (the qualified stable range; Python 3.15 pre-release is
  only a non-blocking forward-compatibility signal);
- an internet connection for installation;
- a code project, even a tiny practice project;
- a terminal and a text editor.

You do **not** need Git, a GitHub account, a web server or Pascal knowledge for
this guide. When this page says “project folder”, it means the top-level folder
that normally contains `README.md` or `src/`.

## 1. Install DocSprout

Open a terminal in your project folder and run:

```bash
python -m pip install "https://github.com/ikelaiah/docsprout/archive/refs/tags/v1.0.0.zip"
```

Then check that the command is available:

```bash
docsprout --help
```

You should see a list of commands such as `build`, `check`, `init` and `serve`.

> [!NOTE] If your terminal says `DocSprout` was not found, close and reopen the
> terminal. You can also run `python -m docsprout --help`.

## 2. Adopt the Markdown you already have

Run this from the same project folder:

```bash
docsprout init
```

You should see a message beginning with `Initialised`. The command detects a
root `README.md`, Markdown inside `docs/`, Git/GitHub details, and common
ancillary Markdown. It never rewrites, moves or copies existing Markdown. It
creates only missing DocSprout configuration:

```text
docs/
├── docsprout.json   # project name and colours
├── layout.json   # pages and navigation order
└── index.md      # only when there was no README or docs page
```

By default, DocSprout publishes only `README.md` and `docs/**/*.md`. It tells you
about `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md` and
`CODE_OF_CONDUCT.md`, but leaves them private until you choose to add them.
Only the repository-root `README.md` has special root-source support. Other
Markdown you want to publish should live under `docs/`.

## 3. See the site now

Run:

```bash
docsprout serve
```

Open <http://127.0.0.1:8000>. The command validates and builds first, then
starts a local-only preview server. It watches `README.md` and `docs/`, rebuilding
after a saved change; reload the browser to see the new page without restarting
the command. Press `Ctrl+C` to stop it. Use
`docsprout serve --port 8000` or `docsprout serve --host 127.0.0.1` when you
need a specific local address.

> [!IMPORTANT] You have finished the beginner path. The site works locally.
> You do not need release tags or GitHub Pages until you choose to publish.

## 4. Make the site yours

If `init` created `docs/index.md`, open it and replace its text with something
small. Otherwise edit the existing `README.md` or a page under `docs/`:

```markdown
# Star Mapper

Star Mapper turns telescope readings into a searchable sky map.

## Start here

Read the quick start to make your first map.
```

The first `#` is the page title. A line beginning with `##` is a section title.
That is enough Markdown to begin.

Next, open `docs/docsprout.json`. `init` has already inferred safe metadata where
it could, including a GitHub repository URL. Change the project name and description if needed. Leave
`schema_version` unchanged:

```json
{
  "schema_version": 1,
  "project": {
    "name": "Star Mapper",
    "description": "Make a searchable map from telescope readings."
  },
  "theme": {
    "accent": "#0f766e",
    "accent_secondary": "#0891b2"
  }
}
```

## 5. Add one useful page

Think of the first thing a new user wants to achieve. Create
`docs/quick-start.md` and show that one task:

```markdown
# Quick start

Install Star Mapper, then run `star-mapper import first-light.csv`.

You should see `Created sky-map.html`.
```

Open `docs/layout.json`. It is now maintainer-owned: DocSprout never silently
adds Markdown, reorders sections, renames entries or removes pages after this
file exists. The root-README project from step 2 starts with this generated
layout. Keep the existing `home` entry unchanged while adding the page.

Before the change, the file may look like this:

```json
{
  "schema_version": 1,
  "home": {
    "path": "README.md",
    "source": "root"
  },
  "unlisted": "exclude",
  "navigation": [
    {
      "title": "Getting started",
      "pages": [
        {
          "title": "Overview",
          "path": "README.md",
          "source": "root"
        }
      ]
    }
  ]
}
```

Add this new page object to the same `pages` list:

```json
{
  "title": "Quick start",
  "path": "quick-start.md"
}
```

After adding the page, the file may look like this:

```json
{
  "schema_version": 1,
  "home": {
    "path": "README.md",
    "source": "root"
  },
  "unlisted": "exclude",
  "navigation": [
    {
      "title": "Getting started",
      "pages": [
        {
          "title": "Overview",
          "path": "README.md",
          "source": "root"
        },
        {
          "title": "Quick start",
          "path": "quick-start.md"
        }
      ]
    }
  ]
}
```

In JSON lists, put a comma after each item except the last one.

`"unlisted": "exclude"` means navigation is the complete publication decision:
Markdown under `docs/` stays private until you list it. The generated layout
for a project that starts with `docs/index.md` has the same structure, but
selects that document as its home page:

```json
"home": {
  "path": "index.md"
}
```

### The two editing cheat sheets

Every common change is an edit to a JSON file, not a command:

| What you want | Edit |
| --- | --- |
| Add a page | Add a page object (its `"title"` and `"path"`) to `docs/layout.json` |
| Add a section | Add a `{"title": ..., "pages": [...]}` object to `navigation` |
| Rename a displayed title | Change that page object's `"title"` in `layout.json` |
| Reorder pages | Move page objects up or down inside their `pages` list |
| Move a page to another section | Cut its object and paste it into another section |
| Change the home page | Change the top-level `"home"` object in `layout.json` |
| Change colours, theme or logo | Edit `docs/docsprout.json` (`theme`, `identity.logo`) |
| Remove a page from the site | Remove its page object from `layout.json` |

The displayed title is independent of the filename, and the written order of
the objects is the navigation order. You finish every edit by saving and
reloading the preview.

For a fuller explanation of `home`, navigation and legacy layouts, see
[Configuration](configuration.md).

## 6. Choose the home page and appearance

The **home page** is the page readers see at the site root. `layout.json.home`
selects that existing published Markdown page; `docsprout.json.homepage` changes
only its cards, banner and visible sections. They are different settings.

The root README shown above is already a valid home-page choice. If you want
`docs/index.md` or another listed docs page instead, change only the `home`
object and keep its matching navigation entry. Then choose colours, a **Style**
(`Classic`, `Paper` or `Midnight`) and a **Mode** (`System`, `Light` or `Dark`)
in [Themes](themes.md). [Customize the home page](homepage-recipes.md) has
complete `docsprout.json` examples.

## 7. Check and audit

Run:

```bash
docsprout check
docsprout audit
```

`check` answers “Can DocSprout safely build this site?” `audit` answers “What
objective documentation problems should I fix?” If `check` fails, read its last
line first; it normally names the file and next correction. Use
`docsprout audit --strict` when warnings should also fail a CI job, and
`docsprout doctor` for a setup summary.

Run `docsprout serve` again and reload the browser. **Quick start** should now
appear in the navigation.

## Where to go next

- Learn a simple, language-neutral writing method in
  [Write documentation people can use](writing-great-docs.md).
- Learn the three configuration files in [Configuration](configuration.md).
- Copy a small working project from the
  [minimal example](https://github.com/ikelaiah/docsprout/tree/v1.0.0/examples/minimal).
- When you truly want a public site, choose the simpler or historical path in
  [GitHub Pages](github-pages.md).
- Look up unfamiliar words in the [glossary](glossary.md).
