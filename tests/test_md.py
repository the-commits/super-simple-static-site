# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2023-2026 Magnus Åberg (The Commits) <himself@magnusaberg.me>

import os
import tempfile
import unittest
from datetime import date
from pathlib import Path
from types import SimpleNamespace

from ssss.common.md.info import parse_date, posts, variables


class Variables(unittest.TestCase):
    def _make_template(self, content):
        path = "/tmp/test_ssss_variables.md"
        with open(path, "w") as f:
            f.write(content)
        return SimpleNamespace(filename=path)

    def tearDown(self):
        path = "/tmp/test_ssss_variables.md"
        if os.path.exists(path):
            os.unlink(path)

    def test_variables_without_meta(self):
        template = self._make_template("# Hello\n\nWorld\n")
        result = variables(template)
        self.assertIn("content", result)
        self.assertIn("<h1>Hello</h1>", result["content"])

    def test_variables_unwraps_single_meta_values(self):
        template = self._make_template("title: My Page\nauthor: Alice\n\n# Hello\n")
        result = variables(template)
        self.assertEqual(result["title"], "My Page")
        self.assertEqual(result["author"], "Alice")

    def test_variables_keeps_multiline_meta_values_as_lists(self):
        template = self._make_template("title: My Page\ntags: one\n    two\n\n# {{ tags | join(', ') }}\n")
        result = variables(template)
        self.assertEqual(result["title"], "My Page")
        self.assertEqual(result["tags"], ["one", "two"])
        self.assertIn("<h1>one, two</h1>", result["content"])

    def test_variables_fenced_code_and_lists(self):
        content = (
            "title: Code Test\n\n"
            "# {{ title }}\n\n"
            "**References:**\n\n"
            "- [Link](https://example.com)\n\n"
            "```c\n"
            "#include <stdio.h>\n"
            "int main(void) { return 0; }\n"
            "```\n"
        )
        template = self._make_template(content)
        result = variables(template)
        self.assertIn("<h1>Code Test</h1>", result["content"])
        self.assertIn('<ul>\n<li><a href="https://example.com">Link</a></li>\n</ul>', result["content"])
        self.assertIn('<pre><code class="language-c">#include &lt;stdio.h&gt;', result["content"])


class Posts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        blog = self.root / "blog"
        blog.mkdir()
        (blog / "index.md").write_text(
            "Title: Blog\n\n"
            "{% for post in posts('blog') -%}\n"
            "- {{ post.title }} {{ post.date }}\n"
            "{% endfor %}\n"
        )
        (blog / "older.md").write_text("Title: Older\nDate: 2026-01-01\n\n# Older\n")
        (blog / "newer.md").write_text("Title: Newer\nDate: 2026-11-01\nDescription: New one\n\n# Newer\n")
        (blog / "no-date.md").write_text("# No date\n")
        (blog / "_draft.md").write_text("Title: Draft\nDate: 2027-01-01\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_posts_reads_meta_sorted_newest_first(self):
        result = posts(self.root, "blog")
        self.assertEqual([p["title"] for p in result], ["Newer", "Older", "No Date"])
        self.assertEqual(result[0]["url"], "/blog/newer.html")
        self.assertEqual(result[0]["page_url"], "/blog/newer")
        self.assertEqual(result[0]["description"], "New one")
        self.assertNotIn("date", result[2])

    def test_variables_exposes_posts_function(self):
        template = SimpleNamespace(filename=str(self.root / "blog" / "index.md"), name="blog/index.md")
        content = variables(template)["content"]
        self.assertIn("<li>Newer 2026-11-01</li>\n<li>Older 2026-01-01</li>", content)
        self.assertNotIn("Draft", content)

    def test_posts_frontmatter_key_does_not_hide_posts_function(self):
        index = self.root / "blog" / "index.md"
        index.write_text("Posts: 10\n" + index.read_text())
        template = SimpleNamespace(filename=str(index), name="blog/index.md")
        result = variables(template)
        self.assertEqual(result["posts"], "10")
        self.assertIn("<li>Newer 2026-11-01</li>", result["content"])


class ParseDate(unittest.TestCase):
    def test_parse_date_iso_with_and_without_padding(self):
        self.assertEqual(parse_date("2026-07-29"), date(2026, 7, 29))
        self.assertEqual(parse_date("2026-7-1"), date(2026, 7, 1))
        self.assertEqual(parse_date("2026-07-29T10:00:00+02:00"), date(2026, 7, 29))
        self.assertEqual(parse_date("2026-07-29 10:00"), date(2026, 7, 29))

    def test_parse_date_rfc2822_and_month_names(self):
        self.assertEqual(parse_date("Wed, 29 Jul 2026 10:00:00 +0200"), date(2026, 7, 29))
        self.assertEqual(parse_date("July 29, 2026"), date(2026, 7, 29))
        self.assertEqual(parse_date("Jul 29, 2026"), date(2026, 7, 29))
        self.assertEqual(parse_date("29 July 2026"), date(2026, 7, 29))

    def test_parse_date_uses_first_line_of_multiline_value(self):
        self.assertEqual(parse_date(["2026-07-29", "ignored"]), date(2026, 7, 29))
        self.assertIsNone(parse_date([]))

    def test_parse_date_returns_none_for_non_dates(self):
        self.assertIsNone(parse_date(None))
        self.assertIsNone(parse_date(""))
        self.assertIsNone(parse_date("2026-13-01"))
        self.assertIsNone(parse_date("someday"))
        self.assertIsNone(parse_date("20260-07-29"))


class PostsDateSort(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        blog = self.root / "blog"
        blog.mkdir()
        (blog / "july.md").write_text("Title: July\nDate: 2026-7-1\n\n# July\n")
        (blog / "november.md").write_text("Title: November\nDate: 2026-11-01\n\n# November\n")
        (blog / "august.md").write_text("Title: August\nDate: August 15, 2026\n\n# August\n")
        (blog / "multiline.md").write_text("Title: Multi\nDate: 2026-12-01\n    later line\n\n# Multi\n")
        (blog / "bad-date.md").write_text("Title: Bad\nDate: someday\n\n# Bad\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_posts_sorts_by_parsed_date(self):
        result = posts(self.root, "blog")
        self.assertEqual([p["title"] for p in result], ["Multi", "November", "August", "July", "Bad"])
        self.assertEqual(result[2]["date"], "August 15, 2026")


class PostsSameDate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        blog = self.root / "blog"
        blog.mkdir()
        for name in ("charlie", "alpha", "delta", "bravo"):
            (blog / (name + ".md")).write_text("Title: " + name + "\nDate: 2026-11-01\n\n# " + name + "\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_posts_with_same_date_are_ordered_by_url(self):
        result = posts(self.root, "blog")
        self.assertEqual([p["title"] for p in result], ["alpha", "bravo", "charlie", "delta"])


if __name__ == "__main__":
    unittest.main()
