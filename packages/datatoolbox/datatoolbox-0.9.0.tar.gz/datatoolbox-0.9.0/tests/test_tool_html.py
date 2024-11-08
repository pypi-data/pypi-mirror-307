#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 14:49:27 2022

@author: ageiges
"""

import copy
import datatoolbox as dt

from util_for_testing import df, df2, sourceMeta

from datatoolbox.tools import html


def test_basic_html_generation():
    html.generate_html(df)
    html.export_to_html(df)
