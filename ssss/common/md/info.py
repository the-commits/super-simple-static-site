# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2023-2026 Magnus Åberg (The Commits) <himself@magnusaberg.me>

from pathlib import Path

import markdown
from jinja2 import Environment

from ssss.common.application.variables import application_default_output_extension


def read_meta(path) -> dict:
    """Return the frontmatter of a Markdown file, with single values unwrapped."""
    meta_md = markdown.Markdown(extensions=["meta"])
    meta_md.convert(Path(path).read_text(encoding="utf-8"))

    meta = dict(meta_md.Meta)
    for key, value in meta.items():
        if isinstance(value, list) and len(value) == 1:
            meta[key] = value[0]
    return meta


def posts(searchpath, directory) -> list[dict]:
    """List the Markdown pages in ``directory`` with their frontmatter.

    ``index.md`` and files staticjinja skips (prefixed with ``_`` or ``.``)
    are left out. Pages are sorted newest first by ``date``; pages without a
    date come last.
    """
    searchpath = Path(searchpath)
    result = []
    for md_file in (searchpath / directory).glob("*.md"):
        if md_file.name == "index.md" or md_file.name[0] in "_.":
            continue
        meta = read_meta(md_file)
        rel_path = md_file.relative_to(searchpath)
        meta.setdefault("title", md_file.stem.replace("-", " ").title())
        meta["url"] = "/" + rel_path.with_suffix(application_default_output_extension()).as_posix()
        meta["page_url"] = "/" + rel_path.with_suffix("").as_posix()
        result.append(meta)

    dated = sorted((p for p in result if p.get("date")), key=lambda p: str(p["date"]), reverse=True)
    undated = sorted((p for p in result if not p.get("date")), key=lambda p: p["url"])
    return dated + undated


def _searchpath(template) -> Path:
    filename = Path(template.filename)
    name = getattr(template, "name", None)
    if name:
        return filename.parents[len(Path(name).parts) - 1]
    return filename.parent


def variables(template):
    raw_content = Path(template.filename).read_text(encoding="utf-8")
    returned_variables = read_meta(template.filename)

    searchpath = _searchpath(template)

    env = Environment()
    env.globals["posts"] = lambda directory: posts(searchpath, directory)
    jinja_template = env.from_string(raw_content)
    rendered_markdown = jinja_template.render(**returned_variables)

    md = markdown.Markdown(extensions=["meta", "fenced_code", "tables", "sane_lists"])
    returned_variables["content"] = md.convert(rendered_markdown)

    return returned_variables
