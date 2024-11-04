# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 13:38:08 2024

@author: zhaoez
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

df = pd.read_csv('movieReplicationSet.csv')

def analyze_movie_by_only_child(data, movie_col='The Lion King (1994)', only_child_col='Are you an only child? (1: Yes; 0: No; -1: Did not respond)', alpha=0.005):
    df = data.copy()
    
    # remove rows with -1 (did not respond) from only child column
    df = df[df[only_child_col].isin([0, 1])]
    
    # removes rows with missing movie ratings (nan)
    df = df.dropna(subset=[movie_col])
    
    # seperate ratings based on only child response
    only_child_ratings = df[df[only_child_col] == 1][movie_col]
    sibling_ratings = df[df[only_child_col] == 0][movie_col]
    
    # mann-whitney u test
    statistic, p_value = stats.mannwhitneyu(only_child_ratings, sibling_ratings, alternative='greater')
    print(f"U statistic: {statistic}")
    
    fig, ax = plt.subplots()
    ratings = np.arange(0, 4.5, 0.5)
    only_child_counts = only_child_ratings.value_counts().reindex(ratings)
    sibling_counts = sibling_ratings.value_counts().reindex(ratings)
    ax.set_xticks(ratings)
    ax.set_xticklabels(ratings)
    ax.set_title('unormalized distribution of ratings for The Lion King')
    ax.set_xlabel('rating')
    ax.set_ylabel('count')
    ax.bar(ratings - 0.1, only_child_counts, width=0.2, label='Only Child')
    ax.bar(ratings + 0.1, sibling_counts, width=0.2, label='Has Siblings')
    ax.legend()
    
    fig, ax = plt.subplots()
    only_child_counts = only_child_ratings.value_counts(normalize=True).reindex(ratings)
    sibling_counts = sibling_ratings.value_counts(normalize=True).reindex(ratings)
    ax.bar(ratings - 0.1, only_child_counts, width=0.2, label='Only Child')
    ax.bar(ratings + 0.1, sibling_counts, width=0.2, label='Has Siblings')
    ax.set_xticks(ratings)
    ax.set_xticklabels(ratings)
    ax.set_title('normalized distribution of ratings for The Lion King')
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
        'only_child_median': only_child_ratings.median(),
        'sibling_median': sibling_ratings.median(),
        'only_child_n': len(only_child_ratings),
        'sibling_n': len(sibling_ratings),
        'total_valid_responses': len(only_child_ratings) + len(sibling_ratings),
        'removed_responses': len(data) - (len(only_child_ratings) + len(sibling_ratings))
    }
    
    return results

def print_analysis_results(results):
    print(f"{results['test_used']}")
    print(f"p-value: {results['p_value']:.4f}")
    print(f"significant at α = 0.005: {results['significant']}")
    print("-" * 50)
    print("only child:")
    print(f"  sample size: {results['only_child_n']}")
    print(f"  median: {results['only_child_median']}")
    print("has sibling:")
    print(f"  sample size: {results['sibling_n']}")
    print(f"  median: {results['sibling_median']}")
    print("-" * 50)
    print(f"Valid responses: {results['total_valid_responses']}")
    print(f"Removed responses: {results['removed_responses']}")
    
results = analyze_movie_by_only_child(df)
print_analysis_results(results)