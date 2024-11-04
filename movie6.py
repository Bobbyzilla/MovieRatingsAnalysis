# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:02:40 2024

@author: zhaoez
"""

import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('movieReplicationSet.csv')

def analyze_all_movies_only_child_effect(data, alpha=0.005):
    # movie columns (first 400 columns)
    #only child question column
    movie_cols = data.columns[:400]
    only_child_col = 'Are you an only child? (1: Yes; 0: No; -1: Did not respond)'
    
    # track significant movies and all movies (proporiton = significant_count/valid_movies)
    significant_count = 0
    valid_movies = 0
    insufficient_ratings = 0
    oof = 0
    
    # filters out rows with -1 in only child response
    valid_responses = data[data[only_child_col].isin([0, 1])]
    
    # iterate through every movie and compare the ratings for only child and sibling for that one movie
    for movie in movie_cols:
        movie_data = valid_responses[[movie, only_child_col]].copy()
        
        # drop nan elements (not rows)
        movie_data = movie_data.dropna(subset=[movie])
            
        # get ratings for only child and sibling
        only_child_ratings = movie_data[movie_data[only_child_col] == 1][movie]
        sibling_ratings = movie_data[movie_data[only_child_col] == 0][movie]
        
        if len(only_child_ratings) < 30 or len(sibling_ratings) < 30:
            insufficient_ratings += 1
        if len(only_child_ratings) < 9 or len(sibling_ratings) < 9:
            oof += 1
            
        # mann-whitney u test and compares p_value to alpha
        statistic, p_value = stats.mannwhitneyu(only_child_ratings, sibling_ratings)
        valid_movies += 1
        if p_value <= alpha:
            significant_count += 1
    
    # calculate proportion
    print(insufficient_ratings)
    print(oof)
    print(significant_count)
    print(valid_movies)
    proportion = significant_count / valid_movies
    return proportion

proportion = analyze_all_movies_only_child_effect(df)
print(f"proportion of movies with significant only child effect: {proportion:.4f}")


