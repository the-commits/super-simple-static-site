from pathlib import Path
import os

from ssss.common.application.variables import application_default_output_extension, application_default_template_file, \
    application_default_template_path, application_default_template_extension
import os
from pathlib import Path

from ssss.common.application.variables import application_default_output_extension, application_default_template_file, \
    application_default_template_path, application_default_template_extension


def run(site, data, **kwargs):
    out = site.outpath / Path(data.name).with_suffix(application_default_output_extension())
    os.makedirs(out.parent, exist_ok=True)
    template = find_template(site, data)
    site.get_template(template).stream(**kwargs).dump(str(out), encoding=site.encoding)


def find_template(site, data):
    default_template = application_default_template_file()

    template_stem = str(Path(data.name).parent)

    if template_stem == ".":
        template_stem = "__" + str(data.name).split(".")[0]

    template = application_default_template_path() + template_stem + application_default_template_extension()
    template_path = os.path.join(site.searchpath, template)

    if not os.path.exists(template_path):
        print("No template found for " + str(data.name))
        print("Looking at: " + template + ", using default template: " + default_template)
        template = default_template

    return template
