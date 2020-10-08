import pandas as pd
import matplotlib.pyplot as plt


def mean_agg_cause(df, state=None, filename='mean_cause.jpg'):
    if state is None:
        tmp = df.reset_index().groupby(['FIRE_SIZE_CLASS',
                                        'DISCOVERY_YEAR',
                                        'DISCOVERY_MONTH',
                                        'STAT_CAUSE_DESCR']) \
            .agg({'FPA_ID': 'count'}) \
            .unstack(level=0)['FPA_ID'] \
            .groupby(['DISCOVERY_MONTH', 'STAT_CAUSE_DESCR']) \
            .mean().unstack(level=-1)
    else:
        tmp = df[df['STATE'] == state].reset_index().groupby(['FIRE_SIZE_CLASS',
                                                              'DISCOVERY_YEAR',
                                                              'DISCOVERY_MONTH',
                                                              'STAT_CAUSE_DESCR']) \
            .agg({'FPA_ID': 'count'}) \
            .unstack(level=0)['FPA_ID'] \
            .groupby(['DISCOVERY_MONTH', 'STAT_CAUSE_DESCR']) \
            .mean().unstack(level=-1)
    plot = tmp.plot(subplots=True, kind='bar',
                    figsize=(12, 240),
                    title=f'Mean(fire counts) per causation vs Month in the US 1995-2015{state}',
                    xlabel='Month',
                    ylabel='# of fires',
                    fontsize=8,
                    rot=0)
    plot[0].get_figures().savefig(filename)


def mean_agg_class(df, state=None, filename='mean_class.jpg'):
    if state is None:
        tmp = df.reset_index().groupby(['FIRE_SIZE_CLASS',
                                        'DISCOVERY_YEAR',
                                        'DISCOVERY_MONTH',
                                        'STAT_CAUSE_DESCR']) \
            .agg({'FPA_ID': 'count'}) \
            .unstack(level=0)['FPA_ID'] \
            .groupby(['FIRE_SIZE_CLASS']) \
            .mean()
    else:
        tmp = df[df['STATE'] == state].reset_index().groupby(['FIRE_SIZE_CLASS',
                                                              'DISCOVERY_YEAR',
                                                              'DISCOVERY_MONTH',
                                                              'STAT_CAUSE_DESCR']) \
            .agg({'FPA_ID': 'count'}) \
            .unstack(level=0)['FPA_ID'] \
            .groupby(['FIRE_SIZE_CLASS']) \
            .mean()
    plot = tmp.plot(subplots=True, kind='bar',
                    figsize=(12, 240),
                    title=f'Mean(fire counts) per causation vs Month in the US 1995-2015{state}',
                    xlabel='Month',
                    ylabel='# of fires',
                    fontsize=8,
                    rot=0)
    plot[0].get_figures().savefig(filename)


def lin_reg_national(df, filename='national_reg'):
    tmp = df.reset_index().groupby(['FIRE_SIZE_CLASS', 'DISCOVERY_YEAR', 'DISCOVERY_MONTH']).agg(
        {'FPA_ID': 'count'})['FPA_ID'].unstack(level=0)
    for fire_class in "ABCDEFG":
    fig, ax = plt.subplots(2, 2, sharex=True, figsize=(15, 15))
    m = 1
    for i in [1, 2]:
        for j in [0, 1]:
            try:
                model = LinearRegression()
                model.fit(np.array(tmp[m][fire_class][tmp[m][fire_class].notnull(
                )].index).reshape(-1, 1), tmp[m][fire_class][tmp[m][fire_class].notnull()])
                print(f'slope = {model.coef_}, quarter = {m}')
                ax[i-1, j-1].plot(tmp[i+j][fire_class][tmp[m][fire_class].notnull()
                                                       ].index, tmp[m][fire_class][tmp[m][fire_class].notnull()])
                ax[i-1, j-1].plot(np.linspace(1992, 2015, tmp[m][fire_class][tmp[m][fire_class].notnull()].shape[0]), model.predict(
                    np.linspace(1992, 2015, tmp[m][fire_class][tmp[m][fire_class].notnull()].shape[0]).reshape(-1, 1)))
                ax[i-1, j-1].set_title(
                    f"National fire trend in the quarter {m} category ({fire_class})")
                ax[i-1, j-1].set_xlabel('Year')
                ax[i-1, j-1].set_ylabel('# of fires')
                ax[i-1, j-1].text(2, 2, f"slope = {model.coef_}")
                m += 1
            except:
                m += 1
    fig.savefig(f'{filename}{fire_class}.jpg')
