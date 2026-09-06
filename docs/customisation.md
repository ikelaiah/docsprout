# Customising sections and identity

Use configuration to rename sections, choose colours, add project links and use
a small project mark in the header.
DocKit keeps the page layout and accessibility behaviour working, so you do
not need to copy or maintain its CSS.

## Before and after: navigation

Edit the `navigation` value inside your existing `docs/layout.json`; leave its
`schema_version`, `home` and `unlisted` entries unchanged. Before, a small site
has one section:

```json
{"navigation": [{"title": "Getting started", "pages": [{"title": "Overview", "path": "index.md"}]}]}
```

After, replace that `navigation` value with deliberate groups in the same
written order:

```json
{"navigation": [
  {"title": "Getting started", "pages": [{"title": "Overview", "path": "index.md"}]},
  {"title": "Reference", "pages": [{"title": "API", "path": "reference/api.md"}]}
]}
```

## Before and after: project identity

### Before (default configuration)

With no `theme` or `identity` object, this configuration uses DocKit's default
blue colour preset and its built-in document mark:

```json
{
  "schema_version": 1,
  "project": {"name": "Example-FP"}
}
```

The top header shows the built-in document mark immediately before
`Example-FP`. Its accent and highlight colour use the default blue pair. There
is no custom identity footer or link, so generated pages have no identity
footer at their bottom.

### After (DocKit's own configuration)

DocKit's documentation site uses this curated non-default preset and local
identity asset:

```json
{
  "schema_version": 1,
  "project": {"name": "DocKit"},
  "theme": {"preset": "purple"},
  "identity": {
    "logo": "docs/assets/dockit-mark.svg",
    "footer": "Built with DocKit.",
    "links": [{"label": "Project", "url": "https://github.com/ikelaiah/dockit-fp"}]
  }
}
```

You can inspect the complete maintained
[`docs/dockit.json`](https://github.com/ikelaiah/dockit-fp/blob/v0.17.0/docs/dockit.json)
and its [local SVG asset](https://github.com/ikelaiah/dockit-fp/blob/v0.17.0/docs/assets/dockit-mark.svg).
On generated DocKit pages, purple is the accent and highlight colour; the
DocKit mark appears immediately before the project name in the top header;
`Built with DocKit.` appears at the bottom in the footer; and the `Project`
link appears in that same footer.

## Add a header logo

`identity.logo` is an optional repository-local path to an SVG or PNG. The
DocKit configuration above is the maintained logo example: it copies
`docs/assets/dockit-mark.svg` into the built site and shows it immediately
before `DocKit` in the top header. Use its configuration and asset together as
the starting point for your own mark.

Create your image at the configured path before building. Paths must stay
inside the repository; absolute paths, parent-directory traversal and other
image formats are rejected. The logo is constrained to a small square header
area and uses `object-fit: contain`, so unusually wide or tall marks keep their
aspect ratio without pushing the title or controls out of place.

The project name remains the accessible name of the header link. The image is
decorative because the adjacent text already names the project. Omit
`identity.logo` to retain DocKit's built-in document mark.
