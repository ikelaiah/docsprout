# Changelog

## 1.1.7

A Markdown correctness and documentation-accuracy patch. Inline code spans now
protect their contents from Markdown interpretation, and the Markdown showcase
documents blockquotes, strikethrough and horizontal rules as supported,
matching behaviour introduced in v1.1.5. No schema, route, machine-format,
CLI, token-name, dependency or Markdown-syntax change: update the package and
workflow pins to `v1.1.7` and rebuild.

### Fixed

- Inline code spans now protect their contents from Markdown interpretation,
  so image, link, emphasis, strikethrough, math and other Markdown-looking
  syntax inside backticks remains literal code.
- Correct the Markdown showcase to document blockquotes, strikethrough and
  horizontal rules as supported features, matching behaviour introduced in
  v1.1.5.

## 1.1.6

A security and hardening patch. Project Markdown is treated as untrusted
input; v1.1.6 closes an attribute-escaping gap in Markdown image rendering and
makes the custom-CSS network boundary explicit. No schema, route,
machine-format, CLI, token-name or theme change: update the package and
workflow pins to `v1.1.6` and rebuild.

### Fixed

- Escape Markdown image alt text correctly for HTML attribute context,
  preventing crafted alt text from injecting attributes into generated `<img>`
  elements. Ordinary Unicode and Markdown text render unchanged.
- Clarify that DocSprout's own generated and bundled assets require no network
  access, while user-provided `theme.custom_css` is copied verbatim and may
  intentionally reference external resources when the generated site is viewed.

### Security

- Project Markdown is untrusted input and generated HTML is escaped. This
  release fixes image alt-text handling so alt content stays inside its
  `alt="..."` attribute; all other renderer attribute contexts were audited
  and required no change.

## 1.1.5

The scannable-sidebar release. The left navigation collapses into logical
groups, the Markdown renderer covers quotes, deletions and rules, and the
capability cards keep a quiet hover. No schema, route or machine-format
changes: update the package and workflow pins to `v1.1.5`, rebuild, and review
the sidebar once.

### Added

- Nested navigation groups in `docs/layout.json`: a section's `pages` entry
  uses either `"path"` for a directly listed page or `"pages"` for a
  collapsible subgroup with one level of child pages. Only the group holding
  the current page starts expanded; `"expanded": true` on a group keeps it
  expanded everywhere. Existing flat layouts load unchanged.
- Standard Markdown blockquotes (`> quote`), strikethrough (`~~deleted~~`)
  and horizontal rules (`---`, `***`, `___` on their own line), with a
  [showcase page](docs/markdown-showcase.md) rendering every supported
  element beside its source.

### Changed

- Reorganised the DocSprout site navigation into `Start here`,
  `Build your site`, `Publish` and `Maintainer reference`, with collapsible
  subgroups (`Quickstart`, `Writing documentation`, `Content & navigation`,
  `Appearance`, `Advanced`, `Checks & auditing`, `Deployment`,
  `Versions & migration`, `Core reference`, `Architecture decisions`).
  All 40 pages and routes are preserved.
- Capability cards now signal hover with the border highlight only; the
  inset top eyebrow is removed.

### Fixed

- Pinned package, workflow examples, docs manifest and guides to `v1.1.5`.

## 1.1.4

The brand-hero, contrast-proof and visual-style release. Generated sites get a
designed home page, four styles in light and dark modes, and a single configured
accent becomes a complete, WCAG-verified theme. No schema, route,
machine-format or documented `--dk-*` token name changes: update the package
and workflow pins to `v1.1.4`, rebuild, and review the home page and link
colours once.

### Added

- Two more visual styles: `e-ink` (flat, near-monochrome, contrast-first) and
  `glassmorphic` (translucent blurred chrome with a solid-token fallback),
  each with light, dark and system modes and the same build-time contrast
  proof as the existing styles.
- [Add DocSprout to an existing repository](docs/existing-repository.md): the
  adoption walkthrough for a project that already has a README or `docs/`.
- [Checks in CI and CD](docs/ci-cd.md): the `check`/`audit` gates with a
  complete GitHub Actions job, portable runner guidance and static-host
  deployment.
- An automatic home-page hero built from the same Markdown: heading, opening
  summary, optional release pill, derived **Get started** (first non-home page)
  and **Repository** (`project.repository_url`) actions, an accent-derived
  backdrop and decorative inline-SVG icons on capability cards.
