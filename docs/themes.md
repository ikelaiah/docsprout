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
[single-version example](https://github.com/ikelaiah/dockit-fp/tree/v0.18.1/examples/single-version)
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
[minimal example](https://github.com/ikelaiah/dockit-fp/tree/v0.18.1/examples/minimal)
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

## The documented `--dk-*` tokens

Since v0.18, the public customisation token family is namespaced `--dk-*`.
These tokens are ordinary CSS custom properties defined on the document root
in every visual theme and colour mode. They are usable from the [custom CSS
escape hatch](custom-css.md) and by any tooling that reads generated styles:

| Token | Meaning |
| --- | --- |
| `--dk-accent` | primary accent (links, selection, active navigation) |
| `--dk-accent-secondary` | secondary accent (hover underlines, highlights) |
| `--dk-bg` | page background |
| `--dk-surface` | elevated surfaces (controls, code chips, callouts) |
| `--dk-text` | primary text |
| `--dk-muted` | secondary text and quiet labels |
| `--dk-border` | separators and control borders |
| `--dk-code-bg` | code block background |
| `--dk-code-text` | code text colour |
| `--dk-raised` | popup/raised surfaces (search results) |
| `--dk-focus-ring` | visible keyboard focus colour |
| `--dk-interactive` | interactive foreground colour derived from the accent |
| `--dk-content-width` | prose column width |
| `--dk-reading-width` | comfortable reading measure inside the prose column |
| `--dk-shell-width` | full page layout width |

These fifteen tokens are the documented customisation contract for 1.x.
Classic, Paper and Midnight each define them in Light, Dark and System modes;
the contract is regression-tested. **Internal** variables that DocKit uses but
does not document—radii, fonts, spacing scales, shadow, control heights and
anything else whose name begins with `--dk-`—are not part of the contract and
may change between releases. Pre-1.0 note: v0.18 renamed the earlier generic
tokens (`--bg`, `--text`, `--interactive`, …) to this family; see the
[Migration guide](migration.md) if you referenced the old names.

## Custom CSS: the advanced escape hatch

Custom CSS is optional, advanced and repository-local. It loads after
DocKit's styles so it can deliberately override them, and DocKit guarantees
the safe inclusion mechanics—but the accessibility of the CSS you write is
your responsibility. Ordinary sites need [presets and exact
colours](themes.md#pick-an-accent-colour) only. See
[Custom CSS (advanced)](custom-css.md) for the complete contract and the
maintained example.

Run `dockit-fp check` after every configuration change. The maintained
[visual fixtures](visual-fixtures.md) explain how to review phone, tablet,
desktop, keyboard and colour-mode behaviour.
