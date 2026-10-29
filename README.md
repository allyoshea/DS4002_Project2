# DS4002_Project2
Potential for Action

This repository contains the process for developing and running a SARIMAX model with chosen predictors to predict monthly residential electricity price changes from the years 2015-2026. 
## Contents of the Repository
### Software and Platform

- **IDE**: Visual Studio Code (VS Code)
- **OS**: Windows 11 or Mac OS 15.1.1 (Sequoia)
- **Terminal**: VS Code Integrated Terminal or Windows PowerShell
- **Programming Language**: Python
- **Version Control / Repository**: GitHub
  
#### Add-On Packages and Libraries

The project uses the following Python packages:
- pandas 2.2.2
- matplotlib 3.8.4
- numpy 1.26.4
- statsmodels 0.14.4
See `requirements.txt` for the complete list of required packages.

Required R packages (readxl, dplyr, purrr, tidywork, patchwork, and scales) are automatically installed if needed when 01_PowerPlantGenerationCalculation.R and 02_eda.R is run. Package versions will just be most recent upon installement. 

### Map of the Documentation

The repository is organized as follows:
```text
DS4002_Project2/
├── LICENSE
├── README.md
├── data
│   ├── CPIAUCSL.csv
│   ├── Coolingdegree.txt
│   ├── ElectricityPrice.csv
│   ├── HeatingDegree.txt
│   ├── NaturalGasPrice_HenryHub.xls
│   ├── README.md
│   ├── Temperature.csv
│   ├── data.csv
│   ├── generation_monthly.xlsx
│   ├── monthly-spending-data-center-us (1)
│   │   ├── monthly-spending-data-center-us.csv
│   │   ├── monthly-spending-data-center-us.metadata.json
│   │   └── readme.md
│   └── us_monthly.csv
├── output
│   ├── 1_correlation_heatmap_R.png
│   ├── 2_calendar_heatmap_R.png
│   ├── 3_yoy_growth_R.png
│   ├── accuracy_vs_goal.png
│   ├── coefficients.png
│   ├── electricity_prices_by_month.png
│   ├── electricity_prices_over_time.png
│   ├── forecast_sarima_12mo.csv
│   ├── forecast_sarimax.csv
│   ├── forecast_sarimax.png
│   ├── holdout.png
│   ├── holdout_results.csv
│   ├── vif_check.png
│   └── vif_table.csv
├── requirements.txt
└── scripts
    ├── 01_PowerPlantGenerationCalculation.R
    ├── 02_VIF.py
    ├── 02_eda.R
    ├── 02_eda.py
    └── 03_sarimax_model_final.py
```
**Folder and File Descriptions**

### Folder and File Descriptions

- `data/` — Contains the raw datasets and combined dataset used to analyze and predict monthly residential electricity prices.
    - `README.md`: Documents the datasets, their sources, and their uses.
    - `CPIAUCSL.csv`: Contains Consumer Price Index data.
    - `Coolingdegree.txt`: Contains cooling degree day data.
    - `ElectricityPrice.csv`: Contains monthly U.S. residential electricity price data.
    - `HeatingDegree.txt`: Contains heating degree day data.
    - `NaturalGasPrice_HenryHub.xls`: Contains Henry Hub natural gas price data.
    - `Temperature.csv`: Contains temperature data used in the analysis.
    - `data.csv`: Contains the combined monthly dataset used for exploratory analysis and forecasting.
    - `generation_monthly.xlsx`: Contains electricity generation data used to calculate monthly U.S. totals.
    - `us_monthly.csv`: Contains processed monthly U.S. electricity generation data.
    - `monthly-spending-data-center-us (1)/`: Contains the data center spending dataset and its documentation.
      - `monthly-spending-data-center-us.csv`: Contains monthly data center spending observations.
      - `monthly-spending-data-center-us.metadata.json`: Contains metadata for the spending dataset.
    - `README.md`: Provides additional documentation for the spending dataset.

- `output/` — Contains figures generated during exploratory data analysis and model evaluation.
    - `1_correlation_heatmap_R.png`: Visualizes correlations among the analyzed variables.
    - `2_calendar_heatmap_R.png`: Visualizes calendar patterns in electricity prices.
    - `3_yoy_growth_R.png`: Displays year-over-year growth patterns.
    - `accuracy_vs_goal.png`: Compares forecasting accuracy with the project goal.
    - `coefficients.png`: Visualizes model coefficients.
    - `electricity_prices_by_month.png`: Displays electricity prices by month.
    - `electricity_prices_over_time.png`: Shows electricity prices over time.
    - `forecast_sarima_12mo.csv`: Stores the 12-month SARIMA forecast.
    - `forecast_sarimax.csv`: Stores SARIMAX forecast results.
    - `forecast_sarimax.png`: Visualizes the SARIMAX forecast.
    - `holdout.png`: Visualizes model performance on the holdout period.
    - `holdout_results.csv`: Stores model evaluation results for the holdout period.
    - `vif_check.png`: Displays the VIF analysis.
    - `vif_table.csv`: Stores the calculated VIF values.
