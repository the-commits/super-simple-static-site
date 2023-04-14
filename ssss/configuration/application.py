import os

from ssss.configuration.arguments import Arguments


class Application(Arguments):

    def __init__(self):
        from ssss import common
        from ssss.common.application import application_default_config_data
        from ssss.common.fs import find_config

        super().__init__()
        self.data = application_default_config_data()
        self.__application_name = common.application.application_name()

        if self.__config is None:
            self.__config = find_config()

        self.load_config()

    def handle_args(self):
        self.parse.add_argument("-c", "--config", help="Path to configuration file")
        args = self.parse.parse_args()

        if args.config is not None:
            if os.path.exists(args.config) and os.path.isfile(args.config):
                self.__config = os.path.abspath(args.config)
            else:
                self.__config = os.path.join(os.getcwd(), args.config)

        else:
            self.__config = None

    def load_config(self):
        import yaml
        with open(self.__config, "r") as file:
            yaml_data = yaml.safe_load(file)

        if yaml_data is not None:
            self.data = self.data | yaml_data
