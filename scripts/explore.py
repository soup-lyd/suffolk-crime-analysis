import pandas as pd            # the library for working with tables of data
from pathlib import Path       # helps find files in folders

# Find every CSV with "street" in its name inside data/raw
files = Path("data/raw").glob("**/*street.csv")

# Read each file and stack them into one big table
df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

print(df.shape)          # (number of rows, number of columns)
df.info()                # column names and data types
print(df.head())         # first 5 rows
print(df.isna().sum())   # how many missing values in each column