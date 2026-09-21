# Write documentation people can use

Good documentation helps a real person finish a real task. It does not need
fancy words, and it does not matter whether the code is Pascal, Python,
JavaScript or something else.

Use this guide before worrying about colours or a perfect site structure.

## Start with one reader and one result

Before writing a page, finish this sentence:

> This page helps **[person]** to **[result]**.

For example:

> This page helps a student who knows basic Pascal to load their first JSON
> file and print one value.

That sentence tells you what belongs on the page. Interesting details that do
not help with the result can move to a later guide or reference page.

## Build the smallest useful set of pages

Most new projects need only four kinds of information:

1. **Overview:** What does this project do, and who is it for?
2. **Installation:** What must the reader have, and what command installs it?
3. **Quick start:** What is the smallest working example?
4. **Help:** What common problem might block the reader?

Add detailed guides and API reference only when readers need them. An honest
four-page site is more useful than twenty empty headings.

For Free Pascal, a quick start might compile one `.pas` file and show its
output. For another language, use that language's smallest normal run command.
The teaching shape stays the same.

## Use the same friendly shape on every task page

A tired reader should not have to guess where the instructions begin. Use this
order:

1. Say what the reader will achieve.
2. List what they need before starting.
3. Give one action per numbered step.
4. Show a complete, small example.
5. Show what success looks like.
6. Explain the most likely failure.
7. Link to one sensible next step.

Use this Markdown page shape:

```markdown
# Create your first report

This guide creates a small report from one input file.

## Before you begin

You need Example Tool 2.0 or newer and a terminal in the project folder.

## 1. Create the input

Save a two-line file named `input.txt` with one name and score per line.

## 2. Run the command

Run `example-tool input.txt` from the project folder.

You should see `Created report.html`.

## If it does not work

If you see `input.txt not found`, check that the terminal and file are in the
same folder.

## Next step

Continue with the page named “Change the report layout”.
```

When the page shape is clear, put commands in their own fenced code blocks so
they are easy to copy:

```bash
example-tool input.txt
```

Name the language after the opening fence when you can. DocSprout highlights
`json`, `pascal` (also `fpc`), `python`, `bash`, `yaml` and `markdown` locally;
other names stay as readable plain code. This never needs a CDN or a browser
extension:

```json
{"retries": 3, "quiet": false}
```

## Make code examples kind

- Prefer one complete small example over several fragments.
- Name the file when the reader must create one.
- Name the folder where a command runs.
- Include required `uses`, imports or setup lines.
- Put sample output after the command, not inside it.
- Use believable names such as `first-light.csv`, not unexplained `foo` and
  `bar`.
- Test every command by copying it into a clean project.

If an example skips something, say what it skips and link to the missing step.
Never make the reader wonder whether the omission is their mistake.

## Write for a tired brain

Readers often arrive after an error, late at night, or while learning several
ideas at once. Help them by using:

- short paragraphs;
- familiar words;
- headings that describe a goal;
- numbered steps for ordered work;
- bullets for choices or facts;
- **must** for requirements and **can** for optional actions;
- exact messages for expected success and common errors.

Define an unavoidable technical term the first time you use it. You can link to
the [glossary](glossary.md) instead of interrupting every guide with a long
definition.

## Review the page as a beginner

Before publishing, ask someone—or your future tired self—to follow the page
without guessing:

- [ ] Does the first paragraph promise a clear result?
- [ ] Are all prerequisites listed before step 1?
- [ ] Does every command say where to run it?
- [ ] Can the smallest example be copied exactly?
- [ ] Does the page show what success looks like?
- [ ] Is the most likely failure explained?
- [ ] Are new terms defined?
- [ ] Is there one clear next step?

Run `docsprout check` after adding the page. It catches broken links and pages
that are missing from navigation. For suggested folder structures, continue to
[Authoring recipes](authoring-recipes.md).
