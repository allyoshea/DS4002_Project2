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
- `scripts/` — Contains the Python scripts used to analyze, build the model, and visualize the data.
- `requirements.txt` — Lists the Python packages required to reproduce the analysis.
- `README.md` — Provides an overview of the project and instructions for reproducing  the results.
- `data/README.md` - Provides metadata information such as data summary, provenance, ethical statement, data dictionary
- `LICENSE` — Contains the project's license.

### Instructions for Reproducing the Results

The following steps describe how to download the project, set up the Python environment, collect the article data, run the sentiment analyses, and generate the final figures.

1. Go to the GitHub repository and copy the HTTPS URL by clicking the <Code> button:

```text
https://github.com/allyoshea/DS4002_Project.git
```

2. Open the **Terminal application on your laptop**. This is the regular computer terminal, not the terminal inside your coding platform.

3. Navigate to the location where you want to save the project, such as your Desktop:

```bash
cd ~/Desktop
```

4. Clone the repository:

```bash
git clone https://github.com/allyoshea/DS4002_Project.git
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
pip install -r requirements.txt
```

#### Step 3: Collect the Predictor 

The repository already contains the collected predictor data (data.csv) , so rerunning the combination of the data is optional to obtain the existing results.

The article URLs are stored in `data/urls.txt`.

To combine the established again, run the following command in the **coding platform's integrated terminal**:

```bash
python scripts/01_scraper.py
```

This script reads the URLs from `data/urls.txt` and saves the article metadata, article text files, and any scraping errors. This will take awhile and to avoid any issues with potential firewalls reference the data/articles folder with the already scraped .txt files. 

#### Step 4: Run SARIMAX analysis 

In the **coding platform's integrated terminal**, run:

```bash
python scripts/02_sentiment.py
```

This produces:

- `data/sentiment_results.csv`
- `data/sentence_sentiment_results.csv`
#### Step 5: Generate SciBERT Figures

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

The project contains 60 BCI-related articles:

- 30 scientific articles
- 30 news/media articles

The resulting datasets and figures can be used to compare sentiment patterns and article length between the two article types.

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
[1] What Are Word Embeddings? | IBM.” Accessed: Sep. 10, 2026. [Online]. Available:
https://www.ibm.com/think/topics/word-embeddings
[2] “Welcome to VaderSentiment’s documentation! — VaderSentiment 3.3.1 documentation.”
Accessed: Sep. 16, 2026. [Online]. Available: https://vadersentiment.readthedocs.io/en/latest/
