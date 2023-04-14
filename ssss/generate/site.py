from staticjinja import Site

from ssss.common.fs.directory import get_full_path, make_empty
from ssss.common.md import variables, render


def build(config):
    bake(config)


def watch(config):
    bake(config, reload_on_change=True)


def bake(config=None, reload_on_change=False):
    source = get_full_path(config.data["source"])
    output = get_full_path(config.data["output"])
    contexts = config.data["contexts"]
    rules = config.data["rules"]

    make_empty(output)

    Site.make_site(
        searchpath=source,
        outpath=output,
        contexts=[(contexts, variables)],
        rules=[(rules, render.run)]
    ).render(use_reloader=reload_on_change)
