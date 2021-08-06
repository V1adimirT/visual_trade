# Стандартные импорты
from typing import List

# Сторонние импорты
import yfinance as yf
import numpy as np
import pandas as pd
from pandas.core import series
from pandas.core.frame import DataFrame
import streamlit as st
from streamlit.uploaded_file_manager import UploadedFile
from typing import List


# Локальные импорты


@st.cache(allow_output_mutation=True)
def loadFile(fileWithQuotes: UploadedFile):
    df = pd.read_csv(fileWithQuotes)

    return df


def getSeries(df: DataFrame):
    columns = ['<HIGH>', '<LOW>']
    df = df[columns].copy()
    df.columns = ['high', 'low']
    df['middle'] = (df.high + df.low) / 2
    df['dt'] = np.log(df.middle / df.middle.shift(1))
    series = df.dt

    return series


@st.cache
def get_ticker_history(ticker: str, dateStart='2010-01-23', dateEnd='2021-05-31'):

   df = yf.download(ticker, start=dateStart, end=dateEnd)

   return df

