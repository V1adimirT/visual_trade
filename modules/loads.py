# Стандартные импорты
from typing import List

# Сторонние импорты
import numpy as np
import pandas as pd
from pandas.core import series
from pandas.core.frame import DataFrame
import streamlit as st
from streamlit.uploaded_file_manager import UploadedFile
from typing import List


# Локальные импорты


@st.cache
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

