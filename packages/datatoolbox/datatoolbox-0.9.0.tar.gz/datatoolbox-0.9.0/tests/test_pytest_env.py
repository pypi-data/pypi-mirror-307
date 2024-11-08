#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 08:52:37 2020

@author: ageiges
"""
import os
import pytest
import datatoolbox
def test_pyttest_enviroment_var():
    assert "PYTEST_VERSION"  in os.environ
    
    assert not ( "PYTEST_VERSION"  not in os.environ)
    
    print(os.environ['PYTEST_VERSION'])
