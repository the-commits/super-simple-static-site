# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2023-2026 Magnus Åberg (The Commits) <himself@magnusaberg.me>

import unittest

from ssss.configuration.arguments import Arguments


class HandleArgs(unittest.TestCase):
    def test_handle_args_raises_not_implemented(self):
        class Bare(Arguments):
            pass

        with self.assertRaises(NotImplementedError):
            Bare()
