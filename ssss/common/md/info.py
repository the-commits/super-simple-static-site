# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2023-2026 Magnus Åberg (The Commits) <himself@magnusaberg.me>

from pathlib import Path

import markdown
from jinja2 import Environment


def variables(template):
    raw_content = Path(template.filename).read_text()
    meta_md = markdown.Markdown(extensions=["meta"])
    meta_md.convert(raw_content)

    returned_variables = dict(meta_md.Meta)
    for key, value in returned_variables.items():
        if isinstance(value, list) and len(value) == 1:
            returned_variables[key] = value[0]

    env = Environment()
    jinja_template = env.from_string(raw_content)
    rendered_markdown = jinja_template.render(**returned_variables)

    md = markdown.Markdown(extensions=["meta", "fenced_code", "tables", "sane_lists"])
    returned_variables["content"] = md.convert(rendered_markdown)

    return returned_variables

