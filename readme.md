# Project Description

The goal of this project to analyze over 20 years data for wildfires in United States of America. The primary data used for this project is [Kaggle's 1.88 Million US Wildfires](https://www.kaggle.com/rtatman/188-million-us-wildfires).

We are also hoping to find correlations and trends and create a model to better predict the size of fire behaviors.

# Project Steps

1. Collect other related data:
   - [x] weather data (with Greg's help)
   - [x] ~~regional data where the wildfire happened:~~ 
     - ~~Is it a campground? national park? - use the OpenStreetMap dataset~~ OpenStreetMap wasn't helpful
     - [x] ~~what type of climate is it? - could be inferred from latitude~~ Used precipitation data and temperature instead
2. Data processing and analysis:
   - [x] Are there more or less wildfires overtime for US and for a specific state?
   - [x]What can we see about correlations between weather/climate type to wildfire occurrences and its scale? Or the cause of fire such as are there more fires caused by human vs nature?
   - Which features in the dataset matter?
   - ~~Does fighting fire aggressively lead to more and and bigger fires in the future? (stretch goal)~~
3. Machine Learning:
   - [x] General structure:
     - [x] Input: county (or longitude and latitude), time of the year (week or month)
     - [x] Output: what is the probability of a wildfire happening?
   - [x] Playing with different models (Gaussian NB, regression, classification models)
   - [x] Evaluating models based on the classification report on top of the accuracy score.

# Tools used

- [Pandas](https://pandas.pydata.org/)
- [Pyspark](https://spark.apache.org/docs/latest/api/python/index.html)
- [Matplotlib](https://matplotlib.org/)
- [Scikit-learn](https://scikit-learn.org/stable/)
- [Plotly](https://plotly.com/)
- [Dask](https://dask.org/)
- [Keras](https://keras.io/)

# Requirements

Before running any code make sure you run the following command in your terminal:

`pip install -r requirements.txt`

# Sample dataset

Here is a sample dataset from our main dataset to experiement with the code. This sample dataset only includes data for wildfires with the size of 500 hectares or more. Note that it was compressed with `gzip`.

[500hc_fires](/fire_data_small.csv.gz)
