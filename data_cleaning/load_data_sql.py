import sqlite3 as lite
import pandas as pd
import matplotlib.pyplot as plt


def loadData(small=False, database_path="FPA_FOD_20170508.sqlite"):
    """
    Loads the data from sqlite and returns a pandas dataframe.
    If `small` is set to `True`, it returns a smaller dataframe.
    """
    database = database_path
    con = lite.connect(database)
    curr = con.cursor()
    if small:
        small_query = 'select FPA_ID, NWCG_REPORTING_AGENCY, NWCG_REPORTING_UNIT_NAME,\
         FIRE_NAME, datetime(DISCOVERY_DATE) as DISCOVERY_DATE, DISCOVERY_TIME,\
         STAT_CAUSE_DESCR, datetime(CONT_DATE) as CONT_DATE, CONT_TIME,\
         FIRE_SIZE, FIRE_SIZE_CLASS, LATITUDE, LONGITUDE, STATE, \
         COUNTY from Fires where FIRE_SIZE > 500'
        fire_500hc = pd.read_sql_query(small_query, con)
        return fire_500hc
    query = 'select FPA_ID, NWCG_REPORTING_AGENCY, NWCG_REPORTING_UNIT_NAME,\
         FIRE_NAME, datetime(DISCOVERY_DATE) as DISCOVERY_DATE, DISCOVERY_TIME,\
         STAT_CAUSE_DESCR, datetime(CONT_DATE) as CONT_DATE, CONT_TIME,\
         FIRE_SIZE, FIRE_SIZE_CLASS, LATITUDE, LONGITUDE, STATE, \
         COUNTY from Fires'

    fire_df = pd.read_sql_query(query, con)
    return fire_df


def writeData(filename='fire_data.csv', small=False, compression='infer', index=False):
    """
    Loads data from the database and write it to the path provided.
    """
    df = loadDataLarge(small)
    df.to_csv(filename, compression=compression, index=index)
