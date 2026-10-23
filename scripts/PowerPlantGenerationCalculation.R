
# Source - https://stackoverflow.com/a/12945838
# Posted by Jeromy Anglim, modified by community. See post 'Timeline' for change history
# Retrieved 2026-10-23, License - CC BY-SA 3.0

library(readxl)    
read_excel_allsheets <- function(filename, tibble = FALSE) {
  sheets <- readxl::excel_sheets(filename)
  x <- lapply(sheets, function(X) readxl::read_excel(filename, sheet = X))
  if(!tibble) x <- lapply(x, as.data.frame)
  names(x) <- sheets
  x
}

generation <- read_excel_allsheets("generation_monthly.xlsx")

gen2020 <- generation$`2020_Final`

keep <- c(paste0(2015:2025, "_Final"), "2026_Preliminary")

gen <- generation[keep] %>%
  map(~ {
    df <- as.data.frame(.x)[, 1:6]
    names(df) <- c("year", "month", "state", "producer", "source", "mwh")
    df
  }) %>%
  bind_rows() %>%
  mutate(year  = suppressWarnings(as.numeric(year)),
         month = suppressWarnings(as.numeric(month)),
         mwh   = suppressWarnings(as.numeric(mwh))) %>%
  filter(!is.na(year))          # drops title/header rows if the sheets were read without skip = 4

us_monthly <- gen %>%
  filter(producer == "Total Electric Power Industry",
         source   == "Total",
         state    != "US-Total") %>%
  group_by(year, month) %>%
  summarise(total_mwh = sum(mwh), .groups = "drop") %>%
  arrange(year, month)

us_monthly
