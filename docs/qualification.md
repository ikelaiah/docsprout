# Qualification evidence for DocSprout v1.1.4

DocSprout v1.1.4 is the brand-hero and contrast-proof release for generated
sites, with the v1.0.0 stable contract preserved. The claims below are the
contract that CI and the maintained fixtures exercise, and every row names how
it is verified. "Supported" means the combination is run by automated
qualification on every pull request and release, not merely believed to work.

The v0.17 and v0.18 matrices are retained as historical evidence for the
contract candidate that v1.0.0 freezes. v1 adds the Five Promises assessment,
clean-room package rehearsal and the explicit compatibility policy; v1.1 adds
the rebrand compatibility evidence and the quality-gate additions; v1.1.2 adds
the typography evidence, v1.1.3 adds the documentation-quality evidence, and
v1.1.4 adds the brand-hero and contrast evidence below.

Evidence levels: **automated** rows run in CI with no browser or network
dependency; **manual** rows are explicit review steps; **unavailable** rows are
not claimed as completed when the required browser tooling is absent.

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
  needs Developer Mode or elevation. DocSprout's escape resistance (document
  sources that resolve outside the repository are rejected) is qualified on
  Windows through an unprivileged directory junction; real symlinks are
  covered on Linux and macOS. CI never hides a failure behind this limitation;
  if neither a symlink nor a junction can be created, the test skips with the
  exact reason.

## Package qualification

- Both package forms are built on every release: the wheel and the source
  distribution (`sdist`).
- A dedicated `lint` CI job runs `ruff check` over the source, tests and
  qualification scripts through the `dev` extra; the linter is not a runtime
  dependency.
- Artifact inspection verifies the module set, bundled KaTeX CSS/JS/fonts,
  the `docsprout = docsprout.cli:main` console entry point and the deprecated
  `dockit-fp = docsprout.cli:main_dockit_fp` alias, metadata version, the
  `dockit_fp` compatibility shim, `Requires-Python` and the absence of runtime
  dependencies.
- The wheel and the sdist are each installed into a fresh virtual environment
  and the whole CLI journey below is run **from a directory outside the
  repository**, so DocSprout works as users receive it — never only inside its
  source tree.
- Built sites are scanned to prove generated output embeds no project paths.

## CLI journey

Every command below is exercised through the installed package on a new
project and on an existing repository, asserting meaningful output and
generated files:

- `docsprout init` — safe adoption; existing Markdown and configuration are
  untouched.
- `docsprout check` — buildability gate with section/page/excluded counts.
- `docsprout audit` — read-only publication diagnostics, text and JSON.
- `docsprout build` — complete site with search index, KaTeX assets and
  release metadata.
- `docsprout serve` — deterministic smoke test: starts on localhost, serves a
  generated page and assets over HTTP, then terminates cleanly.
- `docsprout github-pages` — safe Git-repository preparation (below).
- `docsprout doctor` — project diagnosis for preview and release states.
- `docsprout build-all` and `check-release` — covered by the historical
  release suite.
- Rebrand compatibility — a legacy `docs/dockit.json` project loads and builds;
  `python -m dockit_fp --version` and the `dockit-fp` console script answer
  from the same installation; both configuration names at once fail with an
  actionable ambiguity error.

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
- `docsprout github-pages` generates the release-pinned managed workflow;
  reruns are idempotent; `--update` upgrades only a recognised managed
  workflow (canonical `docsprout-pages.yml` or pre-rebrand `dockit-pages.yml`)
  in place and never creates a second deployment workflow; unmanaged or
  malformed workflows are never overwritten.
- DocSprout never commits, pushes, changes repository settings or writes outside
  the managed files — tests assert the Git history and status stay untouched.
- No GitHub API or network access is required by any local operation.
- The generated `docsprout-pages.yml` pins a released tag exactly; the pinned
  `publish-docs.yml` workflow is what the repository's own Pages deployment
  runs after every release tag.

## Accessibility qualification

Automated structural checks run against the maintained visual fixture and
DocSprout's own built documentation:

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
  deterministic copy, load order after DocSprout's styles, correct nested-page
  references and versioned historical builds. DocSprout does not claim the
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
  model (Markdown, `layout.json`, `docsprout.json`, `serve`) and reports the
  inferred sections when it created the layout; `serve` rebuilds are
  regression-tested for `layout.json` and `docsprout.json` changes.

