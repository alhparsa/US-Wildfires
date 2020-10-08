import os
from typing import *


def get_filepath() -> Tuple[str, bool]:
    """
    If files exists, returns a tuple. The first element of the tuple is the
    real path of the file, and the second element indicates whether the file
    is compressed or not.
    """
    if os.path.isfile('./fire_data.csv'):
        return os.path.realpath('./fire_data.csv')
    elif os.path.isfile('./fire_data.csv.gz'):
        return os.path.realpath('./fire_data.csv.gz')
    elif os.path.isfile('./file_data_small.csv.gz'):
        return os.path.realpath('./file_data_small.csv.gz')
    return None


def pd_load_data() -> spark.DataFrame:
    """
    Returns a data frame if the file exists, otherwise it would raise
    a FileNotFoundError
    """
    path = get_filepath
    if path is None:
        raise FileNotFoundError('Plase make sure either fire_data.csv or \
            fire_data.csv.gz or fire_data_small.csv.gz is in the main \
                 directory')
    return spark.read.csv(real_path, header=True)