- `scripts/` — Contains the scripts used to prepare data, conduct exploratory analysis, and fit and evaluate the SARIMAX model.
    - `01_PowerPlantGenerationCalculation.R`: Processes electricity generation data and calculates monthly U.S. totals.
    - `02_VIF.py`: Calculates variance inflation factors (VIF) to assess multicollinearity among predictors.
    - `02_eda.R`: Performs exploratory data analysis in R and generates visualizations.
    - `02_eda.py`: Performs exploratory data analysis in Python.
    - `03_sarimax_model_final.py`: Fits and evaluates SARIMA and SARIMAX forecasting models.

- `requirements.txt` — Lists the Python packages and versions needed to run the analysis.
- `README.md` — Provides an overview of the project, its organization, software requirements, and instructions for reproducing the analysis.
- `LICENSE` — Specifies the terms under which the project's code and other covered materials may be used, modified, and distributed.
### Instructions for Reproducing the Results

The following steps describe how to download the project, set up the Python environment, prepare the data, run the exploratory data analysis, and generate the model results.

#### Step 1: Download the Repository

1. Navigate to the GitHub repository and click the green **Code** button. Copy the HTTPS URL:

   ```text
   https://github.com/allyoshea/DS4002_Project2.git
   ```

2. Open the Terminal application on your computer.

3. Navigate to the location where you want to save the project, such as your Desktop:

   ```bash
   cd ~/Desktop
   ```

4. Clone the repository:

   ```bash
   git clone https://github.com/allyoshea/DS4002_Project2.git
   ```

5. Navigate into the project folder:

   ```bash
   cd DS4002_Project2
   ```

6. Open the `DS4002_Project2` folder in Visual Studio Code or another compatible coding environment.

#### Step 2: Set Up the Python Environment

The project uses Python for exploratory data analysis, SARIMAX modeling, and visualization. R is used to process the power plant generation data.

1. In Visual Studio Code, select **Terminal → New Terminal** from the top menu.

2. Confirm that the terminal is located in the `DS4002_Project2` directory.
#### Step 2: Set Up the Python and R Environments

The project uses Python for exploratory data analysis, SARIMAX modeling, and visualization. R is used to process power plant generation data and perform additional exploratory data analysis. Both languages can be run from the integrated terminal in Visual Studio Code.

**Python setup**

1. In Visual Studio Code, select **Terminal → New Terminal** from the top menu.
2. Confirm that the terminal is located in the `DS4002_Project2` directory.
3. Create a Python virtual environment:

   ```bash
   python3 -m venv .venv
   ```

4. Activate the virtual environment on macOS:

   ```bash
   source .venv/bin/activate
   ```

   On Windows PowerShell, use:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

5. Install the required Python packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

**R setup**

R must be installed separately on your computer. You do not need to create a separate R environment to run this project. You can run R and Python scripts from the same VS Code terminal, even while the Python virtual environment is activated.

The R scripts require the packages `readxl`, `dplyr`, and `purrr`. To install these packages, open an R console and run:

```r
install.packages(c("readxl", "dplyr", "purrr"))
```

After installing R and the required packages, you can run R scripts from the VS Code terminal using `Rscript`, just as you run Python scripts using `python`. For example:

```bash
Rscript scripts/01_PowerPlantGenerationCalculation.R
```

Make sure the terminal is open in the `DS4002_Project2` project directory before running the scripts.
6. To run the power plant generation processing script, ensure that R is installed. The script uses the R packages `readxl`, `dplyr`, and `purrr`.

#### Step 3: Prepare the Data and Run Exploratory Data Analysis

The `data/` directory contains the source datasets and the combined dataset used for modeling.

The R script `01_PowerPlantGenerationCalculation.R` processes monthly power plant generation data from the source Excel workbook, combines the relevant annual worksheets, standardizes the variables, and aggregates electricity generation by year and month. The script is expected to produce `data/us_monthly.csv`.

If the required source workbook is available in the `data/` directory, run the script using:

```bash
Rscript scripts/01_PowerPlantGenerationCalculation.R
```