- One-hex brand theming: an explicit `theme.accent` without
  `accent_secondary` now derives an analogous secondary instead of inheriting
  the preset pair.
- Build-time contrast proof: `--dk-interactive` and `--dk-focus-ring` values
  are computed against every shipped reading surface in each visual style and
  colour mode, with an internal `--dk-on-interactive` foreground for filled
  actions. A failing light accent is reported by `docsprout check` and as audit
  warning `DK104`, while the built site uses the verification-safe link colour.

### Changed

- The sidebar separates group labels from page entries: section headings are
  quiet small-cap headers, and page links carry the visual weight.
- A configured banner renders as a full-width band at the top of the home-page
  hero, capped at `10rem`. Home-page capability cards form two columns on wider
  screens and one on phones. The DocSprout site uses the header version control
  instead of repeating the release label in its hero.
- The header content aligns with the page shell. DocSprout's own header mark is
  a potted sprout with green leaves, brown soil and a beige pot; Classic hero
  artwork no longer has an accent-coloured top border.
- Capability cards use bordered surfaces with decorative icons and a subtle
  hover lift; the hero replaces the previous plain home-page heading.

### Fixed

- `docsprout serve` no longer serves stale output until restart. A source
  saved while a rebuild was already running stays queued instead of being
  marked as built, transient file errors (editor saves, antivirus locks) no
  longer kill the watcher thread or fail requests, and the preview now
  watches every module that shapes the built site (`assets`, `palette`,
  `highlight`, `config`, `markdown`, `build`), not just two of them.
- `repository_url` becomes the hero's Repository action only when it is an
  http(s) URL, so an unsafe value can never be emitted as a link. `doctor`
  reports the verified accent and any derived secondary.

## 1.1.3

A documentation-quality patch. No configuration, schema, route or token change:
update the package and workflow pins to `v1.1.3` and rebuild. The bundled guides
now demonstrate the home-page banner, require referenced assets to exist before
building, map the most common configuration and Markdown errors to fixes, and
document `docsprout build`, offline archives, `--root` and `doctor` output.

### Changed

- DocSprout's own documentation site now configures the home-page banner it
  documents, and the configuration and home-page guides describe the banner's
  placement, size limits and pre-existing-asset rule.
- Examples that reference banner, logo or custom-CSS files now tell readers to
  create the file first, and troubleshooting covers malformed JSON, invalid
  field values, missing assets, unclosed Markdown blocks and invalid version
  manifests.
- Added a build guide covering `docsprout build` options, deterministic
  offline archives, `--root` and `docsprout doctor` output. The glossary gained
  the navigation, theme and command vocabulary, and the project specification
  is marked historical.

## 1.1.2

A typography release for generated sites. No configuration, schema, route or
token change: update the package and workflow pins to `v1.1.2` and rebuild.
The same Markdown is rendered with cross-platform system font stacks, a
complete heading and outline scale, and typographic punctuation.

### Added

- A cross-platform system font stack (`system-ui` first) for UI, display and
  code text, so generated sites look native on macOS, Linux, iOS and Android
  as well as Windows. No webfont is bundled or fetched.
- Styled `h4`–`h6` headings and matching `toc-level-4`–`toc-level-6` outline
  entries, so deep documents keep the same family, rhythm and keyboard target
  as `h1`–`h3`.
- Running-text typography: `text-wrap:pretty`, `orphans`/`widows`, automatic
  hyphenation with a minimum word length, tabular figures in tables, and no
  code ligatures in fenced blocks.
- `::selection` styling from the theme accent, and a print stylesheet that
  hides navigation, search, controls and the reading-progress bar.

### Changed

- Markdown prose converts `--`, `---`, `...` and straight quotes to
  typographic characters. Inline code, fenced code, math and link targets keep
  their exact characters.

### Fixed

- Repeated headings on one page now receive unique ids (`setup`, `setup-2`)
  instead of colliding, so outline links and heading fragments stay correct.
  The audit still warns (DK103) because links to the shared heading text remain
  ambiguous.

## 1.1.1

A quality patch for the rebrand release. No configuration, schema or route
change: update the package and workflow pins to `v1.1.1` and keep building.

### Fixed

- `init` and `doctor` now name the authoritative configuration file on
  pre-rebrand projects (`docs/dockit.json`), point the configuration hint at
  that file, and print the explicit rename step for the v2.0.0 removal.
