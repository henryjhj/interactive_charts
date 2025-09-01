import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests

st.title("美国股市低波动率股票")

def get_sp500_symbols():
    """Fetches the list of S&P 500 symbols from Wikipedia."""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    tables = pd.read_html(response.text)
    sp500 = tables[0]
    return [str(symbol).replace('-', '.') for symbol in sp500['Symbol'].tolist()]

def get_low_volatility_stocks():
    """Fetches low volatility stocks from the S&P 500."""
    sp500_symbols = get_sp500_symbols()
    low_vol_stocks = []
    for symbol in sp500_symbols:
        # Here you would implement the logic to fetch and analyze the stock data
        # For demonstration, let's assume we have a function `fetch_stock_data`
        stock_data = fetch_stock_data(symbol)
        if is_low_volatility(stock_data):
            low_vol_stocks.append(symbol)
    return low_vol_stocks

def is_low_volatility(stock_data):
    """Determines if a stock is low volatility based on its historical data."""
    # Implement your low volatility logic here
    return True

def fetch_stock_data(symbol):
    """Fetches historical stock data for a given symbol."""
    # Implement your data fetching logic here
    return pd.DataFrame()

# 选择函数
func_name = st.selectbox("选择函数", ["sin", "cos", "tan"])
period = st.slider("选择周期（T）", 1, 10, 2)

# 生成数据
x = np.linspace(-2*np.pi, 2*np.pi, 100)
if func_name == "sin":
    y = np.sin(2 * np.pi * x / period)
elif func_name == "cos":
    y = np.cos(2 * np.pi * x / period)
else:
    y = np.tan(2 * np.pi * x / period)

# 绘制图表
fig, ax = plt.subplots()
ax.plot(x, y, label=f"{func_name}(x)")
ax.legend()
ax.set_title(f"{func_name}(x), T={period}")
st.pyplot(fig)

# 显示文字
st.write("### 数据预览")
st.write("下面是部分 (x, y) 数据点：")

# 转换为 DataFrame
df = pd.DataFrame({
    "x": x,
    f"{func_name}(x)": y
})

# 显示 DataFrame（自动带交互功能：排序、搜索、滚动）
st.dataframe(df.head(10))   # 显示前 10 行

# 如果要静态表格（不可交互）
# st.table(df.head(10))