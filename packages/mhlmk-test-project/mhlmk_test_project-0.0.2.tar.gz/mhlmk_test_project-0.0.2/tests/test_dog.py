"""
Test Dog class
"""

# Standard
import unittest

# First Party
from mhlmk_test_project.dog import dog


class TestDog(unittest.TestCase):
    """
    Dog test class
    """

    def setUp(self):
        self.dog = dog.Dog()

    def test_what_am_i(self):
        """
        testing wham_am_i() nfunction
        """
        expected_output = "I am a dog first but also a mammal"
        actual_output = self.dog.what_am_i()
        self.assertEqual(expected_output, actual_output)


if __name__ == "__main__":
    unittest.main()
