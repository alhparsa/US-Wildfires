import pandas as pd
import data_cleaning.load_data_pd as load_data


def convertTime(df=None):
    """
    Turns the discovery time and containment time into a string
    """
    if df is None:
        df = load_data()
    df = df[(df['DISCOVERY_TIME'].notnull())]
    df = df[(df['CONT_TIME'].notnull())]
    df['DISCOVERY_TIME'] = df['DISCOVERY_TIME'].astype('int')
    df['CONT_TIME'] = df['CONT_TIME'].astype('int')
    df['DISCOVERY_TIME'] = pd.to_datetime(
        (df['DISCOVERY_TIME'] // 100).astype('str').str.zfill(2) +
        ':' + (df['DISCOVERY_TIME'] % 100).astype('str').str.zfill(2))
    df['CONT_TIME'] = pd.to_datetime(
        (df['CONT_TIME'] // 100).astype('str').str.zfill(2) +
        ':' + (df['CONT_TIME'] % 100).astype('str').str.zfill(2))
    return df
