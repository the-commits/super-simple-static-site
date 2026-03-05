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


if __name__ == "__main__":
    unittest.main()
