from asyncio import sleep
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import yfinance as yf
import datetime
import time

st.title("低波动率美股筛选器")

def get_low_volatility_stocks(lookback_years=5, volatility_threshold=3):
    """Fetches low volatility stocks from the S&P 500."""
    df = pd.read_csv("sp500_data_yearly.csv")
    
    # 用列表收集低波动率股票
    low_vol_list = []

    # 获取每只股票历史数据中最高的High和最低的Low，以及Volatility=Max(High)/Min(Low)
    # 如果Volatility小于某个值，则记录该股票的symbol、Max_High、Min_Low、Volatility以及最后的Close价格到low_vol_stocks中
    for symbol in df['symbol'].unique():
        stock_data = df[df['symbol'] == symbol]

        # 如果最早数据不足回看年数则跳过
        if stock_data['year'].min() > (datetime.datetime.now().year - lookback_years):
            continue
        # # 只考虑最近lookback_years年的数据
        stock_data = stock_data[stock_data['year'] >= (datetime.datetime.now().year - lookback_years)]

        max_high = stock_data['High'].max()
        min_low = stock_data['Low'].min()
        volatility = max_high / min_low if min_low != 0 else 0
        last_close = stock_data['Close'].iloc[-1] if not stock_data['Close'].empty else 0
        if volatility < volatility_threshold:
            low_vol_list.append({
                'symbol': symbol,
                'Max_High': max_high,
                'Min_Low': min_low,
                'Volatility': volatility,
                'Last_Close': last_close
            })
    return pd.DataFrame(low_vol_list)

# 用streamlit设定回看年数和volatility阈值
lookback_years = st.slider("选择回看年数", 1, 10, 10)
volatility_threshold = st.slider("选择振幅阈值", 1.0, 5.0, 2.5)
low_vol_stocks = get_low_volatility_stocks(lookback_years, volatility_threshold)

# # 显示低波动率股票
st.write(f"#### 符合上述筛选条件的股票共{low_vol_stocks.shape[0]}只：")
st.dataframe(low_vol_stocks)
