# -*- coding: utf-8 -*-
"""
Compute mortage related stuff
"""
import math


def calc_annual_rate(posted_rate):
    """Account for semi annual compounding"""
    annual_rate = (1 + posted_rate/2)**2 -1
    return annual_rate

def find_mortgage_payment(loan, years, rate, payments_per_year=12):
    """
    Determine monthly payments required to amortize a loan given
    the size of the loan, the number of years, and the interest rate

    Keyword arguments:
    loan: the size of the loan
    years: number of years of the loan
    rate: the annual interest rate (in decimal format)

    Returns: the monthly payment amount
    """
    periods = years * payments_per_year
    rate = calc_annual_rate(rate)
    periodic_interest_rate = (1 + rate)**(1/payments_per_year) -1
    payment = loan * periodic_interest_rate / (1-(1+periodic_interest_rate)**(-periods))
    return payment

def find_cmhc_premium(purchase_price, down_payment):
    """
    Determine the amount of the CMHC premium added onto a mortgage
    Can only be applied to 25 year and under amortization periods
    I'm not checking for that right now, maybe update later

    Keyword arguments:
    purchase_price: price of the house
    down_payment: amount paid down

    Returns: Amount of CMHC insurance, to be added to mortgage
    """
    loan_ratio = down_payment / purchase_price
    loan_amount = purchase_price - down_payment
    if loan_ratio >= 0.2:
        print("Down payment 20% or greater, no premium")
        premium = 0
    elif loan_ratio >= .15:
        premium = loan_amount * 0.028
    elif loan_ratio >= .1:
        premium = loan_amount * 0.031
    elif loan_ratio >= .05:
        premium = loan_amount * 0.04
    else:
        print("Down payment less than 5%, invalid, returning 10% premium")
        premium = loan_amount * 0.1
    return premium


def find_title_fees(purchase_price, mortgage_amount):
    """
    Calculates title fees for Alberta

    Keyword arguments:
    purchase_price: price of the house
    mortgage_amount: amount of the mortgage

    returns:
    Total cost of fees
    """
    def title_calc(amount):
        """
        Formula is the same for purchase and mortgage
        """
        portions = math.ceil(amount / 5000)
        fee = 50 + portions
        return fee

    total_cost = title_calc(purchase_price) + title_calc(mortgage_amount)
    return total_cost

def find_mortgage_payment_stream(loan, years, rate, payments_per_year=12):
    """
    Determine monthly payments required to amortize a loan given
    the size of the loan, the number of years, and the interest rate
    calculates the amount going to interest and principal in each payment

    Keyword arguments:
    loan: the size of the loan
    years: number of years of the loan
    rate: the annual interest rate (in decimal format)
    payments_per_year: payment frequency, eg 52 would be weekly

    Returns: numpy array of interest, principal and total payments
    """


class House:
    def __init__(self, price, down, amort):
        """
        price: list price of the house
        down: down payment in dollars
        amort: list of tuples of years and rates (year, rate)
            e.g [(5, 0.01), (10, 0.02)] is amortized for a total of 15 years
            at 1% for the first 5 and 2% for the last 10
        """
        self.list_price = price
        self.down_payment = down
        self.amortize_tuple = amort
        self.total_amortize = sum(i for i, j in amort)



    
    



if __name__ == '__main__':
    print("All for 100k 25 year 6%")
    print("monthly:")
    print(find_mortgage_payment(*[100000, 25, 0.06, 12]))
