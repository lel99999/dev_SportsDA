# coding: utf-8

# Some inspiration from https://www.kaggle.com/ralston3/march-machine-learning-mania-2016/ncaam-exploratory-analysis, including the nifty method for mapping team names to the dataset

# In[1]:

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ## TO DO
# * Convert ```daynum``` column to ```year```, ```month```, ```day``` columns for human readability and to fit with schema
# * Stats
#     * Figuring out summary stats for games
#     * Kenpom
#     * Sagarin
#     * BPI - type
#     * New stats, like Fastbreak vs slow (tempo stuff)

# In[2]:

file_path = '/data/basketball/2016_march_madness/data/'

reg_df = pd.read_csv(file_path + 'RegularSeasonDetailedResults.csv')
teams_df = pd.read_csv(file_path + 'Teams.csv')
seasons_df = pd.read_csv(file_path + 'Seasons.csv')
team_dict = dict(zip(teams_df['Team_Id'].values, teams_df['Team_Name'].values))
reg_df['Wteam_name'] = reg_df['Wteam'].map(team_dict)
reg_df['Lteam_name'] = reg_df['Lteam'].map(team_dict)

print('================================================')
print('Regular Season data:')
print('================================================')
print(reg_df.head(10))
print('================================================')
print('Teams data:')
print('================================================')
print(teams_df.head(10))


# ### Date manipulation
# I always hate this part. I need to convert ```daynum``` to three columns. Probably need datetime for this. And a lot of patience. And some luck.
# 
# The basic format will be:
# 
# ``` python
# game_date = seasons_df['Dayzero'] + reg_df['daynum']
# ```
# 
# The ```seasons_df['Dayzero']``` variable will have to be converted to a datetime object, and then we can add ```reg_df['daynum']``` to that, I think. After that, we'll have an exact date for each game, from which we can easily extract Year, Month, and Day.

# In[3]:

seasons_df[20:25]


# In[4]:

ts = seasons_df['Dayzero'][20]
fmt = '%m/%d/%Y'
print(ts)
curr_date = datetime.strptime(ts, fmt)
print([curr_date.year,curr_date.month,curr_date.day])


# In[5]:

season_dict = dict(zip(seasons_df['Season'].values, seasons_df['Dayzero'].values))
reg_df['Dayzero'] = reg_df['Season'].replace(season_dict)


# In[6]:

reg_df[['Season','Dayzero']].head(10)


# In[7]:

reg_df['Dayzero'] = reg_df['Dayzero'].apply(lambda x: datetime.strptime(x, fmt))


# In[8]:

# reg_df['Daynum'] - reg_df['Dayzero']
reg_df.dtypes


# In[10]:

reg_df['Gameday'] = reg_df[['Daynum','Dayzero']].apply(    lambda row : timedelta(days = int(row[0])) + row[1],axis=1)
                


# In[11]:

reg_df['Year'] = reg_df['Gameday'].apply(lambda x: x.year)
reg_df['Month'] = reg_df['Gameday'].apply(lambda x: x.month)
reg_df['Day'] = reg_df['Gameday'].apply(lambda x: x.day)


# In[12]:

reg_df[['Season','Year','Month','Day','Gameday','Wteam_name','Lteam_name','Wscore','Lscore']].loc[42000:42005]


# In[13]:

reg_df.columns


# Let's start simple. Going off descriptions in [Who's #1](http://www.goodreads.com/book/show/13530569-who-s-1-the-science-of-rating-and-ranking), we can develop a Massey and Colley system for a particular season. Make a new dataframe for a particular year (say, 2011), then compute Massey and Colley for the whole season, then examine?
# 
# First, how do we generate the Massey matrix?
# 
# * Brute force idea: Get the list of all unique teams, loop through each team, then loop through each game, using team index in list to build the Massey matrix M. Let's try this!
# 
# Might be able to improve this by considering only those games actually played by each team, instead of all games, and use smarter indexing to fill M
# 
# We can implement Colley without too much extra cost if we create the ```b``` vector inside the loop, since the Colley matrix 
# 
# **C** = 2**I** + **M**

