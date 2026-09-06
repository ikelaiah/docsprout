# Qualification

DocKit v0.17 is the qualification release: the claims below are the contract
that CI enforces today, and every row names how it is verified. "Supported"
means the combination is exercised by the automated qualification on every
pull request and release, not merely believed to work.

v0.18.0 is the final pre-1.0 simplification and contract-candidate release.
The v0.17 matrix is retained unchanged and extended with the v0.18 rows at the
end of this page.

Vertices: **automated** rows run in CI with no browser or network dependency;
**manual** rows are small, explicit browser checks listed at the end.

## Supported Python versions

- Python 3.10, 3.11, 3.12, 3.13 and 3.14 on Linux, the full stable matrix.
- `requires-python = ">=3.10"` and the package classifiers agree with the
  tested matrix.
- Python 3.15 pre-release builds are exercised as a non-blocking
  forward-compatibility signal; they are not a support commitment.
- Verification: `python-matrix` CI job runs the complete unit suite on every
  listed version.

## Qualified operating systems

- Linux, Windows and macOS.
- Windows and macOS run the complete unit suite on Python 3.10 (minimum) and
  3.14 (latest stable). The full matrix stays on Linux to keep CI efficient.
- Path handling, temporary directories, subprocess invocations, encoding,
  repository discovery and generated routes are exercised on every OS.
- Windows symlink limitations: creating a real file symlink below `docs/`
  needs Developer Mode or elevation. DocKit's escape resistance (document
  sources that resolve outside the repository are rejected) is qualified on
  Windows through an unprivileged directory junction; real symlinks are
  covered on Linux and macOS. CI never hides a failure behind this limitation;
  if neither a symlink nor a junction can be created, the test skips with the
  exact reason.

## Package qualification

- Both package forms are built on every release: the wheel and the source
  distribution (`sdist`).
- Artifact inspection verifies the module set, bundled KaTeX CSS/JS/fonts,
  the `dockit-fp = dockit_fp.cli:main` console entry point, metadata version,
  `Requires-Python` and the absence of runtime dependencies.
- The wheel and the sdist are each installed into a fresh virtual environment
  and the whole CLI journey below is run **from a directory outside the
  repository**, so DocKit works as users receive it — never only inside its
  source tree.
- Built sites are scanned to prove generated output embeds no project paths.

## CLI journey

Every command below is exercised through the installed package on a new
project and on an existing repository, asserting meaningful output and
generated files:

- `dockit-fp init` — safe adoption; existing Markdown and configuration are
  untouched.
- `dockit-fp check` — buildability gate with section/page/excluded counts.
- `dockit-fp audit` — read-only publication diagnostics, text and JSON.
- `dockit-fp build` — complete site with search index, KaTeX assets and
  release metadata.
- `dockit-fp serve` — deterministic smoke test: starts on localhost, serves a
  generated page and assets over HTTP, then terminates cleanly.
- `dockit-fp github-pages` — safe Git-repository preparation (below).
- `dockit-fp doctor` — project diagnosis for preview and release states.
- `dockit-fp build-all` and `check-release` — covered by the historical
  release suite.

## Repository shapes

A small set of representative shapes sustains the build, navigation and
publication contract (see `tests/test_qualification_shapes.py`):

- repository-root `README.md` as home
- `docs/index.md` only
- explicit `layout.json.home`
- `"unlisted": "exclude"`
- nested documentation folders
- local and nested assets
- file and folder names containing spaces
- Unicode file names and headings
- a repository path containing spaces
- multi-level navigation with previous/next chains
- root README together with `docs/`
- ancillary Markdown (`CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`,
  `CODE_OF_CONDUCT.md`) that is reported but never published by surprise
- a generic non-Pascal repository and a Pascal-oriented repository

## Ecosystem and GitHub Pages

- Ordinary non-Git projects work end to end; `github-pages` refuses them
  with clear guidance.
- Git repositories with and without a GitHub remote are qualified.
- `dockit-fp github-pages` generates the release-pinned managed workflow;
  reruns are idempotent; `--update` upgrades only a recognised DocKit
  workflow; unmanaged or malformed workflows are never overwritten.
- DocKit never commits, pushes, changes repository settings or writes outside
  the managed files — tests assert the Git history and status stay untouched.
- No GitHub API or network access is required by any local operation.
- The generated `dockit-pages.yml` pins a released tag exactly; the pinned
  `publish-docs.yml` workflow is what the repository's own Pages deployment
  runs after every release tag.

