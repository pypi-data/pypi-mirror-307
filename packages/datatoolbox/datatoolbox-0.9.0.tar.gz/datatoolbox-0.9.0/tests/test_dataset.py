#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 14:49:27 2022

@author: ageiges
"""

import copy
import datatoolbox as dt

from util_for_testing import df, df2, sourceMeta

dt.admin.switch_database_to_testing()


def test_dataset_from_pyam():
    res = dt.findp(variable=["Numbers|Ones", "Numbers|Fives"])  # find all
    ds2 = dt.DataSet.from_query(res)

    idf = res.as_pyam()
    ds = dt.DataSet.from_pyam(idf)

    assert (ds == ds2).all()["Numbers|Fives"]
    assert (ds == ds2).all()["Numbers|Ones"]


def test_dataset_from_wide_df():
    res = dt.findp(variable=["Numbers|Ones", "Numbers|Fives"])  # find all
    ds2 = dt.DataSet.from_query(res)

    wdf = res.as_wide_dataframe()
    ds = dt.DataSet.from_wide_dataframe(wdf)

    assert (ds == ds2).all()["Numbers|Fives"]
    assert (ds == ds2).all()["Numbers|Ones"]


def test_dataset_from_query():
    res = dt.findp(variable=["Numbers|Ones", "Numbers|Fives"])  # find all
    ds = dt.DataSet.from_query(res)


def test_sel_methods():
    res = dt.findp(variable=["Numbers|Ones", "Numbers|Fives"])  # find all
    ds = dt.DataSet.from_query(res)

    sub = ds.sel(scenario="Historic")

    exp = {"time": 5, "region": 4, "source": 1, "model": 1}
    assert all([exp[key] == dict(sub.sizes)[key] for key in exp.keys()])

    sub = ds.sel(region="DEU")

    exp = {"time": 5, "source": 1, "pathway": 1}

    sub = ds.sel(time=2012)

    exp = {"region": 4, "source": 1, "pathway": 1}
    assert all([exp[key] == dict(sub.sizes)[key] for key in exp.keys()])


def test_unit_conversion():
    res = dt.findp(variable=["Numbers|One", "Numbers|Fives"])  # find all
    ds = dt.DataSet.from_query(res)
    mm_data = ds["Numbers|Fives"].pint.to("mm")

    assert (mm_data.values == ds["Numbers|Fives"].values * 1000).all()

    # test Emission unit
    test_array = ds["Numbers|Fives"].pint.dequantify().pint.quantify("Mt CO2 / yr")
    test_array = test_array.pint.to("kt CO2/ d")

    assert (test_array.values == 13.689253935660503).all()


if __name__ == "__main__":
    test_dataset_from_query()
    test_sel_methods()
    test_unit_conversion()