# In[35]:

print(reg_df[reg_df['Season'] == 2011].head(5))
reg2011_df = reg_df[reg_df['Season'] == 2011]
team_name_list = reg2011_df['Wteam_name'].unique()
print(len(team_name_list))


# In[36]:

num_teams = len(team_name_list)

M = np.zeros((num_teams,num_teams))


# In[45]:

team_games = reg2011_df[(reg2011_df['Wteam_name'] == team_name_list[0]) | (reg2011_df['Lteam_name'] == team_name_list[0])]
team_games.head(5)


# In[89]:

get_ipython().run_cell_magic('time', '', "m_row = 0# current row in Massey matrix\n\n# also build point differential vector p\np = np.zeros((num_teams,1))\n\n# Colley approach requires b, win differential basically\nb = np.zeros((num_teams,1))\n\nfor k in team_name_list :\n    team_games = reg2011_df[(reg2011_df['Wteam_name'] == k) | (reg2011_df['Lteam_name'] == k)]\n    n_team = np.shape(team_games)[0]\n    # Number of games team played, for diagonal\n\n    times_played = np.zeros((1,np.shape(M)[1])) # basically an array for given row in M\n    \n    # counter for array indexing\n    ctr = 0\n    for j in team_name_list :\n        if j == k :\n            # this is the team itself\n            times_played[0,ctr] = n_team\n        else :\n            # Find all matches between team of interest (k) and opponent (j)\n            matches = team_games[(team_games['Wteam_name'] == j) | (team_games['Lteam_name'] == j)]\n            times_played[0,ctr] = np.negative(matches.shape[0])\n        ctr += 1\n    \n    # now add current row to M\n    M[m_row] = times_played\n    \n    # add cumulative points to p\n    # p_wins is point differential in games won by team k\n    p_wins = np.sum(\\\n        team_games[team_games['Wteam_name'] == k]['Wscore'] - \\\n            team_games[team_games['Wteam_name'] == k]['Lscore']\n    )\n    # p_losses is point differential in games lost by team k (will be negative)\n    p_losses = np.sum(\\\n        team_games[team_games['Lteam_name'] == k]['Lscore'] - \\\n            team_games[team_games['Lteam_name'] == k]['Wscore']\n    )\n    p[m_row] = p_wins + p_losses\n    \n    # Now build Colley right-hand side vector b\n    b[m_row] = 1 + (0.5) * (\\\n        team_games[team_games['Wteam_name'] == k].shape[0] - \\\n            team_games[team_games['Lteam_name'] == k].shape[0]\n    )\n    \n    # iterate to next row in M\n    m_row += 1")


# In[90]:

b


# In[62]:

times_played


# In[91]:

# finally, need to replace row in M with all 1s, and point total 0. 
# By convention, last row is chosen
#
# Before that though, Compute Colley matrix C
C = 2 * np.identity(num_teams) + M

M[-1,:] = np.ones((1,num_teams))
p[-1] = 0


# In[92]:

# Finally, to compute Massey ratings, solve the linear system
# r = M^(-1) * p

massey_ratings = np.linalg.solve(M, p)
colley_ratings = np.linalg.solve(C, b)


# In[70]:

massey_ratings


# In[93]:

ratings2011_df = pd.DataFrame(
    np.column_stack((team_name_list, massey_ratings, colley_ratings)), 
    columns=['Team', 'Massey', 'Colley']
)


# In[94]:

ratings2011_df.sort_values(by='Massey', ascending=False, inplace=True)


# In[95]:

ratings2011_df['Massey_rank'] = ratings2011_df['Massey'].rank(ascending=False)


# In[96]:

ratings2011_df['Colley_rank'] = ratings2011_df['Colley'].rank(ascending=False)


# In[100]:

ratings2011_df


