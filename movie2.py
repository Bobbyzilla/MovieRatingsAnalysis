import pandas as pd
import numpy as np
import re
from scipy.stats import mannwhitneyu

# comparing central tendency - use MW. Do newer movies receive significantly higher or lower ratings?
# comparing overall distribution - use KS - Do we care about differences in shape, spread, etc?

## SIGNIFICANCE TEST USED: Mann Whitney U Test
## WHY? 
# Movie ratings are ordinal (non-categorical). 
# Comparing 2 groups
# Comparing medians rather than entire distributions - care more about central tendency

# define significance level
alpha = 0.005

# read data and store only movie ratings columns to df
df = pd.read_csv(r'/Users/becca/Documents/github/MovieRatingsAnalysis/Movie Replication Set.csv')
df = df.iloc[:,:400]
initial_rows = df.shape[1]

# remove rows where all movie ratings are missing
df.dropna(axis = 'index', how = 'all', inplace = True)
clean_rows = df.shape[1]
dropped_rows = initial_rows - clean_rows
print(f'Number of rows dropped: {dropped_rows}')

# need to extract release year from movie name
release_years = [int(re.search(r'\((\d{4})\)', col).group(1)) for col in df.columns]

# create dict of title and release year
title_year_dict = dict(zip(df.columns, release_years))

# calculate median release year
median_year = np.median(release_years)
median_year

# when categorizing median movies as old
old_titles = [col for col, year in title_year_dict.items() if year <= median_year]
new_titles = [col for col, year in title_year_dict.items() if year > median_year]

old_df = df[old_titles]
new_df = df[new_titles]

old_ratings = old_df.values.flatten()
old_ratings = old_ratings[~np.isnan(old_ratings)]
new_ratings = new_df.values.flatten()
new_Ratings = new_ratings[~np.isnan(new_ratings)]

statistic, pval = mannwhitneyu(
             old_ratings, new_ratings, 
             alternative = 'two-sided', # concerned with if the medians are different rather than greater than/less than
             method = 'auto', # default by the function
             nan_policy = 'omit', # omit NaNs when performing calculation
                        # option: 'propagate', if NaN is present in the row, the output for that row will be NaN
             )
print('Results when categorizing median movies as old: ')
print('Null hypothesis: There is no difference in median ratings between old movies and new movies.')
print(f'Test Statistic: {statistic:.4f}')
print(f'P-Value: {pval:.4f}')
print('Significant?', pval <= alpha)
print('Conclusion: pval < alpha, so the difference in median ratings is too large to be consistent with chance. We reject the null hypothesis.')
print(f'Old Movies Sample Size: {len(old_ratings)}')
print(f'New Movies Sample Size: {len(new_ratings)}')

# when categorizing median movies as new - MAY REMOVE
old_titles = [col for col, year in title_year_dict.items() if year < median_year]
new_titles = [col for col, year in title_year_dict.items() if year >= median_year]

old_df = df[old_titles]
new_df = df[new_titles]

old_ratings = old_df.values.flatten()
old_ratings = old_ratings[~np.isnan(old_ratings)]
new_ratings = new_df.values.flatten()
new_Ratings = new_ratings[~np.isnan(new_ratings)]

statistic, pval = mannwhitneyu(
             old_ratings, new_ratings, 
             alternative = 'two-sided', # concerned with if the medians are different rather than greater than/less than
             method = 'auto', # default by the function
             nan_policy = 'omit', # omit NaNs when performing calculation
                        # option: 'propagate', if NaN is present in the row, the output for that row will be NaN
             )
print('\nResults when categorizing median movies as new: ')
print(f'Test Statistic: {statistic:.4f}')
print(f'P-Value: {pval:.9f}')
print('Significant?', pval <= alpha)
print(f'Old Movies Sample Size: {len(old_ratings)}')
print(f'New Movies Sample Size: {len(new_ratings)}')