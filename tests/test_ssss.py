import os
import stat
import subprocess
from os import unlink

from ssss.common.application.variables import (
    application_default_base_html_content,
    application_default_template_file_content,
    application_default_index_md_content,
)
from ssss.common.fs import make_empty
from ssss.common.fs.file import touch_if_not_exists


def run_ssss(*args, stdin=None):
    result = subprocess.run(
        ["ssss"] + list(args), capture_output=True, text=True, input=stdin
    )
    return result.stdout, result.returncode


def test_ssss_no_args():
    output, returncode = run_ssss()
    assert returncode == 1
    assert "No configuration file found" in output


def test_ssss_version():
    output, returncode = run_ssss("--version")
    assert returncode == 0
    assert "ssss" in output


def test_ssss_short_version():
    output, returncode = run_ssss("-v")
    assert returncode == 0
    assert "ssss" in output


def test_ssss_no_args_after_init():
    output, returncode = run_ssss("--scaffold", "-c", "test.yml")
    assert returncode == 0
    assert (
        "Looking at: _templates/__index.j2, using default template: _templates/default.j2"
        in output
    )

    output, returncode = run_ssss("-c", "test.yml")
    assert returncode == 0
    assert (
        "Looking at: _templates/__index.j2, using default template: _templates/default.j2"
        in output
    )

    unlink("test.yml")
    make_empty("site", True)


def test_ssss_no_args_after_init_with_empty_config():
    touch_if_not_exists("test.yml")
    output, returncode = run_ssss("-c", "test.yml")

    assert returncode == 1
    assert "Configuration file is empty." in output

    unlink("test.yml")


def test_ssss_help_description():
    output, returncode = run_ssss("--help")
    assert returncode == 0
    assert "ssss - Super Simple Static Site" in output

    output, returncode = run_ssss("-h")
    assert returncode == 0
    assert "-h, --help" in output and "show this help message and exit" in output


def test_ssss_long_help():
    output, returncode = run_ssss("--help")
    assert returncode == 0
    assert "-h, --help" in output and "show this help message and exit" in output


def test_ssss_init():
    output, returncode = run_ssss("--init")
    assert returncode == 0

    with open("ssss.yml", "r") as f:
        actual_contents = f.read()

    with open("tests/data/ssss.yml", "r") as f:
        expected_contents = f.read()

    unlink("ssss.yml")
    make_empty("site", True)

    assert actual_contents == expected_contents


def test_ssss_init_only():
    output, returncode = run_ssss("--init")
    assert returncode == 0

    site_exists = os.path.exists("site")
    source_exists = os.path.exists("site/source")
    templates_exist = os.path.exists("site/source/_templates")
    build_exists = os.path.exists("site/build")
    base_not_written = not os.path.exists("site/source/_templates/base.html")
    template_not_written = not os.path.exists("site/source/_templates/default.j2")
    index_not_written = not os.path.exists("site/source/index.md")

    unlink("ssss.yml")
    make_empty("site", True)

    assert site_exists and source_exists and templates_exist and build_exists
    assert base_not_written and template_not_written and index_not_written


def test_ssss_init_with_config():
    output, returncode = run_ssss("--init", "--config", "custom_config.yaml")
    assert returncode == 0

    with open("custom_config.yaml", "r") as f:
        actual_contents = f.read()

    with open("tests/data/ssss.yml", "r") as f:
        expected_contents = f.read()

    unlink("custom_config.yaml")
    make_empty("site", True)

    assert actual_contents == expected_contents


def test_ssss_scaffold():
    output, returncode = run_ssss("--scaffold")
    assert returncode == 0

    site_exists = os.path.exists("site")
    source_exists = os.path.exists("site/source/index.md")
    template_exists = os.path.exists("site/source/_templates/default.j2")
    base_exists = os.path.exists("site/source/_templates/base.html")
    data_exists = os.path.exists("site/build/index.html")

    with open("site/source/index.md", "r") as f:
        index_md_content = f.read()
    with open("site/source/_templates/default.j2", "r") as f:
        template_content = f.read()
    with open("site/source/_templates/base.html", "r") as f:
        base_html_content = f.read()

    unlink("ssss.yml")
    make_empty("site", True)

    assert (
        site_exists
        and source_exists
        and template_exists
        and base_exists
        and data_exists
    )
    assert index_md_content == application_default_index_md_content()
    assert template_content == application_default_template_file_content()
    assert base_html_content == application_default_base_html_content()


