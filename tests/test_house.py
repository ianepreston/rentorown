import pytest
from mortgage import house


@pytest.fixture(scope="module")
def demo_house():
    test_house = house.House(100000)
    return test_house


def test_cmhc_over_20(demo_house):
    """ should have no premium"""
    assert demo_house._find_cmhc_premium(20000) == 0


def test_cmhc_over_15(demo_house):
    """next cutoff is >= 15%"""
    assert demo_house._find_cmhc_premium(15000) == 2380.0


def test_title_fees(demo_house):
    """title fee calc for Alberta"""
    assert demo_house._find_title_fees(80000) == 136


def test_sell(demo_house):
    """right now sell should just return value"""
    assert demo_house.sell() == 100000


def test_buy(demo_house):
    """test buying with defaults
    Shouldn't have CMHC, title fees match above test
    Will need to add more complicated houses to test edge cases later
    """
    buy_dict = demo_house.buy(20000)
    assert buy_dict["mortgage"] == 80000
    assert buy_dict["cash"] == 22436