- Legacy `dockit.json` diagnostics label root fields with the actual file stem
  (`dockit.*`) instead of `docsprout.*`.

### Added

- `docs/troubleshooting.md` maps the exact DocSprout messages to fixes.
- `CONTRIBUTING.md` gains a module-to-tests code map.
- `SECURITY.md`, a Contributor Covenant code of conduct, bug/feature issue
  forms, a pull-request checklist and weekly Dependabot updates.
- `Homepage`, `Documentation`, `Repository`, `Changelog` and `Issues` project
  URLs plus keywords in package metadata.
- A `ruff` lint gate through a `dev` optional dependency, run by a dedicated
  CI job; the runtime stays dependency-free.

### Changed

- The `build.py` document shell is assembled from named fragments instead of
  one 2,566-character line; output is byte-identical across the repository
  docs and the maintained examples. A regression test now rejects any
  `src/docsprout` line longer than 1,000 characters.

## 1.1.0

The rebrand release. DocSprout is the new name for the builder released through
v1.0.0 as DocKit-FP. There is no configuration or schema migration: update the
package and workflow pins to `v1.1.0` and keep building. The stable 1.x contract
is unchanged.

### Changed

- **Rebrand:** DocKit / DocKit-FP is now **DocSprout**. The distribution,
  import package and primary CLI command are `docsprout`; `python -m docsprout`
  is the canonical module entry point.
- New projects create `docs/docsprout.json`. Existing `docs/dockit.json`
  files keep loading; when both files exist DocSprout fails with an actionable
  ambiguity error instead of choosing silently.
- Generated output uses the `.docsprout-site` ownership marker. The old
  `.dockit-fp-site` marker is recognised and replaced when rebuilding.
- Fresh GitHub Pages setup creates `.github/workflows/docsprout-pages.yml`.
  An existing managed `dockit-pages.yml` is recognised and updated in place by
  `docsprout github-pages --update`; unmanaged workflows are never overwritten.
- Browser storage keys are now `docsprout-theme` and
  `docsprout-visual-theme`, migrating automatically from the old
  `dockit-fp-*` keys.
- Offline archives use the `docsprout-docs-<release>` root prefix, and brand
  assets plus repository URLs move to
  `https://github.com/ikelaiah/docsprout`.

### Compatibility

- `dockit-fp` remains a deprecated console-script alias and
  `python -m dockit_fp` remains a deprecated module entry point for at least
  one minor release. `from dockit_fp import __version__` keeps working. The
  aliases, the `docs/dockit.json` filename, the `.dockit-fp-site` marker and
  the managed `dockit-pages.yml` path are scheduled for removal in v2.0.0.
- The `--dk-*` CSS token family, routes, JSON schemas, configuration field
  names and command behavior unrelated to the rebrand are unchanged.

### Upgrading

1. Install the v1.1.0 archive or pinned Git ref instead of v1.0.0.
2. Point caller workflows at `publish-docs.yml@v1.1.0` and run
   `docsprout github-pages --update` where a managed caller already exists.
3. Optionally rename `docs/dockit.json` to `docs/docsprout.json`; never keep
   both.

## 1.0.0

The stable contract release. DocKit v1.0.0 commits to the small, offline-first
workflow qualified through v0.18.1 and makes the Five Promises explicit:
easy to use, easy to learn, easy to look good, easy to create from existing
repositories, and easy to maintain.

### Stability commitment

- Schema-version-1 `dockit.json`, `layout.json` and `versions.json` fields are
  the supported configuration surface.
- CLI commands/options and exit behavior, generated routes, machine-readable
  files, the documented `--dk-*` tokens, safe custom-CSS inclusion and
  reusable-workflow inputs are stable for 1.x.
- Compatible additions are preferred in 1.x. Deprecations remain available for
  at least one minor release and are documented before a future major removal.
- Private Python modules, internal DOM/CSS details, exact generated whitespace
  and human-readable prose remain implementation details.

### User-visible improvements

- A concise README and beginner path now lead from existing Markdown to a local
  preview, configuration, audit and publication.
- Qualification evidence records package, OS, repository-shape, accessibility,
  responsive-fixture, clean-room and Pages rehearsals with known limitations.
- The release process and migration guide explain the boring 0.x → 1.0 path:
  pin v1.0.0, keep schema version 1, use `--dk-*` tokens, and re-run the
  release checks.
