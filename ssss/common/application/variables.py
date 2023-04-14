def application_name() -> str:
    return "ssss"


def application_description() -> str:
    return "ssss or super simple static site, a static site generator heavily dependent on staticjinja and markdown"


def application_version() -> str:
    return "0.0.0a0.post0.dev2"


def application_default_config_data() -> dict:
    return {
        "source": "src",
        "output": "site",
        "contexts": r".*\.md",
        "rules": r".*\.md",
    }
