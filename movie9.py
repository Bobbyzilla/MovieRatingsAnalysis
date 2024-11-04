# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:02:57 2024

@author: zhaoez
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

df = pd.read_csv('movieReplicationSet.csv')

def analyze_movie_distributions(data, movie1='Home Alone (1990)', movie2='Finding Nemo (2003)', alpha=0.005):
    df = data.copy()
    
    # ratings for each moving, remove empty cells element wise
    movie1_ratings = df[movie1].dropna()
    movie2_ratings = df[movie2].dropna()
    #print(movie1_ratings)
    # ks test
    statistic, p_value = stats.ks_2samp(movie1_ratings, movie2_ratings)

    fig, ax = plt.subplots(figsize=(10, 6))
    ratings = np.arange(0, 4.5, 0.5)
    movie1_counts = movie1_ratings.value_counts(normalize=True).reindex(ratings, fill_value=0)
    movie2_counts = movie2_ratings.value_counts(normalize=True).reindex(ratings, fill_value=0)
    
    ax.bar(ratings - 0.1, movie1_counts, width=0.2, label=movie1)
    ax.bar(ratings + 0.1, movie2_counts, width=0.2, label=movie2)
    ax.set_title('normalized rating distributions for Home Alone and Finding Nemo')
    ax.set_xlabel('rating')
    ax.set_ylabel('proportion')
    ax.legend()
    plt.show()
    
    results = {
        'test_used': "Kolmogorov-Smirnov test",
        'test_statistic': statistic,
        'p_value': p_value,
        'significant': p_value <= alpha,
        'movie1_n': len(movie1_ratings),
        'movie1_median': movie1_ratings.median(),
        'movie2_median': movie2_ratings.median(),
        'movie2_n': len(movie2_ratings),
        'total_valid_responses': len(movie1_ratings) + len(movie2_ratings),
        'removed_responses': (len(data) - len(movie1_ratings)) + (len(data) - len(movie2_ratings))
    }
    return results

def print_analysis_results(results):
    print(f"{results['test_used']}")
    print(f"p-value: {results['p_value']}")
    print(f"significance at α = 0.005: {results['significant']}")
    print("-" * 50)
    print("Home Alone (1990):")
    print(f"  sample size: {results['movie1_n']}")
    print(f"  median: {results['movie1_median']}")
    print("Finding Nemo (2003):")
    print(f"  sample size: {results['movie2_n']}")
    print(f"  median: {results['movie2_median']}")
    print("-" * 50)
    print(f"Valid responses: {results['total_valid_responses']}")
    print(f"Removed responses: {results['removed_responses']}")

results = analyze_movie_distributions(df)
print_analysis_results(results)