# Choose colours and a visual theme

This page is the colour and style reference in the
[customisation order](configuration.md#changing-colours-logo-and-presentation).
You do not need CSS to give a DocSprout site its own identity. Start with one
colour preset and one visual style in `docs/docsprout.json`:

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

- **Classic** (`classic`) pairs crisp surfaces with accent-edged section
  headings;
- **Paper** (`paper`) sets long guides on a warm, layered reading sheet with
  lighter serif headings, italic introductory copy and an editorial drop cap;
- **E-ink** (`e-ink`) pairs square, flat surfaces with monospace controls,
  a double-rule page title and still, shadow-free cards;
- **Glassmorphic** (`glassmorphic`) adds softly lit, frosted panels, rounded
  controls and a gradient hero title.

Visitors can switch the Style too. DocSprout remembers both choices in
the browser when storage is available.

Links follow one system in every style: inline content links carry a
persistent underline, because colour alone never identifies them; navigation
chrome—the sidebar, contents, search results, page navigation and
footer—never underlines, signalling hover with a background tint or colour
shift instead, and buttons never underline.

The maintained
[single-version example](https://github.com/ikelaiah/docsprout/tree/v1.1.4/examples/single-version)
starts in Paper (`"style": "paper"`), so its built opening page shows the
warm reading surface before a visitor changes the control.

Classic is the showcase default: it keeps the header, navigation and reading
surface quiet so ordinary Markdown supplies the personality. Paper, E-ink and
Glassmorphic share the same spacing and semantic states, with their own reading
surfaces, typography and chrome. No custom CSS is needed to make any
of them publication-ready.

All four share the same component rules, with theme tokens controlling their
corners and materials in both colour modes. Typography and decoration use local
CSS and system fonts, with no additional downloads.

## E-ink and Glassmorphic in practice

**E-ink** is an ink-on-paper manual: flat white or near-black surfaces, ruled
headings, square corners, permanently underlined links, grid-bordered
tables and an undecorated hero—no shadows, no gradients. Brand decorations such
as the reading-progress bar, callout rails and text selection stay ink-toned
rather than accent-coloured. Code blocks stay dark panels so syntax highlighting
remains readable. It suits long-form reading and displays where colour is
unreliable; its dark variant is a dimmed night-reading surface rather than a
saturated dark theme.

**Glassmorphic** puts a viewport-anchored mesh of soft accent tints behind
frosted chrome: the header, hero, navigation panels, cards and search float on
translucent, blurred layers with specular edges and larger rounded corners. The
hero title carries an accent gradient where the browser supports background
text clipping, and falls back to the solid text colour elsewhere. Titles that
open with an emoji keep solid ink everywhere so the glyph survives. The
mesh tint is capped per stop and translucent surfaces stay mostly opaque, so
every text combination is covered by the same build-time contrast proof as the
other styles; browsers without `backdrop-filter` fall back to the solid surface
tokens, so the style never depends on the blur effect.

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
[minimal example](https://github.com/ikelaiah/docsprout/tree/v1.1.4/examples/minimal)
uses the exact teal values shown above; its built links, selected navigation
and focus state use that accent.

## One accent is enough

You do not have to choose two colours. When you set `theme.accent` without
`accent_secondary`, DocSprout derives an analogous secondary from it, so a
single brand colour still produces a complete theme. An explicit `accent`
overrides the preset's accent, and the derived secondary then comes from that
accent, not from the preset pair. Curated presets keep their documented colour
pair when you do not set an accent.

DocSprout also proves the brand colour against every reading surface it ships.
Link (`--dk-interactive`) and focus (`--dk-focus-ring`) values are computed for
each visual style and colour mode: the exact accent is kept wherever it meets
WCAG AA contrast, and a verification-safe variant is substituted where it
cannot. If your accent fails AA on the light page background,
`docsprout check` prints a note and `docsprout audit` reports `DK104` with the
corrected colour. Decorative surfaces keep using the exact accent you
configured, and filled actions use an internal `--dk-on-interactive` foreground
chosen for contrast.

## Add a banner only when it helps

A home-page banner can show a project logo or useful illustration. It renders
as a full-width band at the top of the home-page hero, above the heading. Save
the image inside your repository first, then reference it and describe it for
people who cannot see it. The file must already exist: `docsprout build` stops
with a validation error when it is missing or unsafe.

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

Since v0.18, the public customisation token family is namespaced `--dk-*`;
v1.0.0 is the stable commitment to the documented family. v1.1.0 renews
that commitment under the DocSprout name without changing a single token.
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
Classic, Paper, E-ink and Glassmorphic each define them in Light, Dark and System modes;
the contract is regression-tested. **Internal** variables that DocSprout uses but
does not document—radii, fonts, spacing scales, shadow, control heights and
anything else whose name begins with `--dk-`—are not part of the contract and
may change between releases. Pre-1.0 note: v0.18 renamed the earlier generic
tokens (`--bg`, `--text`, `--interactive`, …) to this family; see the
[Migration guide](migration.md) if you referenced the old names.

## Custom CSS: the advanced escape hatch

Custom CSS is optional, advanced and repository-local. It loads after
DocSprout's styles so it can deliberately override them, and DocSprout guarantees
the safe inclusion mechanics—but the accessibility of the CSS you write is
your responsibility. Ordinary sites need [presets and exact
colours](themes.md#pick-an-accent-colour) only. See
[Custom CSS (advanced)](custom-css.md) for the complete contract and the
maintained example.

Run `docsprout check` after every configuration change. The maintained
[visual fixtures](visual-fixtures.md) explain how to review phone, tablet,
desktop, keyboard and colour-mode behaviour.
