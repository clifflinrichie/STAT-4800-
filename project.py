import pandas as pd
import numpy as np
import statsmodels.api as sm    # python -m pip install statsmodels  
from sklearn.linear_model import LinearRegression


fb_2019 = pd.read_csv('2021 UVA Football Data-selected\\2019 PFF All Plays.csv', index_col=0)


# Input column names that we care about for calculating expected points
# penaltyyards(situational), kickyards(situational), yardsaftercatch, 
# driveend and, drivestart, playendposition, clock?, down?, distance, fieldposition
# score (home.away score), offscore
ep_variables = ["pff_PENALTYYARDS", "pff_KICKYARDS", "pff_YARDSAFTERCATCH",
                "pff_DRIVEENDFIELDPOSITION", "pff_DRIVESTARTFIELDPOSITION", "pff_PLAYENDFIELDPOSITION",
                "pff_DOWN", "pff_DISTANCE", "pff_FIELDPOSITION", "pff_SCORE", "pff_OFFSCORE"]

fb_2019_EP = fb_2019[ep_variables]

# print(fb_2019_EP.head())

fb_2019_EP.to_csv('ep_var.csv')

def run_simulation():
    y = fb_2019_EP["pff_OFFSCORE"]
    y = np.array(y)
    x_df = fb_2019_EP.drop("pff_OFFSCORE", 1)
    x_df = x_df.fillna(0)
    x = np.array(x_df)
    print(x) 

    linear_regression(x,y)
    advanced_linear_regression(x,y)
    

def linear_regression(x, y):
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    print('coefficient of determination:', r_sq)

    print('intercept:', model.intercept_)

    print('slope:', model.coef_)

    return model

def advanced_linear_regression(x, y):
    x = sm.add_constant(x)
    model = sm.OLS(y, x)
    results = model.fit()
    print(results.summary())

    print('coefficient of determination:', results.rsquared)
    print('adjusted coefficient of determination:', results.rsquared_adj)
    print('regression coefficients:', results.params)

run_simulation()