def test_ssss_init_no_write_permission():
    locked_dir = "/tmp/ssss_locked_dir"
    os.makedirs(locked_dir, exist_ok=True)
    os.chmod(locked_dir, stat.S_IRUSR | stat.S_IXUSR)
    try:
        output, returncode = run_ssss("--init", "-c", locked_dir + "/ssss.yml")
        assert returncode == 1
        assert "No write permission" in output
    finally:
        os.chmod(locked_dir, stat.S_IRWXU)
        os.rmdir(locked_dir)


def test_ssss_init_twice_does_not_overwrite_config():
    run_ssss("--scaffold")

    with open("ssss.yml", "r") as f:
        original = f.read()

    output, returncode = run_ssss("--init")
    assert returncode == 0

    with open("ssss.yml", "r") as f:
        after = f.read()

    unlink("ssss.yml")
    make_empty("site", True)

    assert original == after


def test_ssss_scaffold_with_dedicated_template():
    run_ssss("--scaffold")

    with open("site/source/_templates/__index.j2", "w") as f:
        f.write(
            '{% extends "_templates/base.html" %}\n'
            "{% block content %}\n"
            "<article>{{ content }}</article>\n"
            "{% endblock %}\n"
        )

    output, returncode = run_ssss()
    assert returncode == 0
    assert os.path.exists("site/build/index.html")

    with open("site/build/index.html", "r") as f:
        html = f.read()

    unlink("ssss.yml")
    make_empty("site", True)

    assert "<article>" in html


def test_ssss_scaffold_with_subdirectory_content():
    run_ssss("--scaffold")

    os.makedirs("site/source/blog", exist_ok=True)
    with open("site/source/blog/post.md", "w") as f:
        f.write("# Post\n\nHello from blog.\n")

    output, returncode = run_ssss()
    assert returncode == 0
    assert os.path.exists("site/build/blog/post.html")

    unlink("ssss.yml")
    make_empty("site", True)


def test_ssss_scaffold_writes_sitemap_and_rss_and_llms():
    output, returncode = run_ssss("--scaffold", "-c", "test.yml")
    assert returncode == 0

    assert os.path.exists("site/source/_templates/sitemap.xml.j2")
    assert os.path.exists("site/source/_templates/rss.xml.j2")
    assert os.path.exists("site/source/_templates/llms.txt.j2")

    unlink("test.yml")
    make_empty("site", True)


def test_ssss_scaffold_no_sitemap_skips_sitemap():
    output, returncode = run_ssss("--scaffold", "--no-sitemap", "-c", "test.yml")
    assert returncode == 0
    assert not os.path.exists("site/source/_templates/sitemap.xml.j2")
    assert os.path.exists("site/source/_templates/rss.xml.j2")

    unlink("test.yml")
    make_empty("site", True)


def test_ssss_scaffold_no_feed_skips_rss():
    output, returncode = run_ssss("--scaffold", "--no-feed", "-c", "test.yml")
    assert returncode == 0
    assert not os.path.exists("site/source/_templates/rss.xml.j2")
    assert os.path.exists("site/source/_templates/sitemap.xml.j2")

    unlink("test.yml")
    make_empty("site", True)


def test_ssss_scaffold_no_llm_skips_llms_txt():
    output, returncode = run_ssss("--scaffold", "--no-llm", "-c", "test.yml")
    assert returncode == 0
    assert not os.path.exists("site/source/_templates/llms.txt.j2")
    assert os.path.exists("site/source/_templates/sitemap.xml.j2")

    unlink("test.yml")
    make_empty("site", True)


def test_ssss_scaffold_no_seo_base_html_omits_og():
    output, returncode = run_ssss("--scaffold", "--no-seo", "-c", "test.yml")
    assert returncode == 0

    with open("site/source/_templates/base.html", "r") as f:
        content = f.read()

    unlink("test.yml")
    make_empty("site", True)

    assert 'property="og:title"' not in content
    assert 'name="twitter:card"' not in content
    assert 'rel="canonical"' not in content


def test_ssss_scaffold_overwrite_yes_replaces_file():
    run_ssss("--scaffold", "-c", "test.yml")

    with open("site/source/_templates/base.html", "w") as f:
        f.write("replaced")

    num_prompts = 6
    output, returncode = run_ssss(
        "--scaffold", "-c", "test.yml", stdin="y\n" * num_prompts
    )
    assert returncode == 0

    with open("site/source/_templates/base.html", "r") as f:
        content = f.read()

    unlink("test.yml")
    make_empty("site", True)

    assert "replaced" not in content
    assert "<!doctype html>" in content
