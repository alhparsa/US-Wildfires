from sklearn.ensemble import GradientBoostingClassifier
import dataprocessing
from sklearn.model_selection import train_test_split


def create_model():
    model = GradientBoostingClassifier(
        n_estimators=400, max_depth=3, min_samples_split=2)
    return model


def split_data(X, y):
    return train_test_split(
        X, y.reshape(-1), test_size=0.12, random_state=42)


def prepare_data(df):
    class_enc = {}
    class_dec = {}
    states_dic_enc = {}
    states_dic_dec = {}
    classes = 'ABCDEFG'
    for _, l in enumerate(classes):
        class_enc[l] = _
        class_dec[_] = l
    for i, j in enumerate(df['state'].drop_duplicates().to_numpy()):
        states_dic_enc[j] = i
        states_dic_dec[i] = j

    df['DISCOVERY_MONTH'] = df['discovery_date'].dt.month
    df['DISCOVERY_YEAR'] = df['discovery_date'].dt.year
    df['DISCOVERY_QUARTER'] = df['discovery_date'].dt.quarter
    df = dataprocessing.convertTime(df.rename(
        {'discovery_time': 'DISCOVERY_TIME', 'cont_time': 'CONT_TIME'}, axis=1))
    df['DISCOVERY_TIME_HOUR'] = df['DISCOVERY_TIME'].dt.hour
    tmp = new_df.groupby(['fpa_id', 'state', 'DISCOVERY_MONTH', 'DISCOVERY_YEAR', 'DISCOVERY_TIME_HOUR',
                          'fire_size_class', 'latitude', 'longitude', ]).agg({'tmax': 'mean', 'prcp': 'mean'})
    tmp = tmp.reset_index()
    tmp['fire_size_class'] = tmp['fire_size_class'].map(class_enc)
    tmp['state'] = tmp['state'].map(states_dic_enc)

    X = tmp[['state', 'DISCOVERY_MONTH', 'DISCOVERY_YEAR',
             'DISCOVERY_TIME_HOUR', 'latitude', 'longitude',
             'tmax', 'prcp']]
    y = labels = tmp[['fire_size_class']].to_numpy()
    X_train, X_test, y_train, y_test = split_data(X, y)

    return X_train, X_test, y_train, y_test


def train(X_train, y_train):
    model = create_model()
    model.fit(X_train, y_train)
    return model
