from ssss.configuration import application
from ssss.generate import site


def main():
    __ssss_config__ = None
    try:
        __ssss_config__ = application.Application()
    except FileNotFoundError:
        print("No configuration file found.")
        exit(1)
    except NotImplementedError:
        print("Configuration file is empty.")
        exit(1)

    site.build(__ssss_config__)
