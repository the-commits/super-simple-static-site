# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2023-2026 Magnus Åberg (The Commits) <himself@magnusaberg.me>

import re
from datetime import date, datetime
from email.utils import parsedate_to_datetime
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


def parse_date(value) -> date | None:
    """Parse a frontmatter date for sorting; return None if it isn't a date.

    Accepts ISO dates with or without zero padding (``2026-7-1``, optionally
    followed by a time), RFC 2822 dates (``Wed, 29 Jul 2026 10:00:00 +0200``)
    and English month-name dates (``July 29, 2026``, ``29 Jul 2026``). A
    multi-line value uses its first line.
    """
    if isinstance(value, list):
        value = value[0] if value else None
    if not value:
        return None
    value = str(value).strip()

    iso = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})(?!\d)", value)
    if iso:
        return _make_date(int(iso.group(1)), int(iso.group(2)), int(iso.group(3)))
    return _parse_text_date(value)


def _make_date(year, month, day) -> date | None:
    try:
        return date(year, month, day)
    except ValueError:
        return None


def _parse_text_date(value) -> date | None:
    try:
        return parsedate_to_datetime(value).date()
    except (TypeError, ValueError):
        pass

    for date_format in ("%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%d %b %Y"):
        try:
            return datetime.strptime(value, date_format).date()
        except ValueError:
            pass
    return None


def posts(searchpath, directory) -> list[dict]:
    """List the Markdown pages in ``directory`` with their frontmatter.

    ``index.md`` and files staticjinja skips (prefixed with ``_`` or ``.``)
    are left out. Pages are sorted newest first by ``date`` (see
    ``parse_date``); pages without a date, or with one that can't be parsed,
    come last.
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
    # Sorting is stable, so pre-sorting by url gives posts with the same date
    # the same order on every filesystem.
    result.sort(key=lambda p: p["url"])

    dated = sorted((p for p in result if parse_date(p.get("date"))), key=lambda p: parse_date(p["date"]), reverse=True)
    undated = sorted((p for p in result if not parse_date(p.get("date"))), key=lambda p: p["url"])
    return dated + undated


def _searchpath(template) -> Path:
    """Return the source directory, derived from the template's name relative to it."""
    filename = Path(template.filename)
    name = getattr(template, "name", None)
    if not name:
        raise ValueError("Cannot find the source directory of " + str(filename) + ": template has no name")
    return filename.parents[len(Path(name).parts) - 1]


def variables(template):
    raw_content = Path(template.filename).read_text(encoding="utf-8")
    returned_variables = read_meta(template.filename)

    env = Environment()
    env.globals["posts"] = lambda directory: posts(_searchpath(template), directory)
    jinja_template = env.from_string(raw_content)
    # Passed after the frontmatter so a "posts" key can't hide the helper.
    rendered_markdown = jinja_template.render(returned_variables, posts=env.globals["posts"])

    md = markdown.Markdown(extensions=["meta", "fenced_code", "tables", "sane_lists"])
    returned_variables["content"] = md.convert(rendered_markdown)

    return returned_variables
