import pandas as pd
import numpy as np
import re
from scipy.stats import mannwhitneyu

## SIGNIFICANCE TEST USED: Mann Whitney U Test
## WHY? 
# Movie ratings are ordinal (non-categorical)
# Comparing 2 groups
# Comparing medians rather than entire distribution - care more about central tendency

# define significance level
alpha = 0.005

# read data
df = pd.read_csv(r'/Users/becca/Documents/github/MovieRatingsAnalysis/Movie Replication Set.csv')
df.rename(columns = {'Gender identity (1 = female; 2 = male; 3 = self-described)' : 'genderidentity'}, inplace = True)

female_df = df[df['genderidentity'] == 1].iloc[:, :400]
male_df = df[df['genderidentity'] == 2].iloc[:, :400]

significant_count = 0
movie_count = 0

for movie in female_df.columns:
    female_rating = female_df[movie].dropna()
    male_rating = male_df[movie].dropna()
    
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

# which kinds of movies are rated significantly differently?
