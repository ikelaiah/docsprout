import unittest

from docsprout.markdown import render_markdown


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
