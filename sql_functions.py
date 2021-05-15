Drop_table_sql= ("""
DROP TABLE IF EXISTS {}
""")


staging_fact_create= ("""
CREATE TABLE IF NOT EXISTS staging_fact (
    cicid float,
    i94yr float,
    i94mon float,
    i94cit float,
    i94res float,
    i94port VARCHAR,
    arrdate float,
    i94mode float,
    i94addr VARCHAR,
    depdate float, 
    i94bir float,
    i94visa float,
    count float,
    dtadfile VARCHAR,
    visapost VARCHAR,
    occup  VARCHAR,
    entdepa VARCHAR,
    entdepd VARCHAR,
    entdepu VARCHAR,
    matflag VARCHAR,
    biryear float,
    dtaddto VARCHAR,
    gender VARCHAR,
    insnum VARCHAR,
    airline VARCHAR,
    admnum float,
    fltno VARCHAR,
    visatype VARCHAR,
    PRIMARY KEY (cicid))
""")

lookup_i94port_create= ("""
CREATE TABLE IF NOT EXISTS lookup_i94port (
    Code VARCHAR,
    City VARCHAR,
    State VARCHAR,
    PRIMARY KEY (Code))
""")

lookup_i94cit_i94res_create= ("""
CREATE TABLE IF NOT EXISTS lookup_i94cit_i94res (
    Code VARCHAR,
    Country VARCHAR,
    PRIMARY KEY (Code))
""")

fact_table_create= ("""
CREATE TABLE IF NOT EXISTS fact_table (
    cicid float,
    i94yr float,
    i94mon float,
    i94cit VARCHAR,
    i94res VARCHAR,
    i94port VARCHAR,
    arrdate float,
    i94mode float,
    i94addr VARCHAR,
    i94bir float,
    i94visa float,
    count float,
    dtadfile VARCHAR,
    entdepa VARCHAR,
    matflag VARCHAR,
    dtaddto VARCHAR,
    gender VARCHAR,
    visatype VARCHAR,
    "Origin Country" VARCHAR,
    "Residence Country" VARCHAR,
    "US Port City" VARCHAR,
    PRIMARY KEY (cicid))
""")

GDP_table_create= ("""
CREATE TABLE IF NOT EXISTS GDP_dimension (
    Country VARCHAR,
    "GDP in USD 2010" float,
    "GDP in USD 2011" float,
    "GDP in USD 2012" float,
    "GDP in USD 2013" float,
    "GDP in USD 2014" float,
    "GDP in USD 2015" float,
    "GDP in USD 2016" float,
    PRIMARY KEY (Country))
""")

Population_table_create= ("""
CREATE TABLE IF NOT EXISTS Population_dimension (
    Country VARCHAR,
    "Population 2010" float,
    "Population 2011" float,
    "Population 2012" float,
    "Population 2013" float,
    "Population 2014" float,
    "Population 2015" float,
    "Population 2016" float,
    PRIMARY KEY (Country))
""")

demographic_dimension_create= ("""
CREATE TABLE IF NOT EXISTS US_demographic_dimension (
    City VARCHAR,
    State VARCHAR,
    "Median Age" float,
    "Male Population" float,
    "Female Population" float,
    "Total Population" float,
    "Number of Veterans" float,
    "Foreign-born" float,
    "Average Household Size" float,
    "State Code" VARCHAR,
    Race VARCHAR,
    Count float,
    PRIMARY KEY (City, State, Race))
""")


load_staging_fact = ("""
copy {} from '{}' 
IAM_ROLE '{{}}'
FORMAT AS PARQUET;
""").format(
    'staging_fact',
    's3://chon-de-capstone/sas_data'
)

load_lookup_i94port = ("""
copy {} from '{}' 
IAM_ROLE '{{}}'
IGNOREHEADER 1
ACCEPTINVCHARS
DELIMITER ','
;
""").format(
    'lookup_i94port',
    's3://chon-de-capstone/i94port_lookup_v2.csv'
)

load_lookup_i94cit_i94res = ("""
copy {} from '{}' 
IAM_ROLE '{{}}'
IGNOREHEADER 1
ACCEPTINVCHARS
CSV QUOTE as '\"'
DELIMITER ','
;
""").format(
    'lookup_i94cit_i94res',
    's3://chon-de-capstone/i94cit_i94res_lookup.csv'
)

load_GDP_dimension = ("""
copy GDP_dimension from 's3://chon-de-capstone/world_GDP.txt' 
IAM_ROLE '{}'
IGNOREHEADER 1
DELIMITER '\t'
ACCEPTINVCHARS ;
""")

load_population_dimension = ("""
copy Population_dimension from 's3://chon-de-capstone/world_population.csv' 
IAM_ROLE '{}'
CSV 
IGNOREHEADER 1
ACCEPTINVCHARS ;
""")

load_demographic_dimension = ("""
copy {} from '{}' 
IAM_ROLE '{{}}'
IGNOREHEADER 1
ACCEPTINVCHARS
CSV QUOTE as '\"'
DELIMITER ';'
;
""").format(
    'US_demographic_dimension',
    's3://chon-de-capstone/us-cities-demographics.csv'
)



fact_table_insert = ("""
INSERT INTO fact_table ( cicid, i94yr, i94mon, i94cit, i94res, i94port, arrdate, i94mode, i94addr, i94bir, i94visa, count, dtadfile, entdepa, matflag, dtaddto,
                         gender, visatype, "US Port City", "Origin Country", "Residence Country" ) 
SELECT  
    sf.cicid, sf.i94yr, sf.i94mon, sf.i94cit, sf.i94res, sf.i94port, sf.arrdate, sf.i94mode, sf.i94addr, sf.i94bir, sf.i94visa, sf.count, sf.dtadfile, sf.entdepa, 
    sf.matflag, sf.dtaddto, sf.gender, sf.visatype, b.City, c.Country, d.Country
FROM staging_fact sf
left join lookup_i94port b on (sf.i94port = b.Code)
left join lookup_i94cit_i94res c on (sf.i94cit = c.Code)
left join lookup_i94cit_i94res d on (sf.i94res = d.Code)
""")



demographic_dimension_add_key= ("""
ALTER TABLE US_demographic_dimension 
ADD COLUMN lookup_key VARCHAR ;
""")

demographic_key_update= ("""
UPDATE US_demographic_dimension
SET lookup_key = REPLACE(TRIM(UPPER(City)), ' ', '');
""")

demographic_dimension_drop_column= ("""
ALTER TABLE US_demographic_dimension 
DROP COLUMN City CASCADE ;
""")

demographic_dimension_rename = ("""
ALTER TABLE US_demographic_dimension 
RENAME lookup_key TO City;
""")