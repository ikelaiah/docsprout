# 📚 Make code documentation people can use

**Grow polished documentation from Markdown.**

DocSprout turns Markdown into a searchable, responsive documentation website for
code projects. It originated in the Free Pascal ecosystem and remains
Pascal-friendly, but the input is ordinary Markdown, not Pascal source code.

> [!TIP] New here? Start with [Your first DocSprout site](beginners-guide.md).
> It takes you to a working local preview and explains each step.

## 🧭 Pick one goal

- **I want a working site first.** Follow the
  [beginner's guide](beginners-guide.md). When you need the static files, or a
  ZIP to hand to someone, read [Build and inspect your site](building.md).
- **I want to write clearer guides.** Read
  [Write documentation people can use](writing-great-docs.md).
- **I want to add or reorder pages.** Open [Configuration](configuration.md).
- **I want to change the look.** Try [Themes](themes.md) or
  [customize the home page](homepage-recipes.md).
- **I want to publish.** Run `docsprout github-pages`, then follow [GitHub
  Pages](github-pages.md).
- **I want to catch broken public docs.** Run `docsprout audit` and read the
  [audit guide](audit.md).
- **I want to know what is tested and supported.** Read the [qualification
  evidence](qualification.md).
- **A word is unfamiliar.** Check the [glossary](glossary.md).
- **A command failed.** Find the message in [Troubleshooting](troubleshooting.md).

## ✨ What stays simple

Your project owns its words, Markdown files and visual identity. DocSprout owns
the shared page layout, search, themes, validation and publishing machinery.
Everything needed to browse a built site is stored locally, so the site does
not depend on a hosted JavaScript or CSS service.

DocSprout does not extract API descriptions from source code. Free Pascal
projects can use [PasWeave](pasweave-integration.md) for that job and feed the
resulting Markdown into DocSprout.
