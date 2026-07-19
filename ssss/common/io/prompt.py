# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2023-2026 Magnus Åberg (The Commits) <himself@magnusaberg.me>

def confirm_overwrite(path) -> bool:
    try:
        answer = input(path + " already exists. Overwrite? [y/N] ")
        return answer.strip().lower() == "y"
    except EOFError:
        return False
