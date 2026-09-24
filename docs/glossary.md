# Glossary

You do not need to memorise these terms. Use this page when a guide contains an
unfamiliar word.

Admonition
: A GitHub-style callout block such as `> [!NOTE]`. Supported labels are
  `[!NOTE]`, `[!TIP]`, `[!IMPORTANT]` and `[!WARNING]`.

Audit
: `docsprout audit` reads your published pages and configuration, reports coded
  errors and warnings for publication mistakes, and never changes files.

Audit code
: A stable identifier for one audit finding: `DK001`–`DK005` are errors and
  `DK101`–`DK104` are warnings. See [Audit your documentation](audit.md).

Banner
: One image shown as a full-width band at the top of the home-page hero, above
  the `h1` heading. Configure it with the top-level `banner` object in
  `docsprout.json`.

Build
: Turn source files, such as Markdown, into output files such as a website.
  `docsprout build` writes a site to `build/docs-site` by default.

Capability cards
: Short feature summaries shown under the home page's opening summary. Configure
  them with `homepage.capabilities` in `docsprout.json`.

CDN
: A hosted service that sends website assets. DocSprout bundles its own CSS,
  JavaScript, fonts and mathematics assets, so a built site does not need one.

Check
: `docsprout check` validates configuration, links and anchors without writing
  a site.

CLI
: Command-line interface: a tool you run by typing commands in a terminal.
  `docsprout check` is a CLI command.

Configuration
: Small files that store choices for a tool. DocSprout uses JSON configuration
  for the project identity, navigation and optional release history.

`docsprout.json`
: The identity file under `docs/`, beside `layout.json`. It stores the project
  name, theme, logo, banner, footer and home-page presentation.

Doctor
: `docsprout doctor` reports the project shape, configuration state, release
  state and workflow status; use it first when something is wrong.

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

Hero
: The designed opening section of the home page: the release pill, heading,
  opening summary, derived actions and optional banner artwork. DocSprout builds
  it from plain Markdown with no MDX or custom HTML.

Immutable
: Unable to change. A release tag should keep pointing to the same commit so old
  documentation remains historically accurate.

`layout.json`
: The navigation file under `docs/`. It lists sections and pages, chooses the
  home page and sets the unlisted policy.

Markdown
: Plain text with small markers for structure. For example, `# Title` creates a
  page title and `[Guide](beginners-guide.md)` creates a link.

Mode
: A reader's colour choice: System, Light or Dark. DocSprout remembers it in the
  browser.

Navigation
: The sidebar list of pages. `layout.json` decides its sections, titles, order
  and the home page.

Preset
: One of the four starting colour schemes: `blue`, `teal`, `ocean` or `purple`.

Project folder
: The top-level folder for your code. It often contains `README.md`, `src/`,
  `.git/` or a project file.

Release
: A named version of a project that other people can use, such as `1.2.0`.

Repository
: A project folder whose changes are recorded by Git. People often shorten the
  word to “repo”.

Route
: The output path of a built page, such as `guides/setup.html`. Two listed
  documents must not claim the same route.

Schema version
: The version number at the top of each configuration file, written as
  `schema_version`. Every current file uses `1`; leave it unchanged.

Section
: A titled group of navigation pages in `layout.json`.

SHA
: A long identifier for one Git commit, such as a 40-character hexadecimal
  value. Most beginners can use a tag instead.

Source ref
: The tag or full commit SHA that tells DocSprout where one release's files
  live in Git history.

Style
: The site's starting visual theme: `classic`, `paper`, `midnight`, `e-ink` or
  `glassmorphic`. Visitors can switch it.

Tag
: A stable Git name attached to one commit, usually for a release. For example,
  `v1.2.0` can identify the exact files shipped as version 1.2.0.

Token (`--dk-*`)
: A documented CSS custom property such as `--dk-accent`, safe to use in custom
  CSS across every theme and colour mode.

Version manifest
: The optional `docs/versions.json` file listing current and historical releases
  and the Git tag or commit each one builds from.

Versioned documentation
: A site that keeps separate documentation for current and older releases.

Unlisted
: Markdown under `docs/` that does not appear in navigation. New layouts use
  `"unlisted": "exclude"`, so it is not published.

Workflow
: An automated series of steps. A GitHub Actions workflow is stored as a YAML
  file inside `.github/workflows/`.
