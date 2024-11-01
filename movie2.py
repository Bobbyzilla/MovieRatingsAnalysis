import pandas as pd
import numpy as np
import re
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt

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
print('max year:', max(release_years))
print('min', min(release_years))
year_set = set(release_years)
print(len(year_set))

# calculate median release year
median_year = np.median(release_years)
print(median_year)

# when categorizing median movies as new - MAY REMOVE
old_titles = [col for col, year in title_year_dict.items() if year < median_year]
print('Sample size of old titles: ', len(old_titles))
new_titles = [col for col, year in title_year_dict.items() if year >= median_year]
print('Sample size of new titles: ', len(new_titles))

old_df = df[old_titles]
new_df = df[new_titles]

old_ratings = old_df.values.flatten()
old_ratings = old_ratings[~np.isnan(old_ratings)]
new_ratings = new_df.values.flatten()
new_ratings = new_ratings[~np.isnan(new_ratings)]

statistic, pval = mannwhitneyu(
             old_ratings, new_ratings, 
            #  alternative = 'two-sided', # concerned with if the medians are different rather than greater than/less than
            #  method = 'auto', # default by the function
             nan_policy = 'omit', # omit NaNs when performing calculation
                        # option: 'propagate', if NaN is present in the row, the output for that row will be NaN
             )
print('\nResults when categorizing median movies as new: ')
print(f'Test Statistic: {statistic:.4f}')
print(f'P-Value: {pval}')
print('Significant?', pval <= alpha)
print('Median Rating for Old Movies: ', np.median(old_ratings))
print('Median Rating for New Movies: ', np.median(new_ratings))
print(f'Old Movies Sample Size: {len(old_ratings)}')
print(f'New Movies Sample Size: {len(new_ratings)}')

# box plot and histogram for MW test
# KDE for ks test

# count ratings to get distribution
old_ratings_counts = pd.Series(old_ratings).value_counts().sort_index()
new_ratings_counts = pd.Series(new_ratings).value_counts().sort_index()

# normalize the ratings
old_ratings_normalized = old_ratings_counts / len(old_ratings)
new_ratings_normalized = new_ratings_counts / len(new_ratings)

normalized_df = pd.DataFrame({
    'Old Movies': old_ratings_normalized,
    'New Movies': new_ratings_normalized
}).fillna(0)

# create a boxplot to visualize the difference in ordinal ratings
plt.figure()
normalized_df.plot(kind = 'bar', color = ['blue', 'orange'], width = 0.5)
plt.xlabel('Rating')
plt.ylabel('Proportion')
plt.title('Normalized Ratings Distribution: Old vs New Movies')
plt.legend(title = 'Movie Group')
plt.show()

# normalize the result
# add line that follows the shape of the bar

# large sample size means only need a very small difference to get significance - can detect smaller effects
# overlay the two distributions in a histogram
# three colors - pink, blue, orange etc
# boxplot assumes movie data is continuous
# plots for showing discrete distributions