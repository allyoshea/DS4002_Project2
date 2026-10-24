
library(tidyverse)
library(patchwork)
library(scales)

# ---------- Load & clean ----------
df <- read.csv("data.csv")

BG  <- "#FAFAF7"
INK <- "#2B2B2B"

theme_set(
  theme_minimal(base_size = 12) +
    theme(plot.background  = element_rect(fill = BG, color = NA),
          panel.background = element_rect(fill = BG, color = NA),
          text             = element_text(color = INK),
          axis.text        = element_text(color = INK),
          plot.title       = element_text(face = "bold", size = 16, hjust = 0),
          plot.title.position = "plot")
)

# ---------- 1. Correlation heatmap ----------
vars <- setdiff(names(df), "Date")
cm   <- cor(df[vars], use = "pairwise.complete.obs")

corr_long <- as.data.frame(as.table(cm)) |>
  set_names(c("row", "col", "r")) |>
  mutate(row = factor(row, levels = rev(vars)),                     # first variable at the top
         col = factor(col, levels = vars)) |>
  filter(as.integer(factor(row, levels = vars)) >= as.integer(col)) # keep lower triangle only

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

ggsave("1_correlation_heatmap_R.png", p_corr, width = 9, height = 7, dpi = 200, bg = BG)

# ---------- 2. Calendar heatmap (year x month) ----------
calendar_panel <- function(col, title, palette, fmt) {
  d <- df |>
    transmute(Year  = factor(year(Date), levels = rev(sort(unique(year(Date))))),
              Month = month(Date, label = TRUE),
              v     = .data[[col]]) |>
    mutate(light_text = rescale(v) > 0.6,                           # white text on dark tiles
           label      = ifelse(is.na(v), "", sprintf(fmt, v)))
  
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

p_cal <- calendar_panel("Electricity.Price", "Electricity price (avg ¢/kWh)", "YlOrRd", "%.1f") /
  calendar_panel("Crude",             "Crude oil price ($/barrel)",   "YlGnBu", "%.0f") +
  plot_annotation(title = "Calendar view: when were prices high?",
                  theme = theme(plot.title = element_text(face = "bold", size = 18, color = INK),
                                plot.background = element_rect(fill = BG, color = NA)))

ggsave("2_calendar_heatmap_R.png", p_cal, width = 12, height = 11, dpi = 200, bg = BG)

# ---------- 3. YoY growth: electricity price & oil ----------
yoy <- df |>
  transmute(Date,
            Electricity.Price = (Electricity.Price / lag(Electricity.Price, 12) - 1) * 100,
            Crude               = (Crude / lag(Crude, 12) - 1) * 100) |>   # % change vs. same month last year
  pivot_longer(-Date, names_to = "series", values_to = "yoy") |>
  drop_na() |>
  mutate(fill_group = ifelse(yoy >= 0, series, "Decline"))

latest <- yoy |> group_by(series) |> slice_max(Date, n = 1) |> ungroup()

p_yoy <- ggplot(yoy, aes(Date, yoy, fill = fill_group)) +
  geom_col(width = 31) +                                              # ~one bar per month
  geom_hline(yintercept = 0, color = INK, linewidth = 0.4) +
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

ggsave("3_yoy_growth_R.png", p_yoy, width = 12, height = 8, dpi = 200, bg = BG)

message("done")

# run after the data-loading section of project2_charts.R

# 1. kWh over time: overall trend and any jumps
ggplot(df, aes(Date, Electricity.Price)) +
  geom_line(color = "#E8743B", linewidth = 0.9) +
  geom_smooth(se = FALSE, color = INK, linewidth = 0.6) +
  labs(title = "Avg kWh over time", x = NULL, y = "Avg kWh")

# 2. Distribution: skew and outliers
ggplot(df, aes(Electricity.Price)) +
  geom_histogram(bins = 25, fill = "#E8743B", color = BG) +
  labs(title = "Distribution of Avg kWh", x = "Avg kWh", y = "Months")

# 3. Seasonal pattern: month-by-month spread
ggplot(df, aes(month(Date, label = TRUE), Electricity.Price)) +
  geom_boxplot(fill = "#E8743B", alpha = 0.6) +
  labs(title = "Avg kWh by month", x = NULL, y = "Avg kWh")

# 4. Trend / seasonal / leftover split (only uses complete kWh months)
kwh_ts <- ts(na.omit(df$Electricity.Price), start = c(2015, 1), frequency = 12)
plot(stl(kwh_ts, s.window = "periodic"), main = "STL decomposition of Avg kWh")

# 5. Which series lead kWh, and by how many months
ccf(df$Crude, df$Electricity.Price, na.action = na.pass, lag.max = 12,
    main = "Crude vs. Avg kWh")

# run after the data-loading section of project2_charts.R

season <- df |>
  transmute(Year = year(Date), Month = month(Date, label = TRUE),
            kwh = Electricity.Price) |>
  drop_na() |>
  group_by(Year) |>
  filter(n() == 12) |>                      # full years only, so the yearly average is fair
  mutate(kwh_centered = kwh - mean(kwh)) |>
  ungroup()

ggplot(season, aes(Month, kwh_centered, group = Year, color = Year)) +
  geom_hline(yintercept = 0, color = INK, linewidth = 0.3) +
  geom_line(linewidth = 0.9, alpha = 0.85) +
  scale_color_viridis_c(option = "plasma", end = 0.9) +
  labs(title = "Seasonality in Avg kWh",
       subtitle = "Each line is one year, centered on that year's average",
       x = NULL, y = "Avg kWh vs. year average")

# run after the data-loading section of project2_charts.R

sub <- df |>
  transmute(Date, Year = year(Date), Month = month(Date, label = TRUE),
            kwh = Electricity.Price) |>
  drop_na() |>
  group_by(Month) |>
  mutate(month_avg = mean(kwh)) |>          # each month's own average across all years
  ungroup()

ggplot(sub, aes(Year, kwh)) +
  geom_line(color = "#E8743B", linewidth = 0.9) +
  geom_point(color = "#E8743B", size = 1.2) +
  geom_hline(aes(yintercept = month_avg), color = INK, linetype = "dashed", linewidth = 0.4) +
  facet_wrap(~ Month, nrow = 2) +
  scale_x_continuous(breaks = c(2016, 2020, 2024)) +
  labs(title = "Avg kWh by month, over time",
       subtitle = "Dashed line = that month's average across all years",
       x = NULL, y = "Avg kWh")

# run after the data-loading section of project2_charts.R

rng_k <- range(df$Electricity.Price, na.rm = TRUE)
rng_c <- range(df$Crude, na.rm = TRUE)
a <- diff(rng_k) / diff(rng_c)          # rescale crude onto the kWh range
b <- rng_k[1] - rng_c[1] * a

ggplot(df, aes(Date)) +
  geom_line(aes(y = Crude * a + b, color = "Crude oil ($/barrel)"), linewidth = 0.8) +
  geom_line(aes(y = Electricity.Price, color = "Avg kWh"), linewidth = 1.1, na.rm = TRUE) +
  scale_y_continuous(name = "Avg kWh",
                     sec.axis = sec_axis(~ (. - b) / a, name = "Crude oil ($/barrel)")) +
  scale_color_manual(values = c("Avg kWh" = "#E8743B", "Crude oil ($/barrel)" = "#2E6F95"),
                     name = NULL) +
  labs(title = "Avg kWh vs. crude oil", x = NULL) +
  theme(legend.position = "top",
        axis.title.y.left  = element_text(color = "#E8743B", face = "bold"),
        axis.title.y.right = element_text(color = "#2E6F95", face = "bold"))

