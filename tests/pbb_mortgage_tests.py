import unittest
from pbb_mortgage2 import monthly_payment
from pbb_mortgage2 import acc_bi_weekly_payment
from pbb_mortgage2 import bi_weekly_payment


class MortgageTestCase(unittest.TestCase):
    """Pls work"""

    def test_correct_monthly_payment(self):
        self.assertEqual(monthly_payment(100000, 25, .06), 639.81)
        self.assertEqual(monthly_payment(250000, 25, .03), 1183.11)

    def test_correct_bi_weekly_payment(self):
        self.assertEqual(bi_weekly_payment(100000, 25, .06), 294.90)
        self.assertEqual(bi_weekly_payment(250000, 25, .03), 545.69)
        
    def test_correct_bi_weekly(self):
        self.assertEqual(acc_bi_weekly_payment(100000, 25, .06), 319.90)
        self.assertEqual(acc_bi_weekly_payment(250000, 25, .03), 591.55)
    

if __name__ == '__main__':
    unittest.main()