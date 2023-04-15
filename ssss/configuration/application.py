import os
from pathlib import Path

import yaml

from ssss.common.application import application_default_config_data
from ssss.common.fs import find_config
from ssss.configuration.arguments import Arguments
from ssss.configuration.default import config_file_path


class Application(Arguments):

    def __init__(self):
        self.__init_config = None

        super().__init__()

        self.data = application_default_config_data()

        if self.__init_config:
            self.init_config()

        if self.__config is None:
            self.__config = find_config()

        self.load_config()

    def handle_args(self):
        self.parse.add_argument(
            "-c",
            "--config",
            help="Path to configuration file"
        )
        self.parse.add_argument(
            "--init",
            action="store_true",
            help="Initialize configuration file",
            default=False
        )
        args = self.parse.parse_args()

        if args.config is not None:
            if os.path.exists(args.config) and os.path.isfile(args.config):
                self.__config = os.path.abspath(args.config)
            else:
                self.__config = os.path.join(os.getcwd(), args.config)

        else:
            self.__config = None

        self.__init_config = args.init

    def load_config(self):
        with open(self.__config, "r") as file:
            yaml_data = yaml.safe_load(file)

        if yaml_data is not None:
            self.data = self.data | yaml_data

    def init_config(self):

        if self.__config is None:
            config_path = config_file_path()
        else:
            config_path = Path(self.__config)

        self.__config = config_path.absolute()

        if not config_path.exists():
            with open(config_path, "w") as file:
                yaml.dump(application_default_config_data(), file)
