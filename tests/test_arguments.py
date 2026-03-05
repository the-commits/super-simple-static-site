import unittest

from ssss.configuration.arguments import Arguments


class HandleArgs(unittest.TestCase):
    def test_handle_args_raises_not_implemented(self):
        class Bare(Arguments):
            pass

        with self.assertRaises(NotImplementedError):
            Bare()
