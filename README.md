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
- scikit-learn 1.4.2
- matplotlib 3.8.4
See `requirements.txt` for the complete list of required packages.

### Map of the Documentation

The repository is organized as follows:
```text
DS4002_Project2/
│
├── LICENSE
├── README.md
├── data 
├── output
├── requirements.txt
└── scripts
```
**Folder and File Descriptions**

- `data/` — Contains the predictor data, residential electricity data, and combined dataset. 
- `output/` — Contains the figures generated during exploratory data analysis and analysis plots after model training. 
- `scripts/` — Contains the Python scripts used to build the model, analyze the results, and visualize the data.
- `requirements.txt` — Lists the Python packages required to reproduce the analysis.
- `README.md` — Provides an overview of the project and instructions for reproducing  the results.
- `data/README.md` - Provides metadata information such as data summary, provenance, ethical statement, data dictionary. 
- `LICENSE` — Contains the project's license.

### Instructions for Reproducing the Results

The following steps describe how to download the project, set up the Python environment, collect the article data, run the sentiment analyses, and generate the final figures.

1. Go to the GitHub repository and copy the HTTPS URL by clicking the <Code> button:

```text
https://github.com/allyoshea/DS4002_Project2.git
```

2. Open the **Terminal application on your laptop**. This is the regular computer terminal, not the terminal inside your coding platform.

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

6. Open the `DS4002_Project2` folder in your preferred coding platform, such as Visual Studio Code.

#### Step 2: Set Up the Python Environment

1. Once the project is open in your coding platform, open the **integrated terminal inside the coding platform**. In Visual Studio Code, select **Terminal → New Terminal on top bar of computer normally**.

2. Confirm that the terminal is located in the `DS4002_Project2` folder. If needed, navigate to the folder:

```bash
cd ~/Desktop/DS4002_Project2
```
3. Create a Python virtual environment:

```bash
python -m venv .venv
```
4. Activate the virtual environment:

```bash
source .venv/bin/Activate
```

5. Install the required packages:

```bash
pip install numpy pandas matplotlib statsmodels
```

#### Step 4: Run SARIMAX analysis 

To run the model (found in the scripts folder), run this command.
```bash
python sarimax_price_model.py data.csv --cv
```

This produces:

- `data/sentiment_results.csv`
- `data/sentence_sentiment_results.csv`
#### Step 5: Generate Analysis Plots

Run:

```bash
python scripts/03_eda_sciBert.py
```

This generates the following figures in the `output/` folder:

- `sentiment_composition_stacked.png`
- `positive_pct_by_type.png`
- `negative_pct_by_type.png`
- `neutral_pct_by_type.png`

#### Step 6: Run VADER Sentiment Analysis

Run:

```bash
python scripts/04_sentiment_vader.py
```

This produces:

- `data/vader_sentiment_data.csv`



#### Step 7: Generate VADER Figures

Run:

```bash
python scripts/05_eda_vader.py
```

This generates the following figures in the `output/` folder:

- `vader_sentiment_composition_stacked.png`
- `vader_compound_by_article.png`
- `vader_mean_compound_by_type.png`
- 
#### Step 8: Analyze Article Length

Run:

```bash
python scripts/06_article_length_analysis.py
```

This produces:

- `data/article_length_results.csv`
- `output/article_length_comparison.png`

#### Step 9: Review the Results

After running the scripts, the processed datasets will be located in the `data/` folder and the generated figures will be located in the `output/` folder.

The project contains monthly residential electricity data from January 2015 - August 2026 and the following 9 predictors from the same months:

- Data center spending
- Crude oil prices
- Inflation Rate
- Power plant generation
- Retail sales
- Average Temperature
- Natural Gas Price (Henry Hub)
- Heating degree days
- Cooling degree days

The resulting datasets and figures can be used to compare baseline seasonal prediction of residential electricity data versus model accuracy using the predictors as well. 

### Project Workflow

```text
Clone GitHub Repository
        ↓
Open Project in VS Code
        ↓
Create and Activate Virtual Environment
        ↓
Install Required Packages
        ↓
Scrape Articles
        ↓
articles.csv + article text files
        ↓
Run SciBERT Sentiment Analysis
        ↓
SciBERT Results
        ↓
Run SciBERT EDA
        ↓
Run VADER Sentiment Analysis
        ↓
VADER Results
        ↓
Run VADER EDA
        ↓
Analyze Article Length
        ↓
Figures saved in output/
        ↓
Review and Compare Results
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
