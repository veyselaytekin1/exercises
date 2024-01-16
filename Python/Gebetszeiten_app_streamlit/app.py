import pandas as pd
import numpy as np
import datetime as datetime
from datetime import datetime
import locale
import streamlit as st
import json
from functions import *

with open('/Users/veyselaytekin/Desktop/byte/exercises/Python/Gebetszeiten_app_streamlit/germany.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

cities = [item['name'] for item in data]



st.markdown("<h1 style='text-align: center;'>Willkommen Ramadan</h1>", unsafe_allow_html=True)

selected_city = st.selectbox("Wähle ein Stadt aus:", cities)

st.subheader('Heute')
st.table(Bugun_verileri(selected_city))


st.subheader('Iftara kalan süre')
st.info(kalan_süreyi_hesapla(selected_city))

st.subheader('10 günlük veri')
st.table(imsakiye(selected_city))
