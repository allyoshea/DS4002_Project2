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
The time series data used in this project was obtained from third party publications and remains
subject to the original copyright and licensing terms of the publishers. We do not claim
ownership of the original content. The code, metadata, and analysis are original project materials
shared through the GitHub repository above. The data is therefore still subject to copyright as by
original authors.
## Data dictionary 
| Variable | Description | Data Type | Uncertainty |
|---|---|---|---|
| `KWh_price` | Average monthly residential electricity price in $/kWh | Numeric (response) | National average may conceal regional price differences |
| `Data Center Spending` | Monthly spending on the construction and maintenance of data centers in the US | Numeric (predictor) | Increases sharply in recent months |
| `Crude Oil Prices` | Average crude oil (Brent) price | Numeric (predictor) | Crude oil prices may not directly reflect electricity generation costs |
| `Inflation Rate` | Increase in the CPI-U (inflation) rate | Numeric (predictor) | CPI-U reflects broad consumer prices, not electricity-specific inflation |
| `Power Plant Generation (total net)` | Total net amount of electricity generated in the US per month (supply) | Numeric (predictor) | National generation totals may conceal regional supply differences |
| `Retail Sales` | Amount of electricity supplied to users | Numeric (predictor) | The definition of "users" may be unclear or vary by data source |
| `Average Temperature` | Average temperature in the US | Numeric (predictor) | National averages conceal local differences |
| `Natural Gas Price (Henry Hub)` | Average natural gas price at Henry Hub | Numeric (predictor) | Henry Hub prices may not reflect regional natural gas prices or the costs faced by all electricity generators |
| `Heating-degree days[1]` | Sum of temperature degrees below 65°F over a given period | Numeric (predictor) | A national total may conceal regional heating demand |
| `Cooling-degree days[1]` | Sum of temperature degrees above 65°F over a given period | Numeric (predictor) | A national total may conceal regional cooling demand |
## Exploratory plots
<img width="291" height="133" alt="image" src="https://github.com/user-attachments/assets/fdd7b785-f09a-452f-8592-11e03f045e88" />

<img width="300" height="163" alt="image" src="https://github.com/user-attachments/assets/d0077345-6b4a-48cf-9736-9a782d64ea81" />



