from pathlib import Path

import markdown


def variables(template):
    md = markdown.Markdown(extensions=["meta"])
    markdown_content = Path(template.filename).read_text()
    returned_variables = {"content": md.convert(markdown_content)} | md.Meta

    for key, value in returned_variables.items():
        if isinstance(value, list) and len(value) == 1:
            returned_variables[key] = value[0]

    returned_variables["content"] = handle_meta_variables(returned_variables, returned_variables["content"], md=md)

    return returned_variables


def handle_meta_variables(meta_vars, content, md=markdown.Markdown(extensions=["meta"])):
    from jinja2 import Environment

    env = Environment()
    template = env.from_string(content)
    return md.convert(template.render(**meta_vars))
