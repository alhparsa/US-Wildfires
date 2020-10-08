from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from math import sqrt
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler


def scale(train, test):
    # fit scaler
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler = scaler.fit(train)
    # transform train
    train = train.reshape(train.shape[0], train.shape[1])
    train_scaled = scaler.transform(train)
    # transform test
    test = test.reshape(test.shape[0], test.shape[1])
    test_scaled = scaler.transform(test)
    return scaler, train_scaled, test_scaled


def model(input):
    model = Sequential()

    model.add(LSTM(units=50, return_sequences=True,
                   input_shape=(input.shape[1], 1)))

    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50))
    model.add(Dropout(0.2))

    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    return model


def train(df, model, fire_class='A'):
    tmp = df.reset_index().groupby(['FIRE_SIZE_CLASS', 'DISCOVERY_YEAR', 'DISCOVERY_MONTH']).agg(
        {'FPA_ID': 'count'})['FPA_ID'].unstack(level=0)
    scaler, train_scaled, test_scaled = scale(tmp[fire_class][:240].to_numpy(
    ).reshape(-1, 1), tmp[fire_class][30:270].to_numpy().reshape(-1, 1))
    train = train_scaled.reshape(-1, 1, 1)
    test = test_scaled.reshape(-1, 1, 1)
    model.fit(x=train, y=test, epochs=100, batch_size=32)
    return model
