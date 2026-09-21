# Visual component fixture

Use this maintained page to inspect every built-in visual theme at phone,
tablet and desktop widths in both light and dark colour modes.

> [!IMPORTANT] Keyboard focus must remain visible on every control and link.

## Typography and lists

Readable documentation needs a clear hierarchy, comfortable measure and
predictable rhythm. Inline `PascalCase` identifiers should remain distinct from
body copy, while **strong text** and [useful links](long-form.md) retain enough
contrast.

- [x] Theme tokens stay semantic.
- [ ] Inspect the current viewport.
- Nested lists keep a readable indent:
  - Child items stay attached to their parent.
  - Longer child text wraps without losing the hierarchy.

1. Start with a small viewport.
2. Switch through each visual theme.
3. Repeat in both colour modes.

### Heading level three

#### Heading level four

##### Heading level five

###### Heading level six

Deep headings keep the same family and rhythm as the rest of the hierarchy.

### Typographic details

Prose receives typographic punctuation: "quoted phrases", apostrophes like
don't, a spaced em dash --- like this --- an en dash -- like this -- and a
closing ellipsis... That happens outside code, so `--flag`, `don't` and
`a--b` stay exact. A long compound word such as
Donaudampfschifffahrtsgesellschaftskapitän also stays inside the reading
measure at narrow widths.

## Reference table

| Element | Compact | Comfortable | Wide |
| --- | --- | --- | --- |
| Prose | Focused guides | Default reading | API tables |
| Code | Scrolls safely | Scrolls safely | Shows more context |
| Navigation | Responsive | Responsive | Responsive |

## API reference shape

`TFixturePage`
: A representative page entry used to exercise reference-style prose.

`TFixturePage.Title`
: The visible name shown in navigation and search results.

## Code block

```pascal
procedure Greet(const Name: string);
begin
  WriteLn('Hello, ', Name);
end;
```

## Callout variants

> [!NOTE] Notes provide supporting context without interrupting the task.

> [!WARNING] Warnings identify a recoverable risk before publication.

> [!TIP] Tips identify a safer or faster way to complete a task.

## Responsive Markdown images

Markdown images are responsive by default: oversized artwork shrinks to the
prose column while small badges retain their intrinsic size. This fixture keeps
both cases visible for review at desktop, tablet and phone widths.

![Deliberately oversized prose illustration](assets/oversized-prose-image.svg)

![Small intrinsic-size badge](assets/small-badge.svg)
