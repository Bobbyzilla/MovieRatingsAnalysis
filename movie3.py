import pandas as pd
import numpy as np
import re
from scipy.stats import mannwhitneyu

# # comparing central tendency - use MW. Do newer movies receive significantly higher or lower ratings?
# comparing overall distribution - use KS - Do we care about differences in shape, spread, etc?

## SIGNIFICANCE TEST USED: Mann Whitney U Test
## WHY? 
# Movie ratings are ordinal (non-categorical)
# Comparing 2 groups
# Comparing medians rather than entire distribution - care more about central tendency

# define significance level
alpha = 0.005

# read data
df = pd.read_csv(r'/Users/becca/Documents/github/MovieRatingsAnalysis/Movie Replication Set.csv')
df = df[['Shrek (2001)', 'Gender identity (1 = female; 2 = male; 3 = self-described)']]
df.rename(columns = {'Gender identity (1 = female; 2 = male; 3 = self-described)' : 'genderidentity'}, inplace = True)

# separate female and male ratings and drop NaNs
female_ratings = df[df['genderidentity'] == 1]['Shrek (2001)'].dropna()
male_ratings = df[df['genderidentity'] == 2]['Shrek (2001)'].dropna()

statistic, pval = mannwhitneyu(female_ratings, male_ratings,
                               alternative = 'two-sided', #default
                               method = 'auto', #default,
                               nan_policy = 'raise' #NaNs should have already been removed
)

print('Results for Shrek (2001) Ratings, Female vs Male: ')
print('Null hypothesis: There is no difference in median ratings of Shrek (2001) ratings between female and male viewers.')
print(f'Test Statistic: {statistic:.4f}')
print(f'P-Value: {pval:.4f}')
print('Significant?', pval <= alpha)
print('Conclusion: pval > alpha, so we "decide not to drop the null hypothesis". The result is consistent with chance.')
print(f'Female Ratings Sample Size: {len(female_ratings)}')
print(f'Male Ratings Sample Size: {len(male_ratings)}')

# OPTIONAL: Kruskal-Wallis test for 3 groups (female, male, self-described)
from scipy.stats import kruskal
sd_ratings = df[df['genderidentity'] == 3]['Shrek (2001)'].dropna()

statistic, pval = kruskal(female_ratings, male_ratings, sd_ratings)
print('\nResults for Shrek (2001) Ratings, Female vs Male vs Self-Described Gender: ')
print(f'Test Statistic: {statistic:.4f}')
print(f'P-Value: {pval:.4f}')
print('Significant?', pval <= alpha)
print(f'Female Ratings Sample Size: {len(female_ratings)}')
print(f'Male Ratings Sample Size: {len(male_ratings)}')
print(f'Self-Described Gender Ratings Sample Size: {len(sd_ratings)}') # sample size way too small?