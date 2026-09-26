# Custom CSS (advanced)

Custom CSS is an **advanced escape hatch** for the rare case where presets,
themes and the documented `--dk-*` tokens are not enough. A normal polished
DocSprout site never needs it: start with a [preset and visual theme](themes.md),
then exact [accent colours](themes.md#pick-an-accent-colour). Only when those
are exhausted, add a small stylesheet.

DocSprout guarantees the **safe inclusion mechanism**. It does not guarantee the
accessibility or correctness of the CSS you write. That distinction is the
contract of this feature.

Ordinary Markdown images are responsive by default: oversized images shrink to
the prose column, while smaller images keep their intrinsic size. Custom CSS is
only needed when a project deliberately wants a different presentation.

## Configure one stylesheet

1. Create the stylesheet inside your repository, for example
   `docs/assets/custom.css`.
2. Add `theme.custom_css` to `docs/docsprout.json`:

```json
{
  "schema_version": 1,
  "project": {"name": "MyLibrary-FP"},
  "theme": {
    "preset": "purple",
    "style": "classic",
    "custom_css": "docs/assets/custom.css"
  }
}
```

The path is repository-local, exactly like `identity.logo`. It is optional,
must be non-empty, must end in `.css`, and the file must exist: create the
stylesheet first, because `docsprout check` and `docsprout build` stop with a
validation error such as `theme.custom_css asset ... does not exist` when the
path is wrong. Absolute paths, parent-directory traversal and any path that
resolves outside the repository are rejected, as are symlinks or junctions that
escape the repository root. There is no network fetch and no CSS parser:
DocSprout copies the file and a generated page references it.

## Where and how it loads

The build copies the stylesheet deterministically to `assets/custom.css` and
every generated page—including pages in nested folders and every historical
release in a [versioned build](historical-docs.md)—loads it with a correct
relative reference.

The stylesheet link is placed **after** DocSprout's own `site.css` and KaTeX
styles, so your rules deliberately override DocSprout's defaults. The `--dk-*`
tokens keep working in custom CSS because they are ordinary custom properties
on the document root:

```css
/* docs/assets/custom.css */
.prose h1 {
  color: color-mix(in srgb, var(--dk-accent) 80%, var(--dk-text));
}
.prose blockquote {
  border-left-color: var(--dk-accent-secondary);
}
```

## What DocSprout owns, what you own

DocSprout guarantees the mechanics:

- safe path resolution and rejection of escaping paths;
- deterministic inclusion of the file you configured;
- correct load order (custom CSS last) on every page;
- correct relative references on nested and versioned pages;
- no generated broken links and no network dependence.

The accessibility and quality of **your** CSS is your responsibility. Custom
CSS can override accessible defaults: it can reduce contrast below the
guidelines, remove visible focus indicators, break keyboard-visible states or
hurt readability in the themes and modes you did not check. When you write
custom CSS, verify:

- Light, Dark and System mode;
- Classic, Paper, E-ink and Glassmorphic (visitors can switch the Style);
- phone and desktop widths;
- keyboard focus is still visible and the page works with a keyboard alone.

The maintained [visual fixture](visual-fixtures.md) is the working custom CSS
example: it ships a small `docs/assets/custom.css` and DocSprout's own
documentation builds it in CI.

## Before you reach for custom CSS

1. Choose one of the [four colour presets](themes.md#pick-an-accent-colour).
2. Choose Classic, Paper, E-ink or Glassmorphic.
3. Provide exact [accent colours](themes.md#pick-an-accent-colour) when your
   project already has brand colours.
4. Use the documented [`--dk-*` tokens](themes.md#the-documented-dk-tokens).
5. Only then, write the smallest custom stylesheet that closes the remaining
   gap, and keep it inside the repository.

If your custom CSS is editing the same selectors across many pages, consider
reporting a DocSprout issue with the effect you wanted instead: a documented
token or configuration option is easier for every project to maintain than a
private stylesheet.
