import importlib.metadata


def application_name() -> str:
    return "ssss"


def application_description() -> str:
    long_description = importlib.metadata.metadata(application_name())["description"]
    short_description = long_description.split(".")[1]
    return (
        application_name()
        + " - "
        + "".join([c for c in short_description if c.isalnum() or c.isspace()])
    )


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
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2.1.1/css/pico.min.css">\n'
        "  <title>{{ title }}</title>\n"
        '  <meta name="description" content="{{ description }}">\n'
        "</head>\n"
        "<body>\n"
        '  <main class="container">\n'
        "    {% block content %}{% endblock %}\n"
        "  </main>\n"
        "</body>\n"
        "</html>\n"
    )


def application_default_template_file_content() -> str:
    return (
        '{% extends "_templates/base.html" %}\n'
        "{% block content %}\n"
        "{{ content }}\n"
        "{% endblock %}\n"
    )


def application_default_index_md_content() -> str:
    return (
        "# Welcome\n\n"
        "This is your new **ssss** site.\n\n"
        "Edit `site/source/index.md` to get started.\n"
    )
