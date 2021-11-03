# Andy Chuang, Josh Jeon, Cliff Lin
# Homework 3

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
u_period = filtered_data5['Period'].unique()
u_strength = ['5x5','5x4','4x5'] 
u_strength1 = [1,2,3] # three levels: 5x5, 5x4, 4x5 repsectfully
u_time = filtered_data5['time'].unique()
counts = []
x = []

for p in u_period:
    for s in u_strength:
        for t in u_time:
            counts.append(len(filtered_data5[(filtered_data5['Period']==p)&(filtered_data5['Strength']==s)&(filtered_data5['time']==t)]))
for p in u_period:
    for s in u_strength1:
        for t in u_time:
            x.append([p,s,t])

for i,v in enumerate(x):
    v.append(counts[i])
final_array = np.array(x)
final_df = pd.DataFrame(final_array, columns = ['Period','Strength','Time Bin','Shot Rate'])

# Model Building
from sklearn.linear_model import PoissonRegressor
from sklearn.model_selection import train_test_split
train, test = train_test_split(final_df, test_size=0.2)
y_train = np.array(train['Shot Rate'].copy())
train.drop(columns='Shot Rate', axis=1, inplace=True)
x_train = np.array(train.copy())

y_test = np.array(test['Shot Rate'])
test.drop(columns='Shot Rate', axis=1, inplace=True)
x_test = np.array(test.copy())

pr = PoissonRegressor()
pr.fit(x_train,y_train)
print(pr.score(x_train,y_train))
y_pred = pr.predict(x_test)
print(pr.coef_)

from sklearn.metrics import mean_squared_error
print(np.sqrt(mean_squared_error(y_test,y_pred)))
# we see here that we have a high rmse, we should look into ways to lower this

# Groupings 2 minutes
u_period2 = filtered_data2['Period'].unique()
u_strength2 = ['5x5','5x4','4x5'] 
u_strength12 = [1,2,3] # three levels: 5x5, 5x4, 4x5 repsectfully
u_time2 = filtered_data2['time'].unique()
counts2 = []
x2 = []

for p in u_period2:
    for s in u_strength2:
        for t in u_time2:
            counts2.append(len(filtered_data2[(filtered_data2['Period']==p)&(filtered_data2['Strength']==s)&(filtered_data2['time']==t)]))
for p in u_period2:
    for s in u_strength12:
        for t in u_time2:
            x2.append([p,s,t])

for i,v in enumerate(x2):
    v.append(counts2[i])
final_array2 = np.array(x2)
final_df2 = pd.DataFrame(final_array2, columns = ['Period','Strength','Time Bin','Shot Rate'])

# Model Building
from sklearn.linear_model import PoissonRegressor
from sklearn.model_selection import train_test_split
train2, test2 = train_test_split(final_df2, test_size=0.2)
y_train2 = np.array(train2['Shot Rate'].copy())
train2.drop(columns='Shot Rate', axis=1, inplace=True)
x_train2 = np.array(train2.copy())

y_test2 = np.array(test2['Shot Rate'])
test2.drop(columns='Shot Rate', axis=1, inplace=True)
x_test2 = np.array(test2.copy())

pr2 = PoissonRegressor()
pr2.fit(x_train2,y_train2)
print(pr2.score(x_train2,y_train2))
y_pred2 = pr2.predict(x_test2)
print(pr2.coef_)

from sklearn.metrics import mean_squared_error
print(np.sqrt(mean_squared_error(y_test2,y_pred2)))

# mse was lowered to 177