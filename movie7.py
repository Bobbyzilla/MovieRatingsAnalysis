#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 16:32:26 2024

@author: jayantdabas
"""

import pandas as pd

from scipy import stats

import matplotlib.pyplot as plt

df = pd.read_csv('movieReplicationSet.csv')

alpha = 0.005
  
  
## QUESTION 7
## Do people who like to watch movies socially enjoy 'The Wolf of Wall Street (2013)' more than those who prefer to watch them alone?

wows_alone_ratings  = df[df.iloc[:,476] == 1]['The Wolf of Wall Street (2013)'].dropna()
wows_social_ratings = df[df.iloc[:,476] == 0]['The Wolf of Wall Street (2013)'].dropna()

print('# of people who enjoy movies alone =', len(wows_alone_ratings))
print('# of people who enjoy movies socially =', len(wows_social_ratings))

# Plotting the Distributions
plt.figure(figsize=(12, 6))

alone_count = wows_alone_ratings.value_counts(normalize=True)
social_count = wows_social_ratings.value_counts(normalize=True)

plt.bar(alone_count.index - 0.025, alone_count.to_list(), 0.05, label = 'Solo viewers')
plt.bar(social_count.index + 0.025, social_count.to_list(), 0.05, label = 'Social viewers')

plt.xlabel('Ratings')
plt.ylabel('Counts')
plt.title('The Wolf of Wall Street (2013) - Viewer vs Ratings')
plt.legend()
plt.show()

# Perform Mann-Whitney U Test
mannwhitu = stats.mannwhitneyu(wows_social_ratings, wows_alone_ratings, alternative='greater')

print('Mann-Whitney U test')
print(f'Mann-Whitney U statistic: {mannwhitu.statistic}')
print(f'P-value: {mannwhitu.pvalue}')

if mannwhitu.pvalue < alpha:
  print('p_value < alpha, \nso the difference in viewing preference is statistically significant.\n')
  print('Since we used alternative="greater", People who like to watch movies socially enjoy ‘The Wolf of Wall Street (2013)’ more than those who prefer to watch alone.')
else:
  print('p_value > alpha, \nthere is no statistically significant difference in viewing preference and ratings.')