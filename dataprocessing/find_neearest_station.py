import dask.dataframe as dd
import dask.array as da
import numpy as np
import pandas as pd
from dask.distributed import Client

global stations
global df
global df_dask
global client


def getStations():
    """
    Returns a list of all stations from GHCN. 
    """
    ls = []
    with open('ghcnd-stations.txt', 'r') as f:
        for line in f.readlines():
            ls += [[i for i in line.strip().split() if i != ''][:3]]
    return ls


def haversine_np(report):
    """
    Calculate the distance between each reported location and all of the
    weather stations and returns the closest one.
    """
    global stations
    lat1, lon1 = report['LATITUDE'], report['LONGITUDE']
    lat2, lon2 = stations['lat'], stations['long']
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * da.arcsin(da.sqrt(a))
    km = 6367 * c
    return {'LATITUDE': report['LATITUDE'], 'LONGITUDE': report['LONGITUDE'],
            'closest_station': stations.iloc[np.argmin(km)]['station'],
            'distance': km.min()}


def setup():
    """
    Runs the neccessary functions before it does anything else
    """
    global df
    global dask_df
    global stations
    client
    client = Client(n_workers=4, threads_per_worker=4, memory_limit='2GB')
    df = pd.read_csv('../fire_data.csv',
                     parse_dates=['CONT_DATE', 'DISCOVERY_DATE'],
                     index_col='FPA_ID')
    dask_df = dd.from_pandas(df, npartitions=24)
    stations = pd.DataFrame(getStations(), columns=['station', 'lat', 'long'])
    stations = stations[stations.station.str.startswith('US')]


def getClosestStation():
    """
    Joins the fire dataframe with the closest weather station and writes
    the dataframe to a file.
    """
    setup()
    lat_long = fire[['LATITUDE', 'LONGITUDE']]
    lat_long = lat_long.drop_duplicates()
    val = lat_long.apply(func=haversine_np, axis=1, result_type='expand',
                         meta={
                             'LATITUDE': 'float',
                             'LONGITUDE': 'float',
                             'closet_station': 'str',
                             'distance': 'float'})
    fire_nearest_station = val.join(dask_df, on=['LATITUDE', 'LONGITUDE'])
    fire_nearest_station.to_csv(
        'nearest_station_fire.csv.gz', single_file=True, compression='gzip')
    client.close()
