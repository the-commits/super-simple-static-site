import re
from pathlib import Path
from jinja2 import Template
from staticjinja import Site

from ssss.common.application.variables import (
    application_default_sitemap_content,
    application_default_rss_content,
    application_default_llms_txt_content,
)
from ssss.common.fs.directory import make_empty


def build(config):
    bake(config)
    generate_special_files(config)


def bake(config=None, reload_on_change=False):
    make_empty(config["outpath"])
    cfg_dict = config.config if hasattr(config, "config") else config
    staticjinja_keys = {
        "searchpath",
        "outpath",
        "contexts",
        "rules",
        "encoding",
        "followlinks",
        "filters",
        "env_globals",
    }
    parameters = {k: v for k, v in cfg_dict.items() if k in staticjinja_keys}
    Site.make_site(**parameters).render(use_reloader=reload_on_change)


def generate_special_files(config):
    cfg_dict = config.config if hasattr(config, "config") else config

    outpath = Path(cfg_dict.get("outpath", "site/build"))
    searchpath = Path(cfg_dict.get("searchpath", "site/source"))
    site_globals = cfg_dict.get("env_globals", {})

    no_sitemap = cfg_dict.get("no_sitemap", False)
    no_feed = cfg_dict.get("no_feed", False)
    no_llm = cfg_dict.get("no_llm", False)

    pages = []
    for html_file in sorted(outpath.glob("**/*.html")):
        rel_path = html_file.relative_to(outpath)
        url_path = "/" + str(rel_path)
        content = html_file.read_text(encoding="utf-8")
        title_match = re.search(r"<h1>(.*?)</h1>", content)
        title = title_match.group(1) if title_match else rel_path.stem.replace("-", " ").title()
        pages.append({
            "url": url_path,
            "title": title,
            "description": site_globals.get("description", ""),
            "content": content
        })

    # Render sitemap.xml
    if not no_sitemap:
        sitemap_tmpl = _get_template_content(searchpath, "sitemap.xml.j2", application_default_sitemap_content())
        rendered = Template(sitemap_tmpl).render(pages=pages, site=site_globals, url=site_globals.get("url", ""))
        (outpath / "sitemap.xml").write_text(rendered, encoding="utf-8")

    # Render rss.xml and feed.xml
    if not no_feed:
        rss_tmpl = _get_template_content(searchpath, "rss.xml.j2", application_default_rss_content())
        rendered = Template(rss_tmpl).render(
            pages=pages,
            posts=pages,
            site=site_globals,
            title=site_globals.get("title", ""),
            description=site_globals.get("description", ""),
            url=site_globals.get("url", "")
        )
        (outpath / "rss.xml").write_text(rendered, encoding="utf-8")
        (outpath / "feed.xml").write_text(rendered, encoding="utf-8")

    # Render llms.txt
    if not no_llm:
        llms_tmpl = _get_template_content(searchpath, "llms.txt.j2", application_default_llms_txt_content())
        rendered = Template(llms_tmpl).render(
            pages=pages,
            site=site_globals,
            title=site_globals.get("title", ""),
            description=site_globals.get("description", ""),
            url=site_globals.get("url", ""),
            author=site_globals.get("author", ""),
            email=site_globals.get("email", "")
        )
        (outpath / "llms.txt").write_text(rendered, encoding="utf-8")

    # Render robots.txt
    robots_tmpl = "User-agent: *\nAllow: /\n\nSitemap: {{ url }}/sitemap.xml\n"
    rendered_robots = Template(robots_tmpl).render(site=site_globals, url=site_globals.get("url", ""))
    (outpath / "robots.txt").write_text(rendered_robots, encoding="utf-8")


def _get_template_content(searchpath, filename, default_content):
    custom = searchpath / filename
    if custom.exists():
        return custom.read_text(encoding="utf-8")
    tmpl_custom = searchpath / "_templates" / filename
    if tmpl_custom.exists():
        return tmpl_custom.read_text(encoding="utf-8")
    return default_content

