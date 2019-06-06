"""
Broader calculations around buying a house
"""
import math
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np
import mortgage
from investment import invest


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
    elif loan_ratio >= 0.15:
        premium = loan_amount * 0.028
    elif loan_ratio >= 0.1:
        premium = loan_amount * 0.031
    elif loan_ratio >= 0.05:
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
    legal_fees=1000, title_insurance=500, home_inspection=500, home_appraisal=300
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
    other_costs = legal_fees + title_insurance + home_inspection + home_appraisal
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
        purchase_price - down_payment + find_cmhc_premium(purchase_price, down_payment)
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
    mortgage_amount = find_mortgage(purchase_price, down_payment)
    cash += find_title_fees(purchase_price, mortgage_amount)
    cash += extras
    return cash


def find_monthly_property_tax(house_value, rate=0.0085):
    """taken from city of edmonton tax calculator
    
    Arguments:
        house_value {numeric} -- assessed value of the house
    
    Keyword Arguments:
        rate {float} -- annual tax rate (default: {0.0085})
    """
    return house_value * rate / 12


# Need to rethink this design
class House:
    def __init__(
        self,
        purchase_price,
        down_payment,
        years,
        rate,
        addl_principal=0,
        start_date=date.today().replace(day=1) + relativedelta(months=1),
        payment_type="monthly",
    ):
        self.purchase_price = purchase_price
        self.down_payment = down_payment
        self.mortgage_amount = find_mortgage(purchase_price, down_payment)
        self.cash_to_buy = find_cash_to_buy(purchase_price, down_payment)
        self.df = mortgage.amortize_df(
            self.mortgage_amount, years, rate, addl_principal, start_date, payment_type
        )
        self.df["House Value"] = self.purchase_price
        self.df["Ownership_costs"] = self.df["Payment"]

    def calc_equity(self):
        self.df["Equity"] = self.df["House Value"] - self.df["End_balance"]

    def calc_value(self, rate):
        rate = (1 + rate) ** (1 / 12) - 1
        self.df["House Value"] = np.fv(
            rate, np.arange(len(self.df)), 0, -self.purchase_price
        )
        self.calc_equity()

    def calc_rent(self, rent, inflation):
        self.df["Years_out"] = self.df.index.year - self.df.index.year.min()
        start_month = self.df.index.month[0]
        mask = np.logical_and(
            self.df.index.month < start_month, self.df["Years_out"] > 0
        )
        self.df.loc[mask, "Years_out"] -= 1
        self.df["Rent"] = (1 + inflation) ** self.df["Years_out"] * rent
        self.df.drop(columns=["Years_out"], inplace=True)

    def calc_net_cash(self):
        self.df["Net Cash"] = self.df["Ownership_costs"] - self.df["Rent"]
        self.df["Net Cash"].iloc[0] += self.cash_to_buy

    def calc_other_expense(
        self, tax_rt=0.0085, maint_rt=0.0125, prop_insur=0.0019, other_costs=200
    ):
        combined_rate = (tax_rt + maint_rt + prop_insur) / 12
        self.df["Ownership_costs"] = (
            self.df["House Value"] * combined_rate + other_costs
        )
        self.df["Ownership_costs"] += self.df["Payment"]

    def calc_investment_equity(self, rate):
        rate = (1 + rate) ** (1 / 12) - 1
        equity = [self.df["Net Cash"][0]]
        for i in range(1, len(self.df)):
            new_eq = (equity[i - 1] + self.df["Net Cash"][i]) * (1 + rate)
            equity.append(new_eq)
            self.df["Investment Equity"] = equity


if __name__ == "__main__":
    test = House(600000, 120000, 25, 0.035)
    test.calc_value(0.03)
    test.calc_other_expense()
    test.calc_rent(2800, 0.02)
    test.calc_net_cash()
