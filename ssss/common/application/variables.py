import importlib.metadata


def application_name() -> str:
    return "ssss"


def application_description() -> str:
    return importlib.metadata.metadata(application_name())["description"]


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


def application_default_template_file() -> str:
    return application_default_template_path() \
        + application_default_template_name() \
        + application_default_template_extension()


def application_default_base_html() -> str:
    return application_default_template_path() + "base.html"


def application_default_config_data() -> dict:
    return {
        "source": application_default_source(),
        "output": application_default_output(),
        "data": application_default_data(),
        "encoding": application_default_encoding(),
        "followlinks": application_default_followlinks(),
        "filters": application_default_filters(),
        "globals": {
            "site_name": "Site Name",
            "site_description": "Site Description",
            "site_author": "Site Author",
            "site_url": "https://example.com",
            "site_email": "asssa@example.com",
        },
    }
