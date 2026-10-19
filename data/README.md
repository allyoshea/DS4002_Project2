# Metadata 
## Data Summary 
Our dataset consists of a response variable column, residential home electricity prices per kWh
in the United States, and 9 predictor variable columns, including data such as power plant
generation in kWh, inflation rate (CPI-U), and natural gas price in USD. Each row of the dataset
represents one month from January 2015 to August 2026. This data was manually sourced from
the EIA and NOAA, government sources with publicly available data. CSV files were combined
into one dataset. The original CSV files and associated analysis materials will be available in our
Github here.
## Provenance 
The dataset was collected between October 11th and October 14th, 2026, by three University of
Virginia students (Carter Grohe, Coco Zhao, and Ally O'Shea) for their Data science project (aka
Prototyping) DS 4002 class. Sources and data were manually collected and compiled into one
dataset. EDA was conducted on this dataset, which will be publicly available in our GitHub
repository.
## Ethical Statements 
The dataset consists of publicly available government data and does not
have private information. However, original article content remains subject to the rights and
policies of the original publishers. 
## License 
The text used in this project was obtained from third party publications and remains
subject to the original copyright and licensing terms of the publishers. We do not claim
ownership of the original content. The code, metadata, and analysis are original project materials
shared through the GitHub repository above. The data is therefore still subject to copyright as by
original authors.
## Data dictionary 
| Variable | Description | Data Type | Uncertainty |
|---|---|---|---|
| `article_id` | Identifier assigned to the article during scraping | Integer | IDs reused across scraping batches – not unique identifiers |
| `article_type` | Category identifying whether the article is from a scientific publication or news/media | Categorical | Assigned by project team |
| `source` | Publication or website where the article was found | Categorical/Text | May vary across webpages (i.e. some include www. before) |
| `date` | Publication date of the article | Date | N/A |
| `title` | Title of the article | Text | N/A |
| `author` | Listed author(s) of the article | Text | N/A |
| `url` | Original webpage URL for the article (provided as input) | Text | N/A |
| `description` | Short description or summary associated with the article | Text | May vary based on what publisher includes |
| `text_file` | Path to the locally stored text file | Text | File may not be captured perfectly because of web scraping |
| `retrieved_at` | Date & time when the article was collected | Date/Time | N/A |
| `negative` | Average VADER negative sentiment score across sentences in the article | Numeric | VADER may not interpret scientific/technical language perfectly |
| `neutral` | Average VADER neutral sentiment score across sentences in the article | Numeric | VADER may not interpret scientific/technical language perfectly |
| `positive` | Average VADER positive sentiment score across sentences in the article | Numeric | VADER may not interpret scientific/technical language perfectly |
| `compound` | Average VADER compound sentiment score across sentences in the article; ranges from -1 to +1 | Numeric | VADER is a general-purpose sentiment tool and may not fully capture sentiment in scientific/technical writing |
| `positive_pct` | Proportion of sentences classified as positive by SciBERT | Numeric | SciBERT classifications may not perfectly capture sentiment in scientific/technical language |
| `negative_pct` | Proportion of sentences classified as negative by SciBERT | Numeric | SciBERT classifications may not perfectly capture sentiment in scientific/technical language |
| `neutral_pct` | Proportion of sentences classified as neutral by SciBERT | Numeric | SciBERT classifications may not perfectly capture sentiment in scientific/technical language |
| `overall_sentiment` | Sentiment category with the largest proportion of sentences classified by SciBERT | Categorical | Depends on the model's sentence-level classifications |
| `sentences` | Number of sentences analyzed in the article | Integer | N/A |
## Exploratory plots
