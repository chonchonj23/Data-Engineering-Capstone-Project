import configparser
import os
import pandas as pd
import io
import logging
import boto3
from botocore.exceptions import ClientError

from pyspark.sql import SparkSession
from pyspark.sql.functions import col,sum

from IPython.display import Image

import configparser
import psycopg2

from sql_functions import *



# connect to for AWS Redshift
config = configparser.ConfigParser()
config.read_file(open('credentials.cfg'))
conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
cur = conn.cursor()


# drop all tables, including fact_table, staging_fact, GDP_dimension, Population_dimension, US_demographic_dimension
cur.execute(Drop_table_sql.format("fact_table"))
cur.execute(Drop_table_sql.format("staging_fact"))
cur.execute(Drop_table_sql.format("lookup_i94port"))
cur.execute(Drop_table_sql.format("lookup_i94cit_i94res"))
cur.execute(Drop_table_sql.format("GDP_dimension"))
cur.execute(Drop_table_sql.format("Population_dimension"))
cur.execute(Drop_table_sql.format("US_demographic_dimension"))


# create and load staging fact table
cur.execute(staging_fact_create)
cur.execute(load_staging_fact)

# create and load i94port lookup table
cur.execute(lookup_i94port_create)
cur.execute(load_lookup_i94port)

# create and load i94cit_i94res lookup table
cur.execute(lookup_i94cit_i94res_create)
cur.execute(load_lookup_i94cit_i94res)

# create and load fact table
cur.execute(fact_table_create)
cur.execute(fact_table_insert)

# create and load GDP Dimension
cur.execute(GDP_table_create)
cur.execute(load_GDP_dimension)

# create and load Population Dimension
cur.execute(Population_table_create)
cur.execute(load_population_dimension)


# create and load US Demogrpahic Dimension
cur.execute(demographic_dimension_create)
cur.execute(load_demographic_dimension)
cur.execute(demographic_dimension_add_key)
cur.execute(demographic_key_update)
cur.execute(demographic_dimension_drop_column)
cur.execute(demographic_dimension_rename)


conn.commit()


def check_row_count(table):
    
    select_count = ("""
        select count(*) from {} ;
    """)
    
    cur.execute(select_count.format(table))
    RowCount = cur.fetchone()
    conn.commit()
     
    if RowCount[0] < 1:
        print("No records present in {table}")
        raise ValueError(f"Data quality check failed. {table} returned no results")
    else:
        print(f"Data quality check on {table} passed with {RowCount[0]} records")



check_row_count("fact_table")
check_row_count("GDP_dimension")
check_row_count("Population_dimension")
check_row_count("US_demographic_dimension")