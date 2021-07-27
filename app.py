
# Сторонние импорты
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Локальные импорты
from modules import loads

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('Демо для трейдинга')

fileWithQuotes = st.sidebar.file_uploader("Загрузить тукстовый файл", type="txt")

if fileWithQuotes:
    df = loads.loadFile(fileWithQuotes)
    series = loads.getSeries(df)
    
    st.markdown('Настройки выборки')
    sizeSample = st.slider('Размер выборки', min_value=50, max_value=1000)
    offsetSeries = st.slider('Сещение выборки', min_value=1, max_value=len(series) - sizeSample)
    
    st.markdown('Выбока')
    st.line_chart(series[offsetSeries:offsetSeries + sizeSample])


