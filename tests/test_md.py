# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2023-2026 Magnus Åberg (The Commits) <himself@magnusaberg.me>

import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from ssss.common.md.info import posts, variables


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


if __name__ == "__main__":
    unittest.main()