- Maintained examples and reusable Pages callers pin the stable `v1.0.0`
  workflow.

## 0.18.1

Focused patch release for responsive Markdown images.

### Fixed

- Ordinary Markdown images inside `.prose` now shrink to the content column
  with `max-width: 100%` while preserving their aspect ratio. Images that are
  already smaller than the column retain their intrinsic size, and configured
  homepage banners keep their existing behavior.

## 0.18.0

The final pre-1.0 simplification and contract-candidate release.

### Added

- The `layout.json` editing model is documented as ordinary JSON edits (add,
  remove, rename, reorder, move pages; add and rename sections; change the
  `home` page), with a compact canonical configuration and no authoring
  commands.
- `theme.custom_css`: an optional repository-local `.css` escape hatch that
  is copied deterministically to `assets/custom.css`, loaded after DocKit's
  styles on every page (including nested and versioned builds), and strictly
  guarded against absolute paths, traversal, symlink escapes and missing or
  non-CSS files. DocKit guarantees the inclusion mechanics; the
  accessibility of user-written CSS is the author's responsibility.
- A documented `--dk-*` public token family (fifteen tokens) with contract
  tests across Classic, Paper and Midnight in Light, Dark and System modes.
- Strict configuration diagnostics: unknown fields in schema-1 objects of
  `dockit.json`, `layout.json` and `versions.json` are rejected with
  actionable `Did you mean` suggestions, built from the field families that
  legitimately existed in released tags.
- Deterministic pre-build route-collision detection: exact and
  case-insensitive collisions fail the build with an actionable error
  instead of silently overwriting output.
- Versioned machine formats: `search-index.json` now carries
  `{"schema_version": 1, "entries": [...]}` and `audit --format json`
  reports `"schema_version": 1`.
- `init` guidance: after initialisation DocKit states the mental model
  (Markdown is content, `layout.json` controls pages/sections/order/titles,
  `dockit.json` controls appearance) and names the inferred navigation
  sections when it created the layout.
- An automated compatibility corpus proving representative valid schema-1
  configuration from v0.1.0 through v0.17.0 loads and builds under v0.18.
- New guides: [Custom CSS](docs/custom-css.md) and
  [Machine-readable contracts](docs/machine-contracts.md), plus the
  documented Python API boundary and the `0.x → 1.0` upgrade checklist.
- The maintained visual fixture now dogfoods `theme.custom_css` and the
  documented token family.

### Changed

- The semantic theme tokens were renamed pre-1.0 from the generic `--bg`,
  `--surface`, `--text`, `--muted`, `--border`, `--code`, `--code-text`,
  `--raised`, `--focus-ring` and `--interactive` to the namespaced
  `--dk-*` family; internal implementation variables are explicitly not part
  of the contract. Projects with custom stylesheets should rename tokens
  where they referenced the old names.
- Navigation sections and pages must have non-empty titles; project
  description/repository/site fields must be strings when provided; empty
  titles and wrong metadata types are reported with the exact field path.
- FAQ-style diagnostics: a typo like `"presett"` now reports
  `Unknown field 'theme.presett'. Did you mean 'theme.preset'?`.

### Fixed

- `docs/index.md` plus `docs/docs-index.md` with an alternate home, and
  case-only filename differences, previously risked silently overwriting a
  generated route; they now fail `check`/`build` with a precise message.

## 0.17.0

### Added

- A repeatable qualification matrix: every supported stable CPython (3.10,
  3.11, 3.12, 3.13 and 3.14) on Linux, the minimum and latest Python on
  Windows and macOS, a non-blocking 3.15 pre-release signal, and Python
  classifiers that agree with `requires-python`.
- Installed-package qualification: the wheel and sdist are built, inspected,
  installed into fresh environments and exercised from outside the source
  tree (imports, bundled KaTeX assets, console entry point, the full CLI
  journey and a scan proving generated output embeds no project paths).
- End-to-end CLI qualification for `init`, `check`, `audit`, `build`,
  `serve` and `github-pages` on new and existing projects, with a
  deterministic localhost startup/response/shutdown serve smoke test.
- Representative repository-shape qualification: root README home, docs
  index, explicit `home`, `"unlisted": "exclude"`, nested documentation and
  assets, spaces and Unicode paths, multi-level navigation, ancillary
  Markdown policy, and generic and Pascal-oriented repository shapes.
