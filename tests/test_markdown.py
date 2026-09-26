import html
import json
import re
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from docsprout.build import build_site
from docsprout.markdown import render_markdown


class _ImageCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "img":
            self.images.append({name: value or "" for name, value in attrs})


class MarkdownTests(unittest.TestCase):
    def test_typographic_punctuation_reaches_prose_but_not_code_math_or_link_targets(self) -> None:
        rendered = render_markdown(
            "Quotes \"like this\" and an apostrophe don't stop a dash --- or an en dash -- "
            "or an ellipsis... Keep `--flag`, `don't` and $a--b$ exact, "
            "and [the label -- here](a--b.md).",
            lambda target: target,
        )

        self.assertIn("“like this”", rendered.html)
        self.assertIn("don’t", rendered.html)
        self.assertIn("—", rendered.html)
        self.assertIn("–", rendered.html)
        self.assertIn("…", rendered.html)
        self.assertIn("<code>--flag</code>", rendered.html)
        self.assertIn("<code>don't</code>", rendered.html)
        self.assertIn('data-tex="a--b"', rendered.html)
        self.assertIn('href="a--b.md"', rendered.html)
        self.assertIn("the label – here", rendered.html)

    def test_disambiguates_repeated_heading_slugs_with_a_stable_suffix(self) -> None:
        rendered = render_markdown("## Setup\n\nFirst.\n\n## Setup\n\nSecond.", lambda target: target)

        self.assertEqual(
            ("setup", "setup-2"),
            tuple(identifier for _level, _text, identifier in rendered.headings),
        )
        self.assertIn('id="setup"', rendered.html)
        self.assertIn('id="setup-2"', rendered.html)

    def test_renders_safe_task_lists_for_documentation_checklists(self) -> None:
        rendered = render_markdown("- [ ] Write guide\n- [x] Run check", lambda target: target)

        self.assertIn('class="task-list"', rendered.html)
        self.assertIn('aria-label="Incomplete"', rendered.html)
        self.assertIn('aria-label="Complete"', rendered.html)

    def test_renders_github_style_admonitions_without_the_bang(self) -> None:
        rendered = render_markdown("> [!IMPORTANT] Keep history accurate.", lambda target: target)

        self.assertIn('class="admonition important"', rendered.html)
        self.assertIn("<strong>Important</strong>", rendered.html)

    def test_keeps_wrapped_list_item_content_in_the_same_list_item(self) -> None:
        rendered = render_markdown(
            "- Follow the\n  [beginner's guide](beginners-guide.md).\n- Then build the site.",
            lambda target: target,
        )

        self.assertEqual(
            rendered.html,
            '<ul><li>Follow the <a href="beginners-guide.md">beginner’s guide</a>.</li><li>Then build the site.</li></ul>',
        )

    def test_preserves_indented_nested_lists_inside_their_parent_item(self) -> None:
        rendered = render_markdown(
            "- Parent\n  - Child\n  - Another child\n- Sibling",
            lambda target: target,
        )

        self.assertEqual(
            rendered.html,
            "<ul><li>Parent<ul><li>Child</li><li>Another child</li></ul></li><li>Sibling</li></ul>",
        )

    def test_keeps_following_quote_lines_inside_an_admonition(self) -> None:
        rendered = render_markdown(
            "> [!TIP] Start with one page.\n> It takes only a few minutes.",
            lambda target: target,
        )

        self.assertEqual(
            rendered.html,
            '<aside class="admonition tip"><strong>Tip</strong><p>Start with one page. It takes only a few minutes.</p></aside>',
        )

    def test_marks_inline_display_and_fenced_math_for_katex(self) -> None:
        rendered = render_markdown(
            "Inline $x^2$\n\n$$\n\\int_0^1 x dx\n$$\n\n```math\n\\frac{a}{b}\n```",
            lambda target: target,
        )

        self.assertIn('class="math-inline" data-tex="x^2"', rendered.html)
        self.assertIn('class="math-display" data-tex="\\int_0^1 x dx"', rendered.html)
        self.assertIn('class="math-display" data-tex="\\frac{a}{b}"', rendered.html)

    def test_renders_safe_definition_lists_for_reference_prose(self) -> None:
        rendered = render_markdown(
            "Widget\n: A reusable **component**.\n\nUnsafe <term>\n: Escaped <description>.",
            lambda target: target,
        )

        self.assertIn("<dl><dt>Widget</dt><dd>A reusable <strong>component</strong>.</dd>", rendered.html)
        self.assertIn("<dt>Unsafe &lt;term&gt;</dt><dd>Escaped &lt;description&gt;.</dd>", rendered.html)

    def test_highlights_supported_fenced_code_without_trusting_source_html(self) -> None:
        rendered = render_markdown(
            "```json\n{\"enabled\": true, \"label\": \"<safe>\"}\n```\n\n"
            "```pascal\nprogram Demo;\nbegin\n  WriteLn('hello');\nend.\n```",
            lambda target: target,
        )

        self.assertIn('class="language-json syntax-highlight"', rendered.html)
        self.assertIn('<span class="tok-property">&quot;enabled&quot;</span>', rendered.html)
        self.assertIn('<span class="tok-boolean">true</span>', rendered.html)
        self.assertIn('&lt;safe&gt;', rendered.html)
        self.assertIn('<span class="tok-keyword">program</span>', rendered.html)
        self.assertIn('<span class="tok-function">WriteLn</span>', rendered.html)

    def test_highlights_documented_languages_and_keeps_unknown_fences_plain(self) -> None:
        rendered = render_markdown(
            "```fpc\nbegin WriteLn('hello'); end.\n```\n\n"
            "```python\ndef greet():\n  print('hello')\n```\n\n"
            "```bash\necho hello\n```\n\n"
            "```yaml\nenabled: true\n```\n\n"
            "```markdown\n# Heading\n```\n\n"
            "```text\n<plain>\n```",
            lambda target: target,
        )

        self.assertIn('class="language-fpc syntax-highlight"', rendered.html)
        self.assertIn('<span class="tok-keyword">def</span>', rendered.html)
        self.assertIn('<span class="tok-function">echo</span>', rendered.html)
        self.assertIn('<span class="tok-property">enabled</span>', rendered.html)
        self.assertIn('<span class="tok-heading"># Heading</span>', rendered.html)
        self.assertIn('<pre class="language-text"><code>&lt;plain&gt;</code></pre>', rendered.html)


