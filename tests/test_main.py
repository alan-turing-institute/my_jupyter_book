"""Tests for the hello module."""
import unittest
from io import StringIO
from unittest import mock

import main


class MyTestCase(unittest.TestCase):
    """Test functions from the hello module."""

    def test_get_message(self):
        actual = main.main()
        self.assertIsNone(actual)

    def test_main(self):
        # Redirect stdout
        with mock.patch("sys.stdout", new=StringIO()) as mock_out:
            main.main()

        actual = mock_out.getvalue().strip().split("\n")
        expected = [""]
        self.assertListEqual(expected, actual)

    @unittest.skip
    def test_new_function(self):
        actual = main.main()
        expected = 32
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
