import pytest
from mortgage import rebuild

@pytest.fixture(scope='module')
def demo_house():
    test_house = rebuild.House(100000)
    return test_house


def test_cmhc_over_20(demo_house):
    """ should have no premium"""
    assert demo_house._find_cmhc_premium(20000) == 0


def test_cmhc_over_15(demo_house):
    """next cutoff is >= 15%"""
    assert demo_house._find_cmhc_premium(15000) == 2380.0


def test_title_fees(demo_house):
    """title fee calc for Alberta"""
    assert demo_house._find_title_fees(20000) == 124