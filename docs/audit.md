# Audit your documentation

Before publishing, run:

```bash
docsprout audit
```

`check` asks, **“Can DocSprout safely build this site?”** `audit` asks, **“What
objective documentation problems should I fix?”** Run `check` after changing
configuration or navigation; use this guide for the audit rules and report
formats. Audit is read-only: it never rewrites Markdown, navigation or
configuration.

## Read the report

Errors describe public links, anchors or local assets that cannot work in the
published site. Warnings point out a small number of likely accessibility or
structure mistakes. Warnings do not fail the default command:

```bash
docsprout audit --strict
```

Use `--strict` in a CI job when warnings should also block publication. The
exit status is `0` for a successful audit under the selected policy, `1` for
findings that fail that policy, and `2` for command or configuration errors.

For tools and CI systems, request deterministic JSON:

```bash
docsprout audit --format json
```

The JSON report is a versioned machine contract: it begins with
`"schema_version": 1` and then reports `pages`, `errors`, `warnings` and the
ordered `findings` array. See [Machine-readable contracts](machine-contracts.md).

## What is checked

Audit uses the same configured navigation, root `README.md` handling and
heading IDs as the builder. A Markdown file that exists but is excluded from
`layout.json` is only reported when a published page links to it; drafts are
otherwise intentionally quiet.

| Code | Severity | Meaning |
| --- | --- | --- |
| DK001 | error | Local Markdown page link has no target. |
| DK002 | error | Link points to an existing Markdown file that is not published. |
| DK003 | error | Same-page or cross-page heading anchor is missing. |
| DK004 | error | Local image or asset is missing or outside supported documentation paths. |
| DK005 | error | Local link attempts to escape documentation paths. |
| DK101 | warning | Markdown image has empty alternative text. |
| DK102 | warning | Heading levels skip an intermediate level. |
| DK103 | warning | Two headings share the same anchor text; published anchors receive a numeric suffix. |

Local Markdown assets are published under the generated site's content assets
directory. External `https:` URLs are accepted but never network-checked;
offline, deterministic builds remain the default.

## A small CI gate

Keep the buildability gate and choose the audit policy deliberately:

```bash
docsprout check
docsprout audit --strict --format json
```

Start by fixing errors. Treat warnings as prompts to inspect the document, not
as a writing-style score.
