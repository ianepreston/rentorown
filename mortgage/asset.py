"""Basic asset class to escalate financial flows"""
import math
import numpy as np


def annual_to_monthly_return(annual_return):
    """Convert annual return to monthly"""
    return (1 + annual_return) ** (1 / 12) - 1


def annual_to_monthly_stdev(annual_stdev):
    """Be careful with this one

    It seems like a common method in financial modelling to just take the monthly
    standard deviation and multiply it by sqrt(12) to annualize it. So in reverse that
    would just be the formula below. I haven't looked into what assumptions have to
    hold for this to be valid and I'm planning to be a bit more careful with how I
    parameterise things. But as a first approximation it's a decent helper
    """
    return annual_stdev / math.sqrt(12)


class BaseAsset:
    """Basic way of defining an asset

    Lets you parameterize the distribution it's drawn from,
    Specify the number of simulations and periods to simulate for,
    and plot results of the simulations
    """

    def __init__(
        self,
        dist=np.random.normal,
        dist_args={"loc": 0.006, "scale": 0.06},
        periods=300,
        simulations=100,
    ):
        self.returns = (1 + dist(**dist_args, size=(periods, simulations))).cumprod(
            axis=0
        )
        self.returns[0] = 1


if __name__ == "__main__":
    print(annual_to_monthly_return(0.06))
