import pandas as pd
import numpy as np
import datetime
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
import warnings

from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit 
from joblib import load


def select_period(period):
    periods={"1 Tag":24,"2 Tage":48,"3 Tage":72,"1 Woche":168,"2 Wochen":336}
    return periods[period]


def get_consumption_data(start_date,end_date):
    url = "https://seffaflik.epias.com.tr/transparency/service/consumption/real-time-consumption?startDate="+f'{start_date}'+"&endDate="+f'{end_date}'
    response = requests.get(url,verify=False)
    json_data = json.loads(response.text.encode('utf8'))
    df = pd.DataFrame(json_data["body"]["hourlyConsumptions"]).iloc[:-1]
    df['date']=pd.to_datetime(df.date.str[:16])
    return df


def date_features(df):
    df_c=df.copy()
    df_c['month'] = df_c['date'].dt.month
    df_c['year'] = df_c['date'].dt.year
    df_c['hour'] = df_c['date'].dt.hour
    df_c['quarter'] = df_c['date'].dt.quarter
    df_c['dayofweek'] = df_c['date'].dt.dayofweek
    df_c['dayofyear'] = df_c['date'].dt.dayofyear
    df_c['dayofmonth'] = df_c['date'].dt.day
    df_c['weekofyear'] = df_c['date'].dt.isocalendar().week
    return df_c


def rolling_features(df,fh):
    df_c=df.copy()
    rolling_windows=[fh,fh+3,fh+10,fh+15,fh+20,fh+25]
    lags=[fh,fh+5,fh+10,fh+15,fh+20,fh+30]
    for a in rolling_windows:
        df_c['rolling_mean_'+str(a)]=df_c['consumption'].rolling(a,min_periods=1).mean().shift(1)
        df_c['rolling_std_'+str(a)]=df_c['consumption'].rolling(a,min_periods=1).std().shift(1)
        df_c['rolling_min_'+str(a)]=df_c['consumption'].rolling(a,min_periods=1).min().shift(1)
        df_c['rolling_max_'+str(a)]=df_c['consumption'].rolling(a,min_periods=1).max().shift(1)
        df_c['rolling_var_'+str(a)]=df_c['consumption'].rolling(a,min_periods=1).var().shift(1)
    for l in lags:
        df_c['consumption_lag_'+str(l)]=df_c['consumption'].shift(l)

    return df_c


def forecast_func(df, fh):
    fh_new = fh + 1                             # forecast horizon weekly -we are adding +1 because by indexing we are gonna lost a line, +1 yapinca yine günün ayni saatine denk geliyor 22:00 ise yine 22:00 de oluyor
    date = pd.date_range(start=df.date.tail(1).iloc[0], periods=fh_new, freq='H', name='date')
    date = pd.DataFrame(date)
    df_fea_eng = pd.merge(df, date, how='outer')

    # feature engineering
    df_fea_eng = rolling_features(df_fea_eng, fh_new)
    df_fea_eng = date_features(df_fea_eng)
    df_fea_eng = df_fea_eng[fh_new+30:].reset_index(drop=True)

    # train test split
    split_date = df_fea_eng.date.tail(fh_new).iloc[0]
    historical = df_fea_eng.loc[df_fea_eng['date'] <= split_date] 
    y = historical[['date','consumption']].set_index('date')
    X = historical.drop('consumption', axis=1).set_index('date')
    forecast_df = df_fea_eng.loc[df_fea_eng['date'] > split_date].set_index('date').drop('consumption', axis=1)

    tscv = TimeSeriesSplit(n_splits=3, test_size=fh_new * 20)
    score_list = []
    fold = 1
    unseen_preds = []
    importance = []

    for train_index, test_index in tscv.split(X, y): # burda aslinda datayi bölüyoruz bir altta ciktisi var train_index ne demek oldugunun
        X_train, X_val = X.iloc[train_index], X.iloc[test_index]
        y_train, y_val = y.iloc[train_index], y.iloc[test_index]
        print(X_train.shape, X_val.shape)
        rf = RandomForestRegressor(n_estimators=3, random_state=42)
        rf.fit(X_train, y_train)

        forecast_predcited = rf.predict(forecast_df)
        unseen_preds.append(forecast_predcited) # 3 cross validation sonuclari gelecek galiba n_split=3 oldugu icin. cünkü time serimzi 3 parcaya bölmüstü
        score = mean_absolute_error(y_val, rf.predict(X_val))
        print(f"MAE FOLD - {fold}: {score}")
        score_list.append(score)
        importance.append(rf.feature_importances_) # burdanda 3 farkli sonuclar gelecek
        fold += 1

    print("CV Mean Score: ", np.mean(score_list))

    forecasted=pd.DataFrame(unseen_preds[2],columns=["forecasting"]).set_index(forecast_df.index)

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_fea_eng.date.iloc[-fh_new*5:], y=df_fea_eng.consumption.iloc[-fh_new*5:], name = 'Historical Data', mode = 'lines'))
    fig1.add_trace(go.Scatter(x=forecasted.index, y=forecasted['forecasting'], name = 'Tarihsel Veri', mode = 'lines'))
    return fig1

