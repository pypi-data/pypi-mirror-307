import unittest
from isNumberFour.module1 import isNumberFour

class TestIsNumberFour(unittest.TestCase):
    def test_isNumberFour(self):
        self.assertEqual(isNumberFour(4), True)

if __name__ == "__main__":
    unittest.main()