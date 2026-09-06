# Visual fixtures

The maintained project in `examples/visual-fixtures` exercises typography,
ordered and nested lists, inline code, definition lists, fenced Pascal, wide
tables, callouts, search, theme controls, page navigation, a long document,
the reading-progress indicator and a home-page banner. Its checked-in
`docs/dockit.json` configures `docs/assets/visual-fixture-banner.svg`, so every
fixture build includes the banner above the opening content without a manual
file edit.

Build it locally:

```powershell
$env:PYTHONPATH='src'
python -m dockit_fp build `
  --root examples/visual-fixtures `
  --output build/visual-fixtures
```

Open `build/visual-fixtures/index.html`, then verify this matrix. Browser
content is expected to remain fully local and the console should have no
errors or warnings.

| View | Width | Checks |
| --- | ---: | --- |
| Phone | 360px and 390px | Native navigation disclosure, visible copy control, no page overflow |
| Tablet | 768px | Search and controls wrap cleanly, readable table scrolling |
| Narrow desktop | 1024px | Article measure, heading rhythm and compact navigation remain balanced |
| Desktop | 1440px | Sidebar, article and on-page outline align without crowding |
| Long document | 1024px or wider | Heading rhythm, reading progress and sticky local navigation |

At each useful width, switch among Classic, Paper and Midnight and repeat with
Light and Dark. Use only the keyboard to focus search with `/`, move among
results with Arrow keys/Home/End, close results with Escape, and tab through
version, visual-theme and colour controls. Every focus indicator must be
visible and every control must retain an accessible name.

The fixture sets `layout.content_width` to `wide` so table and code behavior is
easy to inspect. The maintained minimal example uses `compact`; DocKit's own
site uses the omitted `comfortable` default. Together, those checked-in builds
cover the semantic width contract. The checked-in banner is the canonical visual
banner state; use a separate temporary project when you need to inspect the
optional no-banner default.

The fixture is also the maintained [custom CSS](custom-css.md) example: its
`docs/assets/custom.css` uses the documented `--dk-*` tokens, every built page
loads it after DocKit's styles, and CI builds the fixture on every change, so
the safe inclusion mechanism is always exercised.
