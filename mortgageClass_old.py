# -*- coding: utf-8 -*-
"""
Compute mortage related stuff
"""

def calc_annual_rate(posted_rate):
    """
    Account for semi annual compounding
    Posted rates are actually compounded twice per year,
    meaning your actual annual rate is a bit higher than posted
    """
    annual_rate = (1 + posted_rate/2)**2 -1
    return annual_rate

class Mortgage:
    def __init__(self, amount, years_rates, payments_per_year=12):
        """
        Various pure mortgage related functions
        
        Keyword arguments:
        amount: Initial amount of the mortgage
        years_rates: list of tuples of years and rates (year, rate)
            e.g [(5, 0.01), (10, 0.02)] is amortized for a total of 15 years
            at 1% for the first 5 and 2% for the last 10
        payments_per_year: defaults to monthly
        """
        self.init_amount = amount
        self.years = []
        self.rates = []
        for year, rate in years_rates:
            self.years.append(year)
            self.rates.append(rate)
        self.total_amortize = sum(self.years)
        self.rates[:] = [calc_annual_rate(rate) for rate in self.rates]


