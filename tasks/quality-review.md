# Code and output quality review

## Scope and plan

Improve safety, reading comfort and contributor understanding while preserving
the dependency-free CLI, configuration schemas, routes and public CSS tokens.
Keep the completed release plans in this directory as historical records.

1. Fix inline Markdown context handling. Regression cases must prove that code,
   math and emphasis cannot inject HTML attributes or alter link destinations;
   normal formatting and linked images must continue to work.
2. Preserve a working build when a rebuild fails. Reproduce the broken-link
   failure, stage the replacement, and retain owned-output safety checks.
3. Respect the reader's mobile outline choice. Scrolling may update the active
   section, but must not reopen a disclosure the reader closed.
   Also track configured preview assets outside `docs/`, so saved changes
   appear without restarting the preview.
4. Add a readable SVG build diagram and practical diagram-writing guidance;
   explain renderer boundaries and the contributor verification workflow.
5. Run focused regression tests, the complete suite, lint, documentation checks,
   strict audit, package build and visual inspection where tools permit.

## Acceptance checklist

- [x] Inline rendering passes context-boundary regressions and existing tests.
- [x] A failed single-site rebuild leaves the previous output intact.
- [x] The inline outline stays closed until the reader opens it.
- [x] Configured preview assets outside `docs/` trigger rebuilds.
- [x] Diagrams have readable labels, descriptive alternative text and a prose equivalent.
- [x] Full checks pass; remaining findings and verification limits are recorded.

## Findings and verification

### Findings addressed

| Severity | Finding | Change and evidence |
| --- | --- | --- |
| Critical | `_inline` restored generated code/math HTML inside image attributes; code containing a quote could create an `onerror` attribute. Later emphasis passes also rewrote URLs. | Separate HTML, plain description text and original source contexts; protect generated elements from later passes. Five tests in `tests/test_inline_contexts.py` cover injection, literal destinations, linked images, formatted labels and composed targets. |
| Required | `build_site` removed the working site before discovering a broken link. | Stage the complete site beside its destination, check ownership again, and restore the previous directory if installation fails. Six regressions cover failure preservation, cleanup, replacement and ownership. |
| Required | Preview ignored configured logo, banner and CSS files outside `docs/`. | Cache those source paths at build time and include them in snapshots. Three tests cover edits, path changes and deletion/recreation. |
| Required | Section tracking forced the inline outline open again after the reader closed it. | Keep location highlighting independent of disclosure state. Generated-script regression and browser keyboard/scroll checks pass. |
| Improvement | Architecture had no diagram; contributor instructions did not explain inline context boundaries. | Add a narrow SVG with large labels and prose equivalent, a diagram-writing recipe, and focused testing guidance. |

The baseline had 314 passing tests. The final implementation has 329 passing
tests on Windows / Python 3.13.5. `ruff check .`, `docsprout check`,
`docsprout audit --strict` (41 pages, zero errors or warnings), and the own-site
build pass. A wheel and source distribution were built without adding a runtime
dependency.

Headless Chrome inspected the built architecture page in Classic, Paper,
E-ink and Glassmorphic, Light and Dark, at 320, 768, 1024 and 1440 pixels:
32 cases passed with no page overflow, missing diagram, console warning or
JavaScript error. Keyboard checks verified disclosure toggling, closed-state
preservation during scrolling, current-section markers, search results,
ArrowDown and Escape. Phone and desktop screenshots were visually inspected.
Local evidence is in the ignored `build/quality-shots/` directory; full test
output is in `build/quality-tests.log`.

The browser connector was unavailable; an isolated headless Chrome profile
provided runtime checks. This is not screen-reader or cross-browser
qualification, and no release or historical-tag rehearsal was performed.

### Follow-ups recorded at the v1.3.2 review cutoff

- **Required at that review cutoff: README identity during adoption.** `docsprout init` followed by
  `docsprout check` fails for a project containing only `docs/README.md`:
  explicit home validation reserves `README.md` for the root source. With
  both root and docs READMEs, generated navigation instead fails its duplicate
  path check. Address source-aware page identity, home selection and route
  compatibility together in `config.py`, `cli.py` and `build.py`; silently
  excluding one README would hide documentation. Until then, rename the docs
  README to `docs/index.md` and use that path in navigation.
- **Required at that review cutoff: historical build preservation.** `versions.py::build_all`
  still clears its top-level output before rendering all releases. Extend
  staging to the complete multi-release tree and test failure in a later
  release. This pass changed single-site publication only; the build guide
  explicitly describes the historical limitation.
- **FYI: publication failure boundary.** Directory replacement uses two
  renames and is not crash-atomic. If installation and rollback both fail,
  the staging workspace retains the previous site for recovery. The staging
  approach also requires disk space for both the previous and next sites.

The renderer, build and preview fixes received independent review for
correctness, security, readability and compatibility. The patch changes the
package version to 1.3.2 and updates current release pins. It introduces no
runtime dependency, configuration schema, generated route or public CSS token
change. These findings described the review state before the follow-up patch.

### Follow-ups completed for v1.3.3

- Root `README.md` and `docs/README.md` now have source-aware identity,
  independent home selection and distinct output routes. Regression tests run
  `init`, `check`, `audit` and `build` with both pages and verify links in
  both directions.
- `build-all` now stages its complete multi-release site and publishes it only
  after all releases succeed. A regression test injects a failure in the second
  release and confirms the previous output remains byte-for-byte unchanged.
- The configuration, migration, building and qualification guides now describe
  the supported README combinations and historical-output guarantee.
