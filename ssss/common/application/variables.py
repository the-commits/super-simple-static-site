import importlib.metadata


def application_name() -> str:
    return "ssss"


def application_description() -> str:
    return importlib.metadata.metadata(application_name())["description"]


def application_version() -> str:
    return application_name() + " " + importlib.metadata.version(application_name())


def application_template_path() -> str:
    return "_templates"


def application_default_config_data() -> dict:
    return {
        "source": "site/source",
        "output": "site/build",
        "data": r".*\.md",
        "encoding": "utf8",
        "followlinks": True,
        "filters": {},
        "globals": {},
    }
