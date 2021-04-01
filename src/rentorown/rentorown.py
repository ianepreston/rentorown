import locale
locale.setlocale(locale.LC_ALL, '')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from rentorown.asset import BaseAsset, annual_to_monthly_return
from rentorown.house import House, Mortgage


class RentOrOwn:
    """Based on a ton of assumptions, are you financially better off rening or owning?

    Taking two (presumably equivalent) properties, one of which you could rent, and the
    other that you could purchase, which one will leave you financially better off?
    Assuming (among other things) that you invest the difference in cash flow and don't
    just spend it.

    Enter bunch of assumptions about both the rental and owned property, as well as
    other financial assumptions, and based on them the model will show which is the
    better financial decision (assuming I built the model correctly).

    Parameters
        ----------
        monthly_rent: numeric
            Starting monthly rent of the equivalent rental property
        house_price: numeric
            The purchase price of the house
        down_payment: numeric
            The down payment on the house purchase
        mortgage_amortization_years: int
            How many years the mortgage on the house will be amortized over
        mortgage_apr: float
            The posted rate for the mortgage (right now it stays fixed over the whole
            period. I know that's not realistic, to be updated in a future release maybe
        housing_asset_dict: dictionary
            dictionary with keys "dist" and "dist_args" that will be used to parameterize
            the monthly returns of the housing asset. For example, dist could be
            np.random.norm and "dist_args" could be {"loc": 0.005, "scale": 0.02}
            specifying a mean of 0.005 and a standard deviation of 0.02. Note that all
            returns are monthly
        investment_asset_dict: dictionary
            Same as the housing asset dictionary, except this specifies the returns
            of the investment portfolio that the down payment and any net cash flow
            between renting and owning will be put into
        number_of_simulations: int
            How many times to try this simulation, gets a distribution of outcomes to
            compare over
        additional_purchase_costs: numeric, default None
            Home inspection, title insurance etc. If None, defaults to the default of
            additional_costs in the House.buy method
        additional_monthly_costs: numeric, default 0
            any additional costs of ownership, e.g. condo fees
        mortgage_payment_schedule: {"monthly", "bi_weekly", "acc_bi_weekly"}
            payment schedule for the mortgage, default Monthly
        mortgage_additional_payments: numeric, default 0
            If you want to make regular additional payments on your mortgage
        annual_inflation: float, default 0.02
            rent and non mortgage ownership costs will grow at this rate
        monthly_property_tax_rate: float, default None
            percentage of initial home value that will be charged. If default will take
            the default from the House class. Note that this is escalated by inflation,
            not against the forecasted value of the home
        maintenance_cost: float, default 0.01
            The annual percentage of the starting value of the house that will go to
            maintenance and upkeep. Note that this is also escalated by inflation


        TODO
        ----
        Lot of cleanup on __init__, some of the class variables can just be transient, or better
        named. Could use more inline comments. Might be worth breaking up into more
        functions. Some of the nested array Transposes could probably be fixed up.
    """

    def __init__(
        self,
        monthly_rent,
        house_price,
        down_payment,
        mortgage_amortization_years,
        mortgage_apr,
        housing_asset_dict,
        investment_asset_dict,
        number_of_simulations,
        additional_purchase_costs=None,
        additional_monthly_costs=0,
        mortgage_payment_schedule="monthly",
        mortgage_additional_payments=0,
        annual_inflation=0.02,
        monthly_property_tax_rate=None,
        maintenance_cost=0.01,
    ):
        """
        Input all the assumptions that will go into the rent or own model


        """
        house = House(value=house_price)
        if additional_purchase_costs is None:
            buy_dict = house.buy(down_payment=down_payment)
        else:
            buy_dict = house.buy(
                down_payment=down_payment, additional_costs=additional_purchase_costs
            )
        mortgage = Mortgage(
            buy_dict["mortgage"], mortgage_amortization_years, mortgage_apr
        )
        self.mortgage_df = mortgage.amortize(
            addl_pmt=mortgage_additional_payments,
            payment_type=mortgage_payment_schedule,
        )
        self._simulation_periods = self.mortgage_df.shape[0]
        self._inflation = annual_to_monthly_return(annual_inflation)
        if monthly_property_tax_rate is None:
            property_tax = house.monthly_property_tax()
        else:
            property_tax = house.monthly_property_tax(rate=monthly_property_tax_rate)
        maintenance = house_price * maintenance_cost / 12
        non_mortgage_costs_start = property_tax + maintenance + additional_monthly_costs
        non_mortgage_ownership_costs = self._inflated_series(non_mortgage_costs_start)
        own_cash_flow = (
            self.mortgage_df["total_payment"].to_numpy() + non_mortgage_ownership_costs
        )
        own_cash_flow[0] += buy_dict["cash"]
        self.house_appreciation = (
            BaseAsset(
                **housing_asset_dict,
                periods=self._simulation_periods,
                simulations=number_of_simulations,
            ).returns
            * house_price
        )
        own_debt = self.mortgage_df["End_balance"].to_numpy()
        self.own_net_worth = (self.house_appreciation.T - own_debt).T
        rent_cash_flow = self._inflated_series(monthly_rent)
        rent_net_cash_flow = own_cash_flow - rent_cash_flow
        rent_invest_cash_flow = np.maximum(rent_net_cash_flow, 0)
        rent_drawdown_cash_flow = np.minimum(rent_net_cash_flow, 0)
        asset_prices = BaseAsset(
            **investment_asset_dict,
            periods=self._simulation_periods,
            simulations=number_of_simulations,
        ).returns
        self.ap = asset_prices
        asset_units_purchase = (rent_invest_cash_flow / asset_prices.T).T.cumsum(axis=0)
        self.aup = asset_units_purchase
        rent_investment_value = asset_units_purchase * asset_prices
        self.riv = rent_investment_value
        self.rent_net_worth = (rent_investment_value.T - rent_drawdown_cash_flow).T

    def _inflated_series(self, amount):
        """Take an initial value and project it over the forecast period with inflation"""
        base_inflate = np.full(self._simulation_periods, 1 + self._inflation).cumprod()
        inflated = base_inflate * amount
        return inflated

    def histogram(self, period=None):
        """Plot a histogram of rent vs own net worths

        Parameters

        period: int, default None
            What period to compare net worth in, defaults to end of mortgage amortization
        """
        if period is None:
            period = -1
        elif abs(period) > self._simulation_periods - 1:
            print(
                f"period {period} out of range {self._simulation_periods}, setting to last period"
            )
            period = -1
        fig, ax = plt.subplots(figsize=(20, 10))
        plt.hist(
            (self.own_net_worth[period], self.rent_net_worth[period]),
            bins=min(100, self.own_net_worth.shape[0]),
            density=True,
            histtype="step",
            label=("Own", "Rent"),
        )
        plt.legend()
        if period < 0:
            period_label = (self._simulation_periods - period - 1) / 12
        else:
            period_label = period / 12
        plt.title(f"Distribution of results in year {period_label:0.1f}")
        ax.get_yaxis().set_ticks([])
        ax.xaxis.set_major_formatter(StrMethodFormatter("${x:n}"))
        plt.show()

    def median_returns_plot(self):
        """Plot median returns over the whole amortization period"""
        x = np.arange(0, len(self.own_net_worth))
        rent_med = np.median(self.rent_net_worth, 1)
        own_med = np.median(self.own_net_worth, 1)
        fig, ax = plt.subplots(figsize=(20, 10))
        plt.plot(x, own_med, label="Own")
        plt.plot(x, rent_med, label="Rent")
        plt.legend()
        plt.title("Median returns over the investment horizon")
        # ax.get_yaxis().set_ticks([])
        ax.yaxis.set_major_formatter(StrMethodFormatter("${x:n}"))
        plt.xlabel("Months")
        plt.ylabel("Net Worth")
        # ax.xaxis.set_major_formatter(StrMethodFormatter("${x:0.2e}"))
        plt.show()