## Accessibility qualification

Automated structural checks run against the maintained visual fixture and
DocKit's own built documentation:

- every interactive control is a native keyboard-operable element
- visible `:focus-visible` indicators in every theme, including forced-colors
  support
- accessible names for search, version, style, mode, navigation regions and
  copy controls
- search: `aria` wiring, visible help text, keyboard result movement
  (Arrow/Home/End/Enter/Escape), `/` shortcut
- mobile navigation is a native disclosure
- previous/next navigation labels and relationships
- one `h1` per page, no heading-level jumps, usable `id` anchors
- safe links and images with alternative text
- callouts carry a text label, never colour alone
- reduced-motion rule preserved
- code blocks and tables scroll inside their own frames; no page-level
  horizontal overflow
- Light/Dark/System coherence and the shared semantic token contract for
  Classic, Paper and Midnight

## v0.18 additions

The v0.17 matrix above is unchanged. v0.18 adds:

- **Canonical declarative editing model**: regression tests cover the
  layout.json operations table (add/remove/rename/reorder/move pages,
  sections, home) against canonical configurations, and the beginner guides
  are kept synchronized with maintained examples.
- **Strict configuration diagnostics**: unknown fields in schema-1 objects
  are rejected with a `Did you mean` suggestion; valid configuration from
  every released 0.x tag is proven loadable by the automated compatibility
  corpus test.
- **Custom CSS contract**: `theme.custom_css` is qualified for safe path
  resolution (repository-local only, `.css` only, traversal/absolute/symlink
  escape rejected), missing-file and wrong-extension diagnostics,
  deterministic copy, load order after DocKit's styles, correct nested-page
  references and versioned historical builds. DocKit does not claim the
  accessibility of arbitrary user CSS; only the inclusion mechanics are
  qualified.
- **`--dk-*` public token family**: every documented public token is defined
  in Classic, Paper and Midnight × Light, Dark and System; the legacy generic
  token names are proven absent; internal implementation variables are not
  part of the assertions.
- **Route collision protection**: exact and case-insensitive route collisions
  fail the build with an actionable error before output is written.
- **Versioned machine formats**: `search-index.json` and
  `audit --format json` carry `"schema_version": 1`; consumers (browser
  search and tests) are updated in lockstep and regression-tested.
- **`init` guidance**: the post-initialisation output teaches the mental
  model (Markdown, `layout.json`, `dockit.json`, `serve`) and reports the
  inferred sections when it created the layout; `serve` rebuilds are
  regression-tested for `layout.json` and `dockit.json` changes.

## Known limitations

- Real file-symlink creation on Windows requires Developer Mode or an
  elevated shell; the escape-resistance guarantee is still tested through
  junctions (see Operating systems above).
- Git must be installed and on `PATH` for `build-all`, `check-release` and
  `github-pages`; discovery and previews degrade gracefully without Git.
- Browser automation is intentionally not part of CI: the remaining visual
  checks are the small manual matrix below.
- External URLs in documentation are never network-checked; `audit` reports
  this explicitly.
- Custom CSS is author-owned: its accessibility, contrast and responsiveness
  are not DocKit claims. The manual matrix below covers the default site; a
  project that adds `theme.custom_css` should repeat the relevant checks
  with its stylesheet applied.
- If a project uses `theme.custom_css`, the documented `--dk-*` tokens still
  resolve because they are ordinary custom properties on the document root;
  internal `--dk-*` implementation variables are not supported for custom
  stylesheets.

## Manual browser/keyboard matrix

Run these against a locally built site (the visual fixture covers the widest
surface) after major visual or interaction changes; they complement the
automated contract above.

| # | Check |
| --- | --- |
| 1 | Tab from the address bar through search, version, style and mode controls, copy buttons, previous/next and every sidebar link; focus is always visible. |
| 2 | `/` focuses search; type a query; ArrowDown/ArrowUp, Home, End, Enter and Escape behave as described; Tab leaves the result region predictably. |
| 3 | At phone width the mobile navigation opens and closes with Enter/Space on the disclosure and every section link is reachable by keyboard. |
| 4 | Screenshot phone/tablet/desktop widths in Classic, Paper and Midnight × System, Light and Dark; nothing overlaps and no page-level horizontal scroll appears. |
| 5 | With the OS reduced-motion preference on, search results, the reading-progress bar and theme changes do not animate. |
| 6 | With Windows high-contrast / forced-colors enabled, focus outlines and the reading-progress indicator remain visible. |