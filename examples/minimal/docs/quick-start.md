# Quick start

Change the accent colours in `docsprout.json` and rename the `Getting started`
section in `layout.json`, then run:

```bash
docsprout check
docsprout build --output build/docs-site
```

To add another page, create a Markdown file inside `docs/` and add it to the
ordered `navigation` list in `layout.json`.
