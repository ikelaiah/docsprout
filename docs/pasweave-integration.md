# PasWeave integration

PasWeave reads Pascal source and produces API documentation as Markdown.
DocSprout combines Markdown pages into a complete documentation website. You
can use either tool alone, or put PasWeave's generated pages beside your
handwritten guides:

```text
Pascal source -> PasWeave -> generated API Markdown --+
handwritten guides ----------------------------------+-> DocSprout -> site
```

Add the generated Markdown files to `docs/layout.json`, then run
`docsprout check` and `docsprout build` as usual. DocSprout never parses Pascal
source itself.
