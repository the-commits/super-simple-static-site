import os
from pathlib import Path

from ssss.common.application import application_name


def make_empty(dir_path, remove=False):
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        [x if x.is_dir() and make_empty(x, True) else x.is_file() and x.unlink() for x in Path(dir_path).iterdir()]
        if remove:
            os.rmdir(dir_path)


def have_write_permission(dir_path):
    return os.access(dir_path, os.X_OK | os.W_OK)


def get_user_home_directory():
    return os.path.expanduser("~")


def get_user_config_directory():
    return get_user_home_directory() + "/." + application_name()


def get_current_directory():
    return os.getcwd()


def get_full_path(path):
    if path is None or path == "" or path == ".":
        path = get_current_directory()
    return os.path.abspath(path)


def create_directory_if_not_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
