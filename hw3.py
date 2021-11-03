import pandas as pd
import numpy as np
import os
p = r"C:\Users\joshj\Documents\nhl_pbp20162017.csv"
data = pd.read_csv(p, index_col=0)

# Filtering
filtered_data = data[data['Period'].isin([1,2,3])]
filtered_data = filtered_data[filtered_data['Event'] == 'SHOT']

# Binning into intervals
filtered_data2 = filtered_data.copy()
filtered_data4 = filtered_data.copy()
filtered_data5 = filtered_data.copy()

newcol2 = []
for value in filtered_data['Seconds_Elapsed']:
    bin = int(value/120)
    newcol2.append(bin)
filtered_data2['time'] = newcol2

newcol4 = []
for value in filtered_data['Seconds_Elapsed']:
    bin = int(value/240)
    newcol4.append(bin)
filtered_data4['time'] = newcol2

newcol5 = []
for value in filtered_data['Seconds_Elapsed']:
    bin = int(value/300)
    newcol5.append(bin)
filtered_data5['time'] = newcol2

# Groupings
period_groups = dict(filtered_data2['Period'].value_counts())
strength_groups = dict(filtered_data2['Strength'].value_counts())
time_groups = dict(filtered_data2['time'].value_counts())
id_groups = dict(filtered_data2['Game_Id'].value_counts())
team_groups = dict(filtered_data2['Ev_Team'].value_counts())

# Model Building
import sklearn as sk