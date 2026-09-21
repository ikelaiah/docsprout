# Configure your site

You can build a useful site with the files created by `docsprout init`. Change
one thing at a time, run `docsprout check`, and keep the last working version in
Git when possible.

## The three configuration files

| File | What it controls | When you need it |
| --- | --- | --- |
| `docs/docsprout.json` | Project identity, appearance and home-page presentation | Created by `init` |
| `docs/layout.json` | Published pages, navigation order, home page and unlisted policy | Created by `init` |
| `docs/versions.json` | Published release history | Only for a historical site |

These files use JSON. Keep the commas, quotation marks and braces exactly
paired. Every file starts with `"schema_version": 1`; leave that value alone.
If the punctuation is wrong, `docsprout check` names the file and error.

> [!NOTE] Upgrading from DocKit? The identity file may initially be named
> `docs/dockit.json`. That pre-rebrand filename keeps loading, but do not keep
> both names: DocSprout fails with an ambiguity error rather than choosing one
> silently. The
> [migration guide](migration.md#dockit-to-docsprout-1x-rebrand) covers the
> rename.

## Project metadata and colours

Edit `docs/docsprout.json`:

```json
{
  "schema_version": 1,
  "project": {
    "name": "MyLibrary-FP",
    "description": "Useful Pascal tools"
  },
  "theme": {
    "preset": "teal"
  }
}
```

`project.name` appears in the header and browser page title.
`project.description` becomes each generated page's description metadata; it
is not ordinary visible page text. `docsprout init` may add
`project.repository_url` from a GitHub remote. DocSprout stores that value and an
optional `project.site_url`, but does not render `repository_url` or `site_url`
as a footer or project link. Add an `identity.links` entry when readers should
be able to follow a visible project link.

The supported colour presets are `blue`, `teal`, `ocean` and `purple`. Start
with a preset. You can choose exact colours later in [Themes](themes.md).

## Pages, home page and navigation

`docs/layout.json` decides what is public. **Navigation** is the ordered list
of published pages and sections. Its top-level `home` object selects which
listed Markdown page becomes `index.html`, the page readers see at the site's
root. `docsprout.json.homepage` is different: it only controls the presentation of
that selected home page.

Edit `docs/layout.json`. Keep `home` and `unlisted` at the top level and add
pages inside the `navigation` list:

```json
{
  "schema_version": 1,
  "home": {
    "path": "index.md"
  },
  "unlisted": "exclude",
  "navigation": [
    {
      "title": "Get started",
      "pages": [
        {"title": "Overview", "path": "index.md"},
        {"title": "Quick start", "path": "quick-start.md"}
      ]
    },
    {
      "title": "Reference",
      "pages": [
        {"title": "Commands", "path": "reference/commands.md"}
      ]
    }
  ]
}
```

Each default `path` starts inside `docs/`. For example,
`"path": "reference/commands.md"` means the file is
`docs/reference/commands.md`.

For a repository-root README home, keep the matching root navigation page and
replace only the top-level `home` object with:

```json
"home": {
  "path": "README.md",
  "source": "root"
}
```

`"source": "root"` is required only for the exact repository-root
`README.md`. Existing layouts that omit `home` retain the compatible inference:
root README, then `docs/index.md`, then the first listed page. New layouts
should make the selection explicit.

`unlisted` controls what happens to Markdown under `docs/` that is not in
navigation:

- `"error"` is the default and preserves existing strict validation. A missing
  page is reported by `docsprout check`.
- `"exclude"` publishes only listed pages. `check` succeeds and reports the
  number of unlisted documents excluded from the site.

New layouts made by `docsprout init` use `"exclude"`. Existing layouts are
never rewritten; add the field only when you want this explicit publication
policy. There are no include/exclude patterns: the navigation list is the
complete publication decision.

## Editing `layout.json` directly

Every common navigation change is an ordinary edit to `docs/layout.json`.
There are no DocSprout commands for these operations:

| What you want | What you edit |
| --- | --- |
| Add a page | Add a page object to a section's `pages` list |
| Remove a page | Remove its page object |
| Rename a displayed title | Change that page object's `"title"` |
| Reorder pages | Move page objects within a `pages` list |
| Move a page to another section | Cut its object and paste it into another section's `pages` list |
| Add a section | Add a `{"title": ..., "pages": [...]}` object to `navigation` |
| Rename a section | Change that section's `"title"` |
| Change the home page | Change the top-level `"home"` object (its `path` must stay a listed page) |
| Publish or unpublish a page | Add or remove its page object under `"unlisted": "exclude"` |

The `"title"` is independent of the filename: a file named `install-guide.md`
can display as `Getting installed`. The navigation order is the written order
of the objects. That is the complete model—there is no hidden state and no
second navigation representation.

This compact canonical example shows the valuable structure at a glance:

```json
{
  "schema_version": 1,
  "home": {"path": "index.md"},
  "unlisted": "exclude",
  "navigation": [
    {
      "title": "Getting started",
      "pages": [
        {"title": "Overview", "path": "index.md"},
        {"title": "Installation", "path": "installation.md"}
      ]
    },
    {
      "title": "Guides",
      "pages": [
        {"title": "Configuration", "path": "guides/configuration.md"}
      ]
    }
  ]
}
```

DocSprout reports configuration problems precisely. A field that was never part
of a released schema-1 configuration is rejected with the file, the exact
field path and—when a close match exists—a `Did you mean` suggestion. For
example `"theme": {"presett": "purple"}` fails with
`Unknown field 'theme.presett'. Did you mean 'theme.preset'?`. Valid
configuration from every supported 0.x release keeps loading.

## Existing repositories and root README

On its first run, `docsprout init` considers only `README.md` at the repository
root and Markdown under `docs/`. It does not modify either one. Ancillary root
files such as `CHANGELOG.md` and `CONTRIBUTING.md` are deliberately excluded;
detection is not permission to publish.

The generated layout uses this narrow navigation entry for a root README:

```json
{"title": "Overview", "path": "README.md", "source": "root"}
```

`"source": "root"` supports only the exact repository-root `README.md`; it
does not permit `../README.md`, another root file, or any path outside the
repository. A README can link to a configured `docs/` page and a docs page can
link back to the README. Historical builds read the README from the matching
Git release archive.
Only the repository-root `README.md` has special root-source support. Other
Markdown you want to publish should live under `docs/`.

After `layout.json` exists it is authoritative. DocSprout will not discover new
pages, alter order or titles, add ancillary files, or reorganise sections. Add
an ancillary page only by deliberately listing an allowed docs-path in the
layout (for example, after copying or authoring a public docs version yourself).

## Reading width

Add `layout` inside `docs/docsprout.json` when the default width does not suit the
content:

```json
{
  "schema_version": 1,
  "project": {"name": "MyLibrary-FP"},
  "layout": {
    "content_width": "wide"
  }
}
```

Choose:

- `compact` for short, prose-led tutorials;
- `comfortable` for the balanced default;
- `wide` for large tables and code samples.

Omit this setting to keep `comfortable`.
The maintained minimal example uses `compact`, this DocSprout site uses the
omitted `comfortable` default, and the [visual fixture](visual-fixtures.md)
uses `wide` for tables and code.

## Footer links

You can add a short footer and a few useful links inside `docs/docsprout.json`:

```json
{
  "schema_version": 1,
  "project": {"name": "MyLibrary-FP"},
  "identity": {
    "footer": "Built for Free Pascal maintainers.",
    "links": [
      {"label": "Source code", "url": "https://github.com/example/library"}
    ]
  }
}
```

Link URLs must begin with `https://` or `http://`. DocSprout safely escapes the
visible text. The [DocSprout site itself](customisation.md#before-and-after-project-identity)
is the maintained example: its footer text and `Project` link appear together
at the bottom of every generated page.

## Home-page presentation

The default home page works without extra configuration. When you want to
change that page's cards or visible sections, add a `homepage` object to
`docs/docsprout.json`:

```json
{
  "schema_version": 1,
  "project": {"name": "MyLibrary-FP"},
  "homepage": {
    "capabilities": [
      {"title": "Offline", "description": "Every asset ships locally."},
      {"title": "Stable API", "description": "Guides follow each release."}
    ],
    "sections": {
      "release_context": true
    }
  }
}
```

Each card needs a non-empty `title` and `description`. An empty
`capabilities` list hides all cards. The optional section names are
`capabilities`, `banner`, `introduction` and `release_context`, and each accepts
`true` or `false`. Omitted section names use these defaults:

| Section | Default | Effect on the selected home page |
| --- | --- | --- |
| `capabilities` | `true` | Shows the configured cards, or the four standard cards when `homepage.capabilities` is omitted. |
| `banner` | `true` | Shows the configured `banner` image above the home-page content. It has no effect when no banner is configured. |
| `introduction` | `true` | Keeps the first paragraph after the H1 heading. |
| `release_context` | `false` | Hides the release label above the home-page content. |

Start from a complete example in [Customize the home page](homepage-recipes.md).

## Changing colours, logo and presentation

Appearance and identity are `docs/docsprout.json` edits:

| What you want | What you edit |
| --- | --- |
| Change colours | `theme.preset`, or exact `theme.accent` / `theme.accent_secondary` |
| Change the visual style | `theme.style` (`classic`, `paper`, `midnight`) |
| Add a logo | `identity.logo` (repository-local SVG or PNG) |
| Change the footer | `identity.footer` and `identity.links` |
| Add a banner | `banner` with `path` and `alt` |
| Custom CSS (advanced) | `theme.custom_css` — see [Custom CSS](custom-css.md) |

The documented `--dk-*` tokens are the stable customisation surface for
selectors you write yourself; see [Themes](themes.md#the-documented-dk-tokens).

## Release history can wait

Do not add `docs/versions.json` for a local preview or a single-version site.
Add it only when you decide to preserve documentation for older releases. The
[GitHub Pages guide](github-pages.md) helps you choose, and the
[glossary](glossary.md) explains terms such as tag, source ref and immutable.
