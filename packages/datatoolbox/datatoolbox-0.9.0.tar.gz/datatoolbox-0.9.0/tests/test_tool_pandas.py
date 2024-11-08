#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 14:49:27 2022

@author: ageiges
"""

import copy
import datatoolbox as dt

from util_for_testing import df, df2, sourceMeta

from datatoolbox.tools import pandas as tool_for_pd


def test_add_country_names():
    df_ammended = tool_for_pd.addCountryNames(df)
    assert "country_name" in df_ammended.columns


def test_convertIndexToISO():
    df_text = df.copy()
    df_text.index = ["Argentina", "Germany", "France", "United Kindo"]
    df_ammended = tool_for_pd.convertIndexToISO(df_text)
    assert len(df_ammended.index) == 3


def test_yearsColumnsOnly():
    df_with_country_namess = df.copy()
    assert len(tool_for_pd.yearsColumnsOnly(df)) == 5  # removed name column
