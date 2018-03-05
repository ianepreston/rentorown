"""
Broader calculations around buying a house
"""
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