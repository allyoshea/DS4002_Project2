import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/ElectricityPrice.csv")

# Clean the data
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
df["Date"] = pd.to_datetime(
    df["YYYYMM"].astype(str),
    format="%Y%m",
    errors="coerce"
)

# Restrict to 2000–2026
df = df[
    (df["Date"] >= "2000-01-01") &
    (df["Date"] < "2027-01-01")
].dropna(subset=["Date", "Value"])

df = df.sort_values("Date")
 # Average electricity price by calendar month
df["Month"] = df["Date"].dt.month

monthly_avg = df.groupby("Month")["Value"].mean()

plt.figure(figsize=(9, 5))
monthly_avg.plot(kind="bar")
plt.xlabel("Month")
plt.ylabel("Average Electricity Price (cents/kWh)")
plt.title("Average U.S. Residential Electricity Price by Month")
plt.xticks(
    range(12),
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    rotation=0
)
plt.tight_layout()
plt.savefig("electricity_prices_by_month.png", dpi=300)
plt.show()

# Plot electricity prices
plt.figure(figsize=(11, 5))
plt.plot(df["Date"], df["Value"])
plt.xlabel("Date")
plt.ylabel("Electricity Price (cents/kWh)")
plt.title("Monthly U.S. Residential Electricity Prices, 2000–2026")
plt.tight_layout()
plt.show()