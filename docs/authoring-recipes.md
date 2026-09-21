# Authoring recipes

Use these structures as a short starting point. They are ordinary Markdown and
`layout.json` files: no generator-specific source edits or hosted service is
needed.

## Library

```text
docs/
├── index.md
├── start/
│   ├── install.md
│   └── quick-start.md
├── guides/
│   └── configuration.md
└── reference/
    ├── units.md
    └── types.md
```

Place installation and the first working example in **Getting started**. Keep
the public surface under **Reference**. Definition lists work well for a unit's
types and options:

```markdown
Connection
: Opens a client connection using the configured endpoint.

Timeout
: Maximum wait in milliseconds before the operation fails.
```

## Application

```text
docs/
├── index.md
├── users/
│   ├── installation.md
│   └── workflows.md
├── operators/
│   ├── configuration.md
│   └── troubleshooting.md
└── releases.md
```

Separate user workflows from operator guidance. Keep release notes in one
listed page so they remain searchable and visible in the side navigation.

## API reference

```text
docs/
├── index.md
├── concepts.md
├── units/
│   ├── core.md
│   └── io.md
└── compatibility.md
```

Start with concepts, then one page per logical unit or namespace. Add every
public Markdown file to the `navigation` list in `docs/layout.json`; preserve
its explicit `home` selection and `"unlisted": "exclude"` policy. New layouts
keep other docs Markdown private; older layouts retain strict checking until
you explicitly choose that policy.

## Typographic punctuation

DocSprout turns common typewriter punctuation into typographic characters in
prose: straight quotes become curly quotes, `--` becomes an en dash, `---`
becomes an em dash and `...` becomes an ellipsis. Apostrophes inside words
become typographic apostrophes too.

The conversion never touches inline code, fenced code, math or link targets, so
command flags such as `--update`, identifiers such as `a--b` and literal
ellipses in code stay exact. Write the characters you mean in a code span when
precision matters.
