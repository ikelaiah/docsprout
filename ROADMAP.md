# DocSprout roadmap

DocSprout is for code projects that want polished, versioned Markdown documentation
without maintaining a site generator. It remains Pascal-friendly, but does not
require Pascal source code. This roadmap is a guide to direction, not a promise
of dates. Feedback from maintainers will set the order within each milestone.

The path to 1.0 was guided by five promises:

1. **Easy to use.** A maintainer can start, author, check and publish a site
   with short commands and useful diagnostics.
2. **Easy to learn.** A first-time maintainer can understand the mental model,
   choose the next edit and find the route to publication.
3. **Easy to look good.** The default site and every supported theme are
   intentional, readable, responsive and keyboard-accessible.
4. **Easy to create from existing repositories.** A project can adopt existing
   Markdown, assets, structure and identity without a rewrite.
5. **Easy to maintain.** Explicit contracts, qualification evidence and pinned
   release workflows keep future changes reviewable.

The original customisation promise is part of creating and maintaining a site:
project owners shape content, cards, sections, identity and theme through
documented configuration—not Python edits or CSS forks.

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
      removable through `docsprout.json`.
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

## v0.11 — Existing Repo Magic ✅

Safe existing-repository adoption, conservative README/docs discovery, sensible
initial navigation, explicit power-user control, safe root README support, and
`docsprout serve`.

## v0.12 — Beautiful by Default ✅

A minimally configured repository should produce a site that feels
publication-ready without custom CSS, custom assets or extensive theme
configuration.

- [x] Make the Classic homepage, header, sidebar, typography and code
      presentation feel confident and publication-ready by default.
- [x] Refine tables, callouts, search, on-page navigation and previous/next
      navigation without changing their existing schemas or core behavior.
- [x] Verify Paper and Midnight against the shared semantic design contract in
      Light, Dark and System modes.
- [x] Exercise the result with DocSprout's own docs and the maintained visual
      fixture at phone, tablet and desktop widths.
- [x] Preserve keyboard navigation, focus visibility, accessible names,
      reduced-motion behavior and offline/local assets.

## v0.13 — Explicit Home & DocSprout Identity ✅

Select the published home page explicitly and make the public product identity
language-neutral while preserving existing technical identifiers.

## v0.14 — GitHub in One Command

- [x] Prepare conservative DocSprout configuration and a managed Pages workflow
      with `docsprout github-pages`.
- [x] Keep commits, pushes, repository settings and workflow upgrades under
      maintainer control.
- [x] Pin generated workflows, prevent feature-branch deployment and refuse
      unmanaged workflow conflicts.

## v0.15 — Documentation Audit ✅

- [x] Add a deterministic, offline documentation audit for publication-ready
      page links, anchors and local assets.
- [x] Report a small set of actionable accessibility and structure warnings
      without turning DocSprout into a writing-style linter.
- [x] Keep `check` as the buildability gate and make strict audit opt-in.

## v0.16 — Documentation Refinement

- [x] Align the guides, examples, generated layouts and DocSprout's own site on
      explicit `home` and `unlisted` configuration.
- [x] Make the beginner path follow the generated configuration and separate
      `home`, `homepage`, `check`, `audit` and Pages responsibilities clearly.
- [x] Add focused regression checks for canonical layouts and documented
      publishing contracts.

## v0.16.1 — Documentation Examples & Dogfooding

