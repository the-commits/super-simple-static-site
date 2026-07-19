# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2023-2026 Magnus Åberg (The Commits) <himself@magnusaberg.me>

import os
import unittest
from types import SimpleNamespace

from ssss.common.md.info import variables


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


if __name__ == "__main__":
    unittest.main()