The combined dataset, `data/data.csv`, contains the residential electricity price data and selected predictor variables used by the SARIMAX model.

To run the exploratory data analysis script, execute:

```bash
python scripts/02_eda.py
Rscript scripts/02_eda.R
```

This generates the following figures in the `output/` directory:

- `output/electricity_prices_by_month.png`
- `output/electricity_prices_over_time.png`

#### Step 4: Run the SARIMAX Model

The SARIMAX modeling script is located in the `scripts/` directory. To run the model, execute:

```bash
python scripts/03_sarimax_price_model.py
```

If cross-validation is enabled using the `--cv` command-line argument, run:

```bash
python scripts/03_sarimax_price_model.py --cv
```

The script fits the SARIMAX model using the combined dataset and generates forecast and diagnostic figures in the `output/` directory.

Expected outputs include:

- `output/forecast_2.png`
- `output/diagnostics.png`

If cross-validation is run and configured to save its results, the corresponding results file will also be saved in the `output/` directory.

#### Step 5: Review the Results

After running the scripts, the processed datasets will be located in the `data/` directory, and the generated figures will be located in the `output/` directory.

The intended analysis covers monthly U.S. residential electricity prices from January 2015 through June 2026, depending on the observations available in the combined dataset. 
The analysis considers the following nine potential predictors:

- Data center spending
- Crude oil prices
- Inflation rate
- Power plant generation
- Retail sales
- Average temperature
- Natural gas prices (Henry Hub)
- Heating degree days
- Cooling degree days

The resulting datasets, forecast plots, and diagnostic figures can be used to evaluate electricity price trends, seasonal patterns, and the potential contribution of external predictors to forecast accuracy.

### Project Workflow

```text
Clone GitHub Repository
        ↓
Open Project in VS Code
        ↓
Create and Activate Python and R Environments
        ↓
Install Required Packages
        ↓
Verify the Combined Dataset
        ↓
Run Exploratory Data Analysis
        ↓
Run SARIMAX Model and Evaluation
        ↓
Review Forecasts and Diagnostic Figures
```
```
## References 
[1] U.S. Energy Information Administration, “Table 9.8 Average prices of electricity to ultimate
customers,” Monthly Energy Review. [Online]. Available:
https://www.eia.gov/totalenergy/data/browser/index.php?tbl=T09.08#/?f=M&start=200001
(accessed Oct. 16, 2026).
[2] Our World in Data, “Monthly spending on data center construction in the United States”
(data from U.S. Census Bureau and U.S. Bureau of Labor Statistics). [Online]. Available:
https://ourworldindata.org/grapher/monthly-spending-data-center-us (accessed Oct. 16, 2026).
[3] U.S. Energy Information Administration, “Europe Brent spot price FOB (dollars per barrel),”
Petroleum & Other Liquids. [Online]. Available:
https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RBRTE&f=M (accessed Oct.
16, 2026).
[4] U.S. Bureau of Labor Statistics, “Consumer price index historical tables for U.S. city
average,” Mid-Atlantic Information Office. [Online]. Available:
https://www.bls.gov/regions/mid-atlantic/data/consumerpriceindexhistorical_us_table.htm
(accessed Oct. 16, 2026).
[5] NOAA National Centers for Environmental Information, “Climate at a glance: Statewide
time series.” [Online]. Available: https://www.ncei.noaa.gov/access/monitoring/climate-at-a-
glance/statewide/time-series (accessed Oct. 16, 2026).
[6] U.S. Energy Information Administration, “Henry Hub natural gas spot price (dollars per
million Btu),” Natural Gas. [Online]. Available:
https://www.eia.gov/dnav/ng/hist/rngwhhdm.htm (accessed Oct. 16, 2026).
[7] NOAA National Centers for Environmental Information, “Climate at a glance: National time
series.” [Online]. Available: https://www.ncei.noaa.gov/access/monitoring/climate-at-a-
glance/national/time-series (accessed Oct. 16, 2026).
[8] U.S. Energy Information Administration, “Table 1.12 Cooling degree-days by Census
division,” Monthly Energy Review. [Online]. Available:
https://www.eia.gov/totalenergy/data/browser/index.php?tbl=T01.12#/?f=M (accessed Oct. 16,
2026).
[9] U.S. Energy Information Administration, “Table 1.11 Heating degree-days by Census
division,” Monthly Energy Review. [Online]. Available:
https://www.eia.gov/totalenergy/data/browser/index.php?tbl=T01.11#/?f=M (accessed Oct. 16,
2026)
