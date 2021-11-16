"""Tests for the hello module."""
import unittest
from io import StringIO
from unittest import mock

from yaml import Loader, load

from main import main, mask_rec, mask_toc


class MyTestCase(unittest.TestCase):
    """Test functions from the main module."""

    def test_get_message(self):
        actual = main()
        self.assertIsNone(actual)

    def test_main(self):
        # Redirect stdout
        with mock.patch("sys.stdout", new=StringIO()) as mock_out:
            main()

        actual = mock_out.getvalue().strip().split("\n")
        expected = [""]
        self.assertListEqual(expected, actual)


class TestMask(unittest.TestCase):
    """Test the mask function from the main module."""

    def test_mask_empty(self):
        mask_toc({}, {})

    def test_mask_single_profile(self):
        profiles = {"dsg": ["intro", "setup", "version_control/git"]}

        with open("tests/test_files/test_one/_toc.yml", "r") as f:
            toc = load(f, Loader=Loader)["parts"]

        with open("tests/test_files/test_one/dsg_toc.yml", "r") as f:
            expected = load(f, Loader=Loader)["parts"]

        actual = mask_toc(toc, profiles)

        self.assertListEqual(expected, actual)

    def test_simple_case(self):
        toc = {
            "format": "jb-book",
            "root": "intro",
            "parts": [{"chapters": [{"file": "file1"}, {"file": "file2"}]}],
        }
        profiles = [
            "file1",
        ]

        expected = {
            "format": "jb-book",
            "root": "intro",
            "parts": [{"chapters": [{"file": "file1"}]}],
        }
        actual = mask_toc(toc, profiles)
        self.assertDictEqual(expected, actual)

    def test_mask_rec_depth_one(self):
        chapters = [{"file": "mypage1"}, {"file": "mypage2"}]
        whitelist = ["mypage1"]

        expected = [{"file": "mypage1"}]
        actual = mask_rec(chapters, whitelist)

        self.assertListEqual(expected, actual)

    def test_mask_rec_depth_two(self):
        chapters = [
            {"file": "mypage1", "sections": [{"file": "mypage3"}]},
            {"file": "mypage2"},
        ]
        whitelist = ["mypage1"]

        expected = [
            {"file": "mypage1"},
        ]
        actual = mask_rec(chapters, whitelist)

        self.assertListEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
