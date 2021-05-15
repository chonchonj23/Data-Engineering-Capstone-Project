# Udacity data-engineering Capstone Project

#### Project Description

The purpose of this project is to create a simple analytcs database for the i94 immigation data. For example, it can be used to answer questions such as:
- Did GDP and/or population in foreign countries exert any impact on the number of immigrants entering US?
- Did the demographic profiles of the cities influence chosen destinations when immigrants came to US?


#### Data used in this project

I94 Immigration Data: This data comes from the US National Tourism and Trade Office. For more information, please visit below website:
https://www.trade.gov/national-travel-and-tourism-office
    
U.S. City Demographic Data: This data comes from OpenSoft. For more information, please visit below website:
https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data
    
World Bank GDP Data. We are able to use GDP figures in specific years for particular countries. For more information, please visit below website:
https://data.worldbank.org
    
World Bank Population Data. We are able to use population figures in specific years for particular countries. For more information, please visit below website:
https://data.worldbank.org
    

#### Key Steps

There are several key steps that will be performed:
- perform EDA on i94 immigration, GDP, Population, as well as US City Demographics data
- Decide which column not to be used based on missing value %
- load data into S3 (for simulating real life situations where most of the company's data are stored in data lake such as S3)
- perform prelim ETL steps using Spark (at Workspace), and see if it would take long time to load data from S3, as well as export output table to S3 (and it took long time to export output data compared with using Redshift)
- finally perform ETL directly using S3 and Redshift


#### Tools 

- Python (version 3.6.3)
- AWS S3
- AWS Redshift
- Apache Spark (version 2.4.3)


#### Data model

![title](https://chon-de-capstone.s3-us-west-2.amazonaws.com/Data_Model.png)



#### Python Programs

sql_functions.py - this code does all the hard works of ETL, such as dropping table, creating tables, loading data into tables, and table transformation.

etl.py - this code provides the logical code structure for execute the whole ETL pipeline, including data quality checks.

etl-unit-tests.py - this code is mainly for debugging purposes, and can help us isolate individual parts when we need to zoom into a specific part of the program.