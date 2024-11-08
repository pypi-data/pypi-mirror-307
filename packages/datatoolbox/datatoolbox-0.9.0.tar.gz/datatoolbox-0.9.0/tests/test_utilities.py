#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 13:57:45 2020

@author: ageiges
"""

import datatoolbox as dt
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from util_for_testing import auto_close_plot_deco

# %%
dt.admin.switch_database_to_testing()


def test_years_only():
    years = dt.util.yearsColumnsOnly(pd.Index(["2032", "Dec, 23", 1990]))

    assert years == ["2032", 1990]


def test_zip_export():
    zip_file_path = dt.util.zipExport("test_db_export.zip")

    dt.util.update_DB_from_zip(zip_file_path)

    os.remove(zip_file_path)


def test_identify_country():
    assert dt.util.identifyCountry("276") == "DEU"
    assert dt.util.identifyCountry("VI") == "VIR"
    assert dt.util.identifyCountry("IND") == "IND"
    assert dt.util.identifyCountry("Nothing found") is None


# def test_create_graph_basic():
#    from datatoolbox.utilities import get_data_trees,  plot_tree
#    kwargs = dict(model="MESSAGE", scenario="SSP2-19")
#    graphs, scenario = get_data_trees(**kwargs)
#    plot_tree(graphs["Emissions"], scenario, savefig_path=(os.path.join(os.getcwd(), "test.png")))


@auto_close_plot_deco
def test_graph_from_search():
    from datatoolbox.util import plot_query_as_graph

    res = dt.finde(source="Numbers_2020")
    plot_query_as_graph(res)


#


@auto_close_plot_deco
def test_graph_integration():
    dt.finde(source="Numbers_2020").graph()


# if __name__ == '__main__':
#    test_create_graph_basic()
#    test_graph_from_search()
#    test_graph_integration()
