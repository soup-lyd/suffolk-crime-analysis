import pandas as pd
from pathlib import Path

# 1. Load all the monthly files into one table
files = Path("data/raw").glob("**/*street.csv")
df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
print("Rows loaded:", len(df))

# 2. Tidy column names (lowercase, underscores instead of spaces)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# 3. Drop the column that is completely empty
df = df.drop(columns=["context"])

# 4. Turn the month text (e.g. "2026-03") into a proper date
df["month"] = pd.to_datetime(df["month"], format="%Y-%m")

# 5. Check my theory: what crime types have no crime ID?
print("\nCrime types with no crime ID:")
print(df[df["crime_id"].isna()]["crime_type"].value_counts())

# 6. Remove duplicate crimes (only rows that HAVE a crime ID)
before = len(df)
is_duplicate = df["crime_id"].notna() & df.duplicated(subset="crime_id")
df = df[~is_duplicate]
print("\nDuplicates removed:", before - len(df))

# 7. Label the missing outcomes instead of leaving blanks
df["last_outcome_category"] = df["last_outcome_category"].fillna("No outcome recorded")

# 8. Data quality checks (the script stops with an error if these fail)
assert df["crime_type"].notna().all(), "Some rows have no crime type"
assert df["month"].notna().all(), "Some rows have no month"

# 9. Save the clean data
Path("data/clean").mkdir(parents=True, exist_ok=True)
df.to_csv("data/clean/crimes_clean.csv", index=False)
print("\nRows after cleaning:", len(df))