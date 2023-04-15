from staticjinja import Site

from ssss.common.fs.directory import make_empty


def build(config):
    bake(config)


def watch(config):
    bake(config, reload_on_change=True)


def bake(config=None, reload_on_change=False):
    make_empty(config["outpath"])
    parameters = vars(config)["config"]
    Site.make_site(**parameters).render(use_reloader=reload_on_change)
