import argparse

from ssss.common.application import application_name, application_description, application_version


class Arguments:
    def __init__(self):
        self.parse = argparse.ArgumentParser(
            prog=application_name(),
            description=application_description(),
            epilog=application_version(),
        )
        self.handle_args()

    def handle_args(self):
        raise NotImplementedError("Must be implemented by subclass.")
