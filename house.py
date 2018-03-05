"""
Broader calculations around buying a house
"""
import math

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

def other_costs(
    legal_fees=1000,
    title_insurance=500,
    home_inspection=500,
    home_appraisal=300
):
    """
    Easy placeholder for other cash up front costs.
    Can be expanded later
    
    Keyword Arguments:
        legal_fees {int} -- legal fees (default: {1000})
        title_insurance {int} -- title insurance (default: {500})
        home_inspection {int} -- home inspection (default: {500})
        home_appraisal {int} -- home appraisal (default: {300})
    """
    other_costs = (
        legal_fees + title_insurance + home_inspection + home_appraisal
        )
    return other_costs

def find_mortgage(purchase_price, down_payment):
    """
    Compute mortgage based on purchase price and down payment
    Basically just accounts for CMHC
    
    Arguments:
        purchase_price {int or float} -- cost of the house
        down_payment {int or float} -- how much down in dollars
    """
    mortgage = (
        purchase_price - down_payment + 
        find_cmhc_premium(purchase_price, down_payment)
        )
    return mortgage

def find_cash_to_buy(purchase_price, down_payment, extras=other_costs()):
    """
    How much cash you need up front for a given house and down payment
    
    Arguments:
        purchase_price {int or float} -- cost of the house
        down_payment {int or float} -- how much down in dollars
        extras {int or float} -- other expenses
    """
    cash = down_payment
    cash += find_title_fees(purchase_price, mortgage_amount)
    cash += extras
    return cash
