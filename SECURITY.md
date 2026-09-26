# Security policy

## Supported versions

Security fixes are provided for the current stable minor release line.

| Version | Supported |
| --- | --- |
| 1.1.x | Yes |
| < 1.1 | No |

## Reporting a vulnerability

Report suspected vulnerabilities privately through
[GitHub security advisories](https://github.com/ikelaiah/docsprout/security/advisories/new).
Do not open a public issue for a security report.

Include the DocSprout version (`docsprout --version`), your operating system and
Python version, and a minimal reproduction. You should receive a response
within a few days.

## Scope

DocSprout is an offline command-line tool. These guarantees are security
boundaries:

- it never requires credentials and performs no network requests after
  installation;
- it writes only to the selected output directory and the files that `init` or
  `github-pages` create, and refuses to replace directories it does not own;
- it treats project Markdown, configuration and Git data as untrusted input and
  escapes generated HTML;
- generated sites use only bundled local assets, including KaTeX. DocSprout's
  own generated and bundled assets require no network access, and DocSprout
  does not itself fetch resources referenced by custom CSS. User-supplied
  `theme.custom_css` is copied verbatim; when the generated site is viewed,
  that author-owned stylesheet may intentionally reference external resources,
  whose privacy, security and accessibility consequences belong to the author.

A bug in one of those guarantees — path escape, replacing unowned files,
executing project-controlled content, or emitting unescaped HTML — is a
security issue and belongs in a private advisory.
