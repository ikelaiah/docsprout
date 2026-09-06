# Choose colours and a visual theme

You do not need CSS to give a DocKit site its own identity. Start with one
colour preset and one visual style in `docs/dockit.json`:

```json
{
  "schema_version": 1,
  "project": {"name": "MyLibrary-FP"},
  "theme": {
    "preset": "purple",
    "style": "paper"
  }
}
```

## Two choices that do different jobs

Visitors can choose a **Mode**: **System**, **Light** or **Dark**. System
follows their browser or operating-system preference. You do not need to
configure modes.

You choose the site's starting **Style**:

- **Classic** (`classic`) is the clean, dependable default;
- **Paper** (`paper`) gives long guides a warm reading surface;
- **Midnight** (`midnight`) starts with a dark technical look.

Visitors can switch the Style too. DocKit remembers both choices in
the browser when storage is available.

The maintained
[single-version example](https://github.com/ikelaiah/dockit-fp/tree/v0.17.0/examples/single-version)
starts in Paper (`"style": "paper"`), so its built opening page shows the
warm reading surface before a visitor changes the control.

Classic is the showcase default: it keeps the header, navigation and reading
surface quiet so ordinary Markdown supplies the personality. Paper and
Midnight use the same spacing, typography and semantic states, with their own
reading surfaces. No custom CSS is needed to make any of them publication-ready.

## Pick an accent colour

The supported presets are:

| Preset | Good starting point for |
| --- | --- |
| `blue` | A familiar general-purpose site |
| `teal` | Libraries and developer tools |
| `ocean` | A calm technical site |
| `purple` | A more distinctive project identity |

Each preset provides link and highlight colours for both light and dark modes.

If your project already has accessible brand colours, you can provide exact
hexadecimal values:

```json
{
  "schema_version": 1,
  "project": {"name": "MyLibrary-FP"},
  "theme": {
    "accent": "#0f766e",
    "accent_secondary": "#0891b2",
    "style": "classic"
  }
}
```

Test custom colours in both Light and Dark mode. Links, selected navigation and
keyboard focus must remain easy to see. A preset is safer when you are unsure.
The maintained
[minimal example](https://github.com/ikelaiah/dockit-fp/tree/v0.17.0/examples/minimal)
uses the exact teal values shown above; its built links, selected navigation
and focus state use that accent.

## Add a banner only when it helps

A home-page banner can show a project logo or useful illustration. Keep the
image inside your repository and describe it for people who cannot see it:

```json
{
  "schema_version": 1,
  "project": {"name": "MyLibrary-FP"},
  "banner": {
    "path": "docs/assets/project-banner.svg",
    "alt": "MyLibrary-FP logo"
  }
}
```

The `alt` text should communicate the image's meaning. Use empty `alt` text only
when the image is purely decorative and adds no information.

The maintained [visual fixture](visual-fixtures.md) configures the local
`docs/assets/visual-fixture-banner.svg` asset. Build that fixture to see its
banner above the opening content; it is the reproducible banner example, not a
configuration you need to edit by hand.

Run `dockit-fp check` after every configuration change. The maintained
[visual fixtures](visual-fixtures.md) explain how to review phone, tablet,
desktop, keyboard and colour-mode behaviour.
