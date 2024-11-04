#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 16:32:26 2024

@author: jayantdabas
"""

import pandas as pd
from tqdm import tqdm

from scipy import stats

df = pd.read_csv('movieReplicationSet.csv')

alpha = 0.005


## QUESTION 8
## What proportion of movies exhibit such a “social watching” effect?

effect_count = 0

alone = {}
social = {}

for movie in tqdm(df.columns[:400]):
  alone_ratings  = df[movie][df.iloc[:,476] == 1].dropna()
  social_ratings = df[movie][df.iloc[:,476] == 0].dropna()

  alone[movie] = alone_ratings.median()
  social[movie] = social_ratings.median()

  if len(alone_ratings) > 0 and len(social_ratings) > 0:
    # Perform Mann-Whitney U Test
    mannwhitu = stats.mannwhitneyu(social_ratings, alone_ratings)
    if mannwhitu.pvalue < alpha:
          effect_count += 1

print(f"\n\nProportion of movies with a 'social watching' effect: {effect_count / 400}")
