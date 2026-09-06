# DocKit roadmap

DocKit is for code projects that want polished, versioned Markdown documentation
without maintaining a site generator. It remains Pascal-friendly, but does not
require Pascal source code. This roadmap is a guide to direction, not a promise
of dates. Feedback from maintainers will set the order within each milestone.

The path to 1.0 is guided by three promises:

1. **Easy to customise.** A project owner can shape content, cards, sections,
   identity and theme through documented configuration—not Python edits or CSS
   forks.
2. **Easy to use.** A maintainer can start, author, check and publish a site
   with short commands and useful guidance.
3. **Looks good.** The default site and every supported theme are intentional,
   readable, responsive and keyboard-accessible.

The generator will remain small, offline-friendly and straightforward to
maintain while delivering those promises.

## Shipped in v0.1.0–v0.5.0

- Safe Markdown-to-site builds, local search, offline KaTeX and immutable
  historical Git-release builds.
- A guided first-site path, actionable validation and maintained examples.
- Ordered navigation, identity options, colour presets and visual themes.
- Safe Markdown task lists, keyboard search, GitHub Pages publication and an
  explicit configuration-compatibility policy.

## v0.6.0: customise the homepage without code

The next release closes the gap between the attractive default home page and a
project's own story.

- [x] Make the homepage capability cards configurable, reorderable and
      removable through `dockit.json`.
- [x] Let a project choose whether the homepage shows the capability strip,
      banner, introduction and release context.
- [x] Provide copyable homepage recipes for a library, application and API
      reference site.
- [x] Ensure configuration errors identify the exact card or homepage field and
      suggest a correction.
- [x] Keep the default homepage unchanged for existing projects.

## v0.7.0: make authoring and navigation effortless

Writing and finding documentation should feel faster than maintaining a custom
site generator.

- [x] Add the highest-value safe Markdown features requested by Pascal project
      maintainers, with predictable generated HTML.
- [x] Make navigation editing easier with clear section/page summaries and
      useful checks for unreachable or unlisted content.
- [x] Improve search ranking, result previews and keyboard flows while keeping
      every asset local.
- [x] Add concise authoring recipes for common project documentation structures.

## v0.8.0: polish the visual system

Every built-in theme should look deliberate before custom visual surface area is
expanded.

- [x] Refine typography, spacing, tables, callouts, code blocks and long-form
      reading across Classic, Paper and Midnight.
- [x] Add configuration-level layout choices only where they preserve the
      shared semantic theme-token contract.
- [x] Publish visual fixtures for phone, tablet, desktop, light, dark and long
      document views.
- [x] Verify contrast, focus visibility and keyboard behaviour for every theme.

## v0.9.0: make publishing dependable

Release and hosting workflows should be boring, inspectable and hard to get
wrong.

- [x] Improve `doctor`, release checks and GitHub Pages guidance for common
      repository states.
- [x] Provide release-ready examples for a single-version site and a historical
      multi-version site.
- [x] Add deterministic release fixtures and a clear pre-publish checklist.
- [x] Document upgrade compatibility from every supported 0.x configuration.

## v0.11 — Existing Repo Magic

Safe existing-repository adoption, conservative README/docs discovery, sensible
initial navigation, explicit power-user control, safe root README support, and
`dockit-fp serve`.

## v0.12 — Beautiful by Default

A minimally configured repository should produce a site that feels
publication-ready without custom CSS, custom assets or extensive theme
configuration.

- [ ] Make the Classic homepage, header, sidebar, typography and code
      presentation feel confident and publication-ready by default.
- [ ] Refine tables, callouts, search, on-page navigation and previous/next
      navigation without changing their existing schemas or core behavior.
- [ ] Verify Paper and Midnight against the shared semantic design contract in
      Light, Dark and System modes.
- [ ] Exercise the result with DocKit-FP's own docs and the maintained visual
      fixture at phone, tablet and desktop widths.
- [ ] Preserve keyboard navigation, focus visibility, accessible names,
      reduced-motion behavior and offline/local assets.

## v0.13 — Explicit Home & DocKit Identity

Select the published home page explicitly and make the public product identity
language-neutral while preserving existing technical identifiers.

## v0.14 — GitHub in One Command

- [x] Prepare conservative DocKit configuration and a managed Pages workflow
      with `dockit-fp github-pages`.
- [x] Keep commits, pushes, repository settings and workflow upgrades under
      maintainer control.
- [x] Pin generated workflows, prevent feature-branch deployment and refuse
      unmanaged workflow conflicts.

## v0.15 — Documentation Audit ✅

- [x] Add a deterministic, offline documentation audit for publication-ready
      page links, anchors and local assets.
- [x] Report a small set of actionable accessibility and structure warnings
      without turning DocKit into a writing-style linter.
- [x] Keep `check` as the buildability gate and make strict audit opt-in.

## v0.16 — Documentation Refinement

- [x] Align the guides, examples, generated layouts and DocKit's own site on
      explicit `home` and `unlisted` configuration.
