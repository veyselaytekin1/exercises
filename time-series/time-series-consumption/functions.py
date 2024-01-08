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


def get_consumption_data(start_date, end_date):
    url="https://seffaflik.epias.com.tr/transparency/service/consumption/real-time-consumption?startDate="+f'{start_date}'+"&endDate="+f'{end_date}'
    response = requests.get(url, verify=False)
    json_data = json.loads(response.text.encode('utf8'))
    df = pd.DataFrame(json_data['body']['hourlyConsumptions']).iloc[:-1] # the last value can not comes right.
    df['date'] = pd.to_datetime(df.date.str[:16])
    return df

def data_features(df):  # jupyter notebook icinde bu 
    df_copy = df.copy()
    df_copy['month'] = df_copy['date'].dt.month
    df_copy['year'] = df_copy['date'].dt.year
    df_copy['hour'] = df_copy['date'].dt.hour
    df_copy['quarter'] = df_copy['date'].dt.quarter
    df_copy['dayofweek'] = df_copy['date'].dt.dayofweek
    df_copy['dayofyear'] = df_copy['date'].dt.dayofyear
    df_copy['dayofmonth'] = df_copy['date'].dt.day
    df_copy['weekofyear'] = df_copy['date'].dt.isocalendar().week
    return(df_copy)




def rolling_feature(df, fh):
    df_copy = df.copy()                                           
    rolling_windows = [fh, fh+3, fh+10, fh+15, fh+20, fh+25]
    lags = [fh, fh+5, fh+10, fh+15, fh+20, fh+30]
    for a in rolling_windows:
        df_copy['rolling_mean_'+ str(a)] = df_copy['consumption'].rolling(a, min_periods=1).mean().shift(1)    
        df_copy['rolling_std_'+ str(a)] = df_copy['consumption'].rolling(a, min_periods=1).std().shift(1)
        df_copy['rolling_min_'+ str(a)] = df_copy['consumption'].rolling(a, min_periods=1).min().shift(1)
        df_copy['rolling_max_'+ str(a)] = df_copy['consumption'].rolling(a, min_periods=1).max().shift(1)
        df_copy['rolling_var_'+ str(a)] = df_copy['consumption'].rolling(a, min_periods=1).var().shift(1)
    for l in lags:
        df_copy['consuption_lag_'+str(l)]=df_copy['consumption'].shift(l)
    return df_copy



