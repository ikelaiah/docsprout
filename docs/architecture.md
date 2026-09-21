# Architecture

DocSprout has five small layers: configuration discovery, validation, safe
Markdown rendering, static-site generation, and immutable-version orchestration.
The package carries the CSS and browser code so consuming projects do not copy
the implementation. `build` renders a working tree for preview; `build-all`
archives every declared Git tag or full SHA into an isolated temporary tree.

## Compatibility surface

The public compatibility contract consists of:

- documented configuration files and their schema-version-1 fields
  (`docsprout.json`, `layout.json`, `versions.json`);
- the pre-rebrand `docs/dockit.json` filename, the deprecated `dockit-fp`
  console script and the `python -m dockit_fp` module entry point;
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

## Compatibility policy

v1.x prefers compatible additions. Deprecations remain available for at least
one minor release and are documented before a future major removal; schema and
machine-format changes require a new schema version and migration guidance.

## The Python API boundary

DocSprout is primarily a CLI/application package. `docsprout.__version__` is
public and may be used for version inspection. All other modules, classes and
functions are implementation details unless explicitly documented as public;
downstream tools should use the CLI and the machine formats.

## Language of this release

v1.0.0 is the stable commitment point for the **minimal CLI + obvious
declarative configuration** model: `layout.json` is the authoritative
navigation model (pages, sections, titles, order, home, publication),
`docsprout.json` describes appearance and identity, and no authoring-mutator
commands exist. v1.1.0 renews the same model under the DocSprout name; the
pre-rebrand aliases are deprecated and are removed in v2.0.0. The default site
needs no custom CSS; the custom stylesheet mechanism is a deliberately bounded
escape hatch whose inclusion mechanics DocSprout owns and whose accessibility
the author owns.

Downstream projects should pin released tags such as `v1.1.0`, never the main
branch. The stable boundary and deprecation policy are in [Machine-readable
contracts](machine-contracts.md).
