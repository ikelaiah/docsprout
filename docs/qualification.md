# Qualification evidence for DocSprout v1.3.2

DocSprout v1.3.2 is a code-safety and documentation-quality patch that preserves
JSON and Markdown layout compatibility and the v1.0.0 stable contract. The claims below are the contract that CI and the maintained fixtures
exercise. Every row names how it is verified. "Supported" means the combination
is run by automated qualification on every pull request and release, not merely
believed to work.

Evidence levels: **automated** rows run in CI with no browser or network
dependency; **manual** rows are explicit review steps; **unavailable** rows are
not claimed as completed when the required browser tooling is absent.

## Current support at a glance

| Reader question | Current answer | Details |
| --- | --- | --- |
| Which Python versions? | Python 3.10–3.14 | [Supported Python versions](#supported-python-versions) |
| Which operating systems? | Linux, Windows and macOS | [Qualified operating systems](#qualified-operating-systems) |
| What is checked automatically? | The unit suite, package artifacts and generated-site contracts | [Package qualification](#package-qualification) and [accessibility qualification](#accessibility-qualification) |
| What still needs a person? | Browser, keyboard, touch and screen-reader checks | [Manual browser/keyboard matrix](#manual-browserkeyboard-matrix) and [known limitations](#known-limitations) |

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
  Classic, Paper, E-ink and Glassmorphic

## Evidence history

The v0.17 and v0.18 matrices are retained as historical evidence for the
contract candidate that v1.0.0 freezes. v1 adds the Five Promises assessment,
clean-room package rehearsal and the explicit compatibility policy; v1.1 adds
the rebrand compatibility evidence and the quality-gate additions; v1.1.2 adds
the typography evidence, v1.1.3 adds the documentation-quality evidence,
v1.1.4 adds the brand-hero, contrast and four-style evidence, v1.1.5 adds
the grouped-navigation and Markdown-coverage evidence, v1.1.6 adds the
image-alt escaping and custom-CSS contract evidence, v1.1.7 adds the
inline-code literalness and documentation-accuracy evidence, v1.1.8 adds
the protected math/resolver/auditor evidence, and v1.1.9 adds the audit,
preview and release-safety regressions below. v1.1.10 adds compact generated
navigation and accurate `init` publication guidance. v1.2.0 adds Markdown
layout parsing, group expansion, and a full-site migration from JSON. v1.2.1
adds reading-page context, responsive outlines and active-section parity.

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
  in Classic, Paper, E-ink and Glassmorphic × Light, Dark and System; the legacy generic
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

## v1.3.1 additions

- Audit tests cover a missing local non-Markdown asset linked from prose
  (DK004) and an existing asset that stays quiet, matching the documented
  DK004 rule and `check`'s build behaviour.
- Version tests cover an actionable "Git is required" error for `check-release`
  and `_run_git` when Git is unavailable, plus manifest rejection of release
  names reserved for generated output (`versions.json`, `index.html`) and
  names that differ only by case on case-insensitive filesystems.

## v1.3.2 additions

- Inline rendering tests cover generated HTML attribute boundaries, plain image
  descriptions, unchanged link targets and composed Markdown contexts.
- Build and safety tests cover staging a complete site, preserving previous
  output after a failed rebuild, and refusing unowned output directories.
- Preview tests cover local logo, banner and CSS edits outside `docs/`, path
  changes, and restoration of deleted assets.
- Reading-layout tests ensure scroll tracking leaves disclosure state to the
  reader. Browser verification covered four styles, two colour modes and four
  viewports locally; these checks are manual release evidence, not CI jobs.

## v1.3.0 additions

- Generated-page tests cover the glassmorphic hero glow, specular panel
  edges, hover-glowing cards, classic accent rules, paper pull-quote
  callouts, e-ink uppercase subheads with ink callout rails, and
  language-labelled code bars with labelled copy controls.
- The contrast proof still covers every reading surface: no surface hex
  changed, so the palette regression suite passes unchanged.
- The visual fixture checklist records the manual keyboard, phone-width and
  progress checks. Browser and screen-reader checks remain manual release steps.

## v1.2.3 additions

- Generated-page tests cover linked breadcrumb navigation, the always-present
  footer with back-to-top link, hover heading anchors, a search popover
  anchored to the search control with multi-term highlighting and result
  counts, the mobile navigation landmark and auto-opening inline outline.
- Build tests cover stable content-hash `?v=` asset URLs, print rules that
  hide navigation chrome while keeping the footer in ink, and the shared
  z-index and sticky-offset token contract.
- The visual fixture checklist records the manual keyboard, phone-width and
  progress checks. Browser and screen-reader checks remain manual release steps.

## v1.2.2 additions

- Generated-page tests cover the skip link, focusable article target, compact
  phone-header styling and article-based progress calculation.
- Build tests cover missing same-page heading fragments and links to missing or
  unpublished Markdown. The strict documentation audit and site build exercise
  the same checks on this project's pages.
- The visual fixture checklist records the manual keyboard, phone-width and
  progress checks. Browser and screen-reader checks remain manual release steps.

## v1.2.1 additions

- **Reading-page structure**: generated-page tests cover section and subsection
  context, destination labels, a closed inline outline for one or many headings,
  no empty outline rail when a page has no sections, and unchanged home-page
  markup. The maintained fixture records visual checks for these states.
- **Browser behaviour**: local Chromium viewport checks cover 320, 390, 768,
  1024 and 1440 CSS pixels, all three content widths, four styles and both
  colour modes without page overflow. The small-screen outline receives the
  same active heading and `aria-current="location"` as the desktop rail;
  keyboard navigation and anchored-heading clearance below the sticky header
  are checked manually. Touch emulation opens the 44px disclosure target, the
  accessibility tree exposes its summary and labelled navigation, and print
  hides both outlines. The visual fixture guide records how to repeat these
  checks. This browser evidence is manual, separate from the automated CI
  suite; a real screen-reader pass remains a pre-publish review step.

## v1.2.0 additions

- **Compatible authoring formats**: `layout.md` and `layout.json` produce the
  same validated navigation model; projects with both files fail explicitly.
  Tests cover the home page, root README, groups, expansion, escaping, unlisted
  policy, malformed lines, `init`, normal builds and historical builds.
- **Maintained site migration**: DocSprout's 41-page layout is now Markdown.
  Documentation tests check its page order, section membership, home page and
  Quickstart expansion; `check` and strict audit run on this format in CI.

## v1.1.10 additions

- **Readable generated navigation**: `init` writes each generated page on one
  line while preserving schema-1 data and leaving existing layouts untouched.
  CLI tests cover the generated layout and non-destructive re-initialisation.
- **Accurate publication guidance**: `init` identifies an existing layout as
  authoritative instead of claiming discovery published all Markdown. A
  regression test covers this case.
- **Documentation quality**: the beginner guide has one complete, compact
  layout example; documentation tests parse it and check the listed pages and
  selected home. Decision 0013 describes a proposed Markdown outline, with
  no new accepted configuration syntax in this release.

## v1.1.9 additions

- **Audit parity**: regression tests cover multiline inline code and math,
  unmatched indented fence markers, and backticks inside display math. The
  auditor reports only links and images the renderer treats as content.
- **Preview recovery**: a failed build leaves its source snapshot pending, so
  the next poll retries without another edit; a save during a successful build
  still triggers another pass.
- **Release safety**: historical archive tests reject link members before
  extraction on the Python 3.10–3.11 path, offline ZIPs reject traversal in
  release labels, and `check-release` catches edits to a published root README.

## v1.1.8 additions

The protected-context correctness patch makes inline math consistent with
inline code across rendering, resolvers, auditing, and docs; no schema,
route, machine-format, CLI, token-name, dependency, or syntax change:

- **Inline-math literalness**: code and math are stashed together via one
  shared `PROTECTED_SPAN` helper before ordinary transforms, so TeX remains
  literal with only attribute escaping. Tests cover bold, italic,
  strikethrough, links, images, angle brackets, `--flag`, apostrophes, and
  mixed outside-math rendering with decoded `data-tex` assertions.
- **Resolver protection**: raising-resolver tests prove fake links/images
  inside code/math never invoke resolution, while mixed prose resolves only
  the genuine outside target; combined code+math test guards both.
- **Auditor agreement**: the auditor reuses `mask_protected_spans` and skips
  display-math blocks, so code/math/fenced links/images produce no
  DK001/DK002/DK004/DK101 findings while genuine prose links/images are still
  audited, including mixed real-plus-fake cases.
- **Preservation**: v1.1.6 image-alt `quote=True` escaping and v1.1.7
  `InlineCodeLiteralnessTests` remain intact and passing.

## v1.1.7 additions

The Markdown correctness and documentation-accuracy patch makes inline code
truly literal and brings the showcase back into agreement with the renderer;
no schema, route, machine-format, CLI, token-name, dependency or syntax change:

- **Inline-code literalness**: inline code spans are stashed behind
  deterministic NUL-sentinal placeholders during `_inline()` processing, so
  image, link, emphasis, strikethrough, math and other Markdown-looking syntax
  inside backticks remains literal `<code>` with only HTML escaping. Unit tests
  cover image, link, bold, italic, strikethrough, math, angle brackets,
  `--flag`, apostrophes, quotes, and mixed inside/outside rendering.
- **v1.1.6 security preservation**: the image-alt `quote=True` escaping fix
  remains intact; the straight-quote attribute test now reaches the attribute
  through a link/image target (protected from typography) instead of relying
  on incorrect code-span image semantics, plus the existing malicious-alt and
  build-level asset tests.
- **Documentation-showcase accuracy**: the showcase documents standard
  blockquotes, strikethrough, horizontal rules (`---`, `***`, `___`), and
  literal inline code with rendered examples, and a documentation-regression
  test asserts the stale unsupported claims do not return.

## v1.1.6 additions

The security and hardening patch closes an attribute-escaping gap and makes
the custom-CSS network boundary explicit; no schema, route, machine-format,
token-name, CLI or theme change:

- **Image-alt escaping**: Markdown image alt text is escaped for HTML
  attribute context (`"`, `'`, `<`, `>`, `&`), with `html.unescape` applied
  first so legitimate entities are not double-escaped. Regression tests cover
  ordinary alt text, quoted text, special characters and crafted alt text that
  must remain one safe `<img>` element, plus a build-level test that exercises
  asset resolution with real local image assets.
- **Custom-CSS contract**: DocSprout's own generated and bundled assets require
  no network access and DocSprout never fetches custom-CSS references itself;
  user-supplied `theme.custom_css` is copied verbatim and may intentionally
  reference external resources when the site is viewed. Guides, security policy
  and qualification state that those external dependencies belong to the author.

## v1.1.5 additions

The scannable-sidebar release changes navigation presentation and widens
Markdown coverage; no schema, route, machine-format or token-name change:

- **Collapsible groups**: a section's `pages` entry accepts `"path"` or a
  `"pages"` subgroup with one level of child pages; tests cover grouping,
  per-group `"expanded"`, active-group auto-expansion, preserved routes and
  the loading of existing flat layouts.
- **Markdown coverage**: blockquotes, strikethrough and horizontal rules
  render with regression tests, and the maintained showcase page demonstrates
  every supported element beside its source.
- **Quiet hover**: capability cards keep the border highlight without the
  inset top eyebrow; structural and token tests still pass.

## v1.1.4 additions

The brand-hero and contrast-proof release changes presentation and derives new
values; no schema, route, machine-format or token-name change:

- **Automatic hero**: the built home page is asserted to render one hero with
  its heading, opening summary, optional release pill and derived Get
  started/Repository actions; non-home pages stay hero-free, and unsafe
  repository URLs are never emitted.
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
| **Easy to look good** | Structural accessibility, token, responsive-image, theme/mode, content-width, hero/contrast, custom-CSS and maintained visual-fixture tests cover phone/tablet/desktop cases without brittle screenshots. | Automated pass; see Known limitations |
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
- Browser automation is not part of CI. v1.2.1 was checked locally with Chromium
  viewport emulation and the DevTools Protocol, while structural tests run in
  CI. A real screen-reader and native touch-device pass remain manual release
  checks; the matrix below does not imply they run in CI.
- External URLs in documentation are never network-checked; `audit` reports
  this explicitly.
- Custom CSS is author-owned: its accessibility, contrast, responsiveness and
  any external or network dependencies it introduces are not DocSprout claims. The manual matrix below covers the default site; a
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
| 1 | Tab once to reveal Skip to content, activate it, and confirm focus reaches the article below the header. Continue through search, version, style and mode controls, copy buttons, previous/next and every sidebar link; focus is always visible. |
| 2 | `/` focuses search; type a query; ArrowDown/ArrowUp, Home, End, Enter and Escape behave as described; Tab leaves the result region predictably. |
| 3 | At phone width the mobile navigation opens and closes with Enter/Space on the disclosure and every section link is reachable by keyboard. Scroll until the brand row collapses; search and settings remain available, and keyboard focus reveals the brand link. |
| 4 | Screenshot phone/tablet/desktop widths in Classic, Paper, E-ink and Glassmorphic × System, Light and Dark; nothing overlaps and no page-level horizontal scroll appears. |
| 5 | With the OS reduced-motion preference on, search results, the reading-progress bar and theme changes do not animate. |
| 6 | With Windows high-contrast / forced-colors enabled, focus outlines and the reading-progress indicator remain visible. |
| 7 | At desktop and phone widths the home-page hero keeps its copy readable, the derived actions stay keyboard reachable, and a configured banner spans the content width without cutting its text. |
| 8 | On a long reading page, open the phone outline by touch and keyboard, confirm its current section and labelled navigation with a screen reader, follow a nested heading link, and check that the heading clears the sticky header. On desktop, confirm the rail marks the same section. Check that reading progress completes at the article end, before page navigation and footer. |
