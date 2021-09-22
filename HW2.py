## HW2 | 9/23 | Andy Chuang, Josh Jeon, Cliff Lin
"""
1. Page Rank is an algorithm which allows Google Search to rank web pages in their search results. 
-Works by counting the number and quality of links to a page => rough estimate of importance of website
-links analysis algorithm
-assigns numerical weighting to each element of a hyperlinked set of docs
-purpose is to measure relative importance within the set
-outputs a probability distribution used to represent the likelihood that a person randomly
clicking on links will arrive on a particular page. EX: document with PageRank of 0.5 = 50% chance that 
person clicking on random link will be directed to said document.
"""

"""
2. A good "metaphor" for using Markov chains in the ranking problem could be a "bandwagon fan," a fan who tends to support
whichever team is doing better. Each team starts with the same amount of fans - each fan has the choice to change teams or
stay with their current team. They can choose after each iteration.
"""

import pandas as pd
import numpy as np
import os

os.chdir('/Users/joshjeon/Documents')
data = pd.read_csv("SB_box_scores_2019_without_rank.csv", index_col=0)

### finding all unique teams
teams = pd.unique(pd.concat([data['Winner'],data['Loser']]))

### # of unique teams = 217
# print(len(teams))

### # of wins per team
# print(data["Winner"].value_counts())

""" 
The following section was a huge waste of time in an attempt to categorize by conference (which didn't work)
"""
# # data = data.head(500)
# # print(data)
# ### initialize all games winners and losers into categories
# init_cats = []
# for index, game in data.iterrows():
#     init_cats.append([game["Winner"],game["Loser"]])
# # print(init_cats)

# ### append any teams that played each other to their respective categories
# count1 = 0
# count2 = 0
# # for index, game in data.iterrows():
# #     for category in init_cats_copy:
# #         # print(category)
# #         if game["Winner"] in category:
# #             init_cats[count].append(game["Loser"])
# #         if game["Loser"] in category:
# #             init_cats[count].append(game["Winner"])
# #         count += 1
# #     count = 0
# import copy
# init_cats_copy = copy.deepcopy(init_cats)
# # for category1 in init_cats_copy:
# #     for category2 in init_cats_copy:
# #         if category1 != category2:
# #             for temp1 in category1:
# #                 if temp1 in category2:
# #                     init_cats[count1].append(temp1)
# #             for temp2 in category2:
# #                 if temp2 in category1:
# #                     init_cats[count2].append(temp2)
# #         count1 += 1
# #     count2 += 1
# #     count1 = 0
# for category1 in init_cats:
#     for category2 in init_cats:
#         if category1 != category2:
#             if category1[0] in init_cats_copy[count1]:
#                 init_cats_copy[count1].append(category1[1])
#             if category1[1] in init_cats_copy[count1]:
#                 init_cats_copy[count1].append(category1[0])
#             if category2[0] in init_cats_copy[count2]:
#                 init_cats_copy[count2].append(category2[1])
#             if category2[1] in init_cats_copy[count2]:
#                 init_cats_copy[count2].append(category2[0])
#     count1 += 1
#     count2 += 1
#     # count1 = 0
# print(len(init_cats_copy[1]))
# ### get unique values into each category
# temp1 = []
# temp2 = []
# for category in init_cats_copy:
#     for team in category:
#         if team not in temp2:
#             temp2.append(team)
#     temp1.append(temp2)
#     temp2 = []
# print(len(temp1[1]))
# print(len(temp1[3]))
# ### standardize each category
# temp3 = []
# for category in temp1:
#     category.sort()

# ### get each unique categories to find the conferences
# final_categories = []
# for category in temp1:
#     if category not in final_categories:
#         final_categories.append(category)

# print(len(final_categories))

total_team_occurances = pd.concat([data['Winner'],data['Loser']])
print(total_team_occurances.value_counts())

teams = pd.DataFrame(teams)

for index, game in data.iterrows():
    winner = game["Winner"]
    loser = game["Loser"]
    wIndex = teams.loc[teams[0] == winner].index[0]
    lIndex = teams.loc[teams[0] == loser].index[0]
