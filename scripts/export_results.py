import sqlite3
import pandas as pd
from pathlib import Path

Path("dashboard").mkdir(exist_ok=True)
conn = sqlite3.connect("crime.db")

queries = {
    "crime_types": """
        SELECT crime_type, COUNT(*) AS total
        FROM crimes GROUP BY crime_type ORDER BY total DESC""",
    "crimes_by_month": """
        SELECT month, COUNT(*) AS total
        FROM crimes GROUP BY month ORDER BY month""",
    "top_locations": """
        SELECT location, COUNT(*) AS total
        FROM crimes GROUP BY location ORDER BY total DESC LIMIT 10""",
}

for name, sql in queries.items():
    pd.read_sql_query(sql, conn).to_csv(f"dashboard/{name}.csv", index=False)
    print("Saved", name)

conn.close()