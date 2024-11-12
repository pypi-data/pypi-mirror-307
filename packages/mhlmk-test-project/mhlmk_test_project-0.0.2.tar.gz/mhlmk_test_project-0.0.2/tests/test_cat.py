"""
Test Cat class
"""

# Standard
import unittest

# First Party
from mhlmk_test_project.cat import cat


class TestCat(unittest.TestCase):
    """
    Cat test class
    """

    def setUp(self):
        self.cat = cat.Cat()

    def test_what_am_i(self):
        """
        testing wham_am_i() nfunction
        """
        expected_output = "I am a cat first but also a mammal"
        actual_output = self.cat.what_am_i()
        self.assertEqual(expected_output, actual_output)


if __name__ == "__main__":
    unittest.main()