- Accessibility structural qualification across the maintained visual
  fixture and DocKit's own documentation: keyboard-operable native controls,
  visible focus, accessible names, the search keyboard contract, heading
  structure, callout labels, reduced motion, scroller containment,
  Light/Dark/System coherence and the Classic/Paper/Midnight token contract.
- A qualification evidence guide (`docs/qualification.md`) stating exactly
  what is automated, manually verified and known-limited for v0.17.

### Fixed

- Historical `build-all` extraction now works on Python 3.10 and 3.11, where
  tarfile predates the `filter=` keyword; the pre-extraction archive path
  safety validation is preserved on every version.
- The docs-escape symlink test now qualifies Windows without Developer Mode
  through an unprivileged directory junction; when neither a symlink nor a
  junction can be created the skip explains the exact platform limitation.

## 0.16.2

### Added

- Added a shared SVG banner to the README and DocKit home page, plus clearer
  emoji signposts in the README.

## 0.16.1

### Fixed

- Made DocKit's own documentation a maintained identity example: a local SVG
  logo, purple preset, footer text and Project footer link now build together.
- Added a checked-in visual-fixture banner and connected banner, identity and
  footer/link guides to their reproducible rendered examples.
- Rewrote the project-identity before-and-after example so both configurations
  and every visible result are explicit.
- Added an inline favicon to generated sites so ordinary local previews do not
  report a missing favicon request.

## 0.16.0

### Changed

- Aligned DocKit's guides, generated layouts, maintained examples and dogfooded
  site on the modern explicit `home` and `"unlisted": "exclude"` contract.
- Shortened and reordered the beginner path; clarified `home` versus
  `homepage`, `check` versus `audit`, Style versus Mode, and the GitHub Pages
  repository-setting prerequisite.
- Added focused regression coverage so canonical layout examples and managed
  GitHub Pages workflow documentation stay synchronized with the product.

## 0.15.0

### Added

- Read-only `dockit-fp audit` diagnostics for published local page links,
  unpublished Markdown targets, anchors, local assets and unsafe paths.
- Low-noise image-alt, heading-level and duplicate-anchor warnings, with
  deterministic text/JSON reports and optional strict mode.
- `dockit-fp --version` and local Markdown image publishing.

## 0.14.0

### Added

- `dockit-fp github-pages` safely prepares an existing Git repository for a
  single-version GitHub Pages deployment without GitHub CLI authentication or
  network access during setup.
- A deterministic, release-pinned managed workflow with idempotent reruns and
  explicit `--update` support for recognised older DocKit workflows.

### Changed

- `doctor` reports the state and pinned version of the managed GitHub Pages
  workflow when present.

## 0.13.0

### Added

- `layout.json.home` explicitly selects the listed Markdown document published
  as `index.html`, including the repository-root `README.md` with
  `"source": "root"`.

### Changed

- Existing layouts without `home` retain their established root-README,
  `docs/index.md`, then first-listed-page fallback.
- Public documentation and generated-site branding now use DocKit. Repository,
  CLI, Python-module and GitHub Pages workflow identifiers remain `dockit-fp`
  and `dockit_fp` for compatibility.

## 0.12.1

### Added

- Optional safe `identity.logo` support for repository-local SVG and PNG header marks.

### Changed

- Refined homepage cards, previous/next navigation and header control alignment.
- Local previews now rebuild documentation changes without restarting `dockit-fp serve`.

## 0.12.0

### Changed

- Refined the default generated site with calmer header controls, clearer
  navigation hierarchy, stronger typography rhythm and balanced homepage card
  layouts for two, three and four cards.
- Improved code blocks, copy controls, tables, callouts, search results,
  on-page navigation and previous/next navigation across responsive widths.
- Expanded the maintained visual fixture and added nested-list rendering for
  realistic documentation shapes without introducing new configuration or
  external assets.

## 0.11.4

### Changed

- DocKit-FP's own home page now demonstrates homepage capability cards and
  release context, with a guide that connects the configuration to the result.

## 0.11.3

### Changed

- Expanded the beginner add-a-page example to show where a new navigation
  entry belongs before and after the change.

## 0.11.2

### Changed

- Updated current publishing examples and maintained links to v0.11.2.
- Clarified root Markdown support and made the beginner add-a-page example
  preserve the project's existing layout and home entry.

## 0.11.1

### Added

