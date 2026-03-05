import importlib.metadata
from pathlib import Path


def scaffold_directory() -> Path:
    return Path(__file__).parent.parent.parent / "scaffold"


def read_scaffold_file(filename) -> str:
    return (scaffold_directory() / filename).read_text()


def application_name() -> str:
    return "ssss"


def application_description() -> str:
    return application_name() + " - Super Simple Static Site"


def application_version() -> str:
    return application_name() + " " + importlib.metadata.version(application_name())


def application_default_template_path() -> str:
    return "_templates/"


def application_default_template_name() -> str:
    return "default"


def application_default_template_extension() -> str:
    return ".j2"


def application_default_output_extension() -> str:
    return ".html"


def application_default_encoding() -> str:
    return "utf8"


def application_default_data() -> str:
    return r".*\.md"


def application_default_output() -> str:
    return "site/build"


def application_default_source() -> str:
    return "site/source"


def application_default_followlinks() -> bool:
    return True


def application_default_filters() -> dict:
    return {}


def application_default_site() -> dict:
    return {
        "title": "Site Name",
        "description": "Site Description",
        "author": "Site Author",
        "url": "https://example.com",
        "email": "asssa@example.com",
    }


def application_default_template_file() -> str:
    return (
        application_default_template_path()
        + application_default_template_name()
        + application_default_template_extension()
    )


def application_default_base_html() -> str:
    return application_default_template_path() + "base.html"


def application_default_config_data() -> dict:
    return {
        "site": application_default_site(),
    }


def application_default_base_html_content() -> str:
    return read_scaffold_file("base.html")


def application_default_base_html_no_seo_content() -> str:
    content = read_scaffold_file("base.html")
    return strip_seo_blocks(content)


def strip_seo_blocks(content) -> str:
    import re

    pattern = r"    <!-- (?:Canonical|Open Graph|Twitter Card|LLM / AI crawler) -->.*?(?=\n    <!--|\n    <link rel=\"stylesheet\"|\Z)"
    return re.sub(pattern, "", content, flags=re.DOTALL)


def application_default_template_file_content() -> str:
    return read_scaffold_file("default.j2")


def application_default_index_md_content() -> str:
    return read_scaffold_file("index.md")


def application_default_sitemap_content() -> str:
    return read_scaffold_file("sitemap.xml.j2")


def application_default_rss_content() -> str:
    return read_scaffold_file("rss.xml.j2")


def application_default_llms_txt_content() -> str:
    return read_scaffold_file("llms.txt.j2")
