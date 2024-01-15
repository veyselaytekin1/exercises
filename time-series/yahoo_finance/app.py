import streamlit as st
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt

symbol = st.sidebar.text_input('Hisse Senedi Sembolü', value='ASELS')

st.title(symbol + ' Hisse Senedi Grafigi')

start_date = st.sidebar.date_input('Baslangic Tarihi', value=datetime(2020,1,1))
end_date = st.sidebar.date_input('Bitis Tarihi', value=datetime.now())

df = yf.download(symbol+ '.IS', start=start_date, end=end_date)

st.subheader('Hisse Senedi Trend Grafigi')
st.line_chart(df['Close'])

st.subheader('Hisse Senedi fiyatlar Tablosu')
st.write(df)