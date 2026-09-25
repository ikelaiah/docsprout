# Long-form reading fixture

This page exercises sustained reading, section rhythm, the table of contents,
page navigation and the reading-progress indicator.

## Why reading measure matters

Documentation often combines conceptual explanation with exact commands. A
comfortable line length lets a maintainer scan prose without losing their place,
while a wider layout gives tables and source examples enough room. The layout
choice therefore changes the content column without changing the semantic theme
or the meaning of any page.

The default remains comfortable so existing projects keep their established
shape. Compact is useful for tutorial prose. Wide is intended for reference
material with larger tables and code samples; ordinary paragraphs retain a
separate readable maximum measure.

## Repeated sections

Long documents need enough space before headings to make section boundaries
obvious. They also need restrained spacing within a section so related ideas
remain visually connected.

### Keyboard path

Press `/` to focus search. Use Arrow keys, Home and End to move through search
results, Enter to open a result and Escape to close the result region. Tab then
moves through version, visual-theme and colour controls in source order.

### Responsive path

At phone width, navigation becomes a native disclosure and copy buttons remain
visible without hover. At tablet width, the content uses the available space
without horizontal page scrolling. At desktop width, local navigation and the
on-page outline frame the reading column.

## Reference table shape

Reference pages often need more columns than a phone can display. The table is
allowed to scroll inside its own frame while the page itself remains fixed:

| API surface | Type | Required | Notes for maintainers | Since |
| --- | --- | --- | --- | --- |
| `Title` | `string` | yes | Appears in navigation and search | 0.12 |
| `Description` | `string` | no | Keeps the page introduction useful | 0.12 |
| `Source` | `path` | yes | Must remain inside the project | 0.12 |

```pascal
function BuildFixture(const Source: string; WideLayout: Boolean): string;
begin
  if WideLayout then
    Result := 'Reference layout'
  else
    Result := 'Reading layout';
end;
```

## Closing check

The final section makes the fixture tall enough to exercise reading progress and
sticky navigation. Inspect this page in Classic, Paper and E-ink, then repeat
with Light, Dark and System colour choices.
