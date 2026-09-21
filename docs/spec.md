# Spec: DocSprout 0.3.0 (originally DocKit-FP)

## Objective

Build a small, reusable, Free Pascal-first static documentation-site package.
It must render modern and legacy Markdown trees, preserve immutable historical
releases, validate sources, and produce an accessible offline GitHub Pages site.

## Tech stack and commands

- Python 3.10+ standard library only.
- Test: `python -m unittest discover -s tests -v`
- Build package: `python -m build` (when the optional build frontend is installed)
- Local CLI during development: `python -m docsprout --help`

## Structure

`src/docsprout/` is the package; `tests/` contains unit and fixture tests;
`examples/minimal/` is a consumer project; `docs/` contains user guides and
ADRs. Generated output is not committed.

## Behaviour and boundaries

- Always: validate inputs, escape Markdown, use owned-output protection, test
  modern and legacy fixtures, and preserve source-ref isolation.
- Ask first: add third-party dependencies or change reusable workflow inputs.
- Never: parse Pascal, alter reference repositories/tags, use a moving ref for
  a published build, or delete an unowned output directory.

## Success criteria

- `build`, `build-all`, `check`, `check-release`, `init`, and `doctor` give
  useful human/CI output.
- Modern configuration and configuration-free legacy documentation render.
- Each version has isolated search, navigation and source content.
- Generated sites include accessible System/Light/Dark controls, responsive
  structure, semantic theme tokens, banner support and offline assets.
- Validation identifies the relevant file, field and reason.
