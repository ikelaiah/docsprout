# Decision 0011: DocSprout rebrand

DocKit / DocKit-FP is renamed to DocSprout in v1.1.0. The rename covers the
product name, the distribution and import package, the primary CLI command,
the primary configuration filename, the generated-site ownership marker, the
fresh GitHub Pages workflow path and the brand assets. It is a naming
decision, not a contract change: no feature, no schema and no route changes.

## Compatibility decision

The stable 1.x contract is preserved, so the pre-rebrand identifiers keep
working through 1.x and are removed in v2.0.0:

- `dockit-fp` remains a deprecated console-script alias and
  `python -m dockit_fp` remains a deprecated module entry point;
- `from dockit_fp import __version__` keeps returning the public version;
- `docs/dockit.json` keeps loading, while keeping both supported filenames at
  once is an explicit ambiguity error rather than a silent choice;
- a generated directory carrying the old `.dockit-fp-site` marker is
  recognised and replaced with `.docsprout-site`;
- a managed `.github/workflows/dockit-pages.yml` is recognised and updated in
  place by `docsprout github-pages --update`; it is never duplicated and an
  unmanaged file is never overwritten;
- generated pages migrate the `dockit-fp-theme` and
  `dockit-fp-visual-theme` browser keys to the `docsprout-*` names.

The public `--dk-*` CSS custom properties, generated routes, JSON schemas,
configuration field names and command behavior unrelated to the rebrand are
unchanged. New projects use `docs/docsprout.json`,
`.github/workflows/docsprout-pages.yml` and `.docsprout-site`.

## Consequences

- The repository, distribution, package and CLI now share one identity,
  `docsprout`, with the tagline "Grow polished documentation from Markdown."
- The deprecated aliases carry a ready migration path in the changelog and
  migration guide, and their removal is scheduled for the next major release.
- Historical records (earlier changelog entries, task documents, decision
  records and released tags) remain under the names accurate at the time.
