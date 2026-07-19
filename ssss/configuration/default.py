# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2023-2026 Magnus Åberg (The Commits) <himself@magnusaberg.me>

from pathlib import Path

from ssss.common.application import application_name
from ssss.common.fs import get_current_directory
from ssss.common.fs.file import application_config_file_extension


def config_file_path() -> Path:
    ext = application_config_file_extension()[0]
    file_name = application_name()
    return Path(get_current_directory(), file_name).with_suffix(ext)
