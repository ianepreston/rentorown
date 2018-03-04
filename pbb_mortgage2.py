from collections import OrderedDict
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np


def monthly_payment(principal, years, rate): 
    rate = (1 + (rate /2))**2 -1
    periodic_interest_rate = (1 + rate)**(1/12) -1
    periods = years * 12
    np_pay = -round(np.pmt(periodic_interest_rate, periods, principal), 2)
    return np_pay

def bi_weekly_payment(principal, years, rate):
    rate = (1 + (rate /2))**2 -1
    periodic_interest_rate = (1 + rate)**(1/26) -1
    periods = years * 26
    np_pay = -round(np.pmt(periodic_interest_rate, periods, principal), 2)
    return np_pay

def acc_bi_weekly_payment(principal, years, rate):
    pmt = round(monthly_payment(principal, years, rate) / 2, 2)
    return pmt

def amortize(
    principal,
    years,
    rate,
    addl_principal=0,
    start_date=date.today(),
    payment_type='monthly'
):
    """
    generates an ordered dict with each entry an amortization table
    ToDo: Make a real docstring
    """
    periods_dict = {
        'monthly': monthly_payment,
        'bi_weekly': bi_weekly_payment,
        'acc_bi_weekly': acc_bi_weekly_payment
        }
    
    pmt = periods_dict[payment_type](principal, years, rate)
    rate = (1 + (rate /2))**2 -1
    if payment_type == 'monthly':
        periodic_interest_rate = (1 + rate)**(1/12) -1
        date_increment = relativedelta(months=1)
    else:
        periodic_interest_rate = (1 + rate)**(1/26) -1
        date_increment = relativedelta(weeks=2)
    
    # initialize the variables to keep track of the periods and running balance
    per = 1
    beg_balance = principal
    end_balance = principal
    
    while end_balance > 0:
        
        # recalculate interest based on the current balance
        interest = round(periodic_interest_rate * beg_balance, 2)
        
        # Determine payment based on if this will pay off the loan
        pmt = min(pmt, beg_balance + interest)
        principal = pmt - interest
        
        # Ensure additional payment gets adjusted if the loan is being paid off
        addl_principal = min(addl_principal, beg_balance - principal)
        end_balance = beg_balance - (principal + addl_principal)
        
        yield OrderedDict([('Date', start_date),
                           ('Period', per),
                           ('Begin_balance', beg_balance),
                           ('Payment', pmt),
                           ('Principal', principal),
                           ('Interest', interest),
                           ('Additional_payment', addl_principal),
                           ('End_balance', end_balance)
                           ])
        # increment the counter, balance and date
        per += 1
        start_date += date_increment
        beg_balance = end_balance

def amortize_df(
    principal,
    years,
    rate,
    addl_principal=0,
    start_date=date.today(),
    payment_type='monthly'
):
    """Wrapper for amortize to return a df"""
    df = pd.DataFrame(amortize(
        principal, years, rate, addl_principal, start_date, payment_type
        ))
    return df 
        

if __name__ == '__main__':
    df = amortize_df(100000, 25, 0.06, 0)
    df2 = amortize_df(100000, 25, 0.06, 0)
