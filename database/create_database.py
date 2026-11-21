
import sqlite3
import pandas as pd
from pathlib import Path

# Project paths
project_dir = Path(__file__).resolve().parent.parent
csv_path = project_dir / "data" / "procurement_data.csv"
db_path = project_dir / "database" / "procurement.db"

# Read procurement data
df = pd.read_csv(csv_path)

# Connect to SQLite database
with sqlite3.connect(db_path) as conn:
    # Create table and load data
    df.to_sql(
        "procurement",
        conn,
        if_exists="replace",
        index=False
    )

    # Verify records
    result = pd.read_sql_query(
        "SELECT COUNT(*) AS total_records FROM procurement",
        conn
    )

print("SQLite database created successfully!")
print("Total records:", result["total_records"][0])
print("Database saved to:", db_path)