- Optional `layout.json` `"unlisted": "exclude"` policy. It makes the
  navigation list the complete publication decision and reports excluded docs
  during `check`.

### Changed

- Newly generated layouts default to `"unlisted": "exclude"`; existing
  layouts keep strict unlisted-Markdown validation unless changed explicitly.

## 0.11.0

### Added

- Safe existing-repository adoption: `init` discovers only a root README and
  Markdown under `docs/`, derives initial navigation, reports Git/GitHub and
  ancillary Markdown, and preserves all existing Markdown.
- Explicit safe root-README navigation with correct historical-release source
  handling.
- `dockit-fp serve` for validated localhost documentation previews.

### Changed

- Once generated, `layout.json` is maintainer-owned and authoritative; new
  discovery never silently changes it.

## 0.10.0

### Added

- Offline syntax highlighting for JSON, Free Pascal, Python, Bash, YAML and
  Markdown fenced code blocks, with a safe plain-code fallback for other
  languages.

## 0.9.2

### Fixed

- Wrapped list-item text and multi-line GitHub-style callouts now stay together
  in the generated page, so links and follow-up sentences no longer appear as
  stray paragraphs.

## 0.9.1

### Added

- A language-neutral guide for planning and writing useful code documentation,
  plus a plain-language glossary for documentation, Git and publishing terms.
- Documentation usability checks that preserve the short local-preview path and
  learning-first navigation.

### Changed

- Replaced the long, repetitive README with a calm ten-minute path to a local
  preview and goal-based next steps.
- Reworked beginner, configuration, theming and publishing guides around clear
  prerequisites, copyable examples, expected results and recovery steps.
- Moved project internals after learning, customisation and publishing in the
  generated navigation.

## 0.9.0

### Added

- Release-state diagnostics for unsafe, missing, moving and mismatched source
  references, with repository-aware `doctor` guidance.
- Maintained single-version and historical GitHub Pages examples, deterministic
  historical-build coverage and a pre-publish checklist.
- Direct upgrade guidance from every supported 0.x configuration.

### Changed

- The reusable Pages workflow now supports both publication modes and uses the
  current Node 24 GitHub Actions majors.
- Release validation now requires unique immutable references, a matching
  current tag and committed documentation.

## 0.8.0

### Added

- Validated `layout.content_width` choices for compact, comfortable and wide
  documentation, with default-compatible generated markup.
- A maintained long-form visual fixture and a responsive light/dark verification
  matrix for Classic, Paper and Midnight.

### Changed

- Refined typography, spacing, tables, callouts, code blocks, semantic
  interactive colours, focus visibility and reduced-motion behavior.

## 0.7.2

### Fixed

- The Classic visual theme now follows a dark operating-system preference when
  the colour control is set to System.

## 0.7.1

### Fixed

- Historical releases now build with the navigation rules in effect when they
  were authored, while the current release keeps strict unlisted-Markdown
  validation.

## 0.7.0

### Added

- Safe semantic definition lists for API and option reference prose.
- Unlisted-Markdown diagnostics, navigation summaries, ranked local search,
  richer search guidance, and Home/End result movement.
- Copyable library, application, and API-reference authoring recipes.

## 0.6.0

### Added

- Configurable homepage capability cards and independently visible homepage
  sections, with default-compatible output and actionable validation errors.
- Copyable homepage recipes for library, application, and API-reference sites.

## 0.5.0

### Added

- Safe, accessible Markdown task lists and keyboard search-result navigation.
- Explicit configuration schema compatibility and migration policy.

### Changed

- Release validation now covers five immutable documentation versions.

## 0.4.0

### Added

- Classic, Paper and Midnight accessible visual starter themes.
- A semantic visual-theme token contract and keyboard-accessible theme chooser.

## 0.3.0

### Added

- Ordered section navigation and project identity configuration with footer links.
- Curated blue, teal, ocean and purple colour presets.

### Changed

- Published copyable before-and-after customisation examples.

## 0.2.0

### Added

- A maintained two-page example with supported colour and navigation changes.
- Focused configuration-diagnostic regression coverage.

### Changed

- The beginner guide now gives a complete preview-to-GitHub-Pages path.
- Common colour and navigation errors now include a corrective action.

## 0.1.0

- Initial reusable Markdown documentation-site engine.
- Modern and legacy navigation, immutable historical builds, validation,
  version-specific search, themes and GitHub Pages workflow.
