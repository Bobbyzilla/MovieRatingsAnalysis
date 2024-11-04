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

## QUESTION 1
## Are movies that are more popular (operationalized as having more ratings) rated higher than movies that are less popular? 
## [Hint: You can do a median-split of popularity to determine high vs. low popularity movies]

# Select movie ratings
movie_ratings = df.iloc[:, :400]

# Count popularity
popularity_counts = movie_ratings.notna().sum()

# Get median
median_popularity = popularity_counts.median(skipna=True)
print('Median popularity =', median_popularity)

# Split movies using median
high_popularity_movies = popularity_counts[popularity_counts >= median_popularity].index
low_popularity_movies = popularity_counts[popularity_counts < median_popularity].index

print('n (High popularity) =', len(high_popularity_movies))
print('n (Low popularity) =', len(low_popularity_movies))

# Calculate ratings median (excluding missing values)
high_popularity_ratings = movie_ratings[high_popularity_movies].median(skipna=True)
low_popularity_ratings  = movie_ratings[low_popularity_movies].median(skipna=True)

# Plotting the Distributions
plt.figure(figsize=(12, 6))

low_count = low_popularity_ratings.value_counts()
high_count = high_popularity_ratings.value_counts()

plt.bar(low_count.index - 0.025, low_count.to_list(), 0.05, label = 'Low popularity')
plt.bar(high_count.index + 0.025, high_count.to_list(), 0.05, label = 'High popularity')

plt.xlabel('Ratings')
plt.ylabel('Counts')
plt.title('Popularity vs Ratings comparison')
plt.legend()
plt.show()

# Perform Mann-Whitney U Test
mannwhitu = stats.mannwhitneyu(high_popularity_ratings, low_popularity_ratings, alternative='greater')

statistic = mannwhitu.statistic
p_value = mannwhitu.pvalue

print(f'Mann-Whitney U statistic: {statistic}')
print(f'P-value: {p_value}')

# 1) Is the difference significant?
if mannwhitu.pvalue < alpha:
  print('p_value < alpha, \nso the difference in ratings between high and low popularity movies is statistically significant.\n')

  # 2) Which one is higher rating?
  print('Since we used alternative="greater", the p_value shows that movies that are more popular are rated higher than movies that are less popular.')
else:
  print('p_value > alpha, \nthere is no statistically significant difference in ratings between high and low popularity movies.')