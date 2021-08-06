
# Сторонние импорты
from os import write
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from scipy.stats import t

# Локальные импорты
from modules import loads

st.title('Example search level')
variantLoad = st.sidebar.selectbox('Загрузить котировки из:', ['File', 'Yahoo'])
df = pd.DataFrame()

if variantLoad == 'File':
    fileWithQuotes = st.sidebar.file_uploader('Choose file csv with quotes', type='csv')
    if fileWithQuotes:
        df = loads.loadFile(fileWithQuotes=fileWithQuotes)
elif variantLoad == 'Yahoo':
    tickers = ['AAPL']
    ticker = st.sidebar.selectbox('Select', tickers)
    dateStart = st.sidebar.date_input('Start date')
    dateEnd = st.sidebar.date_input('End date')
    df = loads.get_ticker_history(ticker)

if len(df) > 0:
    st.write(df.head())

    hl_2 = np.array((df['High'] + df['Low'])/2)
    dt = []
    dt.append(0)
    for i in range(1, len(hl_2)):
        dt.append(np.log(hl_2[i] / hl_2[i-1]))

    df['H+L/2'] = hl_2
    df['dt'] = dt
    st.markdown('Add new column:')
    st.write(df.head(3))

    t_pri = []
    t_val = []
    degrees_of_freedom = []
    t_pri.append(0)
    t_pri_val = 0
    E_t = []
    E_pred = []
    E_pred.append(0)
    E_pred.append(0)
    E_pred.append(0)

    for i in range(len(dt)):
        degrees_of_freedom.append(t_pri_val - 2)
        
        if t_pri_val - 2 >= 0:
            E_t.append(np.mean(np.array(dt[i::-1])[:t_pri_val]))
            E_pred.append(E_t[i])
        else:
            E_t.append(0)
        
        if t_pri_val - 2 > 0:
            
            sqrtValue1 = float(np.sqrt(t_pri[i] - 2))
            sqrtValue2 = float(np.sqrt((t_pri[i] - 1) / t_pri[i]))
            signValue = float(np.sign(E_pred[i]))
            diffValue = float(dt[i] - E_pred[i])
            arrValue = np.array(dt[i - 1::-1])[:t_pri_val - 1]
            pieceValue = float(t_pri[i] - 1) * float(E_pred[i]**2)
            sqrtValue3 = float(np.sqrt(np.sum(np.square(arrValue)) - pieceValue))

            t_st = sqrtValue1 * sqrtValue2 * signValue * diffValue / sqrtValue3
            t_val.append(t_st)

            if t_val[i] > 0:
                t_pri_val += 1
                t_pri.append(t_pri_val)
            elif abs(t_val[i]) < t.ppf(1 - 0.05*2, t_pri_val - 2):
                t_pri_val += 1
                t_pri.append(t_pri_val)
            else:
                t_pri_val = 2
                t_pri.append(t_pri_val)
        
        elif -2 <= t_pri_val - 2 <= 0:
            t_pri_val += 1
            t_pri.append(t_pri_val)
            t_val.append(0)


    df['n-2=степень свободы'] = degrees_of_freedom
    df['Et=текущий тренд'] = E_t
    df['E(t-1)=предыдущий тренд'] = E_pred[:2858]
    df['T1 - сегодня'] = t_val

    st.markdown('Add new column:')
    st.write(df.head(40))

    rost = []
    trend = list(df[df['n-2=степень свободы'] == 0]['Et=текущий тренд'])
    close_price = list(df[df['n-2=степень свободы'] == 0]['Close'])

    for i in range(0, len(trend), 2):
        try:
            if trend[i] < trend[i + 1]:
                rost.append(close_price[i + 1] - close_price[i])
            else:
                rost.append(close_price[i] - close_price[i + 1])
        except:
            pass

    plt.figure(figsize=(15, 5))
    plt.grid()

    st.line_chart(rost)
