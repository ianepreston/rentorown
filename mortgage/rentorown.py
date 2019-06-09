import numpy as np
from .asset import BaseAsset, annual_to_monthly_return
from .house import House, Mortgage


class RentOrOwn:
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
                simulations=number_of_simulations
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
            simulations=number_of_simulations
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