class ParameterizedRentOrOwn(RentOrOwn):
    """Rent or own with pre built distributions for housing and assets

    Housing crudely estimated from MLS HPI:
    https://www.crea.ca/housing-market-stats/mls-home-price-index/hpi-tool/

    Investment returns taken from 80/20 Stocks Bonds expected returns from
    Canadian Couch Potato
    https://canadiancouchpotato.com/2016/03/21/what-returns-to-expect-when-youre-expecting/
    """

    def __init__(
        self,
        monthly_rent,
        house_price,
        down_payment,
        mortgage_amortization_years,
        mortgage_apr,
        number_of_simulations=10_000,
        additional_purchase_costs=None,
        additional_monthly_costs=0,
        mortgage_payment_schedule="monthly",
        mortgage_additional_payments=0,
        annual_inflation=0.02,
        monthly_property_tax_rate=None,
        maintenance_cost=0.01,
    ):
        super().__init__(
            monthly_rent=monthly_rent,
            house_price=house_price,
            down_payment=down_payment,
            mortgage_amortization_years=mortgage_amortization_years,
            mortgage_apr=mortgage_apr,
            housing_asset_dict={
                "dist": np.random.normal,
                "dist_args": {"loc": 0.004, "scale": 0.0136},
            },
            investment_asset_dict={
                "dist": np.random.normal,
                "dist_args": {"loc": 0.00510, "scale": 0.0266},
            },
            number_of_simulations=number_of_simulations,
            additional_purchase_costs=additional_purchase_costs,
            additional_monthly_costs=additional_monthly_costs,
            mortgage_payment_schedule=mortgage_payment_schedule,
            mortgage_additional_payments=mortgage_additional_payments,
            annual_inflation=annual_inflation,
            monthly_property_tax_rate=monthly_property_tax_rate,
            maintenance_cost=maintenance_cost,
        )
