"""Messing around with refactoring the old code before I commit to a rebuild"""
import math
from collections import OrderedDict
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np


class House:
    """House object, you buy one of these
    
    Parameters
    ----------
    value: numeric
        The purchase price of the house
    """

    def __init__(self, value):
        self.value = value

    def monthly_property_tax(self, rate=0.0085):
        """taken from city of edmonton tax calculator
        
        Parameters
        ----------
        rate: float, default 0.0085
            annual tax rate 
        """
        return self.value * rate / 12

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
        dict
            {'mortgage': mortgage_amt, 'cash': cash}:
            dictionary returning numeric values for amount
            to be mortgaged and cash up front required for purchase
        """
        mortgage_amt = self.value - down_payment + self._find_cmhc_premium(down_payment)
        title_fees = self._find_title_fees(mortgage_amt)
        cash = down_payment + title_fees + additional_costs
        return {"mortgage": mortgage_amt, "cash": cash}

    def sell(self):
        """Sell the house
        
        Eventually we'll want to add closing costs and other
        things in here, but for now this just returns the value

        Returns
        --------
        self.value: numeric
            Just the value of the house
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
        elif loan_ratio >= 0.15:
            premium = loan_amount * 0.028
        elif loan_ratio >= 0.1:
            premium = loan_amount * 0.031
        elif loan_ratio >= 0.05:
            premium = loan_amount * 0.04
        else:
            raise ValueError("Down must be at least 5%")
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


class Mortgage:
    """Base mortgage class
    
    Parameters
    -----------
    principal: numeric
        Value of the mortgage
    years: int
        Amortization period of the mortgage (not term of fixed rate)
    rate: float
        APR rate as posted online, will use AER for actual calculations
    """

    def __init__(self, principal, years, rate):
        self.principal = principal
        self.years = years
        self.rate = rate

    def monthly_payment(self):
        """Payments required for a monthly payment schedule

        Takes APR as an input and compounds semi annually for AER. Canadian
        mortgages are dumb like that.
        
        Parameters
        -----------
        principal: numeric
            The amount of the mortgage
        years: int
            Total amortization period (not the term of the mortgage)
        rate: float
            APR in decimal form, i.e. 6% is input as 0.06
        
        Returns
        --------
        pmt: float
            The amount of the monthly payment
        """
        rate = (1 + (self.rate / 2)) ** 2 - 1
        periodic_interest_rate = (1 + rate) ** (1 / 12) - 1
        periods = self.years * 12
        pmt = -round(np.pmt(periodic_interest_rate, periods, self.principal), 2)
        return pmt

    def bi_weekly_payment(self):
        """Payments required for a bi-weekly payment schedule

        Takes APR as an input and compounds semi annually for AER. Canadian
        mortgages are dumb like that.
        
        Parameters
        -----------
        principal: numeric
            The amount of the mortgage
        years: int
            Total amortization period (not the term of the mortgage)
        rate: float
            APR in decimal form, i.e. 6% is input as 0.06
        
        Returns
        --------
        pmt: float
            The amount of the monthly payment
        """

        rate = (1 + (self.rate / 2)) ** 2 - 1
        periodic_interest_rate = (1 + rate) ** (1 / 26) - 1
        periods = self.years * 26
        pmt = -round(np.pmt(periodic_interest_rate, periods, self.principal), 2)
        return pmt

    def acc_bi_weekly_payment(self):
        """Payments required for an accelerated bi-weekly payment schedule
        
        Takes APR as an input and compounds semi annually for AER. Canadian
        mortgages are dumb like that.
        
        Parameters
        -----------
        principal: numeric
            The amount of the mortgage
        years: int
            Total amortization period (not the term of the mortgage)
        rate: float
            APR in decimal form, i.e. 6% is input as 0.06
        
        Returns
        --------
        pmt: float
            The amount of the monthly payment
        """
        pmt = round(self.monthly_payment() / 2, 2)
        return pmt

    def amortize(self, addl_pmt=0, payment_type="monthly"):
        """Show payments on the mortgage

        Parameters
        ----------
        addl_pmnt: numeric, default 0
            additional regular contributions
        payment_type: ["monthly", "bi_weekly", "acc_bi_weekly"], default "monthly"
            type of payment plan
        
        Returns
        -------
        df: pandas.DataFrame
            Dataframe of mortgage payments showing principal and interest contributions
            and amount outstanding
        """

        def amortizdict(adp=addl_pmt):
            """Yield a dictionary to convert to dataframe"""
            periods_dict = {
                "monthly": self.monthly_payment,
                "bi_weekly": self.bi_weekly_payment,
                "acc_bi_weekly": self.acc_bi_weekly_payment,
            }
            pmt = periods_dict[payment_type]()
            rate = (1 + (self.rate / 2)) ** 2 - 1
            if payment_type == "monthly":
                periodic_interest_rate = (1 + rate) ** (1 / 12) - 1
                date_increment = relativedelta(months=1)
            else:
                periodic_interest_rate = (1 + rate) ** (1 / 26) - 1
                date_increment = relativedelta(weeks=2)

            # initialize the variables to keep track of the periods and running balance
            per = 1
            beg_balance = self.principal
            end_balance = self.principal
            start_date = date.today().replace(day=1) + relativedelta(months=1)

            while end_balance > 0:
                # recalculate interest based on the current balance
                interest = round(periodic_interest_rate * beg_balance, 2)

                # Determine payment based on if this will pay off the loan
                pmt = min(pmt, beg_balance + interest)
                principal = pmt - interest

                # Ensure additional payment gets adjusted if the loan is being paid off
                adp = min(adp, beg_balance - principal)
                end_balance = beg_balance - (principal + adp)

                yield OrderedDict(
                    [
                        ("Date", start_date),
                        ("Period", per),
                        ("Begin_balance", beg_balance),
                        ("Payment", pmt),
                        ("Principal", principal),
                        ("Interest", interest),
                        ("Additional_payment", adp),
                        ("End_balance", end_balance),
                    ]
                )
                # increment the counter, balance and date
                per += 1
                start_date += date_increment
                beg_balance = end_balance

        df = (
            pd.DataFrame(amortizdict())
            .assign(Date=lambda df: pd.to_datetime(df["Date"]))
            .set_index("Date")
            .drop(columns=["Period"])
            .resample("MS")
            .agg(
                {
                    "Begin_balance": "max",
                    "Payment": "sum",
                    "Principal": "sum",
                    "Interest": "sum",
                    "Additional_payment": "sum",
                    "End_balance": "min",
                }
            )
            .assign(total_payment=lambda df: df["Payment"] + df["Additional_payment"])
        )
        return df
