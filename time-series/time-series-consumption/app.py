from functions import *
import streamlit as st
import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Forecasting')

tabs = ['Forecasting', 'About me']

pages = st.sidebar.radio('Tabs', tabs)

if pages == 'Forecasting':
    st.markdown("<h1 style='text-align:center;'>Forecasting des Stromverbrauchs</h1>", unsafe_allow_html= True)
    st.write("""Auf dieser Seite werden Ergebnisse durch die Auswahl der Vorhersagelänge erzielt""")

    fh_selection = st.selectbox("Wählen Sie die Vorhersagelänge", ["1 Tag", "2 Tage", "3 Tage", "1 Woche", "2 Wochen"])
    button = st.button('Forecast')

    if button == True:
        with st.spinner("Es wird erzielt, Bitte warten Sie. Sie können die Ergebnisse in etwa 50 Sekunden sehen"):
            start_date = "2016-01-01"
            end_date = datetime.date.today()
            df = get_consumption_data(start_date=start_date, end_date=end_date)
            fig1 = forecast_func(df, select_period(fh_selection))
            st.markdown("<h3 style='text-align:center;'>Forecast Ergebnisse</h3>", unsafe_allow_html= True)
            st.plotly_chart(fig1)