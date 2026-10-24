"""
Script: 02_eda.py
#
# Purpose:
#     Clean monthly U.S. residential electricity price data and
#     generate exploratory plots to examine long-term price trends
#     and seasonal differences in electricity prices.
#
# Input:
#     data/ElectricityPrice.csv
#
# Outputs:
#     output/electricity_prices_by_month.png, a bar chart showing
#     the average electricity price for each calendar month.
#     output/electricity_prices_over_time.png, a line chart showing
#     monthly U.S. residential electricity prices from 2000 to 2026.
#
# Process:
#     1. Import pandas for data processing and matplotlib for plotting.
#     2. Read the electricity price data from ElectricityPrice.csv.
#     3. Convert electricity price values to numeric format.
#     4. Convert YYYYMM values into dates.
#     5. Restrict the dataset to observations from 2000 through 2026
#        and remove rows with missing dates or price values.
#     6. Sort the observations chronologically.
#     7. Calculate the average electricity price for each calendar month.
#     8. Generate and save a bar chart of average prices by month.
#     9. Generate and save a line chart of electricity prices over time.
#
# Notes:
#     Run this script from the project root directory.
#     The output/ directory must exist before running the script.
#     The monthly averages combine observations across years and
#     are used to explore seasonal patterns in electricity prices.

"""
# Import pandas for data manipulation and matplotlib for plotting.
import pandas as pd
import matplotlib.pyplot as plt


# Load the original electricity price dataset.
df = pd.read_csv("data/ElectricityPrice.csv")


# Convert electricity price values to numeric format.
# Values that cannot be converted are replaced with missing values.
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

# Convert the YYYYMM column into dates using the year and month.
# Invalid date values are converted to missing values.
df["Date"] = pd.to_datetime(
    df["YYYYMM"].astype(str),
    format="%Y%m",
    errors="coerce"
)


# Keep observations from January 2000 through December 2026.
# Remove rows with missing dates or electricity price values.
df = df[
    (df["Date"] >= "2000-01-01") &
    (df["Date"] < "2027-01-01")
].dropna(subset=["Date", "Value"])


# Sort observations chronologically to make the time series easier
# to interpret and plot.
df = df.sort_values("Date")


# Extract the calendar month from each date.
# This allows prices from the same month across different years
# to be grouped together for seasonal analysis.
df["Month"] = df["Date"].dt.month

# Calculate the average electricity price for each calendar month
# across all included years.
monthly_avg = df.groupby("Month")["Value"].mean()


# Create a bar chart comparing average electricity prices by month.
plt.figure(figsize=(9, 5))
monthly_avg.plot(kind="bar")

# Label the axes and add a descriptive title.
plt.xlabel("Month")
plt.ylabel("Average Electricity Price (cents/kWh)")
plt.title("Average U.S. Residential Electricity Price by Month")

# Replace numeric month values with abbreviated month names.
plt.xticks(
    range(12),
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    rotation=0
)

# Adjust the layout and save the chart to the output directory.
plt.tight_layout()
plt.savefig("output/electricity_prices_by_month.png", dpi=300)

# Display the chart.
plt.show()


# Create a line chart showing how electricity prices change over time.
plt.figure(figsize=(11, 5))
plt.plot(df["Date"], df["Value"])

# Label the axes and add a descriptive title.
plt.xlabel("Date")
plt.ylabel("Electricity Price (cents/kWh)")
plt.title("Monthly U.S. Residential Electricity Prices, 2000–2026")

# Adjust the layout and save the chart to the output directory.
plt.tight_layout()
plt.savefig("output/electricity_prices_over_time.png", dpi=300)

# Display the chart.
plt.show()
