import plotly.graph_objects as go
import data_cleaning
import pandas as pd
from typing import *


def visualize_count(df: pd.DataFrame = None, small_data: bool = False):
    """
    Takes in a dataframe and generates an interactive figure in plotly
    and exports it as an SVG file in the figures folder.
    """
    if df is None:
        df = data_cleaning.pd_load_data(small_data)
    df = df.reset_index()
    df = df[['STATE', 'FPA_ID']]
    count_df = df.groupby('STATE').count()
    count_df = count_df.rename(columns={'FPA_ID': 'Count'})
    fig = go.Figure(data=go.Choropleth(
        locations=count_df.index,
        z=count_df['Count'].astype(float),
        locationmode='USA-states',
        colorscale='Reds',
        colorbar_title="# of fires",
    ))

    fig.update_layout(
        title_text='Number of wildfires across US from 1992 to 2015',
        geo_scope='usa',
    )
    fig.write_image('figures/fire_counts.svg')
    fig.show()