- [x] Pair documented identity and theme configuration with a visible,
      repository-local DocSprout example.
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
actions; `layout.json`, `docsprout.json` and `versions.json` describe the site.
See [release notes](CHANGELOG.md#0180) and
[Qualification evidence](docs/qualification.md).

- [x] Keep the command surface operational; making pages, sections, titles,
      order, home and publication ordinary `layout.json` edits with a
      compact canonical example, and appearance/identity `docsprout.json`
      edits.
- [x] Teach the mental model from `init` (Markdown / `layout.json` /
      `docsprout.json` / `serve`) and keep `serve` the centre of authoring,
      with rebuild regression coverage for `layout.json` and `docsprout.json`.
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

## v1.0 — Stable Contract ✅

Version 1.0 is the commitment point: v0.18.1's qualified configuration,
routes, machine formats, `--dk-*` tokens, custom CSS inclusion, CLI surface
and Pages workflow are now documented as the stable 1.x contract.

- [x] Declare the stable configuration contract, compatibility policy and
      deprecation process.
- [x] Complete automated accessibility, responsive-layout and generated-HTML
      coverage for every supported configuration, with manual limitations
      stated honestly.
- [x] Review public documentation, examples, CLI help and release workflow for
      a maintainer's first successful publication.
- [x] Publish the migration/upgrade review from every supported 0.x release
      and the completed 1.0 upgrade checklist.
- [x] Rehearse clean-room adoption, customization, package installation,
      versioned builds and Pages publication.
- [x] Ship only after all Five Promises have qualification evidence.

## v1.1 — DocSprout Rebrand ✅

- [x] Rename the product, distribution, package, CLI command and primary
      configuration to DocSprout while preserving the 1.x compatibility
      aliases (`dockit-fp`, `python -m dockit_fp`, `docs/dockit.json`) for at
      least one minor release.
- [x] Keep routes, JSON schemas, configuration field names and the `--dk-*`
      token family unchanged.
- [x] Qualify the pre-rebrand aliases, the configuration ambiguity error, the
      legacy ownership marker and the managed legacy workflow path.

## v1.1.1 — Quality pass ✅

- [x] Point `init` and `doctor` at the real configuration filename with an
      explicit legacy rename step.
- [x] Add a troubleshooting guide and a module-to-tests code map.
- [x] Add security policy, code of conduct, issue/PR templates and Dependabot.
- [x] Add a `ruff` lint gate as a dev-only extra.
- [x] Split the 2,566-character document shell into named, byte-identical
      parts and guard against pathologically long source lines.

## v1.1.2 — Typography pass ✅

- [x] Resolve cross-platform system font stacks for UI, display and code text
      without bundling or fetching a webfont.
- [x] Style `h4`–`h6` and the matching outline levels, running-text
      hyphenation, tabular figures, selection styling and print output.
- [x] Convert typewriter punctuation to typographic characters in prose while
      protecting inline code, fenced code, math and link targets.
- [x] Disambiguate repeated heading anchors, keep the audit warning, and extend
      the maintained visual fixture and regression tests.

## v1.1.3 — Documentation quality pass ✅

- [x] Make DocSprout's own site configure the home-page banner it documents,
      and explain banner placement, sizing and the pre-existing-asset rule.
- [x] Frame every asset example as "create the file first" so copy-paste cannot
      silently break, and lock the guidance with regression tests.
- [x] Map the most common configuration, asset and Markdown failures in
      troubleshooting, including invalid JSON and version manifests.
- [x] Add a build guide for `build` options, deterministic ZIP archives,
      `--root` and `doctor`, and extend the glossary with the navigation, theme
      and command vocabulary.
- [x] Mark the original v0.3.0 specification as historical and give the
      customisation guides an explicit reading order.

## v1.1.4 — Brand hero and contrast proof ✅

Give every generated site a designed opening and make one brand colour
trustworthy across every theme and mode, without MDX, custom HTML or an
accessibility judgement call.

- [x] Render one automatic home-page hero from the existing Markdown: heading,
      opening summary, release pill, derived `Get started`/`Repository` actions
      and an accent-derived backdrop.
- [x] Add decorative inline-SVG icons and a hover lift to capability cards.
- [x] Derive an analogous `accent_secondary` when an explicit accent omits it.
- [x] Prove link (4.5:1) and focus (3:1) contrast against every shipped surface
      in each style and mode; correct failing values and report them from
      `check` and `audit` (`DK104`).
- [x] Keep every schema, route, machine format and documented `--dk-*` token
      name unchanged, with regression tests and updated guides.

## v1.2 — Visual Range and Adoption Guides

- [x] Add the `e-ink` and `glassmorphic` visual styles, each with light, dark
      and system modes, contrast-proven through the shared palette pipeline
      and documented alongside the existing styles.
- [x] Add an existing-repository adoption guide and a CI/CD guide covering the
      portable check/audit gates and static-host deployment.

## Quality bar

No release is complete unless it is easy to start, easy to understand, easy to
customise and looks good with the default configuration. New visual features
must work without a CDN or framework, retain keyboard accessibility, respect
the existing responsive breakpoints and include a regression test or fixture.

## Non-goals

DocSprout will not become a Pascal source parser or API extractor. PasWeave
remains the companion tool for that job. DocSprout also will not require a
hosted service, JavaScript framework or CDN to build a useful documentation
site.

## How to influence it

Open an issue with the project structure you have, the command you expected to
run, the visual result you wanted and the result you received. Concrete
documentation pain points are more useful than feature votes: they help us
decide which small improvement makes the next project easier to document.
