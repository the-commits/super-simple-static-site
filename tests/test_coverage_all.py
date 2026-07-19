# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2023-2026 Magnus Åberg (The Commits) <himself@magnusaberg.me>

import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch, MagicMock

import ssss
import ssss.__main__
from ssss.common.application import variables
from ssss.common.fs import directory, file
from ssss.common.io import prompt
from ssss.common.md import render
from ssss.configuration.application import Application
from ssss.generate import site


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("/tmp/ssss_coverage_test")
        directory.make_empty(str(self.test_dir), remove=True)
        os.makedirs(self.test_dir, exist_ok=True)
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.old_cwd)
        directory.make_empty(str(self.test_dir), remove=True)

    def test_variables_defaults(self):
        self.assertEqual(variables.application_default_template_path(), "_templates/")
        self.assertEqual(variables.application_default_template_name(), "default")
        self.assertEqual(variables.application_default_template_extension(), ".j2")
        self.assertEqual(variables.application_default_output_extension(), ".html")
        self.assertEqual(variables.application_default_encoding(), "utf8")
        self.assertEqual(variables.application_default_data(), r".*\.md")
        self.assertEqual(variables.application_default_output(), "site/build")
        self.assertEqual(variables.application_default_source(), "site/source")
        self.assertTrue(variables.application_default_followlinks())
        self.assertEqual(variables.application_default_filters(), {})
        self.assertEqual(variables.application_default_base_html(), "_templates/base.html")
        self.assertIn("site", variables.application_default_config_data())
        self.assertIn("<?xml", variables.application_default_sitemap_content())
        self.assertIn("<rss", variables.application_default_rss_content())
        self.assertIn("# {{ title }}", variables.application_default_llms_txt_content())
        self.assertIn("<!doctype html>", variables.application_default_base_html_content())

        stripped = variables.strip_seo_blocks(variables.application_default_base_html_content())
        self.assertNotIn('property="og:title"', stripped)

    def test_directory_and_file_helpers(self):
        self.assertTrue(directory.have_write_permission(str(self.test_dir)))
        self.assertTrue(directory.get_user_home_directory())
        self.assertTrue(directory.get_user_config_directory())
        self.assertEqual(directory.get_current_directory(), os.getcwd())
        self.assertEqual(directory.get_full_path("."), os.getcwd())
        self.assertEqual(directory.get_full_path(""), os.getcwd())
        self.assertEqual(directory.get_full_path(None), os.getcwd())

        sub_dir = self.test_dir / "sub"
        directory.create_directory_if_not_exists(str(sub_dir))
        self.assertTrue(sub_dir.exists())

        test_file = self.test_dir / "test.txt"
        file.touch_if_not_exists(str(test_file))
        self.assertTrue(test_file.exists())
        file.touch_if_not_exists(str(test_file))

        file.write_if_not_exists(str(self.test_dir / "new.txt"), "hello")
        file.write_if_not_exists(str(self.test_dir / "new.txt"), "ignored")

        self.assertIn(".yml", file.application_config_file_extension())
        self.assertIsNone(file.search_config_in_dir(str(self.test_dir)))

        (self.test_dir / "ssss.yml").write_text("site:\n  title: Test\n")
        self.assertIsNotNone(file.search_config_in_dir(str(self.test_dir)))
        self.assertIsNotNone(file.find_config())

        os.remove(self.test_dir / "ssss.yml")
        with self.assertRaises(FileNotFoundError):
            file.find_config()

    def test_prompt_confirm_overwrite(self):
        with patch("builtins.input", return_value="y"):
            self.assertTrue(prompt.confirm_overwrite("foo"))
        with patch("builtins.input", return_value="n"):
            self.assertFalse(prompt.confirm_overwrite("foo"))
        with patch("builtins.input", side_effect=EOFError):
            self.assertFalse(prompt.confirm_overwrite("foo"))

    def test_render_run_and_find_template(self):
        source_dir = self.test_dir / "site" / "source"
        templates_dir = source_dir / "_templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "default.j2").write_text("Default: {{ content }}")
        (templates_dir / "__index.j2").write_text("Index: {{ content }}")

        mock_site = SimpleNamespace(
            searchpath=str(source_dir),
            outpath=self.test_dir / "site" / "build",
            encoding="utf-8",
            get_template=lambda t: SimpleNamespace(
                stream=lambda **kw: SimpleNamespace(
                    dump=lambda path, encoding: Path(path).write_text("Rendered", encoding=encoding)
                )
            ),
        )

        mock_data = SimpleNamespace(name="index.md")
        tmpl = render.find_template(mock_site, mock_data)
        self.assertEqual(tmpl, "_templates/__index.j2")

        render.run(mock_site, mock_data, content="Hello")
        self.assertTrue((self.test_dir / "site" / "build" / "index.html").exists())

    def test_application_and_site_build(self):
        sys_argv_orig = sys.argv
        sys.argv = ["ssss", "--scaffold"]
        try:
            with patch("ssss.configuration.application.confirm_overwrite", return_value=True), patch("ssss.common.io.prompt.confirm_overwrite", return_value=True):
                app = Application()
                app.load_config()
                self.assertEqual(app["encoding"], "utf8")

                site.build(app)
                self.assertTrue((self.test_dir / "site" / "build" / "sitemap.xml").exists())
                self.assertTrue((self.test_dir / "site" / "build" / "rss.xml").exists())
                self.assertTrue((self.test_dir / "site" / "build" / "feed.xml").exists())
                self.assertTrue((self.test_dir / "site" / "build" / "llms.txt").exists())
                self.assertTrue((self.test_dir / "site" / "build" / "robots.txt").exists())
        finally:
            sys.argv = sys_argv_orig

    def test_main_module_execution(self):
        with patch("ssss.main") as mock_main:
            with patch.object(sys, "argv", ["ssss"]):
                import runpy
                runpy.run_module("ssss.__main__", run_name="__main__")
                self.assertTrue(mock_main.called)

    def test_variables_strip_seo_blocks(self):
        content = variables.application_default_base_html_no_seo_content()
        self.assertNotIn('property="og:title"', content)

    def test_site_generate_special_files_md_exception_handling(self):
        outpath = self.test_dir / "site" / "build"
        searchpath = self.test_dir / "site" / "source"
        outpath.mkdir(parents=True, exist_ok=True)
        searchpath.mkdir(parents=True, exist_ok=True)

        (outpath / "bad.html").write_text("<h1>Bad</h1>")
        (searchpath / "bad.md").write_text("dummy md")

        app = SimpleNamespace(
            config={
                "outpath": str(outpath),
                "searchpath": str(searchpath),
                "env_globals": {},
            }
        )
        with patch("markdown.Markdown", side_effect=Exception("md error")):
            site.generate_special_files(app)
        self.assertTrue((outpath / "sitemap.xml").exists())

    def test_application_data_setter_and_custom_init(self):
        sys_argv_orig = sys.argv
        try:
            # Test line 108: existing config path
            existing_config = self.test_dir / "test_existing.yml"
            existing_config.write_text("site:\n  title: Existing\n")
            sys.argv = ["ssss", "-c", str(existing_config)]
            app_exist = Application()
            self.assertEqual(app_exist.data["site"]["title"], "Existing")

            # Test line 56: find_config() when config is None
            (self.test_dir / "ssss.yml").write_text("site:\n  title: Found\n")
            sys.argv = ["ssss"]
            app_found = Application()
            self.assertEqual(app_found.data["site"]["title"], "Found")

            # Test line 187: PermissionError branch in init_config
            with patch("ssss.configuration.application.have_write_permission", return_value=False):
                with self.assertRaises(PermissionError):
                    app_exist.init_config()

            # Test line 140 NotImplementedError branch in load_config
            sys.argv = ["ssss", "--scaffold", "-c", "test_custom.yml"]
            with patch("ssss.configuration.application.confirm_overwrite", return_value=True):
                app = Application()
                with patch("yaml.safe_load", return_value=None):
                    with self.assertRaises(NotImplementedError):
                        app.load_config()
        finally:
            sys.argv = sys_argv_orig

    def test_render_find_template_missing(self):
        mock_site = SimpleNamespace(
            searchpath=str(self.test_dir),
            outpath=self.test_dir,
            encoding="utf-8"
        )
        mock_data = SimpleNamespace(name="nonexistent.md")
        tmpl = render.find_template(mock_site, mock_data)
        self.assertEqual(tmpl, "_templates/default.j2")

    def test_site_get_template_content_custom(self):
        searchpath = self.test_dir / "site" / "source"
        searchpath.mkdir(parents=True, exist_ok=True)
        (searchpath / "custom.j2").write_text("Custom Content")
        res = site._get_template_content(searchpath, "custom.j2", "Default")
        self.assertEqual(res, "Custom Content")

        tmpl_dir = searchpath / "_templates"
        tmpl_dir.mkdir(exist_ok=True)
        (tmpl_dir / "tmpl.j2").write_text("Tmpl Content")
        res2 = site._get_template_content(searchpath, "tmpl.j2", "Default")
        self.assertEqual(res2, "Tmpl Content")

    def test_main_success_and_error_branches(self):
        with patch.object(Application, "__init__", side_effect=FileNotFoundError):
            with patch("builtins.print") as mock_print, self.assertRaises(SystemExit):
                ssss.main()
            mock_print.assert_called_with("No configuration file found.")

        with patch.object(Application, "__init__", side_effect=NotImplementedError):
            with patch("builtins.print") as mock_print, self.assertRaises(SystemExit):
                ssss.main()
            mock_print.assert_called_with("Configuration file is empty.")

        with patch.object(Application, "__init__", side_effect=PermissionError):
            with patch("builtins.print") as mock_print, self.assertRaises(SystemExit):
                ssss.main()
            mock_print.assert_called_with("No write permission for configuration directory.")

        sys_argv_orig = sys.argv
        sys.argv = ["ssss", "--scaffold"]
        try:
            with patch("ssss.generate.site.build") as mock_build, patch("ssss.configuration.application.confirm_overwrite", return_value=True):
                ssss.main()
                self.assertTrue(mock_build.called)
        finally:
            sys.argv = sys_argv_orig

    def test_special_files_options(self):
        app = SimpleNamespace(
            config={
                "outpath": str(self.test_dir / "site" / "build"),
                "searchpath": str(self.test_dir / "site" / "source"),
                "env_globals": {"title": "Test", "description": "Desc", "author": "dev", "email": "d@l", "url": "http://l"},
                "no_sitemap": True,
                "no_feed": True,
                "no_llm": True,
            }
        )
        os.makedirs(self.test_dir / "site" / "build", exist_ok=True)
        os.makedirs(self.test_dir / "site" / "source", exist_ok=True)
        (self.test_dir / "site" / "build" / "index.html").write_text("<h1>Index</h1>")

        site.generate_special_files(app)
        self.assertFalse((self.test_dir / "site" / "build" / "sitemap.xml").exists())
        self.assertFalse((self.test_dir / "site" / "build" / "rss.xml").exists())
        self.assertFalse((self.test_dir / "site" / "build" / "llms.txt").exists())
        self.assertTrue((self.test_dir / "site" / "build" / "robots.txt").exists())

    def test_application_additional_branches(self):
        sys_argv_orig = sys.argv
        sys.argv = ["ssss", "--init"]
        try:
            with patch("ssss.configuration.application.confirm_overwrite", return_value=True):
                app = Application()
                app.init_config()
                self.assertTrue((self.test_dir / "ssss.yml").exists())
        finally:
            sys.argv = sys_argv_orig


if __name__ == "__main__":
    unittest.main()
