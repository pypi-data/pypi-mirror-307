# tests/test_module1.py

import unittest
from package_publishing import add, subtract

class TestModule1(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(-1, 1), 0)
    
    def test_subtract(self):
        self.assertEqual(subtract(2, 1), 1)
        self.assertEqual(subtract(2, 3), -1)

if __name__ == "__main__":
    unittest.main()