## v0.18.1 additions

The v0.18.1 patch adds a shared `.prose img` default that constrains oversized
Markdown images to the prose column, preserves aspect ratio, and leaves smaller
images at intrinsic size. Regression coverage checks the normal, single-version
and versioned build paths, configured banners, custom-CSS ordering, themes and
content-width settings. The maintained visual fixture carries both an
oversized SVG and a small badge for browser review.

## v1.1.0 additions

The rebrand keeps the v1.0.0 contract and adds explicit evidence that the
pre-rebrand names still work:

- **Distribution and CLI**: the wheel and sdist expose `docsprout` plus the
  deprecated `dockit-fp` alias; `python -m docsprout` is canonical and
  `python -m dockit_fp` plus `from dockit_fp import __version__` are qualified
  from an installed package.
- **Configuration**: a legacy `docs/dockit.json` project passes `check` and
  `build`; when both `docsprout.json` and `dockit.json` exist, the command
  fails with an actionable ambiguity error instead of choosing silently.
- **Output ownership**: the `.docsprout-site` marker is written by every
  build, and a directory carrying the old `.dockit-fp-site` marker is
  recognised and replaced.
- **GitHub Pages**: fresh setup creates `docsprout-pages.yml`; a managed
  `dockit-pages.yml` is recognised and updated in place by `--update` without
  creating a second deployment workflow; unmanaged workflows are never
  overwritten.
- **Browser storage**: generated pages migrate `dockit-fp-theme` and
  `dockit-fp-visual-theme` to the `docsprout-*` keys.

## v1.1.1 additions

The quality patch adds gates and guidance without changing the contract:

- **Legacy guidance**: `init` and `doctor` name the actual configuration file
  on pre-rebrand projects and print the rename step; the regression suite
  covers both the legacy and canonical outputs.
- **Troubleshooting**: every documented failure message has a mapped fix,
  checked for the ambiguity, ownership, workflow and release entries.
- **Lint gate**: a dedicated CI job runs `ruff check` over the source, tests
  and qualification scripts through the `dev` extra; the artifact check still
  rejects any unconditional runtime dependency.
- **Readable shell**: the document template is assembled from named fragments;
  recursive hashes prove the generated sites are byte-identical, and a test
  rejects any `src/docsprout` line longer than 1,000 characters.
- **Repository health**: security policy, code of conduct, issue and pull
  request templates and Dependabot updates are in place.

## v1.1.2 additions

The typography release changes presentation only; no configuration, route or
token value changes:

- **Font stacks**: generated sites resolve a cross-platform system stack
  (`system-ui` first, `ui-monospace` first for code) with no bundled or fetched
  webfont; the stacks are pinned by regression tests and the offline guarantee
  is unchanged.
- **Heading and outline scale**: `h4`–`h6` and `.toc-level-4`–`.toc-level-6`
  are styled, and the maintained visual fixture exercises both.
- **Running text**: `text-wrap:pretty`, `orphans`/`widows`, automatic
  hyphenation outside code, tabular figures in tables and a print stylesheet
  are asserted on the built fixture.
- **Typographic punctuation**: prose converts `--`, `---`, `...` and straight
  quotes while inline code, fenced code, math and link targets stay exact;
  unit tests cover each protected case.
- **Unique heading anchors**: repeated headings receive `-2`, `-3` suffixes;
  the audit keeps warning (DK103) when headings share anchor text.

## v1.1.3 additions

The documentation-quality patch changes guides, tests and the project's own
site configuration; no schema, route or token value changes:

- **Banner dogfooding**: DocSprout's own `docs/docsprout.json` configures the
  home-page banner, and the built home page is asserted to render it above the
  heading while other pages stay banner-free.
- **Copy-paste safety**: every guide example that references a banner, logo or
  custom stylesheet now instructs readers to create the file first; tests pin
  the instruction and the validation-error rule.
- **Error coverage**: troubleshooting maps invalid JSON, invalid field values,
  missing assets, unclosed Markdown blocks, unsupported admonitions and invalid
  version manifests to fixes, and the message-coverage test asserts each.
- **Build guide**: `docsprout build` options, deterministic offline ZIP and
  SHA-256 output, `--root` and the full `doctor` output are documented, with
  the guide linked from navigation, README and troubleshooting.
