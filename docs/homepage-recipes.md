# Customize the home page

The home page is the Markdown document selected by `layout.json.home`, rendered
as the site's `index.html`. It may be a listed page under `docs/` or the
repository-root `README.md` with `"source": "root"`. The `homepage` object in
`docs/docsprout.json` only changes the selected home page's presentation; it does
not choose the document. You do not need it unless you want to customise the
landing page.

These recipes decide **presentation**. For page structure, see
[Authoring recipes](authoring-recipes.md); the two pages share archetype names
but edit different layers.

The examples below are values to add to your existing `docs/docsprout.json`;
keep your `schema_version`, `project` and other settings. All but `banner`,
which is a top-level setting, are `homepage` values.

## See it in DocSprout

DocSprout uses the same configuration on this site. Its
[`docs/docsprout.json`](https://github.com/ikelaiah/docsprout/blob/v1.1.5/docs/docsprout.json)
uses these exact values for its home-page banner and capability cards:

```json
{
  "banner": {
    "path": "docs/assets/docsprout-mountain-banner.jpg",
    "alt": "DocSprout banner — Build documentation people can use."
  },
  "homepage": {
    "capabilities": [
      {"title": "Existing-project friendly", "description": "Start with the README and docs you already have."},
      {"title": "Polished with little setup", "description": "Build a searchable documentation site from Markdown."},
      {"title": "Versioned documentation", "description": "Keep released guides available side by side."},
      {"title": "Offline/local assets", "description": "Built sites work without a CDN."}
    ],
    "sections": {"release_context": false}
  }
}
```

```text
docs/docsprout.json
        ↓
banner
        ↓
the banner band at the top of the DocSprout home page hero

homepage.capabilities
        ↓
capability cards below the hero on the DocSprout home page

homepage.sections.release_context: false
        ↓
the home page uses the version control in the header without a release pill
```

Open the generated [DocSprout home page](index.md) to see the banner and cards;
[Configuration](configuration.md#add-a-home-page-banner) covers the banner's
placement and asset rules.

Two to four cards share two roomy columns on desktop and tablet home pages,
then stack in one column on a phone. This is part of the default visual system,
so card configuration remains content-only.

## The automatic hero

The home page opens with a hero built from the same plain Markdown: the `h1`,
the first paragraph (unless `introduction` is `false`), an optional release pill
and a call-to-action row. Both actions are derived, never configured:

- **Get started** links to the first listed page that is not the home page;
- **Repository** links to `project.repository_url` when it is an http(s) URL.

Capability cards render below the hero with a decorative icon chosen from each
card title. The accent-derived backdrop, card hover lift and icons are CSS and
inline SVG, so they stay offline and need no MDX, JavaScript framework or
custom HTML. A configured banner renders as a full-width band at the top of
the hero, before the heading.

## Library

Use this when a library home page should make installation and API confidence
easy to scan. It adds three capability cards below the opening introduction
and shows the current release.

```json
{
  "homepage": {
    "capabilities": [
      {"title": "Installable", "description": "Small, versioned Pascal packages."},
      {"title": "Documented API", "description": "Find each public unit quickly."},
      {"title": "Offline", "description": "Build and browse without a CDN."}
    ],
    "sections": {"release_context": true}
  }
}
```

## Application

Use this when the home page should lead with a product banner and story. Save
the banner image in your repository first (the example uses
`docs/assets/project-banner.svg`), then add this:

```json
{
  "banner": {
    "path": "docs/assets/project-banner.svg",
    "alt": "The Acme Desktop application main window"
  },
  "homepage": {
    "capabilities": [],
    "sections": {"banner": true, "introduction": true}
  }
}
```

`banner` is top-level, not a `homepage` value. Its path must point at a file
that already exists in your repository: `docsprout build` stops with a
validation error if it is missing. The banner appears as a full-width band at
the top of the hero, followed by the introduction, and capability cards stay
hidden. Wide artwork works best: the image keeps its proportions and is only
cropped when a taller image exceeds the `10rem` cap. For a checked-in banner
example, build the maintained
[visual fixture](visual-fixtures.md); its local 1200×240 SVG and `banner`
configuration produce the hero band on the fixture's opening page without
editing the fixture first.

## API reference

Use this when readers should reach a reference-oriented home page quickly. It
hides the opening introduction, adds two reference cards, and shows the
current release label.

```json
{
  "homepage": {
    "capabilities": [
      {"title": "Units", "description": "Organised by namespace and purpose."},
      {"title": "Versions", "description": "Release history remains available."}
    ],
    "sections": {
      "introduction": false,
      "release_context": true
    }
  }
}
```

Run `docsprout check` after changing configuration. Its diagnostics identify
the specific card or section field and provide a correction.
