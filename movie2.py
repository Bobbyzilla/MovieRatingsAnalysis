import pandas as pd
import numpy as np
import re

## SIGNIFICANCE TEST USED: Mann Whitney U Test
## WHY? 
# Movie ratings are ordinal (non-categorical). 
# Comparing 2 groups
# Comparing medians rather than entire distributions ("are they rated differently", not "are they from the same population")

# read data and store only movie ratings columns to df
df = pd.read_csv(r'/Users/becca/Documents/github/MovieRatingsAnalysis/Movie Replication Set.csv')
df = df.iloc[:,:400]
df

# # need to extract release year from movie name
# release_years = [int(re.search(r'\((\d{4})\)', col).group(1) for col in df.iloc[:,:400].columns)]

# # create dict of title and release year, then sort on year ascending
# title_year_dict = {col: extract_year(col)}