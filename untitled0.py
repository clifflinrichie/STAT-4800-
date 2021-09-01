# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 22:44:51 2021

@author: andyc
"""
#%%
import pandas as pd
import numpy as np

filename = r"C:\Users\andyc\Downloads\STAT 4800\2019 PFF All Plays.csv"
data = pd.read_csv(filename)
#%%
data["DRIVEENDFIELDPOSITION"]