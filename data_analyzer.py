# Mat Lockhart
# Thomas Baskin
# Python 3.7

# %%
# Setup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("combined.csv")
df = df.fillna(0)

# %%
# Implementation of the "Probably Doesn't Mean Anything" stat
# Points * field goal %, + TRB + AST + STL + BLK - TOV - PF
# Multiply this by the number of games, and then divide by 100

df['PDMA'] = ((df['FG%'] * df['PTS']) + df['TRB'] + df['AST'] + df['STL'] + df['BLK'] - df['TOV'] - df['PF']) * df['G'] / 100
df['Defense'] = df['BLK'] + df['STL']

print(df)

russel_df = df[df['Player'].isin(['russel'])]
jordan_df = df[df['Player'].isin(['jordan'])]
kareem_df = df[df['Player'].isin(['kareem'])]
lebron_df = df[df['Player'].isin(['lebron'])]

# %%
# Barplot of PDMA

ax = sns.barplot(x='Player', y='PDMA', data=df)
ax.set_title('Player PDMA')
ax.set_ylabel('Season average PDMA (average)')
ax.set_xlabel('Players')
plt.show()

# %%
# Average points per season

sns.distplot(russel_df['PTS'].tolist(), hist=False, label='russel')
sns.distplot(jordan_df['PTS'].tolist(), hist=False, label='jordan')
sns.distplot(kareem_df['PTS'].tolist(), hist=False, label='kareem')
sns.distplot(lebron_df['PTS'].tolist(), hist=False, label='lebron')
plt.xlabel('Points')
plt.ylabel('Percent of Seasons')
plt.figure()

# %%
# Defense per season

sns.distplot(jordan_df['Defense'].tolist(), hist=False, label='jordan')
sns.distplot(kareem_df['Defense'].tolist(), hist=False, label='kareem')
sns.distplot(lebron_df['Defense'].tolist(), hist=False, label='lebron')
plt.xlabel('Stops')
plt.ylabel('Percent of Seasons')
plt.figure()
