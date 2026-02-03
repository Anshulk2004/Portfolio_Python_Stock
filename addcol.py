import pandas as pd

FILE = "Holdings_Portfolio_Data.csv"

df = pd.read_csv(FILE)

df["acquired_date"] = None
df["quantity"] = None
df["total_invested"] = None
df["user_id"] = 1

df.to_csv(FILE, index=False)

print("Columns added successfully")
