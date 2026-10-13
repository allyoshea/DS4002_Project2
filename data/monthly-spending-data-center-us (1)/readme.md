# Monthly spending on data center construction in the United States - Data package

This data package contains the data that powers the chart ["Monthly spending on data center construction in the United States"](https://ourworldindata.org/grapher/monthly-spending-data-center-us?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website. It was downloaded on October 13, 2026.

### Active Filters

A filtered subset of the full data was downloaded. The following filters were applied:

## CSV structure

Each row is an observation for an entity (usually a country or region) at a timepoint.

- "Entity" — the name of the entity, e.g. "United States".
- "Code" — our internal entity code. For most countries this is the [ISO alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) code, e.g. "USA"; historical and other non-standard entities get a custom code.
- "Year" or "Day" — the timepoint. Annual data has a "Year" column holding an integer year; otherwise a "Day" column holds a date string in the form "YYYY-MM-DD".
- The final column is the data column — the time series that powers the chart. Downloaded with the "full data" option it corresponds to the time series below; with "only selected data visible in the chart" it is transformed depending on the chart type, so the correspondence may be less direct.


## Metadata.json structure

The .metadata.json file contains metadata about the data package. The "charts" key contains information to recreate the chart, like the title, subtitle etc. The "columns" key contains information about each of the columns in the csv, like the unit, timespan covered, citation for the data etc.

## How we process data at Our World in Data

Our World in Data is almost never the original producer of the data - almost all of the data we use has been compiled by others. If you want to re-use data, it is your responsibility to ensure that you adhere to the sources' license and to credit them correctly. Please note that a single time series may have more than one source - e.g. when we stitch together data from different time periods by different producers or when we calculate per capita metrics using population data from a second source.

Preparing this data involves several processing steps. Depending on the data, this can include standardizing country names and world region definitions, converting units, calculating derived indicators such as per capita measures, as well as adding or adapting metadata such as the name or the description given to an indicator.
[Read about our data pipeline](https://docs.owid.io/projects/etl/).

## Detailed information about the data


### Monthly spending on data center construction in the United States – US Census Bureau
This only includes work done on-site to construct data center buildings each month, including materials and construction labor. It excludes the cost of IT hardware inside the buildings, like servers and storage, which can account for a large share of total investment. This data is expressed in US dollars, adjusted for inflation. Only private construction is included.
Last updated: October 2, 2026  
Next expected update: December 2026  
Unit: constant 2021 US$  
Source: United States Census Bureau (2026); U.S. Bureau of Labor Statistics (2026) – with major processing by Our World in Data  

#### How to cite this data

United States Census Bureau (2026); U.S. Bureau of Labor Statistics (2026) – with major processing by Our World in Data

#### What you should know about this data
- This indicator shows monthly spending on the physical construction of data center buildings in the United States. It represents the actual value of work done at construction sites each month, including materials, labor, and contractor costs.
- This data doesn't include maintenance work, land purchases, or the computer equipment that goes inside data centers (like servers and storage systems). This means it captures only a small part of total data center investment, since IT hardware represents a significant additional cost.
- Only privately-owned construction projects are counted. Projects owned by federal, state, or local governments are not included.
- Data centers power a wide range of online services beyond AI, such as streaming services and cloud storage.
- The values shown are not seasonally adjusted, meaning they reflect actual monthly spending and typical seasonal patterns, including slower winter construction and busier summer periods.
- Recent months are preliminary and are revised as more complete reports arrive. Once a year, the Census Bureau also revises the previous two years of data, and these annual revisions can be substantial.
- This indicator is adjusted for inflation using a composite price index that equally weights the producer price indexes (PPIs) for new industrial building and new warehouse building construction — the approach the US Bureau of Economic Analysis adopted for data center construction in its [2025 annual update](https://apps.bea.gov/scb/issues/2025/11-november/1125-nea-annual-update.htm).

#### Notes on our processing step for this indicator
We adjusted for inflation using a composite price index that equally weights the US Bureau of Labor Statistics' producer price indexes (PPIs) for new industrial building and new warehouse building construction, each rebased so that its 2021 annual average = 100. This follows the approach the US Bureau of Economic Analysis adopted for data center construction in its [2025 annual update](https://apps.bea.gov/scb/issues/2025/11-november/1125-nea-annual-update.htm).


## Sources

These are the sources behind the data in this package. Each time series above names the ones it draws on in its citation.

### United States Census Bureau – Value of Private Construction Put in Place

Monthly construction spending data for private construction in the United States, broken down by construction type.
The dataset includes datacenter construction spending measured as not seasonally adjusted monthly values in millions of dollars.

Estimates for private nonresidential categories such as data centers and offices come from the Construction Progress
Reporting Survey (CPRS), in which owners of sampled construction projects (drawn from Dodge Data & Analytics project
lists) report the value of work done each month until completion. Estimates include materials, labor, architectural
and engineering costs, overhead, interest and taxes paid during construction, and contractor's profits.

Producer: United States Census Bureau  
Published: 2026-10-01  
Retrieved on: 2026-10-02  
Retrieved from: https://www.census.gov/construction/c30/historical_data.html  
Direct download: https://www.census.gov/construction/c30/xlsx/privtime.xlsx  
License: Public Domain  

Citation: U.S. Census Bureau, Value of Construction Put in Place Survey (VIP), Private Construction Spending Time Series

### U.S. Bureau of Labor Statistics – US PPI New Nonresidential Building Construction

Producer price indexes (PPIs) for new nonresidential building construction in the United States, covering new office, new warehouse, and new industrial building construction.

BLS uses a method in which building models are developed and specified to represent the buildings being constructed in the marketplace. Multiple models were developed for each building type to accommodate variations in building design. The building models are described as a series of unique production elements or "assemblies" in BLS terminology. Each building assembly represents a building construction activity that can be fully defined as a unique portion of the total project. Each assembly is made up of unit-price components that define the specific type and quantity of materials, labor, and equipment necessary for the assembly's installation.

A professional cost-estimating firm developed the building models under BLS direction. To achieve an output price, BLS combines the detailed material and installation (labor and related equipment) cost data, which are updated quarterly by the cost-estimating firm, with margin (overhead and profit) data collected monthly by BLS directly from building construction contractors. BLS aggregates output price changes captured at the assembly level each month to represent the changes in output prices for the total structure. Therefore, the BLS output indexes attempt to measure changes in the input costs for these structures, along with changes in contractor markups.

Producer: U.S. Bureau of Labor Statistics  
Published: 2026  
Retrieved on: 2026-10-02  
Retrieved from: https://www.bls.gov/ppi/factsheets/producer-price-index-data-for-nonresidential-building-construction-sector-new-office-building-construction-naics-236223.htm  
License: Public domain (https://www.bls.gov/opub/copyright-information.htm)  

Citation: U.S. Bureau of Labor Statistics

    