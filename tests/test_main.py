"""Tests for the hello module."""
import unittest
from io import StringIO
from unittest import mock

from yaml import Loader, load

from main import main, mask_dict


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
        mask_dict({}, {})

    def test_mask_single(self):
        profiles = {"dsg": ["intro", "setup", "version_control/git"]}

        with open("tests/test_files/test_one/_toc.yml", "r") as f:
            toc = load(f, Loader=Loader)["parts"]

        with open("tests/test_files/test_one/dsg_toc.yml", "r") as f:
            expected = load(f, Loader=Loader)["parts"]

        actual = mask_dict(toc, profiles)

        self.assertListEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
