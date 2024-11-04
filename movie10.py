# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 13:41:15 2024

@author: zhaoez
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

df = pd.read_csv('movieReplicationSet.csv')

franchises = ['Star Wars', 'Harry Potter', 'The Matrix', 'Indiana Jones', 
              'Jurassic Park', 'Pirates of the Caribbean', 'Toy Story', 'Batman']

# get the columns of the franchise movies
def get_franchise_movies(df, franchise_keyword):
    franchise_movies = []
    for col in df.columns:
        if franchise_keyword in col:
            franchise_movies.append(col)
    return franchise_movies

# calc signifigance for each of the franchise movies
def analyze_franchise(df, franchise_movies, franchise_name, alpha=0.005): 
    # get ratings for each movie, dropping NaN element wise
    ratings_by_movie = []
    for movie in franchise_movies:
        ratings = df[movie].dropna()
        ratings_by_movie.append(ratings)
    # perform kw test
    h_statistic, p_value = stats.kruskal(*ratings_by_movie)
    
    movie_stats = []
    for movie, ratings in zip(franchise_movies, ratings_by_movie):
        rating_counts = ratings.value_counts(normalize=True).sort_index()
        movie_stats.append({
            'movie': movie,
            'normalized_counts': rating_counts,
            'median': ratings.median(),
            'n': len(ratings)
        })
    
    results = {
        'franchise': franchise_name,
        'movies': franchise_movies,
        'movie_stats': movie_stats,
        'h_statistic': h_statistic,
        'p_value': p_value,
        'significant': p_value <= alpha,
        'n_movies': len(franchise_movies)
    }
    
    return results

def print_franchise_results(results):
    print(f"\n{results['franchise']} inconsistent quality analysis")
    print("-" * 50)
    print(f"number of movies: {results['n_movies']}")
    print(f"kw h statistic: {results['h_statistic']:.4f}")
    print(f"p-value: {results['p_value']}")
    print(f"significance at α = 0.005: {results['significant']}")
    print("\nmovie stat:")
    for stat in results['movie_stats']:
        print(f"\n{stat['movie']}:")
        print(f"  median: {stat['median']:.2f}")
        print(f"  sample size: {stat['n']}")

def plot_franchise_barcharts(df, franchise_results):
    fig, ax = plt.subplots(figsize=(15, 6))
    
    # Plot normalized bar charts for each movie's rating distribution
    for i, movie_stats in enumerate(franchise_results['movie_stats']):
        normalized_counts = movie_stats['normalized_counts'].reindex(np.arange(0.5, 4.5, 0.5))
        ax.bar(
            normalized_counts.index + i * 0.1,
            normalized_counts.values,
            width=0.1,
            label=movie_stats['movie'].split('(')[0].strip()
        )
    
    ax.set_title(f"{franchise_results['franchise']} franchise ratings normalized")
    ax.set_xlabel('rating')
    ax.set_ylabel('proportion')
    ax.legend()
    plt.xticks(np.arange(0.5, 4.5, 0.5))
    plt.show()

franchise_results = []
for franchise in franchises:
    franchise_movies = get_franchise_movies(df, franchise)
    results = analyze_franchise(df, franchise_movies, franchise)
    franchise_results.append(results)
    print_franchise_results(results)
    plot_franchise_barcharts(df, results)
print(f"\nnumber of inconsistent franchises: {sum(1 for result in franchise_results if result['p_value'] <= 0.005)}")