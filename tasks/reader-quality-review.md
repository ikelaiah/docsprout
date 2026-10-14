# Reader experience and maintainability review

Review date: 15 October 2026. Changes are prepared for v1.4.0, based on v1.3.3.

## Findings addressed

- **Nested-page search:** Resolve entry URLs against the search index. Browser
  checks follow a result from a nested route under `/preview/`.
- **Search interaction:** Preserve the query on Escape, prevent hidden results
  from opening with Enter, reopen with ArrowDown, and respect dismissal when a
  delayed index arrives. Keyboard and loading checks pass.
- **Search recovery:** Validate entries when the index loads and distinguish
  loading, unavailable, and no-match states. Checks cover HTTP, JSON and
  entry-shape failures, an empty index, and the legacy array.
- **Markdown lists:** Retain ordered-list starting numbers and keep mixed
  nested lists attached to the intended parent. Regression tests cover both.
- **Keyboard access:** Keep the skip link in WebKit's default Tab sequence
  with `tabindex="0"`. Browser checks confirm Tab reaches it and Enter focuses
  the article.
- **Browser qualification:** Add a shared Playwright harness, pinned
  development-only npm dependency, local server under a path prefix, and an
  isolated CI job for each browser. CI preserves logs, results, and screenshots
  for 14 days.
- **Docs and diagrams:** Add a full-size diagram link and equivalent prose,
  explain local-file search restrictions and recovery, and demonstrate resumed
  numbered steps.

## Verification

- `python -m unittest discover -s tests -t . -v`: **337 tests passed** on
  Windows with Python 3.13.5. The two affected accessibility tests passed
  again after a final test cleanup.
- `ruff check .`, `node --check tests/browser_reader.mjs`, and
  `git diff --check` pass.
- `docsprout check` passes for 41 pages. `docsprout audit --strict` reports
  zero errors and warnings; it does not check external URLs.
- `docsprout build --output build/final-quality-site` builds all 41 pages.
- On Node 24.21.0 with Playwright 1.63.0, Chromium 153.0.8010.12 and
  Playwright WebKit 26.6 pass nested links, keyboard behavior, delayed/error/
  empty states, image descriptions, heading order, focus checks, keyboard
  operation of page-outline and mobile disclosures, print navigation, and 32
  diagram/theme cases each.
- The page is served under `/preview/`; result links keep that prefix. The
  visual matrix covers 320, 768, 1024 and 1440 pixels, four themes, and light
  and dark modes. Phone and desktop screenshots were inspected in both modes;
  diagram labels remain readable at phone width.
- The CI workflow YAML parses and its Chromium/Firefox/WebKit matrix,
  30-minute limit, debug console capture, and `always()` artifact upload were
  checked. GitHub Actions evidence is pending the release candidate PR.

Useful screenshots are in ignored `build/reader-artifacts/`:

- [Phone diagram, 320px](../build/reader-artifacts/webkit-diagram-320.png)
- [Desktop diagram, 1440px](../build/reader-artifacts/webkit-diagram-1440.png)
- [Phone, dark](../build/reader-artifacts/webkit-320-classic-dark.png) and
  [phone, light](../build/reader-artifacts/webkit-320-classic-light.png)
- [Desktop, dark](../build/reader-artifacts/webkit-1440-paper-dark.png) and
  [desktop, light](../build/reader-artifacts/webkit-1440-paper-light.png)

Per-browser logs, `build.log`, `run.log`, and `results.json` are saved beside
them. CI also preserves the browser `console.log`.

## Limits

The installed Playwright Firefox launches but cannot spawn its tab subprocess in
this Windows sandbox (`Error:-2147024809`); `browserContext.newPage()` fails
before DocSprout code runs. Firefox remains in the Ubuntu CI matrix, which has
not yet run from this workspace. Playwright WebKit is not the Safari app. No
screen reader was available for actual observation; `docs/visual-fixtures.md`
gives a short NVDA/VoiceOver procedure. Playwright WebKit is not Safari, and no
screen reader was available here; retain those as manual checks. The CI job
will provide qualification evidence after the release candidate runs.
