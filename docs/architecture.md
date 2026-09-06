# Architecture

DocKit-FP has five small layers: configuration discovery, validation, safe
Markdown rendering, static-site generation, and immutable-version orchestration.
The package carries the CSS and browser code so consuming projects do not copy
the implementation. `build` renders a working tree for preview; `build-all`
archives every declared Git tag or full SHA into an isolated temporary tree.

## Compatibility surface

The public compatibility contract consists of:

- documented configuration files and their schema-version-1 fields
  (`dockit.json`, `layout.json`, `versions.json`);
- CLI commands, options and exit-code semantics;
- generated routes (see [Machine-readable contracts](machine-contracts.md));
- machine formats: `search-index.json`, `release.json`, built-site
  `versions.json` and `audit --format json`;
- the documented `--dk-*` public token family;
- the custom CSS inclusion mechanism (`theme.custom_css`);
- reusable-workflow inputs.

Internal selectors, DOM wrappers, exact generated whitespace, private Python
modules and human CLI prose are deliberately not part of the contract; see
the boundary in [Machine-readable contracts](machine-contracts.md).

## The Python API boundary

DocKit-FP is primarily a CLI/application package. `dockit_fp.__version__` is
public and may be used for version inspection. All other modules, classes and
functions are implementation details unless explicitly documented as public;
downstream tools should use the CLI and the machine formats.

## Language of this release

v0.18.0 is the final pre-1.0 simplification release. Its theme is
**minimal CLI + obvious declarative configuration**: `layout.json` is the
authoritative navigation model (pages, sections, titles, order, home,
publication), `dockit.json` describes appearance and identity, and no
authoring-mutator commands exist. The default site needs no custom CSS; the
custom stylesheet mechanism is a deliberately bounded escape hatch whose
inclusion mechanics DocKit owns and whose accessibility the author owns.

Downstream projects should pin released tags such as `v0.18.0`, never
the main branch.
