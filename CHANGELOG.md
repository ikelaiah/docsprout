# Changelog

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
