import os
import unittest

from ssss.common.fs.directory import get_full_path, get_current_directory
from ssss.common.fs.file import write_if_not_exists


class Fullpath(unittest.TestCase):
    def test_empty_full_path(self):
        path = get_full_path("")
        self.assertEqual(get_current_directory(), path)

    def test_dot_full_path(self):
        path = get_full_path(".")
        self.assertEqual(get_current_directory(), path)


class WriteIfNotExists(unittest.TestCase):
    def test_creates_file_with_content(self):
        path = "/tmp/test_write_if_not_exists.txt"
        if os.path.exists(path):
            os.unlink(path)
        write_if_not_exists(path, "hello")
        with open(path, "r") as f:
            self.assertEqual(f.read(), "hello")
        os.unlink(path)

    def test_does_not_overwrite_existing_file(self):
        path = "/tmp/test_write_if_not_exists_existing.txt"
        with open(path, "w") as f:
            f.write("original")
        write_if_not_exists(path, "new content")
        with open(path, "r") as f:
            self.assertEqual(f.read(), "original")
        os.unlink(path)


if __name__ == "__main__":
    unittest.main()
