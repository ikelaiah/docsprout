# Glossary

You do not need to memorise these terms. Use this page when a guide contains an
unfamiliar word.

Build
: Turn source files, such as Markdown, into output files such as a website.
  `docsprout build` writes a site to `build/docs-site` by default.

CDN
: A hosted service that sends website assets. DocSprout bundles its own CSS,
  JavaScript, fonts and mathematics assets, so a built site does not need one.

CLI
: Command-line interface: a tool you run by typing commands in a terminal.
  `docsprout check` is a CLI command.

Configuration
: Small files that store choices for a tool. DocSprout uses JSON configuration
  for the project identity, navigation and optional release history.

Git
: A tool that records changes to files. A saved point in Git history is called
  a commit.

GitHub Actions
: GitHub's system for running automated jobs, such as checking and publishing a
  documentation site.

GitHub Pages
: GitHub's service for hosting a static website from a repository.

Home page
: The page a reader sees at the site's root. `layout.json.home` selects which
  listed Markdown page becomes the home page; `docsprout.json.homepage` controls
  only that selected page's presentation.

`HEAD`
: Git's name for the exact commit currently checked out in your project folder.

Immutable
: Unable to change. A release tag should keep pointing to the same commit so old
  documentation remains historically accurate.

Markdown
: Plain text with small markers for structure. For example, `# Title` creates a
  page title and `[Guide](beginners-guide.md)` creates a link.

Project folder
: The top-level folder for your code. It often contains `README.md`, `src/`,
  `.git/` or a project file.

Release
: A named version of a project that other people can use, such as `1.2.0`.

Repository
: A project folder whose changes are recorded by Git. People often shorten the
  word to “repo”.

SHA
: A long identifier for one Git commit, such as a 40-character hexadecimal
  value. Most beginners can use a tag instead.

Source ref
: The tag or full commit SHA that tells DocSprout where one release's files
  live in Git history.

Tag
: A stable Git name attached to one commit, usually for a release. For example,
  `v1.2.0` can identify the exact files shipped as version 1.2.0.

Versioned documentation
: A site that keeps separate documentation for current and older releases.

Unlisted
: Markdown under `docs/` that does not appear in navigation. New layouts use
  `"unlisted": "exclude"`, so it is not published.

Workflow
: An automated series of steps. A GitHub Actions workflow is stored as a YAML
  file inside `.github/workflows/`.
