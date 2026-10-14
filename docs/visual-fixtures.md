# Visual fixtures

The maintained project in `examples/visual-fixtures` exercises the automatic
hero with its derived actions and card icons, typography,
ordered and nested lists, the full `h1`–`h6` heading and outline scale,
typographic punctuation, inline code, definition lists, fenced Pascal with
language-labelled code bars, wide
tables, callouts, search, theme controls, page navigation, a long document,
the reading-progress indicator, responsive Markdown images and a home-page
banner. Its checked-in
`docs/docsprout.json` configures `docs/assets/visual-fixture-banner.svg`, so every
fixture build includes the banner as hero artwork without a manual
file edit. The checked-in image is a 1200×240 SVG: a teal field with a light
document mark and the words "Visual fixture".

Build it locally:

```powershell
$env:PYTHONPATH='src'
python -m docsprout build `
  --root examples/visual-fixtures `
  --output build/visual-fixtures
python -m docsprout build `
  --root examples/minimal `
  --output build/minimal
```

Open `build/visual-fixtures/index.html`, then verify this matrix. Browser
content is expected to remain fully local and the console should have no
errors or warnings.

| View | Width | Checks |
| --- | ---: | --- |
| Phone | 320px, 360px and 390px | Native navigation disclosure, visible copy control, no page overflow; the header loses its brand row after scrolling while search and settings stay available; the hero stacks its banner band above the copy, action buttons wrap, oversized Markdown images stay within the prose column and small badges remain intrinsic |
| Tablet | 768px | Search and controls wrap cleanly, readable table scrolling, responsive Markdown images; the long-form page has a closed, keyboard-operable “On this page” disclosure after its title |
| Narrow desktop | 1024px | Article measure and heading rhythm remain balanced; the long-form page uses the inline outline instead of a right rail |
| Desktop | 1440px | Sidebar, article and on-page outline align without crowding; the hero banner spans the content width without cutting its text; card icons align on the card baseline; oversized Markdown images stay within the prose column |
| Long document | Above 1024px | Heading rhythm, reading progress and sticky local navigation |

At each useful width, switch among Classic, Paper, E-ink and
Glassmorphic and repeat with Light and Dark. Use only the keyboard to focus search with `/`, move among
results with Arrow keys/Home/End, close results with Escape, and tab through
version, visual-theme and colour controls. Every focus indicator must be
visible and every control must retain an accessible name.

On `long-form.html`, check that its section label sits above the title and
that Previous names its destination's section. Expand the inline outline with
the keyboard at 1024px and below, follow a nested heading link, and check that
the heading is visible below the sticky header. Reopen the outline and check
that the current section is marked, as it is in the desktop outline. On
scroll, the outline must keep the open or closed state you chose; tracking the
active section must not reopen it. On `build/minimal/quick-start.html`, check
that a page without section headings
has no empty outline or reserved right column, and that Previous names the
destination's section. Repeat these checks in print preview: the section label
remains, while page navigation and both versions of the outline are omitted.

From the top of each page, press Tab once and use **Skip to content**. Focus
should move to the article below the header. On a phone, scroll until the
brand row collapses, then focus the brand with the keyboard to reveal it
without hiding search or settings. On the long-form page, the progress bar
should reach its end as the last article content reaches the viewport bottom,
before the page navigation and footer.

With a screen reader, confirm that the disclosure announces its collapsed and
expanded state, the "Page outline" navigation is labelled, and the current
section link is announced after opening it.

The fixture sets `layout.content_width` to `wide` so table and code behavior is
easy to inspect. The maintained minimal example uses `compact`; DocSprout's own
site uses the omitted `comfortable` default. Together, those checked-in builds
cover the semantic width contract. The checked-in banner is the canonical visual
banner state; use a separate temporary project when you need to inspect the
optional no-banner default.

DocSprout's own [Architecture](architecture.md#follow-one-build) page includes
a vertical SVG build diagram. Check its label legibility at 320px and 1440px,
in light and dark mode. It must remain within the article width; its nearby
prose must explain the same sequence without relying on the image.

The repository's `tests/browser_reader.mjs` automates the architecture-page
width/theme checks, accessible focus order, page-outline and mobile navigation
disclosures, and search keyboard, loading and error cases in Chromium, Firefox
and WebKit. Setup and
commands are in `CONTRIBUTING.md`. Keep the manual fixture checks above for
code copying, tables, print output and screen-reader behavior. WebKit here
means Playwright's WebKit build; it does not qualify Apple's Safari.

With NVDA on Windows or VoiceOver on macOS, start at the top of the long-form
fixture. Confirm the skip link moves focus to the article, the mobile and page
outline disclosures announce collapsed and expanded state, search announces
its name and result updates, and the current heading link is announced as the
location changes. Record the browser, screen reader and observed result; the
automated browser suite cannot make these screen-reader observations.

The fixture is also the maintained [custom CSS](custom-css.md) example: its
`docs/assets/custom.css` uses the documented `--dk-*` tokens, every built page
loads it after DocSprout's styles, and CI builds the fixture on every change, so
the safe inclusion mechanism is always exercised.
