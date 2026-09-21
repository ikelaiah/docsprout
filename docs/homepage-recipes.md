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
[`docs/docsprout.json`](https://github.com/ikelaiah/docsprout/blob/v1.1.3/docs/docsprout.json)
contains a home-page banner, capability cards and release context:

```json
{
  "banner": {
    "path": "docs/assets/docsprout-banner.svg",
    "alt": "DocSprout banner — Build documentation people can use."
  },
  "homepage": {
    "capabilities": [
      {"title": "Existing-project friendly", "description": "Start with the README and docs you already have."},
      {"title": "Offline/local assets", "description": "Built sites work without a CDN."}
    ],
    "sections": {"release_context": true}
  }
}
```

```text
docs/docsprout.json
        ↓
banner
        ↓
the banner image above the home page heading on the DocSprout home page

homepage.capabilities
        ↓
capability cards below the opening summary on the DocSprout home page

homepage.sections.release_context
        ↓
the current release label above the DocSprout home page
```

Open the generated [DocSprout home page](index.md) to see all three effects;
[Configuration](configuration.md#add-a-home-page-banner) covers the banner's
placement and asset rules.

The built-in presentation adapts to the number of cards: two, three and four
cards form balanced columns on a desktop, then move to two columns on a tablet
and one column on a phone. This is part of the default visual system, so card
configuration remains content-only.

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
validation error if it is missing. The banner appears above the heading,
followed by the introduction, and capability cards stay hidden. Wide artwork
works best: the image spans the content width and is capped at `16rem` tall.
For a checked-in banner example, build the maintained
[visual fixture](visual-fixtures.md); its local 1200×240 SVG and `banner`
configuration produce the image above the fixture's opening content without
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
