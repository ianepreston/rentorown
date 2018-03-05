#!/opt/anaconda/bin/ipython
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 16:01:26 2018

@author: cornucrapia
"""
import unittest
from mortgage import *

class MortgageTestCase(unittest.TestCase):
    """Tests for mortgage.py"""


    def test_correct_monthly_payment(self):
        """for monthly payment schedule"""
        self.assertEqual(round(find_mortgage_payment(100000, 25, 0.06), 2), 639.81)

    def test_correct_biweekly_payment(self):
        """for bi weekly payment schedule"""
        self.assertEqual(round(find_mortgage_payment(100000, 25, 0.06, 24), 2), 319.51)

    def test_correct_weekly_payment(self):
        """ 52 payments per year"""
        self.assertEqual(round(find_mortgage_payment(100000, 25, 0.06, 52), 2), 147.37)

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
        