import pandas as pd
import sqlite3

# 1. Read the clean data
df = pd.read_csv("data/clean/crimes_clean.csv", parse_dates=["month"])

# 2. Store the month as simple text like "2026-03" (easier to query in SQL)
df["month"] = df["month"].dt.strftime("%Y-%m")

# 3. Create the database file and load the table
conn = sqlite3.connect("crime.db")
df.to_sql("crimes", conn, if_exists="replace", index=False)

# 4. Check it worked
count = conn.execute("SELECT COUNT(*) FROM crimes").fetchone()[0]
print("Rows in database:", count)
conn.close()