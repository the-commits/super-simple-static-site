import os
from pathlib import Path

import yaml

from ssss.common.application import application_default_config_data, application_version
from ssss.common.application.variables import (
    application_default_template_path,
    application_default_template_file,
    application_default_base_html,
    application_default_source,
    application_default_output,
    application_default_data,
    application_default_encoding,
    application_default_followlinks,
    application_default_filters,
    application_default_site,
    application_default_base_html_content,
    application_default_base_html_no_seo_content,
    application_default_template_file_content,
    application_default_index_md_content,
    application_default_sitemap_content,
    application_default_rss_content,
    application_default_llms_txt_content,
)
from ssss.common.fs import find_config
from ssss.common.fs.directory import (
    get_full_path,
    create_directory_if_not_exists,
    have_write_permission,
)
from ssss.common.io import confirm_overwrite
from ssss.common.md import variables, render
from ssss.configuration.arguments import Arguments
from ssss.configuration.default import config_file_path


class Application(Arguments):
    def __init__(self):
        self.config = {}
        self.__init_config = None
        self.__scaffold = None
        self.__no_seo = False
        self.__no_llm = False
        self.__no_feed = False
        self.__no_sitemap = False

        super().__init__()

        self.data = application_default_config_data()

        if self.__init_config:
            self.init_config()

        if self.__config is None:
            self.__config = find_config()

        self.load_config()

    def handle_args(self):
        self.parse.add_argument("-c", "--config", help="Path to configuration file")
        self.parse.add_argument(
            "--init",
            action="store_true",
            help="Create configuration file and site directory structure",
            default=False,
        )
        self.parse.add_argument(
            "--scaffold",
            action="store_true",
            help="Run --init and write starter template and content files",
            default=False,
        )
        self.parse.add_argument(
            "-v",
            "--version",
            action="version",
            version=application_version(),
        )
        self.parse.add_argument(
            "--no-seo",
            action="store_true",
            help="Omit SEO meta tags (og:*, twitter:*, canonical) from scaffold",
            default=False,
        )
        self.parse.add_argument(
            "--no-llm",
            action="store_true",
            help="Omit llms.txt from scaffold and build",
            default=False,
        )
        self.parse.add_argument(
            "--no-feed",
            action="store_true",
            help="Omit RSS feed from scaffold and build",
            default=False,
        )
        self.parse.add_argument(
            "--no-sitemap",
            action="store_true",
            help="Omit sitemap.xml from scaffold and build",
            default=False,
        )
        args = self.parse.parse_args()

        if args.config is not None:
            if os.path.exists(args.config) and os.path.isfile(args.config):
                self.__config = os.path.abspath(args.config)
            else:
                self.__config = os.path.join(os.getcwd(), args.config)

        else:
            self.__config = None

        self.__init_config = args.init or args.scaffold
        self.__scaffold = args.scaffold
        self.__no_seo = args.no_seo
        self.__no_llm = args.no_llm
        self.__no_feed = args.no_feed
        self.__no_sitemap = args.no_sitemap

    def load_config(self):
        with open(self.__config, "r") as file:
            yaml_data = yaml.safe_load(file)

        if yaml_data is not None:
            site_data = self.data.get("site", {}) | yaml_data.get("site", {})
            site_filters = self.data.get("filters", {}) | yaml_data.get("filters", {})
            self.data = self.data | yaml_data
            self.data["site"] = site_data
            self.data["filters"] = site_filters

            self.set_config()
            self.create_structure()

            if self.__scaffold:
                self.create_scaffold()

        else:
            raise NotImplementedError

    def set_config(self):
        self.data = {k: v for k, v in self.data.items() if v}
        self.config["searchpath"] = get_full_path(
            self.data.get("source", application_default_source())
        )
        self.config["outpath"] = get_full_path(
            self.data.get("output", application_default_output())
        )
        self.config["contexts"] = [
            (self.data.get("data", application_default_data()), variables)
        ]
        self.config["rules"] = [
            (self.data.get("data", application_default_data()), render.run)
        ]
        self.config["encoding"] = str(
            self.data.get("encoding", application_default_encoding())
        )
        self.config["followlinks"] = str(
            self.data.get("followlinks", application_default_followlinks())
        )
        self.config["filters"] = dict(
            self.data.get("filters", application_default_filters())
        )
        self.config["env_globals"] = dict(
            self.data.get("site", application_default_site())
        )

    def init_config(self):

        if self.__config is None:
            config_path = config_file_path()
        else:
            config_path = Path(self.__config)

        self.__config = config_path.absolute()

        if have_write_permission(config_path.parent):
            if not config_path.exists() or confirm_overwrite(str(config_path)):
                with open(config_path, "w") as file:
                    yaml.dump(application_default_config_data(), file)
        else:
            raise PermissionError

    def __getitem__(self, item):
        return self.config[item]

    def create_structure(self):
        create_directory_if_not_exists(self.config["outpath"])
        create_directory_if_not_exists(self.config["searchpath"])

        create_directory_if_not_exists(
            os.path.join(self.config["searchpath"], application_default_template_path())
        )

    def create_scaffold(self):
        base_html_content = (
            application_default_base_html_no_seo_content()
            if self.__no_seo
            else application_default_base_html_content()
        )

        files = [
            (
                os.path.join(
                    self.config["searchpath"], application_default_base_html()
                ),
                base_html_content,
            ),
            (
                os.path.join(
                    self.config["searchpath"], application_default_template_file()
                ),
                application_default_template_file_content(),
            ),
            (
                os.path.join(self.config["searchpath"], "index.md"),
                application_default_index_md_content(),
            ),
        ]

        if not self.__no_sitemap:
            files.append(
                (
                    os.path.join(
                        self.config["searchpath"],
                        application_default_template_path() + "sitemap.xml.j2",
                    ),
                    application_default_sitemap_content(),
                )
            )

        if not self.__no_feed:
            files.append(
                (
                    os.path.join(
                        self.config["searchpath"],
                        application_default_template_path() + "rss.xml.j2",
                    ),
                    application_default_rss_content(),
                )
            )

        if not self.__no_llm:
            files.append(
                (
                    os.path.join(
                        self.config["searchpath"],
                        application_default_template_path() + "llms.txt.j2",
                    ),
                    application_default_llms_txt_content(),
                )
            )

        for path, content in files:
            if not os.path.exists(path) or confirm_overwrite(path):
                with open(path, "w") as file:
                    file.write(content)
