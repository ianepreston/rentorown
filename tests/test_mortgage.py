"""Tests for the mortgage class"""
import pytest
from mortgage import house


@pytest.fixture(scope="module")
def mortgage100k():
    test_mortgage = house.Mortgage(100000, 25, 0.06)
    return test_mortgage


@pytest.fixture(scope="module")
def mortgage250k():
    test_mortgage = house.Mortgage(250000, 25, 0.03)
    return test_mortgage


def test_correct_monthly_payment(mortgage100k, mortgage250k):
    assert mortgage100k.monthly_payment() == 639.81
    assert mortgage250k.monthly_payment() == 1183.11


def test_correct_bi_weekly_payment(mortgage100k, mortgage250k):
    assert mortgage100k.bi_weekly_payment() == 294.90
    assert mortgage250k.bi_weekly_payment() == 545.69


def test_correct_acc_bi_weekly_payment(mortgage100k, mortgage250k):
    assert mortgage100k.acc_bi_weekly_payment() == 319.90
    assert mortgage250k.acc_bi_weekly_payment() == 591.55


def test_correct_interest(mortgage250k):
    df = mortgage250k.amortize()
    assert df["Interest"].sum().round(2) == 104_934.71
    assert df["Principal"].sum().round(2) == 250_000.0
    df = mortgage250k.amortize(payment_type="bi_weekly")
    assert df["Interest"].sum().round(2) == 104_696.21
    assert df["Principal"].sum().round(2) == 250_000.0
    df = mortgage250k.amortize(payment_type="acc_bi_weekly")
    assert df["Interest"].sum().round(2) == 92_042.94
    assert df["Principal"].sum().round(2) == 250_000
