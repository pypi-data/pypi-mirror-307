#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
----------- DATATOOLBOX -------------
This is a python tool box project for handling global datasets.
It contains the following features:

    Augumented pandas DataFrames adding meta data,
    Automatic unit conversion and table based computations
    ID based data structure
    Package specific helper functions (see: tools/)

Authors: Andreas Geiges
         Jonas Hörsch
         Gaurav Ganti
         Matthew Giddens

"""

from . import version

__version__ = version.__version__
import time

all_tt = time.time()

import os

tt = time.time()
from . import config

print("Config initialised in {:2.4f} seconds".format(time.time() - tt))
tt = time.time()
from . import core

if config.DEBUG:
    print("Init of core in {:2.4f} seconds".format(time.time() - all_tt))


try:
    tt = time.time()
    from . import database

    if config.DEBUG:
        print("Database import in {:2.4f} seconds".format(time.time() - tt))

    core.DB = database.Database()
    db_connected = True
except Exception:
    import traceback

    print("Database connection broken. Running without database connection.")
    traceback.print_exc()
    db_connected = False


tt = time.time()
interfaces = core.LazyLoader("interfaces", globals(), "datatoolbox.interfaces")
# from . import interfaces

if config.DEBUG:
    print("Interfaces loaded in {:2.4f} seconds".format(time.time() - tt))

tt = time.time()
from . import util as util

if config.DEBUG:
    print("Utils loaded in {:2.4f} seconds".format(time.time() - tt))

from . import admin as admin

tt = time.time()
import pint

print("Utils loaded in {:2.4f} seconds".format(time.time() - tt))


# %% DATA STRUCTURES
tt3 = time.time()
from .data_structures import Datatable, TableSet, DataSet, read_csv

if config.DEBUG:
    print("Data structures loaded in {:2.4f} seconds".format(time.time() - tt3))

# %% IO

if config.DEBUG:
    print("IO loaded in {:2.4f} seconds".format(time.time() - tt))

# %% SETS
# Predefined sets for regions and scenrarios

from .sets import SCENARIOS, REGIONS, PATHWAYS

# %% indexing

from . import indexing as idx

# %% UNITS

units = core.unit_registry

# %% DATABASE
if db_connected:
    # here some main database methods are exposed to the package level. See
    # core.py for the linked methods. The mapping is done in a function to allow
    # re-assignment if the database instance is changing, e.g. for testing purposes.
    core.link_main_package_methods(locals(), core.DB)
# %% TOOLS
# Tools related to packages
if config.DEBUG:
    tt = time.time()

tools = core.LazyLoader("tools", globals(), "datatoolbox.tools")


# %% UNITS

conversionFactor = units.conversionFactor

# get country ISO code
getCountryISO = util.getCountryISO


# convenience functions
get_time_string = core.get_time_string
get_date_string = core.get_date_string


if db_connected:
    if config.PATH_TO_DATASHELF == os.path.join(
        config.MODULE_PATH, "data/SANDBOX_datashelf"
    ):
        print(
            """
              ################################################################
              You are using datatoolbox with a testing database as a SANDBOX.
              This allows for testing and initial tutorial use.
              
    
              For creating an empty dataase please use:
                  "datatoolbox.admin.create_empty_datashelf(pathToDatabase)"
    
              For switching to a existing database use: 
                  "datatoolbox.admin.change_personal_config()"
                  
                  
              ################################################################
              """
        )
else:
    print(
        """
          ################################################################
          
          You are using datatoolbox with no database connected
          
          Access functions and methods to database are not available.
              
          ################################################################
          """
    )


if config.DEBUG:
    print("Full datatoolbox init took {:2.4f} seconds".format(time.time() - all_tt))
