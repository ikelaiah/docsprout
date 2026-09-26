# How DocSprout renders Markdown

Most sections of this page show the Markdown source first, in a code block,
then the same content rendered by DocSprout underneath. Write the source in a
file under `docs/`, save, and reload your preview to see the same result on
your own site.

The examples use only the Markdown that DocSprout supports. Common syntax it
leaves alone is listed under
[What DocSprout does not render](#what-docsprout-does-not-render).

## Headings and the page outline

A page begins with one `#` heading. It becomes the page title in navigation
and search, so a page never needs a second one. This page's title is *How
DocSprout renders Markdown*. Section headings start at `##`:

```markdown
# Page title

## A section

### A subsection
```

Levels three to six below are real headings. They appear in the page outline,
each one gets a linkable address, and the build checks that levels never skip
upward. Keep heading text to plain words: markup written inside a heading
lands in the outline and in the address.

### Example heading level three

#### Example heading level four

##### Example heading level five

###### Example heading level six

## Emphasis and inline code

```markdown
**strong emphasis**, *emphasis*, and `inline code`
```

**strong emphasis**, *emphasis*, and `inline code` — write it that way in
prose. Only asterisks make emphasis; `__underscores__` stay literal. A code
span keeps its characters exact: the typographic conversion described below
never touches it, so `--flag` and `a--b` survive untouched.

Emphasis and code can sit inside a link label, as in **bold text inside
[this link](building.md)**.

## Links

```markdown
Start with [Build and inspect your site](building.md), jump to
[Headings and the page outline](#headings-and-the-page-outline) on this
page, or open [KaTeX](https://katex.org/).
```

Rendered:

Start with [Build and inspect your site](building.md), jump to
[Headings and the page outline](#headings-and-the-page-outline) on this
page, or open [KaTeX](https://katex.org/).

Three target types appear above: a page in this site, a heading on this
page, and an external site. Link targets are checked while the site builds.
Only `http`, `https` and `mailto` addresses are allowed; relative `.md`
targets must name a page that is published in `layout.json`; and `#fragment`
jumps must match a heading on the target page. Anything else stops the build
with a message that names the file.

## Images

```markdown
![DocSprout project mark](assets/docsprout-mark.svg)
```

![DocSprout project mark](assets/docsprout-mark.svg)

Image files live under `docs/` and are referenced from the page, so this file
uses `assets/...`. Alt text after the `!` is required: it is what a screen
reader announces and what remains when the image fails to load. Large images
shrink to the reading column, while small marks such as the one above keep
their own size.

## Lists

```markdown
- First item
- Second item
  - Nested item
  - Another nested item

1. First step
2. Second step

- [x] Task already done
- [ ] Task still open
```

Rendered:

- First item
- Second item
  - Nested item
  - Another nested item

1. First step
2. Second step

- [x] Task already done
- [ ] Task still open

Bullets accept `-`, `*` or `+`; numbered items accept `1.` or `1)`. Indent
two spaces to nest, and write `- [ ]` or `- [x]` for a task. Text wrapped onto
the next indented line joins the same item, while a blank line starts a new
list.

## Tables

```markdown
| Element | Family | Notes |
| --- | --- | --- |
| Heading | Block | `#` to `######` |
| Bold | Inline | asterisks |
| Table | Block | header, divider, rows |
```

Rendered:

| Element | Family | Notes |
| --- | --- | --- |
| Heading | Block | `#` to `######` |
| Bold | Inline | asterisks |
| Table | Block | header, divider, rows |

The first row is the header, the divider needs three or more dashes, and each
row needs a cell for every column. Column alignment markers such as `:---`
are accepted but ignored; alignment is set by the theme. Wide tables scroll
sideways instead of breaking the page, and inline formatting works inside
cells.

## Callouts

A callout starts a blockquote with a label in square brackets. Only these
four labels exist:

```markdown
> [!NOTE] Supporting detail that does not interrupt the task.

> [!TIP] A faster or safer way to finish.

> [!IMPORTANT] Something the reader must not miss.

> [!WARNING] A recoverable risk to check first.
```

Rendered:

> [!NOTE] Supporting detail that does not interrupt the task.

> [!TIP] A faster or safer way to finish.

> [!IMPORTANT] Something the reader must not miss.

> [!WARNING] A recoverable risk to check first.

The marker must begin the line, and further `>` lines underneath join the
same callout. Any other label, such as `CAUTION`, stops the build.

## Definition lists

A term on its own line, then a colon and the description. This shape suits
reference pages:

```markdown
Preview server
: Serves the built site locally and rebuilds after a saved change.
Audit
: Reports objective documentation problems in the published pages.
```

Rendered:

Preview server
: Serves the built site locally and rebuilds after a saved change.
Audit
: Reports objective documentation problems in the published pages.

Terms follow one another directly and a blank line ends the list. The
[Glossary](glossary.md) is built from terms in this shape.

## Code blocks

Three backticks on their own line open a code block, a language name may
follow them, and three backticks close it. Only the language may follow the
backticks: an extra word makes the line unrecognisable as a fence, which
leaves the block open and stops the build.

Fence markers must start at column 0. The sample below indents them by one
space only because it sits inside another code block:

```markdown
## Install DocSprout

 ```bash
 python -m pip install "docsprout"
 ```
```

DocSprout highlights `json`, `python`, `bash`, `yaml`, `markdown`, `pascal`
and their short aliases locally — no network, no CDN. Any other language is
shown as plain escaped text in a labelled block. A copy control appears on
every code block.

```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

```json
{"project": {"name": "Star Mapper"}, "schema_version": 1}
```

```bash
docsprout build --output build/site
```

```text
Anything that is not a highlighted language stays exactly as written.
```

## Mathematics

Inline math uses single dollar delimiters:

```markdown
Euler's identity is $e^{i\pi} + 1 = 0$.
```

Euler's identity is $e^{i\pi} + 1 = 0$.

Display math stands on its own line:

$$
\int_0^1 x^2\,dx = \frac{1}{3}
$$

A fenced `math` block is the clearest source for a long expression. Math is
rendered by the bundled KaTeX runtime, so it works offline; see
[Mathematics](math.md) for details.

## Typographic punctuation

```markdown
"Quoted words", an apostrophe like don't, an em dash --- like this,
an en dash -- like this, and a closing ellipsis...
```

"Quoted words", an apostrophe like don't, an em dash --- like this, an en
dash -- like this, and a closing ellipsis... The conversion happens in prose
only: code spans, math and link targets keep their exact characters, so
`--flag` never becomes a dash. [Authoring recipes](authoring-recipes.md)
explains the rule in full.

## What DocSprout does not render

This Markdown is deliberately small. The syntax below prints literally, or
does something other than what other tools do. Each example is shown inside
a code block; the line after it explains what happens.

> [!WARNING] Two mistakes stop the build rather than printing literally: an
> admonition label outside NOTE, TIP, IMPORTANT and WARNING, and a code fence
> left unclosed. The terminal message names the file and the line.

A plain quotation prints its own `>` characters:

```markdown
> An ordinary quotation.
```

It appears as text starting with `>`, not as a quotation. Use a callout
instead.

A horizontal rule has no form. Three dashes on a line of their own become an
em dash inside a paragraph:

```markdown
First section.

---

Second section.
```

Start a new section with a `##` heading instead.

Strikethrough is not available:

```markdown
Use ~~deleted words~~ sparingly.
```

The tildes stay visible. Use plain words, or **strong emphasis** instead.

Footnotes are not collected:

```markdown
A claim[^1].

[^1]: The source of the claim.
```

Both lines print as written. Put the note in a callout or in a definition
list.

Page front matter has no special meaning. A `---` block at the top of the
file is printed as visible text:

```markdown
---
title: My page
---

The real content starts here.
```

Delete the front matter; site settings belong in
[Configuration](configuration.md), in `docsprout.json` and `layout.json`.

Angle-bracket autolinks are not recognised:

```markdown
Open <https://example.com> for details.
```

The angle brackets appear in the output. Write the label and the target in
the link form shown under [Links](#links).

Raw HTML is escaped and shown as text, never executed:

```markdown
<span style="color: red">Warning</span>
```

The reader sees the tags themselves. Write Markdown instead, and use
[Custom CSS](custom-css.md) for presentation.

Underscores do not make emphasis:

```markdown
__bold__ and _italic_ stay literal
```

Use double asterisks around bold text and single asterisks around italic
text.

Indented code blocks are treated as paragraphs:

```markdown
    docsprout build
```

Four spaces are not a code block here. Use three backticks instead.

Setext heading underlines do not exist:

```markdown
A section title
---------------
```

The underline prints as punctuation after the title. Write `## A section
title` instead, with the hashes at the start of the line.

Trailing spaces do not force a line break:

```markdown
first line  
second line
```

The two lines are joined into one sentence. Begin a new paragraph with a
blank line.

Link titles are not supported:

```markdown
[Docs](building.md "Hover text")
```

The quoted text ends up inside the address and breaks the link. Leave it
out.

## Cheat sheet

One file containing the syntax from this page. Copy it into `docs/`, add it
to `layout.json`, point the image at a file you have or delete that line, and
run `docsprout serve` to see every construct at once:

```markdown
# My page title

## A section

### A subsection

**strong**, *emphasis*, `inline code`

[Site link](https://example.com)

![Descriptive alt text](assets/image.svg)

- Bullet
  - Nested bullet

1. Numbered step

- [ ] Open task
- [x] Done task

> [!NOTE] A callout.

| Column | Column |
| --- | --- |
| Cell | Cell |

Term
: Description

Euler's identity is $e^{i\pi} + 1 = 0$.

"Smart" punctuation converts --- in prose only.
```

## Where to go next

- [Write documentation people can use](writing-great-docs.md) for structure
  and voice before you write more pages.
- [Your first DocSprout site](beginners-guide.md) builds a site from an
  ordinary project folder.
- [Authoring recipes](authoring-recipes.md) for page layouts that suit a
  library, an application or an API reference.
- [Mathematics](math.md) for the bundled KaTeX setup.
- [Visual fixtures](visual-fixtures.md) for every component in every theme
  and colour mode.
- [Glossary](glossary.md) for any term used on this site.
