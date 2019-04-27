"""Messing around with refactoring the old code before I commit to a rebuild"""
import math
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import altair as alt

# Have to have a start point for math, next month seems as good as anything
START_DATE = date.today().replace(day=1) + relativedelta(months=1)

class House():
    """House object, you buy one of these"""    
    def __init__(self, value):
        """Right now the only thing it starts with is a value/price"""
        self.value = value
    
    def buy(self, down_payment, additional_costs=2300):
        """Buy the house
        
        Parameters
        ----------
        down_payment: numeric
            The dollar amount of the down payment
        additional_costs: numeric, default 2300
            legal fees, title insurance, home inspection,
            home appraisal, etc. default value from
            Preet Bannerjee's rent or own excel sheet
            # http://www.preetbanerjee.com/general/is-renting-a-home-always-a-waste-of-money-no/
        
        Returns
        -------
        {'mortgage': mortgage_amt, 'cash': cash}:
            dictionary returning numeric values for amount
            to be mortgaged and cash up front required for purchase
        """
        mortgage_amt = (
            self.value -
            down_payment +
            self._find_cmhc_premium(down_payment)
        )
        title_fees = self._find_title_fees(mortgage_amt)
        cash = down_payment + title_fees + additional_costs
        return {'mortgage': mortgage_amt, 'cash': cash}
    
    def sell(self):
        """Sell the house
        
        Eventually we'll want to add closing costs and other
        things in here, but for now this just returns the value
        """
        return self.value
    
    def _find_cmhc_premium(self, down_payment):
        """ Helper function for buy()
        Determine the amount of the CMHC premium added onto a mortgage
        Can only be applied to 25 year and under amortization periods
        I'm not checking for that right now, maybe update later

        Parameters
        ----------
        down_payment: numeric
            amount paid down

        Returns
        -------
        premium: numeric
            Amount of CMHC insurance, to be added to mortgage
        """
        loan_ratio = down_payment / self.value
        loan_amount = self.value - down_payment
        if loan_ratio >= 0.2:
            premium = 0
        elif loan_ratio >= .15:
            premium = loan_amount * 0.028
        elif loan_ratio >= .1:
            premium = loan_amount * 0.031
        elif loan_ratio >= .05:
            premium = loan_amount * 0.04
        else:
            raise ValueError('Down must be at least 5%')
        return premium

    def _find_title_fees(self, mortgage_amount):
        """Helper function for buy()
        Calculates title fees for Alberta

        Parameters
        ----------
        mortgage_amount: numeric
            amount of the mortgage

        Returns
        -------
        total_cost: float
            all title fees
        """
        def title_calc(amount):
            """Formula is the same for purchase and mortgage"""
            portions = math.ceil(amount / 5000)
            fee = 50 + portions
            return fee

        total_cost = title_calc(self.value) + title_calc(mortgage_amount)
        return total_cost
        


