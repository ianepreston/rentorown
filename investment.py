from collections import OrderedDict
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd

def invest(
    start_balance,
    growth_rate,
    years,
    monthly_contrib=0,
    start_date=date.today().replace(day=1) + relativedelta(months=1)
):
    periodic_interest_rate = (1 + growth_rate)**(1/12) -1
    date_increment = relativedelta(months=1)
    periods = years * 12
    beg_balance = start_balance
    end_balance = start_balance
    stream = []
    for per in range(0, periods):
        interest = round(periodic_interest_rate * beg_balance, 2)
        increase = interest + monthly_contrib
        end_balance = beg_balance + increase
        to_add = {
            'Date': start_date,
            'Period': per,
            'Begin_balance': beg_balance,
            'Increase': increase,
            'End_balance': end_balance
        }
        stream.append(to_add)
        start_date += date_increment
        beg_balance = end_balance
        df = pd.DataFrame(stream)
        df.set_index('Date', inplace=True)
        good_order = [
            'Period',
            'Begin_balance',
            'Increase',
            'End_balance'
        ]
        df = df[good_order]
    return df

if __name__ == '__main__':
    test = invest(100, .1, 5)

