
# Script: 02_eda.R
# Purpose:
# The purpose of this script is to create exploratory plots from the collected data.csv. This script gives us
# plots to better understand the correlation between predictors as well as trends in the response over time.
#
# Process:
# 1. Install and load the required packages.
# 2. Load the dataset and set up the plot theme.
# 3. Create a correlation heatmap to compare relationships between variables.
# 4. Create calendar heatmaps to visualize monthly electricity and crude oil prices.
# 5. Create year-over-year growth plots to compare changes in electricity and crude oil prices.
# 6. Save the plots to the output folder.
#
# Input:
#     data/data.csv
# Output:
#     output/1_correlation_heatmap_R.png
#     output/2_calendar_heatmap_R.png
#     output/3_yoy_growth_R.png

# Install any required packages that are not already installed.
packages <- c("tidyverse", "patchwork", "scales")

new_packages <- packages[!(packages %in% installed.packages()[, "Package"])]

if (length(new_packages) > 0) {
  install.packages(new_packages, repos = "https://cloud.r-project.org")
}
# Load the required packages.
library(tidyverse)
library(patchwork)
library(scales)


# Load the dataset containing electricity prices and predictor variables.
df <- read.csv("data/data.csv") %>%
  mutate(Date = as.Date(Date))


# Set background and text colors for the plots.
BG  <- "#FAFAF7"
INK <- "#2B2B2B"

# Set a consistent theme to use across all plots.
theme_set(
  theme_minimal(base_size = 12) +
    theme(plot.background  = element_rect(fill = BG, color = NA),
          panel.background = element_rect(fill = BG, color = NA),
          text             = element_text(color = INK),
          axis.text        = element_text(color = INK),
          plot.title       = element_text(face = "bold", size = 16, hjust = 0),
          plot.title.position = "plot")
)


# 1. Correlation heatmap
# Exclude the Date column and calculate correlations between variables.
vars <- setdiff(names(df), "Date")
cm   <- cor(df[vars], use = "pairwise.complete.obs")

# Convert the correlation matrix into a data frame for plotting.
# Set the variable order and keep only the lower triangle to avoid duplicate correlations.
corr_long <- as.data.frame(as.table(cm)) |>
  set_names(c("row", "col", "r")) |>
  mutate(row = factor(row, levels = rev(vars)),
         col = factor(col, levels = vars)) |>
  filter(as.integer(factor(row, levels = vars)) >= as.integer(col))

# Create a heatmap with correlation values displayed in each tile.
p_corr <- ggplot(corr_long, aes(col, row, fill = r)) +
  geom_tile(color = BG, linewidth = 1.5) +
  geom_text(aes(label = sprintf("%.2f", r), color = abs(r) > 0.5),
            fontface = "bold", size = 3.6) +
  scale_color_manual(values = c(`TRUE` = "white", `FALSE` = INK), guide = "none") +
  scale_fill_distiller(palette = "RdBu", direction = -1, limits = c(-1, 1),
                       name = "Correlation") +
  coord_fixed() +
  labs(title = "Are our variables correlated?", x = NULL, y = NULL) +
  theme(panel.grid  = element_blank(),
        axis.text.x = element_text(angle = 35, hjust = 1))

# Save the correlation heatmap to the output folder.
ggsave("output/1_correlation_heatmap_R.png", p_corr, width = 9, height = 7, dpi = 200, bg = BG)


# 2. Calendar heatmaps
# Create a function to plot monthly values across years for a selected variable.
calendar_panel <- function(col, title, palette, fmt) {

  # Prepare the year, month, and variable values for the calendar heatmap.
  d <- df |>
    transmute(Year  = factor(year(Date), levels = rev(sort(unique(year(Date))))),
              Month = month(Date, label = TRUE),
              v     = .data[[col]]) |>
    mutate(light_text = rescale(v) > 0.6,
           label      = ifelse(is.na(v), "", sprintf(fmt, v)))

  # Plot each year as a row and each month as a column.
  # Tile colors represent values, and labels display the monthly values.
  ggplot(d, aes(Month, Year, fill = v)) +
    geom_tile(color = BG, linewidth = 1.5) +
    geom_text(aes(label = label, color = light_text), size = 2.8) +
    scale_color_manual(values = c(`TRUE` = "white", `FALSE` = INK), guide = "none") +
    scale_fill_distiller(palette = palette, direction = 1, na.value = BG, guide = "none") +
    scale_x_discrete(position = "top") +
    labs(title = title, x = NULL, y = NULL) +
    theme(panel.grid = element_blank(),
          plot.title = element_text(size = 13))
}

# Create calendar heatmaps for electricity and crude oil prices.
# Combine both plots vertically and add an overall title.
p_cal <- calendar_panel("Electricity.Price", "Electricity price (avg ¢/kWh)", "YlOrRd", "%.1f") /
  calendar_panel("Crude",             "Crude oil price ($/barrel)",   "YlGnBu", "%.0f") +
  plot_annotation(title = "Calendar view: when were prices high?",
                  theme = theme(plot.title = element_text(face = "bold", size = 18, color = INK),
                                plot.background = element_rect(fill = BG, color = NA)))

# Save the combined calendar heatmaps.
ggsave("output/2_calendar_heatmap_R.png", p_cal, width = 12, height = 11, dpi = 200, bg = BG)


# 3. Year-over-year growth
# Calculate the percentage change from the same month in the previous year.
# A 12-month lag is used because the data are monthly.
yoy <- df |>
  transmute(Date,
            Electricity.Price = (Electricity.Price / lag(Electricity.Price, 12) - 1) * 100,
            Crude               = (Crude / lag(Crude, 12) - 1) * 100) |>
  # Reshape the data so electricity and crude oil growth can be plotted together.
  pivot_longer(-Date, names_to = "series", values_to = "yoy") |>
  drop_na() |>
  # Use a separate fill group to show negative growth as a decline.
  mutate(fill_group = ifelse(yoy >= 0, series, "Decline"))

# Find the latest available year-over-year growth value for each variable.
latest <- yoy |> group_by(series) |> slice_max(Date, n = 1) |> ungroup()

# Create bar charts showing year-over-year growth for electricity and crude oil.
p_yoy <- ggplot(yoy, aes(Date, yoy, fill = fill_group)) +
  geom_col(width = 31) +
  geom_hline(yintercept = 0, color = INK, linewidth = 0.4) +
  # Label the latest growth value in each panel.
  geom_text(data = latest, aes(label = sprintf("latest: %+.1f%%", yoy)),
            inherit.aes = FALSE, x = latest$Date, y = latest$yoy,
            hjust = 1, vjust = -0.6, nudge_x = -100, fontface = "bold", color = INK) +
  scale_fill_manual(values = c(Electricity.Price = "#E8743B",
                               Crude               = "#2E6F95",
                               Decline             = "#9AA5B1"),
                    guide = "none") +
  scale_y_continuous(labels = label_number(suffix = "%")) +
  facet_wrap(~ series, ncol = 1, scales = "free_y") +
  labs(title = "Year-over-year change: electricity price vs. crude oil",
       subtitle = "color = growth   |   grey = decline", x = NULL, y = NULL) +
  theme(panel.grid.minor   = element_blank(),
        panel.grid.major.x = element_blank(),
        strip.text         = element_text(face = "bold", size = 13, hjust = 0, color = INK),
        plot.subtitle      = element_text(color = "#666666"))

# Save the year-over-year growth plots.
ggsave("output/3_yoy_growth_R.png", p_yoy, width = 12, height = 8, dpi = 200, bg = BG)


# Print a message when the script finishes running.
message("done")