- [x] Make the beginner path follow the generated configuration and separate
      `home`, `homepage`, `check`, `audit` and Pages responsibilities clearly.
- [x] Add focused regression checks for canonical layouts and documented
      publishing contracts.

## v0.16.1 — Documentation Examples & Dogfooding

- [x] Pair documented identity and theme configuration with a visible,
      repository-local DocKit example.
- [x] Keep a built visual fixture for the optional home-page banner.
- [x] Protect canonical visual examples with focused documentation and build
      regression tests.

## v0.17 — Qualification ✅

Python/OS/package/ecosystem/accessibility qualification, enforced by the
repeatable CI matrix or explicitly documented where a manual browser check
remains necessary. See [Qualification evidence](docs/qualification.md).

- [x] Qualify every supported stable CPython (3.10–3.14) on Linux, minimum
      and latest Python on Windows and macOS, plus a non-blocking 3.15
      forward-compatibility signal.
- [x] Qualify wheel and sdist build, artifact inspection, fresh-environment
      installation and the whole CLI journey from outside the source tree.
- [x] Qualify `init`, `check`, `audit`, `build`, `serve` and `github-pages`
      end to end on new and existing projects, including deterministic
      localhost serve smoke tests.
- [x] Qualify representative repository shapes: root READMEs, docs indexes,
      explicit homes, unlisted-exclude, nested docs and assets, spaces,
      Unicode, multi-level navigation, ancillary Markdown policy, and
      generic and Pascal-oriented repositories.
- [x] Qualify the ecosystem: non-Git projects, Git repositories with and
      without remotes, idempotent `github-pages` preparation, and the
      no-commit/no-push/no-settings rule.
- [x] Qualify generated-site accessibility fundamentals structurally, with a
      small documented manual browser/keyboard matrix for visual checks.

## v0.18 — Simple Configuration & Stable Customisation ✅

The final pre-1.0 simplification and contract-candidate release. Theme:
**minimal CLI + obvious declarative configuration.** Commands perform
actions; `layout.json`, `dockit.json` and `versions.json` describe the site.
See [release notes](CHANGELOG.md#0180) and [Qualification evidence]
(docs/qualification.md).

- [x] Keep the command surface operational; making pages, sections, titles,
      order, home and publication ordinary `layout.json` edits with a
      compact canonical example, and appearance/identity `dockit.json`
      edits.
- [x] Teach the mental model from `init` (Markdown / `layout.json` /
      `dockit.json` / `serve`) and keep `serve` the centre of authoring,
      with rebuild regression coverage for `layout.json` and `dockit.json`.
- [x] Offer the three customisation levels: presets and exact colours,
      documented intermediate configuration, and the deliberately bounded
      repository-local custom CSS escape hatch with tested safe inclusion.
- [x] Establish the documented `--dk-*` public token family (pre-1.0 rename
      documented) with contract tests in every theme and mode, and state
      which selectors/DOM internals are not stable.
- [x] Tighten configuration diagnostics (`Did you mean` suggestions for
      unknown fields, non-empty titles, typed metadata) while preserving
      every released 0.x schema-1 configuration (automated corpus).
- [x] Harden the route contract with pre-build collision detection, version
      `search-index.json` and `audit` JSON machine output, and document all
      machine contracts and the Python API boundary.
- [x] Bring the migration guide through v0.18 and add the `0.x → 1.0`
      upgrade checklist.

## v1.0 — Stable Contract

Version 1.0 is the commitment point: the supported configuration and workflow
become dependable foundations for code projects. v0.18 candidates the
contracts (declarative configuration, routes, machine formats, `--dk-*`
tokens, custom CSS inclusion, CLI surface); v1.0 formally commits to them.

- [ ] Declare the stable configuration contract, compatibility policy and
      deprecation process.
- [ ] Complete a full accessibility, responsive-layout and generated-HTML
      verification matrix for every supported configuration.
- [ ] Review public documentation, examples, CLI help and release workflow for
      a maintainer's first successful publication.
- [ ] Publish the final migration/upgrade review from every 0.x release and
      the completed 1.0 upgrade checklist.
- [ ] Rehearse the first publication end to end and prove that easy to
      customise, easy to use and good-looking defaults are true of the
      shipped artifact.
- [ ] Ship only when the three promises—easy to customise, easy to use and
      looks good—are demonstrably true. If v0.18 leaves no genuine blockers,
      v1.0 is the next planned release.

## Quality bar

No release is complete unless it is easy to start, easy to understand, easy to
customise and looks good with the default configuration. New visual features
must work without a CDN or framework, retain keyboard accessibility, respect
the existing responsive breakpoints and include a regression test or fixture.

## Non-goals

DocKit will not become a Pascal source parser or API extractor. PasWeave
remains the companion tool for that job. DocKit also will not require a
hosted service, JavaScript framework or CDN to build a useful documentation
site.

## How to influence it

Open an issue with the project structure you have, the command you expected to
run, the visual result you wanted and the result you received. Concrete
documentation pain points are more useful than feature votes: they help us
decide which small improvement makes the next project easier to document.
