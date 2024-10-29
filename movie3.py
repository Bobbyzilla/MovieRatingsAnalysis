import pandas as pd
import numpy as np
import re

## SIGNIFICANCE TEST USED: 
## WHY? 

# define significance level
alpha = 0.005

# read data
df = pd.read_csv(r'/Users/becca/Documents/github/MovieRatingsAnalysis/Movie Replication Set.csv')