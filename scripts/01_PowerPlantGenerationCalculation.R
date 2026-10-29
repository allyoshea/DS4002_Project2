
# Script: 01_PowerPlantGenerationCalculation.R
#
# Purpose:
#     Process monthly U.S. electricity generation data to create
#     a cleaned dataset for use as a predictor in the SARIMAX
#     model of residential electricity prices.
#
# Input:
#     data/generation_monthly.xlsx
#
# Output:
#     data/us_monthly.csv, a cleaned dataset containing total
#     monthly electricity generation in megawatt-hours.
#
# Process:
#     1. Install required R packages if they are not already installed.
#     2. Load the readxl, dplyr, and purrr packages.
#     3. Read all worksheets from generation_monthly.xlsx.
#     4. Select the finalized annual worksheets from 2015 through
#        2025 and the preliminary 2026 worksheet.
#     5. Standardize column names across the selected worksheets.
#     6. Combine the worksheets into a single dataset.
#     7. Convert year, month, and generation values to numeric
#        formats and remove rows without valid years.
#     8. Filter for total electricity generation across reporting
#        states, excluding the national aggregate row.
#     9. Group records by year and month and sum generation
#        across states.
#    10. Sort the resulting dataset chronologically.
#    11. Export the cleaned dataset to data/us_monthly.csv.
#
# Notes:
#     Run this script from the project root directory.
#     The data/ directory and input workbook must exist before
#     running the script.
#     The exported CSV can be used when preparing the combined
#     dataset for the SARIMAX model.


# Install required packages if they are not already installed.
# readxl imports Excel files, dplyr handles data cleaning, and
# purrr applies functions across the workbook's worksheets.
packages <- c("readxl", "dplyr", "purrr")

# Identify which required packages are not currently installed.
new_packages <- packages[
  !packages %in% installed.packages()[, "Package"]
]

# Install any missing packages before loading them.
if (length(new_packages) > 0) {
  install.packages(new_packages, repos = "https://cloud.r-project.org")
}

# Load the packages needed to import and process the data.
library(readxl)
library(dplyr)
library(purrr)


# Source - https://stackoverflow.com/a/12945838
# Posted by Jeromy Anglim, modified by community.
# Retrieved 2026-10-23, License - CC BY-SA 3.0

# Define a function to read every worksheet in an Excel workbook.
# Each worksheet is returned as a separate data frame, with its
# worksheet name retained for later selection.
read_excel_allsheets <- function(filename, tibble = FALSE) {
  sheets <- readxl::excel_sheets(filename)

  # Import each worksheet and optionally convert it to a data frame.
  x <- lapply(sheets, function(X) readxl::read_excel(filename, sheet = X))

  if (!tibble) {
    x <- lapply(x, as.data.frame)
  }

  # Name each imported data frame after its original worksheet.
  names(x) <- sheets
  x
}


# Import all worksheets from the monthly electricity generation workbook.
generation <- read_excel_allsheets("data/generation_monthly.xlsx")


# Select finalized annual data for 2015–2025 and preliminary data for
# 2026. The worksheet names must match those in the Excel workbook.
keep <- c(paste0(2015:2025, "_Final"), "2026_Preliminary")


# Process the selected worksheets individually before combining them.
gen <- generation[keep] %>%
  map(~ {
    # Keep the six columns needed for the analysis.
    df <- as.data.frame(.x)[, 1:6]

    # Apply consistent names so the same operations work across years.
    names(df) <- c("year", "month", "state", "producer", "source", "mwh")
    df
  }) %>%

  # Combine the annual worksheets into one dataset.
  bind_rows() %>%

  # Convert the year, month, and generation values to numeric.
  # Suppress warnings for text values that cannot be converted.
  mutate(
    year = suppressWarnings(as.numeric(year)),
    month = suppressWarnings(as.numeric(month)),
    mwh = suppressWarnings(as.numeric(mwh))
  ) %>%

  # Remove title or header rows that do not contain a valid year.
  filter(!is.na(year))


# Keep records representing total electricity generation from all
# reporting states. Exclude the national aggregate to avoid counting
# it alongside the individual state totals.
us_monthly <- gen %>%
  filter(
    producer == "Total Electric Power Industry",
    source == "Total",
    state != "US-Total"
  ) %>%

  # Sum generation across states for each year and month.
  group_by(year, month) %>%
  summarise(total_mwh = sum(mwh), .groups = "drop") %>%

  # Arrange the output in chronological order.
  arrange(year, month)


# Export the cleaned monthly dataset as a CSV file so it can be
# used by other scripts or incorporated into the modeling dataset.
write.csv(
  us_monthly,
  "data/us_monthly.csv",
  row.names = FALSE
)
