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
p = r"C:\Users\joshj\Downloads\SB_box_scores_2019_without_rank.csv"
data = pd.read_csv(p, index_col=0)
# os.chdir('/Users/joshjeon/Documents')
# data = pd.read_csv("SB_box_scores_2019_without_rank.csv", index_col=0)

### finding all unique teams
teams = pd.unique(pd.concat([data['Winner'],data['Loser']]))
print(data["Winner"])
for d in data["Winner"]:
    print(d)
for x in df["Date Time"]:
    

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
total_team_occurances = np.array(total_team_occurances)
# create initial transition matrix
teams = pd.DataFrame(teams)
transition = np.zeros((teams.size,teams.size))
count = 0
for index, game in data.iterrows():
    winner = game["Winner"]
    loser = game["Loser"]
    wp = game["Pts_winner"]
    lp = game["Pts_loser"]
    wIndex = teams.loc[teams[0] == winner].index[0]
    lIndex = teams.loc[teams[0] == loser].index[0]
    transition[lIndex][wIndex] = (wp/(wp+lp))
    transition[wIndex][lIndex] = (lp/(lp+wp))

# replace all unknown games with p = 0.5
# for i in range(len(transition[0])):
#     for j in range(len(transition[0])):
#        if i != j:
#            if transition[i][j] == 0:
#                transition[i][j] = 0.5
# corner = len(transition[0])-1
# sum1 = 0
# sum2 = 0
# sum_col = 0
# sum_row = 0
# for i in range(len(transition[0])):
#     corner = corner - i
#     # sum_col = sum(transition[:,corner])-sum1
#     # sum_row = transition.sum(axis=1)[corner]-sum2
#     transition[i:corner,corner] = np.true_divide(transition[i:corner,corner], (1+sum1))
#     transition[corner,i:corner] = np.true_divide(transition[corner,i:corner], (1+sum2))
#     sum1 = 0
#     sum2 = 0
#     for i in range(corner-len(transition[0])-1):
#         sum1 += transition[i,corner-1]
#         sum2 += transition[corner-1,i]
#     corner = len(transition[0])-1

### make the matrix row-stochastic
for i in range(len(transition[0])):
    sum_row = transition[i].sum()
    transition[i] /= sum_row

### get proportions of games played
gamesPlayed = []
count = 0
tempTeams = np.array(teams)
for team in tempTeams:
    for played in total_team_occurances:
        if played == team:
            count += 1
    gamesPlayed.append(count)
    count = 0
gamesPlayed = np.array(gamesPlayed, dtype = np.float64)
gamesPlayed /= data.shape[0]
gamesPlayed = np.reshape(gamesPlayed,(217,1))

### multiply transition matrix by proportions of games played
for i in range(1):
    gamesPlayed = transition.dot(gamesPlayed)
gp = pd.DataFrame(gamesPlayed,columns = ["rank"])
gp['index_col'] = range(217)
gp = gp.sort_values(by='rank')
gp2 = np.array(gp['index_col'])
ranks = []
for i in gp2:
    ranks.append(tempTeams[i][0])
print(ranks)