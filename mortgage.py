"""
Collection of functions deal with mortgage calculations
Based heavily on http://pbpython.com/amortization-model-revised.html
ToDo:
DataFrame should automatically condense bi-weekly payments to monthly
More tests
More docstrings
"""
from collections import OrderedDict
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np

def monthly_payment(principal, years, rate):
    """
    Return the monthly payment based on amount, amortization period, and rate
    Takes APR as an input and compounds semi annually for AER. Canadian
    mortgages are dumb like that.
    
    Arguments:
        principal {int or float} -- The amount of the mortgage
        years {int} -- Total amortization period (not the term of the mortgage)
        rate {float} -- APR in decimal form, i.e. 6% is input as 0.06
    
    Returns:
        [float] -- The amount of the monthly payment
    """
    rate = (1 + (rate /2))**2 -1
    periodic_interest_rate = (1 + rate)**(1/12) -1
    periods = years * 12
    np_pay = -round(np.pmt(periodic_interest_rate, periods, principal), 2)
    return np_pay

def bi_weekly_payment(principal, years, rate):
    """
    Return the bi-weekly payment based on amount, amortization period, and rate
    Takes APR as an input and compounds semi annually for AER. Canadian
    mortgages are dumb like that.
    
    Arguments:
    principal {int or float} -- The amount of the mortgage
    years {int} -- Total amortization period (not the term of the mortgage)
    rate {float} -- APR in decimal form, i.e. 6% is input as 0.06
    
    Returns:
        [float] -- The amount of the monthly payment
    """

    rate = (1 + (rate /2))**2 -1
    periodic_interest_rate = (1 + rate)**(1/26) -1
    periods = years * 26
    np_pay = -round(np.pmt(periodic_interest_rate, periods, principal), 2)
    return np_pay

def acc_bi_weekly_payment(principal, years, rate):
    """
    Return the accelerated bi-weekly payment based on amount, amortization 
    period, and rate Takes APR as an input and compounds semi annually for AER.
    Canadian mortgages are dumb like that. For accelerated bi-weekly the
    formula is just your monthly payment divided by two so this function
    depends on the monthly payment above.
    
    Arguments:
    principal {int or float} -- The amount of the mortgage
    years {int} -- Total amortization period (not the term of the mortgage)
    rate {float} -- APR in decimal form, i.e. 6% is input as 0.06
    
    Returns:
    [float] -- The amount of the monthly payment
    """
    pmt = round(monthly_payment(principal, years, rate) / 2, 2)
    return pmt

def amortize(
    principal,
    years,
    rate,
    addl_principal=0,
    start_date=date.today().replace(day=1) + relativedelta(months=1),
    payment_type='monthly'
):
    """
    Creates a mortgage payment table with interest payments, outstanding
    balance for the entire amortization period.
    
    Arguments:
        principal {int or float} -- The amount of the mortgage
        years {int} -- Total amortization period (not the term of the mortgage)
        rate {float} -- APR in decimal form, i.e. 6% is input as 0.06
    
    Keyword Arguments:
        addl_principal {int} -- [additional regular payments] (default: {0})
        start_date {[type]} -- [when the mortgage starts] (default: today)
        payment_type {str} -- monthly, bi_weekly or acc_bi_weekly
         (default: {'monthly'})
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
    start_date=date.today().replace(day=1) + relativedelta(months=1),
    payment_type='monthly'
):
    """Wrapper for amortize to return a df"""
    df = pd.DataFrame(amortize(
        principal, years, rate, addl_principal, start_date, payment_type
        ))
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df.drop('Period', axis='columns', inplace=True)
    # Resulting DataFrame should be monthly regardless of payment frequency
    if payment_type != 'monthly':
        df_weekly = df.copy()
        df = df_weekly['Begin_balance'].resample('M').max()
        df = pd.concat(
            [df, df_weekly['End_balance'].resample('M').min()], axis=1
            )
        for col in ['Payment', 'Principal', 'Interest', 'Additional_payment']:
            df = pd.concat(
                [df, df_weekly[col].resample('M').sum()], axis=1
            )
        df.index = df.index.map(lambda d: d.replace(day=1))
    return df 
        

if __name__ == '__main__':
    df = amortize_df(100000, 25, 0.06, 0, payment_type="bi_weekly")