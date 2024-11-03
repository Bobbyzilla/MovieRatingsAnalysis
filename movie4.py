import pandas as pd
import numpy as np
import re
from scipy.stats import mannwhitneyu

# define significance level
alpha = 0.005

# read data
df = pd.read_csv(r'/Users/becca/Documents/github/MovieRatingsAnalysis/Movie Replication Set.csv')
df.rename(columns = {'Gender identity (1 = female; 2 = male; 3 = self-described)' : 'genderidentity'}, inplace = True)

female_df = df[df['genderidentity'] == 1].iloc[:, :400]
male_df = df[df['genderidentity'] == 2].iloc[:, :400]

significant_count = 0
movie_count = 0
small_female_count = 0
small_male_count = 0
below_20_male_count = 0

for movie in female_df.columns:
    female_rating = female_df[movie].dropna()
    male_rating = male_df[movie].dropna()
    if len(male_rating) <= 8:
        print(f'Sample Size of {movie} too small. Female group size: {len(female_rating)}')
        print(f'Male group size: {len(male_rating)}')
        small_male_count += 1            
    
    statistic, pval = mannwhitneyu(female_rating, male_rating)
    if pval < alpha:
        significant_count += 1
    movie_count += 1


proportion_signif = significant_count / movie_count

print('Results for Proportion of Movies Rated Differently Between Female and Male: ')
print('Null hypothesis: NEED NULL HYPOTHESIS')
print(f'Proportion Rated Differently: {(proportion_signif * 100):.2f}%')
print('Conclusion: NEED CONCLUSION')
print(f'Female Ratings Sample Size: {len(female_df)}')
print(f'Male Ratings Sample Size: {len(male_df)}')
print('Number of movies with insufficient female ratings: ', small_female_count)
print('Number of movies with insufficient male ratings: ', small_male_count)
print('Number of movies with male ratings < 20: ', below_20_male_count)