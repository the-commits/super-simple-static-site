import re
from pathlib import Path
from jinja2 import Environment, Template, select_autoescape
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
    import markdown

    cfg_dict = config.config if hasattr(config, "config") else config

    outpath = Path(cfg_dict.get("outpath", "site/build"))
    searchpath = Path(cfg_dict.get("searchpath", "site/source"))
    site_globals = cfg_dict.get("env_globals", {})

    site_title = site_globals.get("title", "Site Name")
    site_desc = site_globals.get("description", "Site Description")
    site_url = site_globals.get("url", "http://localhost:8000")
    site_author = site_globals.get("author", "developer")
    site_email = site_globals.get("email", "developer@localhost")

    no_sitemap = cfg_dict.get("no_sitemap", False)
    no_feed = cfg_dict.get("no_feed", False)
    no_llm = cfg_dict.get("no_llm", False)

    pages = []
    for html_file in sorted(outpath.glob("**/*.html")):
        rel_path = html_file.relative_to(outpath)
        url_path = "/" + str(rel_path)
        content = html_file.read_text(encoding="utf-8")

        # Try to read matching markdown file metadata
        rel_md = rel_path.with_suffix(".md")
        md_path = searchpath / rel_md
        meta = {}
        if md_path.exists():
            try:
                raw_md = md_path.read_text(encoding="utf-8")
                md_meta = markdown.Markdown(extensions=["meta"])
                md_meta.convert(raw_md)
                meta = md_meta.Meta
            except Exception:
                pass

        changefreq = meta.get("changefreq", ["monthly"])[0] if "changefreq" in meta else "monthly"
        default_prio = "1.0" if url_path == "/index.html" else "0.5"
        priority = meta.get("priority", [default_prio])[0] if "priority" in meta else default_prio

        title = meta.get("title", [None])[0] if "title" in meta else None
        if not title:
            title_match = re.search(r"<h1>(.*?)</h1>", content)
            title = title_match.group(1) if title_match else rel_path.stem.replace("-", " ").title()

        description = meta.get("description", [site_desc])[0] if "description" in meta else site_desc

        pages.append({
            "url": url_path,
            "title": title,
            "description": description,
            "changefreq": changefreq,
            "priority": priority,
            "content": content
        })

    xml_env = Environment(autoescape=select_autoescape(["xml", "html"]))

    # Render sitemap.xml
    if not no_sitemap:
        sitemap_tmpl = _get_template_content(searchpath, "sitemap.xml.j2", application_default_sitemap_content())
        rendered = xml_env.from_string(sitemap_tmpl).render(
            pages=pages,
            site=site_globals,
            url=site_url
        )
        (outpath / "sitemap.xml").write_text(rendered, encoding="utf-8")

    # Render rss.xml and feed.xml
    if not no_feed:
        rss_tmpl = _get_template_content(searchpath, "rss.xml.j2", application_default_rss_content())
        rendered = xml_env.from_string(rss_tmpl).render(
            pages=pages,
            posts=pages,
            site=site_globals,
            title=site_title,
            description=site_desc,
            url=site_url
        )
        (outpath / "rss.xml").write_text(rendered, encoding="utf-8")
        (outpath / "feed.xml").write_text(rendered, encoding="utf-8")

    # Render llms.txt
    if not no_llm:
        llms_tmpl = _get_template_content(searchpath, "llms.txt.j2", application_default_llms_txt_content())
        rendered = Template(llms_tmpl).render(
            pages=pages,
            site=site_globals,
            title=site_title,
            description=site_desc,
            url=site_url,
            author=site_author,
            email=site_email
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

