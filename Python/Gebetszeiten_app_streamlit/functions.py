import pandas as pd
import numpy as np
import datetime as datetime
from datetime import datetime
import locale

def imsakiye(sehir):
    df = pd.read_html(f'https://www.milliyet.com.tr/ramazan/imsakiye/almanya-{sehir}-iftar-vakti/')[0]
    df['date'] = df['Tarih'].str.extract(r'\d+\. Gün (\d+ \w+ \d{4})')
    df = df.drop('Tarih', axis = 1)
    locale.setlocale(locale.LC_TIME, 'tr_TR')
    df['date'] = pd.to_datetime(df['date'], format='%d %B %Y')
    df['date'] = df['date'].dt.date
    date_column = df.pop('date')
    df.insert(0, 'date', date_column)
    return df

def Bugun_verileri(sehir):
    df = imsakiye(sehir)
    return df[0:1]

def on_gunluk_veri(sehir):
    df = imsakiye(sehir)
    return df

def kalan_süreyi_hesapla(sehir):
    df = imsakiye(sehir)
    now = datetime.now()
    aksam_time = pd.to_datetime(df['Akşam'][0], format='%H:%M')
    combined_aksam_time = datetime.combine(now.date(), aksam_time.time())
    # Eğer aksam zamanı şu andan önceyse, bir sonraki gün için hesapla
    if combined_aksam_time < now:
        combined_aksam_time = datetime.combine(now.date() + timedelta(days=1), aksam_time.time())
    remaining_time = combined_aksam_time - now
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes = remainder // 60
    kalan_sure = "Kalan süre: {} hours {} minute".format(hours, minutes)
    return kalan_sure