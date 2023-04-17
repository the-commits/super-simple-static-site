import unittest

from ssss.common.fs.directory import get_full_path, get_current_directory


class Fullpath(unittest.TestCase):
    def test_empty_full_path(self):
        path = get_full_path("")
        self.assertEqual(get_current_directory(), path)

    def test_dot_full_path(self):
        path = get_full_path(".")
        self.assertEqual(get_current_directory(), path)


if __name__ == '__main__':
    unittest.main()
