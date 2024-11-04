# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 16:18:09 2024

@author: zhaoez
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

df = pd.read_csv('movieReplicationSet.csv')

def analyze_movie_by_gambling(data, movie_col='The Wolf of Wall Street (2013)', gambling_col='Have you gambled or bet for money?', alpha=0.005):
    df = data.copy()
    
    #ensures that there is a response in the column even if verified that every row has an associated response
    df = df[df[gambling_col].isin([1, 2, 3, 4])]
    
    # removes rows with missing movie ratings (nan)
    df = df.dropna(subset=[movie_col])
    
    # seperate ratings based on gambling response, i chose to seperate it this way b/c
    # the question was posed as if it was expecting a binary response but still on a 
    # scale of 1-4 so I split the scale into two groups to determine gambling habits
    gambling_ratings = df[df[gambling_col].isin([3, 4])][movie_col]
    non_gambling_ratings = df[df[gambling_col].isin([1, 2])][movie_col]
    
    # mann-whitney u test
    statistic, p_value = stats.mannwhitneyu(gambling_ratings, non_gambling_ratings, alternative='greater')
    print(f"U statistic: {statistic}")
    
    fig, ax = plt.subplots()
    ratings = np.arange(0, 4.5, 0.5)
    gambler_counts = gambling_ratings.value_counts().reindex(ratings)
    non_gambler_counts = non_gambling_ratings.value_counts().reindex(ratings)
    ax.set_xticks(ratings)
    ax.set_xticklabels(ratings)
    ax.set_title('unormalized distribution of ratings for The Wolf of Wall Street')
    ax.set_xlabel('rating')
    ax.set_ylabel('count')
    ax.bar(ratings - 0.1, gambler_counts, width=0.2, label='gambler')
    ax.bar(ratings + 0.1, non_gambler_counts, width=0.2, label='non-gambler')
    ax.legend()
    
    fig, ax = plt.subplots()
    gambler_counts = gambling_ratings.value_counts(normalize=True).reindex(ratings)
    non_gambler_counts = non_gambling_ratings.value_counts(normalize=True).reindex(ratings)
    ax.bar(ratings - 0.1, gambler_counts, width=0.2, label='gambler')
    ax.bar(ratings + 0.1, non_gambler_counts, width=0.2, label='non-gambler')
    ax.set_xticks(ratings)
    ax.set_xticklabels(ratings)
    ax.set_title('normalized distribution of ratings for The Wolf of Wall Street')
    ax.set_xlabel('rating')
    ax.set_ylabel('proportion')
    ax.legend()
    plt.show()
    
    results = {
        'test_used':"Mann-Whitney U test",
        'test_statistic': statistic,
        'p_value': p_value,
        # true or false
        'significant': p_value <= alpha,
        'gambler_median': gambling_ratings.median(),
        'non_gambler_median': non_gambling_ratings.median(),
        'gambling_n': len(gambling_ratings),
        'non_gambling_n': len(non_gambling_ratings),
        'total_valid_responses': len(gambling_ratings) + len(non_gambling_ratings),
        'removed_responses': len(data) - (len(gambling_ratings) + len(non_gambling_ratings))
    }
    
    return results

def print_analysis_results(results):
    print(f"{results['test_used']}")
    print(f"p-value: {results['p_value']:.4f}")
    print(f"significant at α = 0.005: {results['significant']}")
    print("-" * 50)
    print("gambler:")
    print(f"  sample size: {results['gambling_n']}")
    print(f"  median: {results['gambler_median']}")
    print("non-gambler:")
    print(f"  sample size: {results['non_gambling_n']}")
    print(f"  median: {results['non_gambler_median']}")
    print("-" * 50)
    print(f"Valid responses: {results['total_valid_responses']}")
    print(f"Removed responses: {results['removed_responses']}")
    
results = analyze_movie_by_gambling(df)
print_analysis_results(results)