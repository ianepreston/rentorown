import unittest
from house import find_cmhc_premium
from house import find_title_fees

class HouseTestCase(unittest.TestCase):
    """Tests for house.py"""
    def test_cmhc_over_20(self):
        """ should have no premium"""
        self.assertEqual(find_cmhc_premium(100000, 20000), 0)

    def test_cmhc_over_15(self):
        """next cutoff is >= 15%"""
        self.assertEqual(find_cmhc_premium(100000, 15000), 2380.0)

    def test_title_fees(self):
        """title fee calc for Alberta"""
        self.assertEqual(find_title_fees(202500, 162000), 174)


if __name__ == '__main__':
    unittest.main()