- **Structure and vocabulary**: the v0.3.0 specification is marked historical,
  the customisation pages state a reading order, the two recipe pages
  distinguish page structure from home-page presentation, and the glossary
  covers the navigation, theme and command vocabulary.

## v1.1.4 additions

The brand-hero and contrast-proof release changes presentation and derives new
values; no schema, route, machine-format or token-name change:

- **Automatic hero**: the built home page is asserted to render one hero with
  its heading, opening summary, release pill and derived Get started/Repository
  actions; non-home pages stay hero-free, and unsafe repository URLs are never
  emitted.
- **Capability card icons**: every card receives a deterministic decorative
  inline SVG chosen from its title; tests count the icons and pin the
  accessible-hidden markup.
- **One accent is enough**: an explicit `theme.accent` without
  `accent_secondary` derives an analogous secondary; tests cover derivation and
  preset preservation.
- **Contrast proof**: WCAG relative luminance and contrast ratios are computed
  per visual style and colour mode; tests assert 4.5:1 interactive-text and
  3:1 focus contrast against every shipped surface, the correction of a failing
  accent, the `check` note and the `DK104` audit warning. A regression test
  keeps the palette surface constants and the stylesheet in sync.

## The Five Promises

| Promise | Qualification evidence | Result |
| --- | --- | --- |
| **Easy to use** | Installed wheel and sdist journeys run `init`, `serve`, `check`, `audit`, `build`, `doctor` and Pages preparation from outside the source tree. | Automated pass |
| **Easy to learn** | README, beginner guide, configuration, publishing, audit and migration paths are checked for the short preview path, declarative mental model and next-step links. | Automated documentation pass |
| **Easy to look good** | Structural accessibility, token, responsive-image, theme/mode, content-width, hero/contrast, custom-CSS and maintained visual-fixture tests cover phone/tablet/desktop cases without brittle screenshots. | Automated pass; see Browser automation status |
| **Easy to create from existing repositories** | Generic/Pascal-shaped, root-README, nested, Unicode, spaces, assets, explicit-home, unlisted and ancillary-file adoption fixtures pass; Pages setup is idempotent and non-mutating. | Automated pass |
| **Easy to maintain** | Schema corpus, route collision checks, machine-format checks, workflow pin checks, deterministic archive/build tests, contributor guidance and release checks pass. | Automated pass |

The stable contract is deliberately smaller than the implementation: see
[Machine-readable contracts](machine-contracts.md) for the exact schema fields,
CLI options, exit semantics, routes, machine files, public tokens and workflow
inputs. The [v1.0 decision record](decisions/0010-v1-stable-contract.md)
records the compatibility and deprecation policy.

## Clean-room release rehearsal

The release gate builds a wheel and sdist, inspects both archives, installs each
into a fresh virtual environment, and runs the installed qualification script
from a temporary working directory outside the source tree. It also rehearses
existing-repository adoption, custom identity/theme/banner/CSS configuration,
single-version Pages preparation, immutable versioned `check-release` and
`build-all`, deterministic output, and local `serve` HTTP delivery. No runtime
operation requires a network connection after installation.

## Known limitations

- Real file-symlink creation on Windows requires Developer Mode or an
  elevated shell; the escape-resistance guarantee is still tested through
  junctions (see Operating systems above).
- Git must be installed and on `PATH` for `build-all`, `check-release` and
  `github-pages`; discovery and previews degrade gracefully without Git.
- Browser automation is intentionally not part of CI: the remaining visual
  checks are the small manual matrix below.
- **Browser automation status:** browser automation is intentionally not part
  of CI (Chrome DevTools MCP was not available during v1.0.0 qualification).
  Full browser geometry, console and keyboard inspection therefore remains
  unavailable for every release, including v1.1.4; the automated
  structural/fixture coverage and live Pages sanity checks are reported
  separately and do not imply a full browser review.
- External URLs in documentation are never network-checked; `audit` reports
  this explicitly.
- Custom CSS is author-owned: its accessibility, contrast and responsiveness
  are not DocSprout claims. The manual matrix below covers the default site; a
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
| 7 | At desktop and phone widths the home-page hero keeps its copy readable, the derived actions stay keyboard reachable, and a configured banner spans the content width without cutting its text. |
