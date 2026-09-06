# Customize the home page

The home page is the Markdown document selected by `layout.json.home`, rendered
as the site's `index.html`. It may be a listed page under `docs/` or the
repository-root `README.md` with `"source": "root"`. The `homepage` object in
`docs/dockit.json` only changes the selected home page's presentation; it does
not choose the document. You do not need it unless you want to customise the
landing page.

The examples below are `homepage` values to add to your existing
`docs/dockit.json`; keep your `schema_version`, `project` and other settings.

## See it in DocKit

DocKit uses the same configuration on this site. Its
[`docs/dockit.json`](https://github.com/ikelaiah/dockit-fp/blob/v0.18.0/docs/dockit.json)
contains capability cards and release context:

```json
{
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
docs/dockit.json
        ↓
homepage.capabilities
        ↓
capability cards below the opening summary on the DocKit home page

homepage.sections.release_context
        ↓
the current release label above the DocKit home page
```

Open the generated [DocKit home page](index.md) to see both effects.

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

Use this when the home page should lead with a product banner and story. After
you add the image at the configured path, it shows the banner and introduction
but hides capability cards.

```json
{
  "banner": {"path": "docs/assets/banner.png", "alt": "The Acme Desktop application"},
  "homepage": {
    "capabilities": [],
    "sections": {"banner": true, "introduction": true}
  }
}
```

For a checked-in banner example, build the maintained
[visual fixture](visual-fixtures.md). Its local SVG and `banner` configuration
produce the image above the fixture's opening content without editing the
fixture first.

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

Run `dockit-fp check` after changing configuration. Its diagnostics identify
the specific card or section field and provide a correction.
