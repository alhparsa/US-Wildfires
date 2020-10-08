import pandas as pd
import numpy as np
import os
from typing import *


def get_filepath(small_dataset: bool = False) -> Tuple[str, bool]:
    """
    If files exists, returns a tuple. The first element of the tuple is the
    real path of the file, and the second element indicates whether the file
    is compressed or not.
    """
    if small_dataset:
        return os.path.realpath('./fire_data_small.csv.gz'), True
    if os.path.isfile('./fire_data.csv'):
        return os.path.realpath('./fire_data.csv'), False
    elif os.path.isfile('./fire_data.csv.gz'):
        return os.path.realpath('./fire_data.csv.gz'), True
    elif os.path.isfile('./file_data_small.csv.gz'):
        return os.path.realpath('./file_data_small.csv.gz'), True
    return None


def pd_load_data(small_dataset: bool = False) -> pd.DataFrame:
    """
    Returns a data frame if the file exists, otherwise it would raise
    a FileNotFoundError
    """
    path = get_filepath(small_dataset)
    if path is None:
        raise FileNotFoundError('Plase make sure either fire_data.csv or \
            fire_data.csv.gz or fire_data_small.csv.gz is in the main \
                 directory')
    real_path, compressed = path
    if compressed:
        return pd.read_csv(real_path, compression='gzip', low_memory=False,
                           index_col=0,
                           parse_dates=['DISCOVERY_DATE', 'CONT_DATE'])
    return pd.read_csv(real_path, low_memory=False, index_col=0,
                       parse_dates=['DISCOVERY_DATE', 'CONT_DATE'],)