def _collect_images(output: str) -> list[dict[str, str]]:
    collector = _ImageCollector()
    collector.feed(output)
    return collector.images


def _assert_single_safe_image(output: str, *, src: str, alt_text: str) -> dict[str, str]:
    tags = re.findall(r"<img\b[^>]*>", output)
    assert len(tags) == 1, f"expected one image element, found {tags!r} in {output!r}"
    assert re.fullmatch(r'<img src="[^"]*" alt="[^"]*">', tags[0]), f"image element is not one safe element: {tags[0]!r}"
    images = _collect_images(output)
    assert len(images) == 1, f"expected one parsed image, found {images!r}"
    image = images[0]
    assert set(image) == {"src", "alt"}, f"image has unexpected attributes: {image!r}"
    assert "onerror" not in image and "onclick" not in image, f"injected event attribute: {image!r}"
    assert image["src"] == src, f"unexpected src: {image!r}"
    assert image["alt"] == alt_text, f"unexpected alt text: {image!r}"
    return image


class ImageAltEscapingTests(unittest.TestCase):
    def test_ordinary_alt_text_is_preserved(self) -> None:
        rendered = render_markdown("![Normal diagram](images/diagram.svg)", lambda target: target)

        _assert_single_safe_image(rendered.html, src="images/diagram.svg", alt_text="Normal diagram")
        self.assertIn('alt="Normal diagram"', rendered.html)

    def test_quoted_alt_text_keeps_typography_without_breakout(self) -> None:
        rendered = render_markdown('![A "quoted" diagram](images/diagram.svg)', lambda target: target)

        # Straight quotes in prose become typographic quotes, which stay literal in the attribute.
        _assert_single_safe_image(rendered.html, src="images/diagram.svg", alt_text="A “quoted” diagram")
        self.assertIn('alt="A “quoted” diagram"', rendered.html)

    def test_special_characters_are_escaped_without_double_escaping(self) -> None:
        rendered = render_markdown("![Fish & chips <diagram>](images/diagram.svg)", lambda target: target)

        _assert_single_safe_image(rendered.html, src="images/diagram.svg", alt_text="Fish & chips <diagram>")
        self.assertIn('alt="Fish &amp; chips &lt;diagram&gt;"', rendered.html)
        self.assertNotIn("&amp;amp;", rendered.html)

    def test_malicious_alt_cannot_inject_attributes(self) -> None:
        payloads = [
            '![x" onerror="alert(1)](images/diagram.svg)',
            "![x' onclick='alert(1)](images/diagram.svg)",
            '![a "\' <>& onclick="alert(1)" onerror=\'alert(1)](images/diagram.svg)',
        ]
        for source in payloads:
            with self.subTest(source=source):
                rendered = render_markdown(source, lambda target: target)
                images = _collect_images(rendered.html)
                self.assertEqual(1, len(images))
                image = images[0]
                self.assertEqual({"src", "alt"}, set(image))
                self.assertNotIn("onerror", image)
                self.assertNotIn("onclick", image)
                self.assertEqual("images/diagram.svg", image["src"])
                # The payload text stays as text inside alt; it must not become markup.
                self.assertIn("onerror" if "onerror" in source else "onclick", html.unescape(image["alt"]))
                tags = re.findall(r"<img\b[^>]*>", rendered.html)
                self.assertEqual(1, len(tags))
                self.assertIsNotNone(re.fullmatch(r'<img src="[^"]*" alt="[^"]*">', tags[0]))

    def test_straight_quote_alt_reaching_the_attribute_is_escaped(self) -> None:
        # Code spans are protected from typographic quotes, so a straight quote
        # survives to the image substitution. The attribute must still be safe.
        # This payload produced alt="x" onerror="alert(1)" on v1.1.5.
        rendered = render_markdown('`![x" onerror="alert(1)](images/diagram.svg)`', lambda target: target)

        self.assertIn("&quot;", rendered.html)
        images = _collect_images(rendered.html)
        self.assertEqual(1, len(images))
        image = images[0]
        self.assertEqual({"src", "alt"}, set(image))
        self.assertNotIn("onerror", image)
        self.assertEqual("images/diagram.svg", image["src"])
        self.assertEqual('x" onerror="alert(1)', image["alt"])
        tags = re.findall(r"<img\b[^>]*>", rendered.html)
        self.assertEqual(1, len(tags))
        self.assertIsNotNone(re.fullmatch(r'<img src="[^"]*" alt="[^"]*">', tags[0]))

    def test_build_publishes_malicious_alt_safely_with_real_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            (docs / "images").mkdir(parents=True)
            (docs / "images" / "diagram.svg").write_text("<svg/>", encoding="utf-8")
            (docs / "index.md").write_text(
                "# Home\n\n"
                "![Normal diagram](images/diagram.svg)\n\n"
                "![Fish & chips <diagram>](images/diagram.svg)\n\n"
                '![x" onerror="alert(1)](images/diagram.svg)\n',
                encoding="utf-8",
            )
            (docs / "docsprout.json").write_text(json.dumps({"schema_version": 1, "project": {"name": "Demo"}}), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({
                "schema_version": 1,
                "navigation": [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}]}],
            }), encoding="utf-8")

            build_site(root=root, output=root / "site", release="dev")

            page = (root / "site" / "index.html").read_text(encoding="utf-8")
            images = _collect_images(page)
            content_images = [image for image in images if "content/images/diagram.svg" in image.get("src", "")]
            self.assertEqual(3, len(content_images))
            for image in content_images:
                with self.subTest(image=image):
                    self.assertEqual({"src", "alt"}, set(image))
                    self.assertNotIn("onerror", image)
                    self.assertNotIn("onclick", image)
            alts = sorted(image["alt"] for image in content_images)
            self.assertIn("Normal diagram", alts)
            self.assertIn("Fish & chips <diagram>", alts)
            self.assertTrue(any("onerror" in alt for alt in alts))
            self.assertIn('alt="Fish &amp; chips &lt;diagram&gt;"', page)
            self.assertTrue((root / "site" / "assets" / "content" / "images" / "diagram.svg").is_file())
