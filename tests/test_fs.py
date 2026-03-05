import os
import unittest

from ssss.common.fs.directory import get_full_path, get_current_directory, make_empty
from ssss.common.fs.file import find_config, write_if_not_exists, touch_if_not_exists
from ssss.common.application import application_name
from ssss.common.application.variables import read_scaffold_file


class Fullpath(unittest.TestCase):
    def test_empty_full_path(self):
        path = get_full_path("")
        self.assertEqual(get_current_directory(), path)

    def test_dot_full_path(self):
        path = get_full_path(".")
        self.assertEqual(get_current_directory(), path)

    def test_none_full_path(self):
        path = get_full_path(None)
        self.assertEqual(get_current_directory(), path)


class MakeEmpty(unittest.TestCase):
    def test_make_empty_nonexistent_path_is_noop(self):
        make_empty("/tmp/ssss_does_not_exist_xyz")


class FindConfig(unittest.TestCase):
    def test_finds_config_in_current_directory(self):
        config_path = os.path.join(get_current_directory(), application_name() + ".yml")
        with open(config_path, "w") as f:
            f.write("site:\n  title: Test\n")
        try:
            result = find_config()
            self.assertEqual(result, os.path.abspath(config_path))
        finally:
            os.unlink(config_path)


class WriteIfNotExists(unittest.TestCase):
    def test_creates_file_with_content(self):
        path = "/tmp/test_write_if_not_exists.txt"
        if os.path.exists(path):
            os.unlink(path)
        write_if_not_exists(path, "hello")
        with open(path, "r") as f:
            self.assertEqual(f.read(), "hello")
        os.unlink(path)

    def test_does_not_overwrite_existing_file(self):
        path = "/tmp/test_write_if_not_exists_existing.txt"
        with open(path, "w") as f:
            f.write("original")
        write_if_not_exists(path, "new content")
        with open(path, "r") as f:
            self.assertEqual(f.read(), "original")
        os.unlink(path)


class TouchIfNotExists(unittest.TestCase):
    def test_touch_creates_file(self):
        path = "/tmp/test_touch_if_not_exists.txt"
        if os.path.exists(path):
            os.unlink(path)
        touch_if_not_exists(path)
        self.assertTrue(os.path.exists(path))
        os.unlink(path)

    def test_touch_existing_file_is_noop(self):
        path = "/tmp/test_touch_if_not_exists_existing.txt"
        with open(path, "w") as f:
            f.write("original")
        touch_if_not_exists(path)
        with open(path, "r") as f:
            self.assertEqual(f.read(), "original")
        os.unlink(path)


if __name__ == "__main__":
    unittest.main()


class ReadScaffoldFile(unittest.TestCase):
    def test_read_scaffold_base_html_returns_string(self):
        content = read_scaffold_file("base.html")
        self.assertIsInstance(content, str)
        self.assertIn("<!doctype html>", content)

    def test_read_scaffold_base_html_has_og_meta(self):
        content = read_scaffold_file("base.html")
        self.assertIn('property="og:title"', content)
        self.assertIn('property="og:description"', content)
        self.assertIn('property="og:url"', content)

    def test_read_scaffold_base_html_has_twitter_meta(self):
        content = read_scaffold_file("base.html")
        self.assertIn('name="twitter:card"', content)
        self.assertIn('name="twitter:title"', content)

    def test_read_scaffold_base_html_has_canonical(self):
        content = read_scaffold_file("base.html")
        self.assertIn('rel="canonical"', content)

    def test_read_scaffold_base_html_has_color_scheme(self):
        content = read_scaffold_file("base.html")
        self.assertIn('name="color-scheme"', content)

    def test_read_scaffold_default_j2_returns_string(self):
        content = read_scaffold_file("default.j2")
        self.assertIsInstance(content, str)
        self.assertIn("{% block content %}", content)

    def test_read_scaffold_index_md_has_welcome(self):
        content = read_scaffold_file("index.md")
        self.assertIsInstance(content, str)
        self.assertIn("Welcome to your ssss-site", content)

    def test_read_scaffold_base_html_has_rss_link(self):
        content = read_scaffold_file("base.html")
        self.assertIn('type="application/rss+xml"', content)

    def test_read_scaffold_base_html_has_sitemap_link(self):
        content = read_scaffold_file("base.html")
        self.assertIn('rel="sitemap"', content)

    def test_read_scaffold_sitemap_xml_is_valid(self):
        content = read_scaffold_file("sitemap.xml.j2")
        self.assertIn("<urlset", content)
        self.assertIn("sitemaps.org", content)

    def test_read_scaffold_rss_xml_is_valid(self):
        content = read_scaffold_file("rss.xml.j2")
        self.assertIn("<rss", content)
        self.assertIn("<channel>", content)

    def test_read_scaffold_llms_txt_is_valid(self):
        content = read_scaffold_file("llms.txt.j2")
        self.assertIn("# ", content)
        self.assertIn("{{ url }}", content)
