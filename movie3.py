import pandas as pd
import numpy as np
import re
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt

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

# count ratings to get distribution
female_ratings_counts = pd.Series(female_ratings).value_counts().sort_index()
male_ratings_counts = pd.Series(male_ratings).value_counts().sort_index()

# normalize the ratings
female_ratings_normalized = female_ratings_counts / len(female_ratings)
male_ratings_normalized = male_ratings_counts / len(male_ratings)

normalized_df = pd.DataFrame({
    'Female Viewers': female_ratings_normalized,
    'Male Viewers': male_ratings_normalized
}).fillna(0)

# create a barplot to visualize the difference in ordinal ratings
plt.figure()
normalized_df.plot(kind = 'bar', color = ['blue', 'orange'], width = 0.5)
plt.xlabel('Ratings')
plt.ylabel('Proportion')
plt.title('Normalized Ratings Distribution for \'Shrek (2001)\': Female vs Male Viewers')
plt.legend(title = 'Movie Group')
plt.show()