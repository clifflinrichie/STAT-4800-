import pandas as pd
import numpy as np
import json

data = r"C:\Users\andyc\Downloads\STAT 4800\2019 PFF All Plays.csv"
fb_2019 = pd.read_csv(data, index_col=0)
"""
fb_2016 = pd.read_csv('2021 UVA Football Data-selected\\2016 PFF All Plays.csv', index_col=0)
fb_2017 = pd.read_csv('2021 UVA Football Data-selezcted\\2017 PFF All Plays.csv', index_col=0)
fb_2018 = pd.read_csv('2021 UVA Football Data-selected\\2018 PFF All Plays.csv', index_col=0)
fb_2019 = pd.read_csv('2021 UVA Football Data-selected\\2019 PFF All Plays.csv', index_col=0)
"""

# columns with mixed data types
# 4,81,85,86,94,95,101,112,143,154,155,163
# Reference column names json to find column name
# subtract by 1 because python indexes by 0 but pandas doesn't recognize that
#%%
# Input column names that we care about for calculating expected points
ep_columns = []
fb_2019_EP = fb_2019[ep_columns]
# print(fb_2015_EP)

#%%
# Find type of a column
print(fb_2019['pff_WEEK'].apply(type))

#%%
# Use this to filter by column given an index
# can either print all list, or can index "column_index" for a specific column
column_index = [3,80,84,85,93,94,100,111,142,153,154,162]
print("\nMIXED TYPES: \n")
all_mixed_df = fb_2019.iloc[:,column_index]
print(list(all_mixed_df.columns))

#%%
# Use this to output anything into JSON
"""
column_names = {fb_2015.columns.get_loc(c): c for idx, c in enumerate(fb_2015.columns)}

with open("column_names_by_index.json", "w") as outfile:
    json.dump(column_names, outfile)
"""
#%%
# Problem #2 DRIVEENDFIELDPOSITION variable
# Only transformed variables that are based off MIDLINE 
fb_2019["pff_DRIVEENDFIELDPOSITION"] = fb_2019["pff_DRIVEENDFIELDPOSITION"] + 50
print(fb_2019["pff_DRIVEENDFIELDPOSITION"])

#%%
# Problem #2 DRIVESTARTFIELDPOSITION variable
fb_2019["pff_DRIVESTARTFIELDPOSITION"] = fb_2019["pff_DRIVESTARTFIELDPOSITION"] + 50
print(fb_2019["pff_DRIVESTARTFIELDPOSITION"])
#%%
# Problem #2 FIELDPOSITION variable
fb_2019["pff_FIELDPOSITION"] = fb_2019["pff_FIELDPOSITION"] + 50
print(fb_2019["pff_FIELDPOSITION"])
