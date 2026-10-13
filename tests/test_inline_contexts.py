"""Inline formatting must never cross into generated HTML attributes."""

from html.parser import HTMLParser
import unittest

from docsprout.markdown import render_markdown


class Elements(HTMLParser):
    def __init__(self, source: str) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str | None]]] = []
        self.feed(source)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append((tag, dict(attrs)))


class InlineContextTests(unittest.TestCase):
    def test_code_and_math_in_image_descriptions_cannot_create_attributes(self) -> None:
        for description in ('`" onerror="alert`', '$x^2$', '**bold** and ~~old~~'):
            with self.subTest(description=description):
                rendered = render_markdown(f'![{description}](diagram.svg)', lambda target: target)
                tags = Elements(rendered.html).tags
                self.assertEqual(['p', 'img'], [tag for tag, _attrs in tags])
                self.assertEqual({'src', 'alt'}, set(tags[1][1]))
                self.assertNotIn('<', tags[1][1]['alt'])

    def test_link_targets_reach_the_resolver_and_browser_unchanged(self) -> None:
        for target in ('https://example.test/$value$', 'https://example.test/`value`',
                       'https://example.test/**value**', 'https://example.test/~~value~~',
                       'https://example.test/`&amp;`', 'https://example.test/$&quot;$'):
            with self.subTest(target=target):
                resolved = []

                def resolve(value: str) -> str:
                    resolved.append(value)
                    return value

                rendered = render_markdown(f'[Example]({target})', resolve)
                self.assertEqual([target], resolved)
                self.assertEqual([('p', {}), ('a', {'href': target})], Elements(rendered.html).tags)

    def test_unsupported_image_inside_a_target_does_not_crash(self) -> None:
        rendered = render_markdown('[Example](https://example.test/![alt](image.svg))', lambda target: target)
        self.assertIn(('a', {'href': 'https://example.test/![alt](image.svg)'}), Elements(rendered.html).tags)

    def test_formatted_link_label_does_not_format_its_target(self) -> None:
        rendered = render_markdown('[**Read** `--flag` $x$](https://example.test/**path**)', lambda target: target)
        self.assertIn('<strong>Read</strong> <code>--flag</code>', rendered.html)
        self.assertIn('data-tex="x"', rendered.html)
        self.assertIn(('a', {'href': 'https://example.test/**path**'}), Elements(rendered.html).tags)

    def test_linked_image_keeps_safe_plain_alt_and_exact_destinations(self) -> None:
        rendered = render_markdown('[![A `--flag` diagram](diagram.svg)](guide.md)', lambda target: target)
        self.assertEqual(
            [('p', {}), ('a', {'href': 'guide.md'}), ('img', {'src': 'diagram.svg', 'alt': 'A --flag diagram'})],
            Elements(rendered.html).tags,
        )
