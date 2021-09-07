import pandas as pd
import numpy as np
import json
# pairplot
from seaborn import pairplot

data = r"C:\Users\andyc\Downloads\STAT 4800\2019 PFF All Plays.csv"
# fb_2019 = pd.read_csv(data, index_col=0)
"""
fb_2016 = pd.read_csv('2021 UVA Football Data-selected\\2016 PFF All Plays.csv', index_col=0)
fb_2017 = pd.read_csv('2021 UVA Football Data-selected\\2017 PFF All Plays.csv', index_col=0)
fb_2018 = pd.read_csv('2021 UVA Football Data-selected\\2018 PFF All Plays.csv', index_col=0)
"""
fb_2019 = pd.read_csv('2021 UVA Football Data-selected\\2019 PFF All Plays.csv', index_col=0)

# columns with mixed data types
# 4,81,85,86,94,95,101,112,143,154,155,163
# Reference column names json to find column name
# subtract by 1 because python indexes by 0 but pandas doesn't recognize that

# Find type of a column
# print(fb_2019['pff_WEEK'].apply(type))

# Use this to filter by column given an index
# can either print all list, or can index "column_index" for a specific column
column_index = [3,80,84,85,93,94,100,111,142,153,154,162]
print("\nMIXED TYPES: \n")
all_mixed_df = fb_2019.iloc[:,column_index]
print(list(all_mixed_df.columns))

# Use this to output anything into JSON
"""
column_names = {fb_2015.columns.get_loc(c): c for idx, c in enumerate(fb_2015.columns)}

with open("column_names_by_index.json", "w") as outfile:
    json.dump(column_names, outfile)
"""
# Problem #2 DRIVEENDFIELDPOSITION variable
# Only transformed variables that are based off MIDLINE 
fb_2019["pff_DRIVEENDFIELDPOSITION"] = fb_2019["pff_DRIVEENDFIELDPOSITION"] + 50
fb_2019["pff_DRIVESTARTFIELDPOSITION"] = fb_2019["pff_DRIVESTARTFIELDPOSITION"] + 50
fb_2019["pff_FIELDPOSITION"] = fb_2019["pff_FIELDPOSITION"] + 50

"""
print(fb_2019["pff_DRIVEENDFIELDPOSITION"])
print(fb_2019["pff_DRIVESTARTFIELDPOSITION"])
print(fb_2019["pff_FIELDPOSITION"])
"""

# Input column names that we care about for calculating expected points
# penaltyyards(situational), kickyards(situational), yardsaftercatch, 
# driveend and, drivestart, playendposition, clock?, down?, distance, fieldposition
# score (home.away score), offscore
ep_variables = ["pff_PENALTYYARDS", "pff_KICKYARDS", "pff_YARDSAFTERCATCH", 
                "pff_DRIVEENDFIELDPOSITION", "pff_DRIVESTARTFIELDPOSITION", "pff_PLAYENDFIELDPOSITION",
                "pff_CLOCK", "pff_DOWN", "pff_DISTANCE", "pff_FIELDPOSITION", "pff_SCORE", "pff_OFFSCORE"]
fb_2019_EP = fb_2019[ep_variables]

print("\nData frame for variables we care about: \n")
print(fb_2019_EP.head())
print("\nAmount of missing values for each column: \n")
print(fb_2019_EP.isna().sum())
print("\nDetails of dataframe: \n")
print(fb_2019_EP.info())
print("\nSummary statistics on numeric columns: \n")
print(fb_2019_EP.describe())
# fb_2019_EP.to_csv('EP_var_initial_statistics.csv')
fb_2019_EP.describe().to_csv('EP_var_initial_statistics_summary.csv')

plot = pairplot(fb_2019_EP)
plot.savefig('fig.png')