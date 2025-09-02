import os
import time
import requests
import pandas as pd
import yfinance as yf

# Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = "FEGKNSTFXYYOYT0Z"

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
    from io import StringIO
    tables = pd.read_html(StringIO(response.text))
    sp500 = tables[0]
    return [str(symbol).replace('-', '.') for symbol in sp500['Symbol'].tolist()]

def fetch_stock_data(symbol, period="10y", interval="1mo", auto_adjust=True):
    """Fetches historical stock data for a given symbol from Yahoo Finance."""
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period, interval=interval, auto_adjust=auto_adjust)
    return data

def download_data():
    symbols = get_sp500_symbols()
    all_data = pd.DataFrame()
    for symbol in symbols:  # Limiting to first 3 symbols for demo purposes
        print(f"Downloading data for {symbol}...")
        try:
            data = fetch_stock_data(symbol)
            data['symbol'] = symbol
            print(data.head())
            all_data = pd.concat([all_data, data], axis=0)
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
        # Respect yfinance API rate limits
        time.sleep(3)
    return all_data

def to_yearly(data):
    """Converts monthly stock data to yearly data."""
    # 按 symbol 和年份分组
    data = data.copy()
    data['year'] = data.index.year
    grouped = data.groupby(['symbol', 'year'])
    yearly = grouped.agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
    }).reset_index()
    yearly['year'] = yearly['year'].astype(int)
    return yearly

def main():
    data = download_data()
    print("Data download complete.")
    data.to_csv("sp500_data_monthly.csv")
    yearly_data = to_yearly(data)
    yearly_data.to_csv("sp500_data_yearly.csv")

if __name__ == "__main__":
    main()