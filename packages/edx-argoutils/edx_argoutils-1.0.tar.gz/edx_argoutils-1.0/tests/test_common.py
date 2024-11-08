#!/usr/bin/env python

"""
Tests for BigQuery utils in the `edx_argoutils` package.
"""

from prefect.core import Flow

from edx_argoutils import common


def test_generate_dates():
    with Flow("test") as f:
        task = common.generate_dates(
            start_date='2020-01-01',
            end_date='2020-01-05'
        )
    state = f.run()
    assert state.is_successful()
    assert state.result[task].result == ['20200101', '20200102', '20200103', '20200104']


def test_generate_month_start_dates():
    with Flow("test") as f:
        task = common.generate_month_start_dates(
            start_date='2023-01-31',
            end_date='2023-05-05'
        )
    state = f.run()
    assert state.is_successful()
    assert state.result[task].result == ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01']


def test_get_unzipped_cartesian_product():
    with Flow("test") as f:
        task = common.get_unzipped_cartesian_product(
            input_lists=[[1, 2, 3], ["a", "b", "c"]]
        )
    state = f.run()
    assert state.is_successful()
    assert state.result[task].result == [
      (1, 1, 1, 2, 2, 2, 3, 3, 3),
      ("a", "b", "c", "a", "b", "c", "a", "b", "c")
    ]
