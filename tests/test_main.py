"""Tests for the hello module."""
import unittest
from io import StringIO
from unittest import mock

from yaml import Loader, load

from main import main, mask_parts, mask_toc


class TestMain(unittest.TestCase):
    """Test main function from the main module."""

    def test_main(self):
        # Redirect stdout
        with mock.patch("sys.stdout", new=StringIO()) as mock_out:
            main()

        actual = mock_out.getvalue().strip().split("\n")
        expected = [""]
        self.assertListEqual(expected, actual)


class TestMask(unittest.TestCase):
    """Test the mask function from the main module."""

    maxDiff = None

    def test_mask_single_profile(self):
        whitelist = ["intro", "setup", "version_control/git"]

        with open("tests/test_files/test_one/_toc.yml", "r") as f:
            toc = load(f, Loader=Loader)

        with open("tests/test_files/test_one/dsg_toc.yml", "r") as f:
            expected = load(f, Loader=Loader)

        actual = mask_toc(toc, whitelist)

        self.assertDictEqual(expected, actual)

    def test_mask_toc(self):
        with mock.patch("main.mask_parts") as mock_parts:
            mock_parts.return_value = 5.5

            toc = {
                "format": "jb-book",
                "root": "intro",
                "parts": [1, 2, 3],
            }
            whitelist = [
                "a filename",
            ]

            expected = {
                "format": "jb-book",
                "root": "intro",
                "parts": 5.5,
            }
            actual = mask_toc(toc, whitelist)

            self.assertDictEqual(expected, actual)
            mock_parts.assert_called_once_with([1, 2, 3], whitelist)

    def test_chapters(self):
        parts = [{"chapters": [{"file": "file1"}, {"file": "file2"}]}]
        whitelist = [
            "file1",
        ]

        expected = [{"chapters": [{"file": "file1"}]}]
        actual = mask_parts(parts, whitelist)
        self.assertListEqual(expected, actual)

    def test_sections(self):
        parts = [
            {
                "chapters": [
                    {"file": "file1", "sections": [{"file": "file2"}]},
                    {"file": "file3", "sections": [{"file": "file4"}]},
                ]
            },
            {"chapters": [{"file": "file5"}]},
        ]
        whitelist = [
            "file1",
            "file2",
        ]

        expected = [
            {
                "chapters": [
                    {"file": "file1", "sections": [{"file": "file2"}]},
                ]
            }
        ]
        actual = mask_parts(parts, whitelist)
        self.assertListEqual(expected, actual)

    def test_sub_sections(self):
        parts = [
            {
                "chapters": [
                    {
                        "file": "file1",
                        "sections": [
                            {
                                "file": "file2",
                                "sections": [{"file": "file3"}, {"file": "file4"}],
                            }
                        ],
                    },
                ]
            },
        ]
        whitelist = [
            "file1",
            "file2",
            "file4",
        ]

        expected = [
            {
                "chapters": [
                    {
                        "file": "file1",
                        "sections": [
                            {"file": "file2", "sections": [{"file": "file4"}]}
                        ],
                    },
                ]
            }
        ]
        actual = mask_parts(parts, whitelist)
        self.assertListEqual(expected, actual)

    def test_preserves_title(self):
        parts = [
            {
                "chapters": [
                    {
                        "file": "file1",
                        "title": "title1",
                        "sections": [
                            {
                                "file": "file2",
                                "title": "title2",
                                "sections": [
                                    {"title": "title3", "file": "file3"},
                                    {"title": "title4", "file": "file4"},
                                ],
                            }
                        ],
                    },
                ]
            },
        ]
        whitelist = [
            "file1",
            "file2",
            "file3",
        ]

        expected = [
            {
                "chapters": [
                    {
                        "file": "file1",
                        "title": "title1",
                        "sections": [
                            {
                                "title": "title2",
                                "file": "file2",
                                "sections": [{"title": "title3", "file": "file3"}],
                            }
                        ],
                    },
                ]
            }
        ]
        actual = mask_parts(parts, whitelist)
        self.assertListEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
