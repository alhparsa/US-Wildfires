import data_cleaning
import pandas as pd
import dataprocessing


def annual_fire_class_national(df=None, filename='national fires per quarter.jpg'):
    """
    Generates a series of plots per quarter per fire class,
    for the whole country.
    """
    if df is None:
        df = data_cleaning.pd_load_data()
    df['DISCOVERY_QUARTER'] = df['DISCOVERY_DATE'].dt.quarter
    plot = df.reset_index().groupby(
        ['FIRE_SIZE_CLASS', 'DISCOVERY_YEAR', 'DISCOVERY_QUARTER']).agg(
            {'FPA_ID': 'count'}).unstack(level=0).unstack(level=-1)['FPA_ID'] \
        .plot(
        subplots=True,
        figsize=(12, 104),
        xlabel='Year',
        ylabel='Number of records',
        title='Number of fires over the years per quarter per fire class')
    plot[0].get_figure().savefig(filename)


def quarterly_plot(df=None, filename='cause of fire.jpg'):
    """
    Creates a plot # of fires per category quarterly from 1992 - 2015 and
    saves it to the `filename`.
    """
    if df is None:
        df = data_cleaning.pd_load_data()
    df['DISCOVERY_MONTH'] = df['DISCOVERY_DATE'].dt.month
    df['DISCOVERY_YEAR'] = df['DISCOVERY_DATE'].dt.year
    df['DISCOVERY_QUARTER'] = df['DISCOVERY_DATE'].dt.quarter
    tmp = df[['DISCOVERY_MONTH', 'DISCOVERY_YEAR', 'DISCOVERY_QUARTER',
              'FIRE_SIZE_CLASS', 'FIRE_SIZE', 'STAT_CAUSE_DESCR',
              'STATE']].reset_index()
    plot = tmp.groupby(['DISCOVERY_YEAR', 'DISCOVERY_QUARTER',
                        'STAT_CAUSE_DESCR']).agg({'FPA_ID': 'count'})['FPA_ID'] \
        .unstack(level=-1).unstack(level=-1) \
        .plot(
        kind='bar',
        subplots=True,
        figsize=(12, 104),
        xlabel='Year',
        ylabel='# of fires',
        title='# of fires per category quarterly from 1992 - 2015')
    plot[0].get_figure().savefig(filename)


def annual_plot(df=None, filename='state annual fires.jpg'):
    """
    Creates a plot of # of fires for each state since 1992 - 2015 and
    saves it to the `filename`.
    """
    if df is None:
        df = data_cleaning.pd_load_data()
    df['DISCOVERY_MONTH'] = df['DISCOVERY_DATE'].dt.month
    df['DISCOVERY_YEAR'] = df['DISCOVERY_DATE'].dt.year
    df['DISCOVERY_QUARTER'] = df['DISCOVERY_DATE'].dt.quarter
    tmp = df[['DISCOVERY_MONTH', 'DISCOVERY_YEAR', 'DISCOVERY_QUARTER',
              'FIRE_SIZE_CLASS', 'FIRE_SIZE', 'STAT_CAUSE_DESCR',
              'STATE']].reset_index()
    plot = tmp.groupby(['STATE', 'DISCOVERY_YEAR']).agg({'FPA_ID': 'count'}) \
        .unstack(level=0)['FPA_ID'] \
        .plot(subplots=True,
              figsize=(12, 104),
              xlabel='Year',
              ylabel='# of fires',
              title='# of fires per year for each state since 1992 - 2015')
    plot[0].get_figure().savefig(filename)


def fire_records_obsv(df=None, filename='national records obsv fires.jpg', state=False):
    """
    Creates a plot of time of observations vs number of records. if flag
    `state` is set to `True` then it will generate a plot per state
    otherwise, it will generate for the whole country.
    """
    if df is None:
        df = data_cleaning.pd_load_data()
    if type(df['DISCOVERY_TIME'][0]) != pd._libs.tslibs.timestamps.Timestamp:
        df = dataprocessing.convertTime(df)
    df['DISCOVERY_TIME_HOUR'] = df['DISCOVERY_TIME'].dt.hour
    if state:
        plot = df.reset_index().groupby(['DISCOVERY_TIME_HOUR', 'STATE']) \
            .agg({'FPA_ID': 'count'})['FPA_ID'].unstack(level=-1) \
            .plot(subplots=True,
                  kind='bar',
                  xlabel='Time',
                  ylabel='Number of records',
                  rot=60,
                  title='# of fire records per hour (24HR) for each state',
                  figsize=(12, 104))
        plot[0].get_figure().savefig(filename)
        return

    plot = df.reset_index().groupby(['DISCOVERY_TIME_HOUR']) \
        .agg({'FPA_ID': 'count'})['FPA_ID'].plot(
        kind='bar',
        xlabel='Time',
        ylabel='Number of records',
        rot=60,
        title='# of fire records per hour (24HR)')
    plot.get_figure().savefig(filename)
